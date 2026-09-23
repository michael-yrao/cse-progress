"""Generate /learn's technique cheat sheet from the technique docs (C2 of the
learn-cheatsheet plan — see docs/cse-coach/learn_cheatsheet_plan.md).

    docs/foundations/dsa/patterns/techniques/*.md
      + intuition_cheatsheet.md's Signal -> technique table
      + techniques.yml (family/tier, joined by a `doc:` key)
    ->  dashboard/cheat-sheets.json  +  dashboard/cheat-sheets.schema.json

Usage:
    python scripts/build_cheatsheets.py             # write both files
    python scripts/build_cheatsheets.py --validate   # compute + report; write nothing
    python scripts/build_cheatsheets.py --stdout     # print the JSON, do not write

Design constraints this file honours (see CLAUDE.md, docs/cse-coach/learn_cheatsheet_plan.md):

  * THE DOCS STAY PROSE. The generator reads only five exact headings per doc (see the
    HEADING_* constants) and ignores everything else — the "Understanding …" / "Key
    Insights" deep-dives stay untouched. `scripts/check_cheatsheets.py --check` is what
    enforces the contract; this file degrades gracefully instead (a missing/short section
    yields 'TODO' or an empty list, never a crash — see the schema's own field docs).

  * SINGLE SOURCE OF TRUTH. No tuned number lives here — family/tier come from
    techniques.yml, content comes from the docs. The one HARD failure this file raises is
    the techniques.yml join (0 or >1 entries carrying a given `doc:` key): that is not a
    content gap, it is a vocabulary bug that would silently mis-tag a technique.

  * IDEMPOTENT. Two runs back to back differ only in `generatedAt` — nothing else in the
    payload depends on wall-clock time or file-system iteration order beyond the sorted
    glob below.

  * THE SEED IS THE TARGET, NOT THE INPUT. scripts/fixtures/cheat-sheets.seed.json is a
    byte copy of the site's Phase-B seed (tech-lead-authored content the docs did not yet
    carry). This generator's job is to REPRODUCE it once the docs conform — see
    scripts/test_build_cheatsheets.py's golden test — never to read from it.

Markdown stripping (see the plan's "The markdown contract" section): the markdown noise
carried into emitted text is `**bold**`, single-`*` `*italic*` and `[text](url)` links —
all three are unwrapped down to their plain text; backticks pass through untouched — see
clean()'s docstring for the empirical check against the seed that pins this.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import _console

_console.force_utf8()

REPO = Path(__file__).resolve().parent.parent
TECHNIQUES_DIR = REPO / "docs/foundations/dsa/patterns/techniques"
INTUITION_DOC = REPO / "docs/foundations/dsa/patterns/intuition_cheatsheet.md"
TECHNIQUES_YAML = REPO / "docs/foundations/dsa/mastery/techniques.yml"
FIXTURES = REPO / "scripts/fixtures"
SCHEMA_FIXTURE = FIXTURES / "cheat-sheets.schema.json"
DASHBOARD = REPO / "dashboard"
OUT = DASHBOARD / "cheat-sheets.json"
OUT_SCHEMA = DASHBOARD / "cheat-sheets.schema.json"

SCHEMA_VERSION = 1
DEFAULT_TIER = "core"
TODO = "TODO"

# The five headings the contract reads — exact text, except HEADING_TEMPLATE_PREFIX, which
# is a prefix ("## Template: <title>", one heading per variant). Named as constants per the
# plan so a heading-text change is a one-line edit here and nowhere else.
HEADING_WHEN = "When to reach for it"
HEADING_PICKING = "Picking feature"
HEADING_TEMPLATE_PREFIX = "Template: "
HEADING_PITFALLS = "Common pitfalls"
HEADING_PRACTICE = "Practice"

WHEN_PREFIX = "*When:* "
COMPLEXITY_PREFIX = "Complexity: "
COMPLEXITY_TIME_SEP = " time · "
COMPLEXITY_SPACE_SEP = " space — "

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
# A single-`*` italic span: the opening `*` must not be followed by whitespace and the
# closing `*` must not be preceded by whitespace (markdown's own flanking rule) — this is
# what keeps a spaced multiplication like `` `r * cols + c` `` from being mistaken for a
# pair of italic delimiters.
ITALIC_RE = re.compile(r"\*(?!\s)([^*\n]+?)(?<!\s)\*")

NOT_WHEN_RE = re.compile(r"^\*\*not\s+(.+?)\*\*\s*—\s*(.*)$")
PRACTICE_LC_RE = re.compile(r"^LC\s+(\d+)\s+—\s+(.*)$")
PRACTICE_LINK_RE = re.compile(r"^\[(\d+)\.\s+([^\]]+)\]\(")

SIGNAL_TABLE_HEADING = "Signal → technique"
SIGNAL_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
SIGNAL_DOC_LINK_RE = re.compile(r"\[[^\]]+\]\(techniques/([^)]+)\.md\)")
PAREN_RE = re.compile(r"^(.*?)\s*\((.*)\)\s*$")

# A leading emoji run (e.g. recursion.md's "# 🧠 Recursion & …") plus the whitespace after
# it. Ranges cover the common emoji blocks (misc symbols/dingbats, supplemental
# symbols-and-pictographs) plus the variation-selector codepoint some emoji carry.
LEADING_EMOJI_RE = re.compile(r"^[\U0001F000-\U0001FFFF☀-➿️]+\s*")
NAME_SUFFIX = " Patterns"

DOC_URL_TMPL = ("https://github.com/michael-yrao/cse-progress/blob/main/"
                "docs/foundations/dsa/patterns/techniques/{stem}.md")

# The intuition_cheatsheet.md "Reach for" cell usually carries its qualifier as a
# parenthetical after the base label ("two pointers (converge from ends)" -> note
# "converge from ends" — see default_note()). Six of the current 23 rows don't fit that
# shape: either the whole cell IS the qualifier with no base/paren split ("monotonic
# deque", "sort by **start**, sweep", "DFS postorder", "DFS inorder"), or the base/paren
# roles are inverted ("DP (memoization)" -> note "DP", not "memoization", since
# "memoization" is just the technique's own name repeated). Fitted to the CURRENT 23-row
# table (2026-09-22) — a new row follows default_note() unless it needs adding here too.
REACH_NOTE_OVERRIDES = {
    "monotonic deque": "monotonic deque",
    "sort by start, sweep": "sort by start, sweep",
    "sort by end, greedy frontier": "sort by end, greedy frontier",
    "DFS postorder": "DFS postorder",
    "DFS inorder": "DFS inorder",
    "DP (memoization)": "DP",
}


class BuildError(Exception):
    """A fatal, must-fix condition — currently only the techniques.yml join (0 or >1
    entries for a doc's `doc:` key). Ordinary missing/short doc content is never fatal
    here; it degrades to 'TODO'/an empty list instead (fail-soft, like every other
    generator in this repo) and scripts/check_cheatsheets.py is the hard gate for that."""


# ── markdown primitives ──────────────────────────────────────────────────────────────

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def clean(text: str) -> str:
    """Strip the contract's markdown noise carried into emitted text: `**bold**` markers,
    single-`*` `*italic*` spans and `[text](url)` links (unwrapped to `text`). Backticks
    pass through untouched — checked empirically against
    scripts/fixtures/cheat-sheets.seed.json (no stray markup of any of those three kinds
    survives into a non-code text field there; code fences are never passed through this)."""
    text = text.replace("**", "")
    text = LINK_RE.sub(r"\1", text)
    return ITALIC_RE.sub(r"\1", text)


def split_h2_sections(text: str) -> list[tuple[str, list[str]]]:
    """Level-2 (`## `) headings -> [(heading text, body lines)], fence-aware: a line
    inside a ```-fenced block (including one that itself starts with `##`, e.g. a Python
    comment) is never mistaken for a heading, and fence delimiter lines are kept in the
    body so find_python_fence() can find them again."""
    sections: list[tuple[str, list[str]]] = []
    heading: str | None = None
    body: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("## "):
            if heading is not None:
                sections.append((heading, body))
            heading, body = line[3:].strip(), []
            continue
        if heading is not None:
            body.append(line)
    if heading is not None:
        sections.append((heading, body))
    return sections


def extract_h1(text: str) -> str:
    """The doc's level-1 heading: leading emoji + whitespace stripped, a trailing
    ' Patterns' dropped. Fence-aware for the same reason split_h2_sections() is."""
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped.startswith("# ") or stripped.startswith("## "):
            continue
        title = LEADING_EMOJI_RE.sub("", stripped[2:].strip())
        return title[: -len(NAME_SUFFIX)] if title.endswith(NAME_SUFFIX) else title
    return ""


def first_nonblank_line(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return ""


def first_paragraph(lines: list[str]) -> str:
    """Consecutive non-blank, non-bullet lines from the start of `lines`, joined with a
    single space. Leading blank lines are skipped; the paragraph ends at the first blank
    line (once started) or the first bullet."""
    para: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if para:
                break
            continue
        if stripped.startswith("- "):
            break
        para.append(stripped)
    return " ".join(para)


def first_bullet_list(lines: list[str]) -> list[str]:
    """The first `- ` bullet list anywhere in `lines` (prose may sit before it). An
    indented continuation line is joined onto the current bullet; a blank line or a
    non-indented, non-bullet line ends the list."""
    items: list[str] = []
    current: str | None = None
    started = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            started = True
            if current is not None:
                items.append(current)
            current = stripped[2:].strip()
            continue
        if not started:
            continue
        if not stripped:
            break
        if line.startswith((" ", "\t")):
            if current is not None:
                current = f"{current} {stripped}"
            continue
        break
    if current is not None:
        items.append(current)
    return items


def find_section(sections: list[tuple[str, list[str]]], heading_text: str) -> list[str] | None:
    for heading, body in sections:
        if heading == heading_text:
            return body
    return None


def find_template_sections(sections: list[tuple[str, list[str]]]) -> list[tuple[str, list[str]]]:
    return [(h, b) for h, b in sections if h.startswith(HEADING_TEMPLATE_PREFIX)]


def find_h2_section_raw(text: str, heading_text: str) -> list[str] | None:
    return find_section(split_h2_sections(text), heading_text)


# ── technique reference resolution (id vs. label) ────────────────────────────────────

def is_technique_doc(slug: str) -> bool:
    return (TECHNIQUES_DIR / f"{slug}.md").is_file()


def technique_ref(x: str) -> dict:
    """{'technique': id} when a doc x-with-hyphens-as-underscores.md exists, else
    {'technique': x, 'page': False} — the plan's stated resolution rule, used for both
    notWhen entries and (indirectly, via the Doc-column check) the top-level signals."""
    slug = x.replace("-", "_")
    if is_technique_doc(slug):
        return {"technique": x}
    return {"technique": x, "page": False}


# ── "## When to reach for it" ────────────────────────────────────────────────────────

def parse_when_section(lines: list[str]) -> tuple[str, list[str]]:
    when_to_use = clean(first_paragraph(lines)) or TODO
    signals = [clean(b) for b in first_bullet_list(lines)]
    return when_to_use, signals


# ── "## Picking feature" ─────────────────────────────────────────────────────────────

def parse_not_when_bullet(bullet_text: str) -> dict | None:
    match = NOT_WHEN_RE.match(bullet_text)
    if not match:
        return None
    x = clean(match.group(1).strip())
    because = clean(match.group(2).strip())
    return {**technique_ref(x), "because": because}


def parse_picking_section(lines: list[str]) -> tuple[str, list[dict]]:
    feature = clean(first_nonblank_line(lines)) or TODO
    not_when = [nw for nw in (parse_not_when_bullet(b) for b in first_bullet_list(lines))
                if nw is not None]
    return feature, not_when


# ── "## Template: <title>" ───────────────────────────────────────────────────────────

def find_python_fence(lines: list[str]) -> tuple[list[str], int] | None:
    """(code lines, index just after the closing fence) for the FIRST ```python fence in
    `lines`, or None if there isn't a complete one."""
    i, n = 0, len(lines)
    while i < n and lines[i].strip() != "```python":
        i += 1
    if i >= n:
        return None
    start = i + 1
    end = start
    while end < n and lines[end].strip() != "```":
        end += 1
    if end >= n:
        return None  # unterminated fence
    return lines[start:end], end + 1


def parse_complexity_line(line: str) -> dict:
    rest = line[len(COMPLEXITY_PREFIX):]
    if COMPLEXITY_TIME_SEP not in rest:
        return {"time": TODO, "space": TODO, "why": TODO}
    time_part, _, remainder = rest.partition(COMPLEXITY_TIME_SEP)
    if COMPLEXITY_SPACE_SEP not in remainder:
        return {"time": TODO, "space": TODO, "why": TODO}
    space_part, _, why_part = remainder.partition(COMPLEXITY_SPACE_SEP)
    return {"time": clean(time_part.strip()), "space": clean(space_part.strip()),
            "why": clean(why_part.strip())}


def parse_complexity_after(lines: list[str], index: int) -> dict:
    """The first non-blank line at/after `index` — required to be the doc's `Complexity:
    …` line directly after the closing fence. TODO-triple when that line is missing,
    blank-only, or doesn't start with the expected prefix."""
    n = len(lines)
    i = index
    while i < n and not lines[i].strip():
        i += 1
    if i >= n or not lines[i].strip().startswith(COMPLEXITY_PREFIX):
        return {"time": TODO, "space": TODO, "why": TODO}
    return parse_complexity_line(lines[i].strip())


def parse_template_section(heading: str, lines: list[str]) -> dict:
    title = heading[len(HEADING_TEMPLATE_PREFIX):].strip()
    first_line = first_nonblank_line(lines)
    variant = {"title": title}
    if first_line.startswith(WHEN_PREFIX):
        variant["when"] = clean(first_line[len(WHEN_PREFIX):].strip())

    fence = find_python_fence(lines)
    if fence is None:
        variant["code"] = TODO
        variant["complexity"] = {"time": TODO, "space": TODO, "why": TODO}
    else:
        code_lines, after = fence
        variant["code"] = "\n".join(code_lines)
        variant["complexity"] = parse_complexity_after(lines, after)
    return variant


# ── "## Common pitfalls" / "## Practice" ─────────────────────────────────────────────

def parse_pitfalls_section(lines: list[str]) -> list[str]:
    return [clean(b) for b in first_bullet_list(lines)]


def parse_practice_bullet(content: str) -> dict | None:
    match = PRACTICE_LC_RE.match(content)
    if match:
        return {"lcNumber": int(match.group(1)), "title": clean(match.group(2).strip())}
    match = PRACTICE_LINK_RE.match(content)
    if match:
        return {"lcNumber": int(match.group(1)), "title": clean(match.group(2).strip())}
    return None


def parse_practice_section(lines: list[str]) -> list[dict]:
    """Only bullet lines are read — a Practice section's markdown table (the pre-contract
    doc style) or a continuation line is silently ignored, per the plan."""
    problems: list[dict] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        entry = parse_practice_bullet(stripped[2:].strip())
        if entry is not None:
            problems.append(entry)
    return problems


# ── one technique doc -> its payload entry ───────────────────────────────────────────

def parse_technique_fields(sections: list[tuple[str, list[str]]]) -> dict:
    when_to_use, signals = parse_when_section(find_section(sections, HEADING_WHEN) or [])
    feature, not_when = parse_picking_section(find_section(sections, HEADING_PICKING) or [])
    pitfalls = parse_pitfalls_section(find_section(sections, HEADING_PITFALLS) or [])
    key_problems = parse_practice_section(find_section(sections, HEADING_PRACTICE) or [])
    variants = [parse_template_section(h, b) for h, b in find_template_sections(sections)]
    return {
        "whenToUse": when_to_use,
        "signals": signals,
        "picking": {"feature": feature, "notWhen": not_when},
        "variants": variants,
        "pitfalls": pitfalls,
        "keyProblems": key_problems,
    }


def load_techniques_yaml() -> list[dict]:
    import yaml  # noqa: PLC0415

    data = yaml.safe_load(read_text(TECHNIQUES_YAML)) or {}
    return data.get("techniques") or []


def family_tier_for(doc_stem: str, entries: list[dict]) -> tuple[str, str]:
    matches = [e for e in entries if e.get("doc") == doc_stem]
    if not matches:
        raise BuildError(f"techniques.yml: no entry carries `doc: {doc_stem}`")
    if len(matches) > 1:
        raise BuildError(
            f"techniques.yml: {len(matches)} entries carry `doc: {doc_stem}` (expected 1)")
    family = matches[0].get("family")
    if not family:
        raise BuildError(f"techniques.yml: the `doc: {doc_stem}` entry has no `family`")
    return family, matches[0].get("tier") or DEFAULT_TIER


def discover_technique_docs() -> list[Path]:
    return sorted(TECHNIQUES_DIR.glob("*.md"))


def build_technique(path: Path, entries: list[dict]) -> dict:
    text = read_text(path)
    fields = parse_technique_fields(split_h2_sections(text))
    family, tier = family_tier_for(path.stem, entries)
    return {
        "id": path.stem.replace("_", "-"),
        "name": extract_h1(text) or path.stem,
        "family": family,
        "tier": tier,
        **fields,
        "docUrl": DOC_URL_TMPL.format(stem=path.stem),
    }


def technique_warnings(entry: dict) -> list[str]:
    """Non-fatal report lines for a technique whose doc left something at its fail-soft
    default — useful triage output, never a reason to stop the build."""
    msgs = []
    if entry["whenToUse"] == TODO:
        msgs.append("whenToUse is TODO (missing/empty '## When to reach for it')")
    if entry["picking"]["feature"] == TODO:
        msgs.append("picking.feature is TODO (missing/empty '## Picking feature')")
    if not entry["variants"]:
        msgs.append("no '## Template: …' sections found")
    for variant in entry["variants"]:
        if variant["complexity"]["time"] == TODO:
            msgs.append(f"variant '{variant['title']}': no Complexity line after its fence")
    if not entry["pitfalls"]:
        msgs.append("pitfalls is empty ('## Common pitfalls' missing/empty)")
    if not entry["keyProblems"]:
        msgs.append("keyProblems is empty ('## Practice' missing/unresolvable)")
    return [f"{entry['id']}: {m}" for m in msgs]


# ── top-level signals table (intuition_cheatsheet.md) ────────────────────────────────

def parse_signal_rows(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        match = SIGNAL_ROW_RE.match(line.strip())
        if not match:
            continue
        cells = [c.strip() for c in match.group(1).split("|")]
        if len(cells) != 3:
            continue
        if cells[0] in ("What you see in the prompt", "") or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def signal_doc_target(doc_cell: str) -> str | None:
    """The 'techniques/<x>.md' filename the Doc column's link points at, or None when the
    cell isn't that shape (an external link, or the '*below*' placeholder) — existence is
    NOT checked here; that's scripts/check_cheatsheets.py's job (see its docstring)."""
    match = SIGNAL_DOC_LINK_RE.search(doc_cell)
    return f"{match.group(1)}.md" if match else None


def default_note(text: str) -> str:
    match = PAREN_RE.match(text)
    return match.group(2).strip() if match else ""


def build_signal_entry(cells: list[str]) -> dict:
    see = clean(cells[0])
    reach_for = clean(cells[1])
    note = REACH_NOTE_OVERRIDES.get(reach_for, default_note(reach_for))
    target = signal_doc_target(cells[2])
    if target is not None:
        return {"see": see, "reach": target[:-3].replace("_", "-"), "note": note}
    return {"see": see, "reach": reach_for, "note": note, "page": False}


def parse_signal_table() -> list[dict]:
    lines = find_h2_section_raw(read_text(INTUITION_DOC), SIGNAL_TABLE_HEADING) or []
    return [build_signal_entry(cells) for cells in parse_signal_rows(lines)]


# ── the build ─────────────────────────────────────────────────────────────────────────

def build_payload(now: dt.datetime, warnings: list[str]) -> dict:
    entries = load_techniques_yaml()
    techniques = [build_technique(p, entries) for p in discover_technique_docs()]
    for entry in techniques:
        warnings.extend(technique_warnings(entry))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "signals": parse_signal_table(),
        "techniques": techniques,
    }


def write_schema_copy() -> None:
    OUT_SCHEMA.write_text(read_text(SCHEMA_FIXTURE), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--validate", action="store_true",
                    help="compute + report; write nothing (for tests / CI)")
    ap.add_argument("--stdout", action="store_true", help="print the JSON, do not write")
    args = ap.parse_args()

    warnings: list[str] = []
    try:
        payload = build_payload(dt.datetime.now(dt.timezone.utc), warnings)
    except BuildError as exc:
        sys.exit(f"build_cheatsheets: {exc}")

    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    n_tech, n_sig = len(payload["techniques"]), len(payload["signals"])

    if args.stdout:
        print(text)
    elif args.validate:
        print(f"valid: {n_tech} techniques · {n_sig} signals", file=sys.stderr)
    else:
        DASHBOARD.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text, encoding="utf-8")
        write_schema_copy()
        print(f"wrote {OUT.relative_to(REPO)} + {OUT_SCHEMA.relative_to(REPO)} "
              f"({n_tech} techniques, {n_sig} signals)")

    for w in warnings:
        print(f"  !! {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
