"""One-off: seed dashboard/bigo.yml from the site's own complexity metadata.

The Big-O Trainer's manifest (`dashboard/bigo.yml`) needs a time/space bound for every
solution file — 130 LeetCode numbers. Hand-writing all of them is the exact busywork the
grounded-solutions contract exists to avoid, and the site already carries this information
twice: every `*.steps.ts` file's `AlgorithmMeta` declares its own `timeComplexity`/
`spaceComplexity`, and `big-o-questions.data.ts` (the trainer's old hand-written question
set, retired once this has run) carries a worked explanation for 26 of them. This script
reads both, maps their inconsistent spellings onto `export_bigo.COMPLEXITY_POOL`, and
writes a manifest a human then edits by hand — TODO where nothing mapped, a "verify" tag
on everything that did.

READ-ONLY w.r.t. the solutions: never writes a `dsa/leetcode/*.py` file or anything under
`--site`. Run once; re-running with `--force` clobbers any hand-edit already made to the
output, which `--force` says plainly.

Usage:
    python scripts/seed_bigo.py --site ../michael-yrao.github.io             # write dashboard/bigo.yml
    python scripts/seed_bigo.py --site ../michael-yrao.github.io --stdout    # print YAML, write nothing
    python scripts/seed_bigo.py --site ../michael-yrao.github.io --force     # overwrite an existing bigo.yml
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import yaml

import _console
import export_bigo
import export_showcase as es
import links

_console.force_utf8()

REPO = Path(__file__).resolve().parent.parent
DASHBOARD = REPO / "dashboard"
DEFAULT_OUT = DASHBOARD / "bigo.yml"
SHOWCASE_MANIFEST = DASHBOARD / "showcase.yml"

STEPS_GLOB = "src/app/algorithms/**/*.steps.ts"
QUESTIONS_REL = "src/app/core/data/big-o-questions.data.ts"

EXPLANATION_WRAP_WIDTH = 88
_QUALIFIER_STRIP_CHARS = " -—"  # space, hyphen, em dash — the site's own separators


class SeedError(Exception):
    """A fatal problem reading the site or the solutions. Never caught silently: this is
    a one-off tool and a partial/garbled seed is worse than a loud failure."""


# ── site text parsing (pure: text in, no filesystem access) ─────────────────────────────

_LC_NUMBER = re.compile(r"\blcNumber:\s*(\d+)")
_DIFFICULTY = re.compile(r"\bdifficulty:\s*'([^']*)'")
_COMPLEXITY_PAIR = re.compile(r"timeComplexity:\s*'([^']*)'\s*,\s*spaceComplexity:\s*'([^']*)'")


def parse_steps_file(text: str) -> dict:
    """lcNumber, difficulty, and the problem-level (time, space) pair for one
    `*.steps.ts` file, plus every per-variant pair as `variants`.

    A file's `AlgorithmMeta` declares exactly one (time, space) pair of its own — the
    FIRST complexity pair found after the `lcNumber:` line, regardless of whether its
    `SolutionVariant`s are separate consts declared BEFORE the meta object (their pairs
    then precede `lcNumber:`) or objects inline inside the meta's own `solutions: [...]`
    array (their pairs then follow the problem-level one). Every other pair found — before
    `lcNumber:` or after the first one past it — is a variant pair, in file order.
    """
    lc_match = _LC_NUMBER.search(text)
    if lc_match is None:
        raise SeedError("no `lcNumber:` found — not an AlgorithmMeta steps file")
    lc_pos = lc_match.start()

    difficulty_match = _DIFFICULTY.search(text)
    difficulty = difficulty_match.group(1) if difficulty_match else None

    pairs = [(m.start(), m.group(1), m.group(2)) for m in _COMPLEXITY_PAIR.finditer(text)]
    before = [(t, s) for pos, t, s in pairs if pos < lc_pos]
    after = [(t, s) for pos, t, s in pairs if pos > lc_pos]
    if not after:
        raise SeedError(
            f"lc {lc_match.group(1)}: no problem-level complexity pair found after `lcNumber:`")
    problem_time, problem_space = after[0]

    return {
        "lcNumber": int(lc_match.group(1)),
        "difficulty": difficulty,
        "time": problem_time,
        "space": problem_space,
        "variants": before + after[1:],
    }


_QUESTION_ID = re.compile(r"id:\s*'([^']*)'")
_CONTEXT = re.compile(r"context:\s*'([^']*)'")
_CORRECT_TIME = re.compile(r"correctTime:\s*'([^']*)'")
_CORRECT_SPACE = re.compile(r"correctSpace:\s*'([^']*)'")
_TIME_EXPLANATION = re.compile(r"timeExplanation:\s*'([^']*)'")
_SPACE_EXPLANATION = re.compile(r"spaceExplanation:\s*'([^']*)'")
_LINKED_LC = re.compile(r"linkedProblemLcNumber:\s*(\d+)")


def _first_group(pattern: re.Pattern, text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1) if match else None


def parse_questions(text: str) -> dict[int, list[dict]]:
    """lc -> the BIG_O_QUESTIONS blocks naming it, each as {note, whyTime, whySpace,
    correctTime, correctSpace}, in file order.

    Splits the array on every object's `id:` field — the first field of every block,
    present exactly once — so `code:`'s multi-line Python (which could otherwise confuse a
    naive brace-matcher) never has to be parsed at all.
    """
    starts = [m.start() for m in _QUESTION_ID.finditer(text)]
    by_lc: dict[int, list[dict]] = {}
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        block = text[start:end]
        lc_match = _LINKED_LC.search(block)
        if lc_match is None:
            continue
        by_lc.setdefault(int(lc_match.group(1)), []).append({
            "note": _first_group(_CONTEXT, block),
            "whyTime": _first_group(_TIME_EXPLANATION, block),
            "whySpace": _first_group(_SPACE_EXPLANATION, block),
            "correctTime": _first_group(_CORRECT_TIME, block),
            "correctSpace": _first_group(_CORRECT_SPACE, block),
        })
    return by_lc


# ── normalise_label: the site's inconsistent spellings -> one canonical pool ────────────

_O_PAREN = re.compile(r"O\(")
_WHITESPACE = re.compile(r"\s+")
_PLUS_NM = re.compile(r"^O\(\s*[mn]\s*\+\s*[mn]\s*\)$")
_PLUS_VE = re.compile(r"^O\(\s*(?:V\s*\+\s*E|n\s*\+\s*e)\s*\)$")
_MIN_NK = re.compile(r"^O\(\s*min\(\s*n\s*,\s*k\s*\)\s*\)$")
_MAX_MN = re.compile(r"^O\(\s*max\(\s*m\s*,\s*n\s*\)\s*\)$")


def _extract_balanced(text: str, open_index: int) -> str:
    """`text[open_index:end]` for the parenthesized group opening at `text[open_index]`.
    Raises ValueError on an unbalanced string (a malformed site string, not our bug to
    crash the whole run over)."""
    depth = 0
    for index in range(open_index, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return text[open_index:index + 1]
    raise ValueError(f"unbalanced parentheses in {text!r}")


def _apply_spelling_map(label: str) -> str:
    """The site's known inconsistent spellings collapsed onto their canonical form — see
    the plan's label contract. Everything else passes through unchanged (still checked
    against the live pool by the caller, so an unrecognized spelling correctly falls to
    TODO rather than being silently forced into a wrong canonical label)."""
    label = label.replace("×", "·")            # × → ·
    label = re.sub(r"\s*·\s*", "·", label)      # no spaces around ·
    if _PLUS_NM.match(label):
        return "O(n + m)"
    if _PLUS_VE.match(label):
        return "O(V+E)"
    if _MIN_NK.match(label):
        return "O(min(n, k))"
    if _MAX_MN.match(label):
        return "O(max(m, n))"
    return label


def normalise_label(raw: str) -> tuple[str | None, str]:
    """(canonical-or-None, leftover qualifier) for one site complexity string.

    Takes the first balanced `O(...)` anywhere in `raw`, collapses its inner whitespace,
    applies the known spelling map, then checks membership against the LIVE
    `export_bigo.COMPLEXITY_POOL` — never a locally held copy, so a pool change here never
    goes stale. Text left over after the closing paren (`amortized`, `per add`, `— at most
    26 tasks`, …) is the qualifier; the raw text itself always stays available to the
    caller for the "site said" verify comment, so nothing here is lossy.
    """
    match = _O_PAREN.search(raw)
    if match is None:
        return None, raw.strip(_QUALIFIER_STRIP_CHARS)
    try:
        label = _extract_balanced(raw, match.start())
    except ValueError:
        return None, raw.strip(_QUALIFIER_STRIP_CHARS)

    qualifier = raw[match.start() + len(label):].strip(_QUALIFIER_STRIP_CHARS)
    label = _apply_spelling_map(_WHITESPACE.sub(" ", label).strip())
    if label in export_bigo.COMPLEXITY_POOL:
        return label, qualifier
    return None, qualifier


def build_qualifier_note(time_qualifier: str, space_qualifier: str) -> str | None:
    """The manifest `note:` text when an entry has no matching question context: a shared
    qualifier once, or `"time: …; space: …"` when the two axes' qualifiers differ."""
    if time_qualifier and space_qualifier:
        if time_qualifier == space_qualifier:
            return time_qualifier
        return f"time: {time_qualifier}; space: {space_qualifier}"
    return time_qualifier or space_qualifier or None


def pick_question_block(blocks: list[dict], seeded_time: str | None,
                         seeded_space: str | None) -> tuple[dict | None, bool]:
    """(block, was_ambiguous) — the block whose normalised correct pair equals the
    entry's own seeded (time, space) pair (the LC 206 case: iterative vs recursive carry
    different correct pairs). No blocks -> (None, False). One block -> it, unambiguous.
    Multiple with no unique match -> the first, flagged ambiguous."""
    if not blocks:
        return None, False
    if len(blocks) == 1:
        return blocks[0], False
    seeded = (seeded_time, seeded_space)
    matches = [b for b in blocks
               if (normalise_label(b["correctTime"] or "")[0],
                   normalise_label(b["correctSpace"] or "")[0]) == seeded]
    if len(matches) == 1:
        return matches[0], False
    return blocks[0], True


# ── seeding: one manifest entry per solution file, using export_bigo's own pick rule ────

@dataclass(frozen=True)
class SummaryEvent:
    kind: str
    key: str
    detail: str = ""


@dataclass(frozen=True)
class SeedResult:
    entry: dict
    folder: str
    verify_comment: str | None
    time_todo_reason: str | None
    space_todo_reason: str | None


@dataclass(frozen=True)
class SiteFields:
    entry_fields: dict
    verify_comment: str | None
    time_todo_reason: str | None
    space_todo_reason: str | None
    events: tuple[SummaryEvent, ...] = field(default_factory=tuple)


_FILE_LEADING_NUM = re.compile(r"^(\d+)_")


def discover_solution_files() -> dict[int, list[Path]]:
    """lc -> every solution file matching it, across every configured source root — more
    than one file means a twin (currently only 1216)."""
    by_lc: dict[int, list[Path]] = {}
    for root in links.source_roots():
        for path in sorted(root.glob("*/*.py")):
            match = _FILE_LEADING_NUM.match(path.name)
            if match:
                by_lc.setdefault(int(match.group(1)), []).append(path)
    return by_lc


def load_steps_by_lc(site: Path) -> dict[int, dict]:
    by_lc: dict[int, dict] = {}
    for path in sorted(site.glob(STEPS_GLOB)):
        text = path.read_text(encoding="utf-8")
        parsed = {**parse_steps_file(text), "path": path.relative_to(site).as_posix()}
        by_lc[parsed["lcNumber"]] = parsed
    return by_lc


def load_showcase_entries() -> list[dict]:
    data = yaml.safe_load(SHOWCASE_MANIFEST.read_text(encoding="utf-8")) or {}
    return data.get("entries") or []


def _dated_candidate_dates(table: dict[str, ast.AST], lines: list[str]) -> list[str]:
    """Every dated candidate's date string — the same inputs
    `export_bigo.latest_dated_attempt` reads, so a tie it breaks is visible here too."""
    dates: list[str] = []
    for _container, symbol, node in export_bigo.candidate_symbols(table):
        start = es.def_start_line(node)
        banner = es.leading_comment_block(lines, start)
        banner_lines = lines[banner[0] - 1:banner[1]] if banner else []
        date = es.attempt_date(symbol, banner_lines)
        if date is not None:
            dates.append(date)
    return dates


def _has_latest_date_tie(table: dict[str, ast.AST], lines: list[str]) -> bool:
    dates = _dated_candidate_dates(table, lines)
    return bool(dates) and dates.count(max(dates)) > 1


def _undated_fallback_pick(table: dict[str, ast.AST]) -> tuple[str | None, str]:
    """(container, symbol) for a file with NO dated attempt at all: the candidate lowest
    in the file (highest `def_start_line`) — the tie-break `latest_dated_attempt` already
    uses among equal dates, extended to "nothing is dated"."""
    candidates = export_bigo.candidate_symbols(table)
    if not candidates:
        raise SeedError("no Solution methods or top-level defs/classes found")
    container, symbol, _node = max(candidates, key=lambda c: es.def_start_line(c[2]))
    return container, symbol


def _resolve_symbol_fields(table: dict[str, ast.AST], lines: list[str],
                            key: str) -> tuple[dict, list[SummaryEvent]]:
    """({} or {'symbol': ..., 'container': None}, events) for a non-twin entry. Empty
    when the file has a dated attempt — `export_bigo.py` auto-picks it at build time."""
    if export_bigo.latest_dated_attempt(table, lines) is not None:
        events = [SummaryEvent("latest-date-tie", key)] if _has_latest_date_tie(table, lines) else []
        return {}, events
    container, symbol = _undated_fallback_pick(table)
    fields = {"symbol": symbol, **({"container": None} if container is None else {})}
    return fields, [SummaryEvent("explicit-symbol", key)]


def _site_fields(lc: int, key: str, steps_by_lc: dict[int, dict],
                  questions_by_lc: dict[int, list[dict]]) -> SiteFields:
    """Everything the site's own data contributes to one entry: the time/space bounds
    (a canonical label or TODO_LABEL), an optional note/whyTime/whySpace, and the
    comments `render_yaml` attaches."""
    steps = steps_by_lc.get(lc)
    if steps is None:
        todo = export_bigo.TODO_LABEL
        reason = "no site match — fill in"
        return SiteFields({"time": todo, "space": todo}, None, reason, reason,
                           (SummaryEvent("todo-no-site-match", key),))

    canon_time, qual_time = normalise_label(steps["time"])
    canon_space, qual_space = normalise_label(steps["space"])
    verify_comment = f"seeded from site — verify ({steps['path']}: {steps['time']}/{steps['space']})"

    events: list[SummaryEvent] = []
    if canon_time is None:
        events.append(SummaryEvent("todo-unmappable", key, steps["time"]))
    if canon_space is None:
        events.append(SummaryEvent("todo-unmappable", key, steps["space"]))
    # `export_bigo.build_payload` skips the WHOLE entry when EITHER axis is TODO, so
    # "both axes mapped" (reaches big-o.json as-is) and "one axis mapped, one TODO"
    # (still skipped until the learner fills the TODO in) are different outcomes worth
    # telling apart in the summary — a flat "seeded" count previously overstated how many
    # entries actually reach big-o.json today.
    if canon_time is not None and canon_space is not None:
        events.append(SummaryEvent("seeded-both", key))
    elif canon_time is not None or canon_space is not None:
        events.append(SummaryEvent("seeded-partial", key))

    block, ambiguous = pick_question_block(questions_by_lc.get(lc, []), canon_time, canon_space)
    text_fields: dict = {}
    if block is not None:
        events.append(SummaryEvent("question-used", key))
        if ambiguous:
            events.append(SummaryEvent("question-ambiguous", key))
        text_fields = {k: block[v] for k, v in
                       (("note", "note"), ("whyTime", "whyTime"), ("whySpace", "whySpace"))
                       if block.get(v)}
    else:
        note = build_qualifier_note(qual_time, qual_space)
        if note:
            text_fields = {"note": note}

    fields = {"time": canon_time or export_bigo.TODO_LABEL,
              "space": canon_space or export_bigo.TODO_LABEL, **text_fields}
    time_reason = None if canon_time is not None else f"site said '{steps['time']}'"
    space_reason = None if canon_space is not None else f"site said '{steps['space']}'"
    return SiteFields(fields, verify_comment, time_reason, space_reason, tuple(events))


def seed_single_entry(lc: int, path: Path, steps_by_lc: dict[int, dict],
                       questions_by_lc: dict[int, list[dict]]
                       ) -> tuple[SeedResult, list[SummaryEvent]]:
    lines = es.read_lines(path)
    table = es.symbol_table(ast.parse("\n".join(lines)))
    key = export_bigo.entry_key({"lc": lc})

    symbol_fields, symbol_events = _resolve_symbol_fields(table, lines, key)
    site = _site_fields(lc, key, steps_by_lc, questions_by_lc)

    entry = {"lc": lc, **symbol_fields, **site.entry_fields}
    result = SeedResult(entry, path.parent.name, site.verify_comment,
                         site.time_todo_reason, site.space_todo_reason)
    return result, symbol_events + list(site.events)


def seed_twin_entries(lc: int, files: list[Path], steps_by_lc: dict[int, dict],
                       questions_by_lc: dict[int, list[dict]], showcase_entries: list[dict]
                       ) -> tuple[list[SeedResult], list[SummaryEvent]]:
    """One entry per twin file, with `file:`/`variant:`/`symbol:` taken from
    `dashboard/showcase.yml`'s own entry for that same file — never auto-picked, since
    the two files are unrelated attempts at the same number, not variants of one file."""
    by_file = {e.get("file"): e for e in showcase_entries if e.get("lc") == lc}
    results: list[SeedResult] = []
    events: list[SummaryEvent] = [SummaryEvent("twin", str(lc))]
    for path in files:
        file_rel = path.relative_to(REPO).as_posix()
        showcase_entry = by_file.get(file_rel)
        if showcase_entry is None:
            raise SeedError(
                f"lc {lc}: twin file '{file_rel}' has no matching dashboard/showcase.yml "
                f"entry (need its variant/symbol to seed bigo.yml)")
        variant = showcase_entry["variant"]
        key = export_bigo.entry_key({"lc": lc, "variant": variant})
        is_top_level_class = "container" in showcase_entry and showcase_entry["container"] is None
        symbol_fields = {"symbol": showcase_entry["symbol"],
                          **({"container": None} if is_top_level_class else {})}
        events.append(SummaryEvent("explicit-symbol", key))

        site = _site_fields(lc, key, steps_by_lc, questions_by_lc)
        events.extend(site.events)

        entry = {"lc": lc, "variant": variant, "file": file_rel, **symbol_fields, **site.entry_fields}
        results.append(SeedResult(entry, path.parent.name, site.verify_comment,
                                   site.time_todo_reason, site.space_todo_reason))
    return results, events


def seed_all(site: Path, steps_by_lc: dict[int, dict], questions_by_lc: dict[int, list[dict]],
             showcase_entries: list[dict]) -> tuple[list[SeedResult], list[SummaryEvent]]:
    results: list[SeedResult] = []
    events: list[SummaryEvent] = []
    for lc, files in sorted(discover_solution_files().items()):
        if len(files) > 1:
            entry_results, entry_events = seed_twin_entries(
                lc, files, steps_by_lc, questions_by_lc, showcase_entries)
        else:
            single_result, entry_events = seed_single_entry(lc, files[0], steps_by_lc, questions_by_lc)
            entry_results = [single_result]
        results.extend(entry_results)
        events.extend(entry_events)
    return results, events


# ── render_yaml: hand-rendered — PyYAML can't emit comments ─────────────────────────────

HEADER_COMMENT = """\
# The Big-O Trainer's manifest: one entry per LeetCode number (or per twin file, keyed
# `lc:variant`), picking which real attempt answers its time/space question.
# `symbol`/`container` default the same way dashboard/showcase.yml's do — the latest
# DATED attempt in the file, ties -> the symbol lowest in the file; an entry only needs
# an explicit `symbol:` when nothing in its file is dated. `time`/`space` must be a label
# from scripts/export_bigo.py's COMPLEXITY_POOL, or `TODO` for a bound not yet filled in.
#
# Seeded once from the site's own per-problem complexity metadata and its 26 existing
# question explanations by scripts/seed_bigo.py — every seeded entry is tagged "seeded
# from site — verify"; a TODO bound or a bare qualifier note is the learner's own rep to
# fill in, not this script's guess. See decisions.yml `bigo-contract`."""

_YAML_PLAIN_SAFE = re.compile(r"^[^\s:#'\"\[\]{},&*!|>%@`][^:#]*$")


def _yaml_scalar(value: str) -> str:
    """A YAML plain scalar for `value` when safe, else a double-quoted one. Defensive:
    every field this manifest writes is currently a safe identifier/path/pool-label, but
    nothing here re-derives PyYAML's own quoting rules, so this stays explicit."""
    if value and _YAML_PLAIN_SAFE.match(value) and not value.endswith((":", "#")):
        return value
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _field_line(field_name: str, value: str, todo_reason: str | None) -> str:
    line = f"    {field_name}: {_yaml_scalar(value)}"
    return f"{line}  # {todo_reason}" if todo_reason else line


def _render_block_scalar(field_name: str, text: str) -> list[str]:
    """A YAML folded block scalar (`>-`) for a long free-text field — round-trips through
    `yaml.safe_load` back to the exact normalized text regardless of wrap width, since a
    folded scalar joins its lines with single spaces."""
    normalized = _WHITESPACE.sub(" ", text).strip()
    wrapped = textwrap.wrap(normalized, width=EXPLANATION_WRAP_WIDTH, break_long_words=False) or [normalized]
    return [f"    {field_name}: >-"] + [f"      {line}" for line in wrapped]


def _render_entry(result: SeedResult) -> list[str]:
    entry = result.entry
    out = [f"  - lc: {entry['lc']}"]
    if result.verify_comment:
        out.append(f"    # {result.verify_comment}")
    for field_name in ("variant", "file", "symbol"):
        if field_name in entry:
            out.append(f"    {field_name}: {_yaml_scalar(entry[field_name])}")
    if "container" in entry:
        out.append("    container: null")
    out.append(_field_line("time", entry["time"], result.time_todo_reason))
    out.append(_field_line("space", entry["space"], result.space_todo_reason))
    for field_name in ("note", "whyTime", "whySpace"):
        if entry.get(field_name):
            out.extend(_render_block_scalar(field_name, entry[field_name]))
    out.append("")
    return out


def render_yaml(results: list[SeedResult]) -> str:
    lines = [HEADER_COMMENT, "schemaVersion: 1", "entries:"]
    current_folder: str | None = None
    for result in results:
        if result.folder != current_folder:
            lines.append("")
            lines.append(f"  # ── {result.folder} ──")
            current_folder = result.folder
        lines.extend(_render_entry(result))
    return "\n".join(lines) + "\n"


# ── summary report (stderr) ──────────────────────────────────────────────────────────

def _summary_line(label: str, keys: list[str]) -> str:
    tail = ", ".join(keys) if keys else "(none)"
    return f"{label}: {len(keys)} — {tail}"


def print_summary(events: list[SummaryEvent]) -> None:
    by_kind: dict[str, list[SummaryEvent]] = {}
    for event in events:
        by_kind.setdefault(event.kind, []).append(event)

    def keys(kind: str) -> list[str]:
        return [e.key for e in by_kind.get(kind, [])]

    unmappable = [f"{e.key} ({e.detail!r})" for e in by_kind.get("todo-unmappable", [])]
    print(_summary_line("seeded (both axes)", keys("seeded-both")), file=sys.stderr)
    print(_summary_line("partially seeded (one axis TODO — skipped until filled)",
                         keys("seeded-partial")), file=sys.stderr)
    print(_summary_line("TODO (no site match)", keys("todo-no-site-match")), file=sys.stderr)
    print(_summary_line("TODO (unmappable)", unmappable), file=sys.stderr)
    print(_summary_line("explicit symbol", keys("explicit-symbol")), file=sys.stderr)
    print(_summary_line("latest-date ties", keys("latest-date-tie")), file=sys.stderr)
    print(_summary_line("questions used", keys("question-used")), file=sys.stderr)
    ambiguous = keys("question-ambiguous")
    if ambiguous:
        print(f"multi-question choices (tied on the seeded pair — took the first): "
              f"{', '.join(ambiguous)}", file=sys.stderr)
    twins = keys("twin")
    if twins:
        print(f"twins (seeded both files — the site's one pair may fit only one): "
              f"{', '.join(twins)}", file=sys.stderr)


# ── CLI ───────────────────────────────────────────────────────────────────────────────

def _load_and_seed(site: Path) -> tuple[list[SeedResult], list[SummaryEvent]]:
    """(results, events) for every solution file, or a SeedError naming the problem."""
    steps_by_lc = load_steps_by_lc(site)
    if not steps_by_lc:
        raise SeedError(f"no *.steps.ts files found under '{site}' — is --site correct?")
    questions_by_lc = parse_questions((site / QUESTIONS_REL).read_text(encoding="utf-8"))
    showcase_entries = load_showcase_entries()
    return seed_all(site, steps_by_lc, questions_by_lc, showcase_entries)


def _self_check(rendered: str) -> None:
    """Every rendered entry must round-trip through YAML and pass export_bigo's own shape
    validation — a seeding bug fails loudly HERE, never surfaces later as a confusing
    export_bigo.py error at build time."""
    parsed = yaml.safe_load(rendered)
    for raw_entry in parsed["entries"]:
        export_bigo._validate_entry_shape(raw_entry)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True, metavar="PATH",
                     help="path to the michael-yrao.github.io checkout")
    ap.add_argument("--out", metavar="PATH", default=str(DEFAULT_OUT),
                     help="where to write the manifest (default: dashboard/bigo.yml)")
    ap.add_argument("--force", action="store_true", help="overwrite --out if it already exists")
    ap.add_argument("--stdout", action="store_true", help="print the YAML, do not write")
    args = ap.parse_args()

    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"ERROR: --site '{site}' is not a directory", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out)
    if not args.stdout and out_path.exists() and not args.force:
        print(f"ERROR: '{out_path}' already exists — this is a one-off seed; pass "
              f"--force to overwrite it (which clobbers any hand-edit already made there).",
              file=sys.stderr)
        sys.exit(1)

    try:
        results, events = _load_and_seed(site)
    except (SeedError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    results = sorted(results, key=lambda r: (r.folder, r.entry["lc"], r.entry.get("variant") or ""))
    rendered = render_yaml(results)
    _self_check(rendered)
    print_summary(events)

    if args.stdout:
        print(rendered)
        return

    DASHBOARD.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"wrote {out_path} ({len(results)} entries)")


if __name__ == "__main__":
    main()
