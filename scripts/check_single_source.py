"""Find engine values that are stated in more than one place.

    python scripts/check_single_source.py            # report
    python scripts/check_single_source.py --check    # exit 1 if anything drifted

Why this exists
---------------
`cse.config.yml` is the source of truth for every tuned number in the engine — review
intervals, the effort ceiling, the comfort weights. By Aug 17, 2026 each of those also
existed in a script's `DEFAULT_CONFIG` **and** in CLAUDE.md prose, so every knob had three
copies and nothing checked that they agreed. They did not:

  - the effort ceiling was lowered 9.0 -> 8.0 on Aug 16. The config got it. CLAUDE.md kept
    saying 9.0 for a day, and a budget check run off that stale number passed two days that
    were actually over the real ceiling.
  - the SD lane slot was simultaneously 2.0 (effort_budget.md), 3.0 (config + CLAUDE.md) and
    "not priced at all" (the config's own ceiling note). Three live answers, no way to tell
    which was current except by reading the git log.

The failure is always silent, and it is always the copy nobody executes from that goes
stale — the executable copy gets corrected the first time it produces a wrong answer.

Two checks, because the two kinds of copy fail differently
---------------------------------------------------------
**A. Script defaults vs the config (exact).** Both sides are machine-readable, so this is a
literal comparison with no heuristics and no false positives. These are the dangerous copies:
a stale default silently changes what the engine COMPUTES.

**B. Prose restating a value (heuristic).** Cheap to write, impossible to make exact — prose
says "+30 days" where the config says `streak1: 30`. Reported as warnings. These copies do
not change behavior; they mislead the reader, which is how the ceiling incident happened.

⚠️ **History is not drift.** A dated derivation ("Decisions, Aug 7: ceiling starts at 9.0")
is a record of how a number was settled and MUST NOT be back-dated. Mark those lines or
sections with `single-source-ok` in a comment and this skips them. Without that escape the
report is mostly history, and a report that is mostly noise stops being read — the same
failure mode `technique_coverage.py` documents for its own unmatched specs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "cse.config.yml"

#: Opt-out marker. A line carrying it, or any line under a `<!-- single-source-ok: ... -->`
#: heading until the next heading of the same level, is treated as history.
OPT_OUT = "single-source-ok"

#: Prose swept for restated values. Schedules are EXCLUDED: a weekly build legitimately
#: records "Wed = 7.5 units" and "8.0 ceiling" as the arithmetic of that week, and archived
#: ones are frozen history by definition.
PROSE_GLOBS = (
    "CLAUDE.md",
    "AGENTS.md",
    "docs/foundations/**/*.md",
    ".claude/memory/*.md",
)
PROSE_EXCLUDE = ("docs/foundations/schedules/",)

#: Script defaults that mirror a config key. (module path, default-dict name, {default key:
#: dotted config path}). This is the whole point of check A — every pair here is a value
#: living in two files that must agree.
SCRIPT_DEFAULTS = (
    (
        "scripts/update_review_dates.py",
        "DEFAULT_CONFIG",
        {
            "clean_provisional": "intervals.clean.provisional",
            "clean_streak1": "intervals.clean.streak1",
            "clean_streak2": "intervals.clean.streak2",
            "graduated": "intervals.clean.graduated",
            "shaky": "intervals.shaky",
            "blank": "intervals.blank",
            "graduate_at_streak": "graduate_at_streak",
            "source_root": "solutions.roots.0",
        },
    ),
    (
        "scripts/effort_budget.py",
        "defaults",
        {
            "ceiling": "effort_budget.ceiling",
            "floor_min": "effort_budget.floor_min",
            "comfort_units": "effort_budget.comfort_units",
            "difficulty": "effort_budget.difficulty",
        },
    ),
)

#: Words that mean "this line is talking about <config key>". Auto-derived from the key path
#: where the name is already a word (ceiling, floor, provisional); listed here only where
#: prose uses different vocabulary than the YAML does.
ALIASES = {
    "intervals.clean.streak1": ("streak 1", "streak1", "s1"),
    "intervals.clean.streak2": ("streak 2", "streak2", "s2"),
    "intervals.clean.graduated": ("graduated", "retired", "spot check"),
    "intervals.shaky": ("shaky",),
    "intervals.blank": ("blank",),
    "graduate_at_streak": ("streak", "graduate"),
    "effort_budget.floor_min": ("floor",),
}

#: ⚠️ A cue plus the bare digit is FAR too loose — the first draft of this check produced 84
#: findings of which most were `×3`, "Priority 3" and any stray 2 on a line containing the
#: word "blank". A report that is mostly noise is one nobody opens, which would make this
#: script another rule that exists and does not fire.
#:
#: So the number must also appear in a form that ASSERTS it as the value — `+30`, `30 days`,
#: `= 30`, `8 u/day`, `streak 3`. Mentioning a number near a cue is not a restatement;
#: stating it as the setting is. Keyed by dotted-path prefix, first match wins.
VALUE_FORMS = (
    ("intervals.", (r"\+\s*{n}\b", r"\b{n}\s*[-–]?\s*days?\b")),
    ("graduate_at_streak", (r"(?:streak|tier)[\s\-]*{n}\b", r"[:=]\s*{n}\b")),
    ("effort_budget.ceiling", (r"\b{n}\s*(?:u\b|units?)", r"ceiling[\s:=of]*{n}\b",
                               r"\b{n}\s*/\s*(?:day|{n})", r"[:=]\s*{n}\b")),
    ("effort_budget.floor_min", (r"\b{n}\s*(?:u\b|units?)", r"floor[\s:=of]*{n}\b",
                                 r"[:=]\s*{n}\b")),
    # Weight tables read "🔴 3.0" / "Easy 0.5" — the cue sits right against the number.
    ("effort_budget.comfort_units.", (r"{cue}\s*[:=]?\s*{n}\b",)),
    ("effort_budget.difficulty.", (r"{cue}\s*[:=]?\s*{n}\b",)),
)


def forms_for(dotted: str) -> tuple[str, ...]:
    for prefix, forms in VALUE_FORMS:
        if dotted.startswith(prefix):
            return forms
    return (r"[:=]\s*{n}\b",)


#: Vocabulary that was RETIRED, and what replaced it. A rule file still speaking a dead
#: dialect is worse than one that is merely out of date: it reads as current, and the agent
#: cannot tell which of two contradicting files to obey without checking the git log.
#:
#: Found the hard way — `feedback_daily_cap.md` still said "never more than 5 problems a day"
#: and routed overflow to "Sunday's system-design sprint" a week after the effort budget
#: replaced the count and four days after that SD slot stopped existing. Nothing surfaced it.
#:
#: ⚠️ Dated logs legitimately speak the old dialect (that IS the history), so the same
#: file-level `single-source-ok` marker exempts them.
RETIRED_TERMS = (
    ("daily_cap", "the effort budget — units, not a problem count (CLAUDE.md + effort_budget:)"),
    ("sd_lane_units", "nothing — SD is off-board and unpriced since Aug 16, 2026"),
    ("sd_deep_dive_units", "nothing — SD is off-board and unpriced since Aug 16, 2026"),
    ("SD lane", "the SD mock slot; it is scheduled here, executed in sd-progress, and NOT priced"),
    ("blind sprint", "nothing — retired with the three-lane SD model, Aug 13, 2026"),
    ("Bootstrap → Transition", "nothing — the SD arc was retired Aug 13, 2026"),
    ("ai_progress", "nothing — the AI System Engineering track was removed Aug 13, 2026"),
)


def check_retired(files: list[Path]) -> list[str]:
    findings = []
    for path in files:
        rel = path.relative_to(REPO).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        if any(OPT_OUT in ln.lower() for ln in lines[:5]):
            continue
        # A memory file's YAML frontmatter carries its own `name:` — a redirect stub for a
        # retired rule would otherwise be flagged for being named after the thing it retires.
        body_starts = 0
        if lines and lines[0].strip() == "---":
            end = next((i for i, ln in enumerate(lines[1:], 1) if ln.strip() == "---"), 0)
            body_starts = end
        for n, line in enumerate(lines, 1):
            if n <= body_starts:
                continue
            low = line.lower()
            # A line that says the thing is GONE is the fix, not the bug. Naming a retired
            # concept in order to retire it ("no blind sprints", "the SD lane was priced
            # at...") must not be flagged, or the report punishes the documentation that
            # does its job and the signal drowns.
            if any(w in low for w in (OPT_OUT, "superseded", "retired", "no longer",
                                      "not priced", "removed", "used to", "was simultaneously",
                                      "are gone", "is gone", "referents are gone", "once carried")):
                continue
            for term, replacement in RETIRED_TERMS:
                t = term.lower()
                if t not in low:
                    continue
                before = low[:low.index(t)]
                if re.search(r"(?:\bno|\bnot|\bnever|\bzero)\s+\S*\s*$", before):
                    continue  # "no blind sprints", "never an SD lane"
                findings.append(f"{rel}:{n}: `{term}` is retired -> {replacement}")
                break
    return findings


def load_yaml() -> dict:
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        sys.exit("check_single_source: needs PyYAML (pip install pyyaml)")
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}


def dig(cfg: dict, dotted: str):
    """Resolve 'intervals.clean.streak1' / 'solutions.roots.0' against the config."""
    cur = cfg
    for part in dotted.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            if not isinstance(cur, dict) or part not in cur:
                return None
            cur = cur[part]
    return cur


def read_default_dict(path: Path, name: str) -> dict | None:
    """Pull a literal dict assigned to `name` out of a script, without importing it.

    Importing would execute the module (and effort_budget.py reads the tracker at import
    time). `ast.literal_eval` on the assignment is enough: these are literals by design.
    """
    import ast

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return None
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for t in targets:
            if isinstance(t, ast.Name) and t.id == name and node.value is not None:
                try:
                    return ast.literal_eval(node.value)
                except ValueError:
                    return None
    return None


def check_script_defaults(cfg: dict) -> list[str]:
    findings = []
    for rel, dict_name, mapping in SCRIPT_DEFAULTS:
        path = REPO / rel
        defaults = read_default_dict(path, dict_name)
        if defaults is None:
            findings.append(f"{rel}: could not read `{dict_name}` — check skipped")
            continue
        for key, dotted in mapping.items():
            if key not in defaults:
                continue
            want, got = dig(cfg, dotted), defaults[key]
            if want is None:
                continue
            if want != got:
                findings.append(
                    f"{rel}:{dict_name}[{key!r}] = {got!r}  but  cse.config.yml "
                    f"{dotted} = {want!r}"
                )
    return findings


def cues_for(dotted: str) -> tuple[str, ...]:
    if dotted in ALIASES:
        return ALIASES[dotted]
    tail = dotted.split(".")[-1]
    return tuple(w for w in tail.split("_") if len(w) >= 4) or (tail,)


def prose_files() -> list[Path]:
    seen: list[Path] = []
    for pattern in PROSE_GLOBS:
        for p in sorted(REPO.glob(pattern)):
            rel = p.relative_to(REPO).as_posix()
            if p.is_file() and not any(rel.startswith(x) for x in PROSE_EXCLUDE):
                seen.append(p)
    return seen


def check_prose(cfg: dict) -> list[str]:
    tracked = []
    for _, _, mapping in SCRIPT_DEFAULTS:
        for dotted in mapping.values():
            val = dig(cfg, dotted)
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                tracked.append((dotted, val))
            elif isinstance(val, dict):
                # Weight tables: each entry is its own value, and its KEY is the cue
                # ("🔴 3.0", "Easy 0.5"), so flatten rather than skipping the block.
                for k, v in val.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        tracked.append((f"{dotted}.{k}", v))
    tracked = sorted(set(tracked))

    findings = []
    for path in prose_files():
        rel = path.relative_to(REPO).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        # File-level opt-out: a log is historical in its ENTIRETY (every entry is dated and
        # states what a number was at the time). Marking those line by line would be absurd
        # and would guarantee the marker rots, so one declaration near the top covers it.
        if any(OPT_OUT in ln.lower() for ln in lines[:5]):
            continue
        skipping = False
        for n, line in enumerate(lines, 1):
            low = line.lower()
            if line.lstrip().startswith("#") or line.lstrip().startswith("<!--"):
                # A heading or comment carrying the marker opens a history section; any
                # other heading closes it.
                skipping = OPT_OUT in low
                if OPT_OUT in low:
                    continue
            if skipping or OPT_OUT in low:
                continue
            # A tracker/coverage DATA row is not a restatement: a Streak column holding 3,
            # or a Next Review holding a date, is the value APPLIED, which is what the
            # engine is for. Data rows carry an ISO date and several pipes; a legend or a
            # rules table does not.
            if line.count("|") >= 4 and re.search(r"\d{4}-\d{2}-\d{2}", line):
                continue
            for dotted, val in tracked:
                cues = cues_for(dotted)
                if not any(c.lower() in low for c in cues):
                    continue
                # The value as prose writes it — 30 and 30.0, 8 and 8.0 — but only when the
                # surrounding text ASSERTS it (see VALUE_FORMS), never a bare digit.
                num = rf"{re.escape(f'{val:g}')}(?:\.0+)?"
                cue_alt = "|".join(re.escape(c) for c in cues)
                hit = any(
                    re.search(f.format(n=num, cue=f"(?:{cue_alt})"), low)
                    for f in forms_for(dotted)
                )
                if hit:
                    findings.append(f"{rel}:{n}: states {dotted} = {val:g} — {line.strip()[:88]}")
                    break
    return findings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any value is stated in more than one place")
    args = ap.parse_args()

    cfg = load_yaml()
    hard = check_script_defaults(cfg)
    soft = check_prose(cfg)
    dead = check_retired(prose_files())

    if hard:
        print(f"\n❌ SCRIPT DEFAULTS DISAGREE WITH cse.config.yml ({len(hard)})")
        print("   These change what the engine COMPUTES. Fix by deleting the default or "
              "making it read the config.")
        for f in hard:
            print(f"   {f}")
    if soft:
        print(f"\n⚠️  VALUES RESTATED IN PROSE ({len(soft)})")
        print("   Prose should POINT at the config, not copy it — a copy goes stale "
              "silently. Mark genuine")
        print(f"   history with `{OPT_OUT}` in a comment on the line or its heading.")
        for f in soft:
            print(f"   {f}")
    if dead:
        print(f"\n🪦 RETIRED VOCABULARY STILL IN RULE FILES ({len(dead)})")
        print("   These read as current and contradict the live rule. Rewrite as a redirect, "
              "or mark the")
        print(f"   file `{OPT_OUT}` if it is a dated log.")
        for f in dead:
            print(f"   {f}")
    if not hard and not soft and not dead:
        print("✅ every tracked value is stated in exactly one place")

    if args.check and (hard or dead):
        sys.exit(1)


if __name__ == "__main__":
    main()
