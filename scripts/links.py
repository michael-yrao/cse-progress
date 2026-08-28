"""Emit the `[file] · [LC/NC]` link pair for one or more problems — the SOURCE FIX for
the link rule outside a scaffold.

`new_problem.py` already prints a `LINKS:` line on every scaffold, and that case has not
lapsed since Aug 3, 2026. The kickoff / restate / hand-over / "what's next" cases have no
such tool, so their links get hand-authored — and the dominant failure is TRANSCRIPTION:
copying a path out of a schedule row, which stores `../../../dsa/...` (correct relative to
that file, three folders deep) but DEAD when the chat renderer resolves it from the repo
root. That is the Aug 27, 2026 lapse (self_eval_log.md).

This tool removes the transcription. Give it problem numbers; it prints one
`[<number> <title>](<repo-root-relative path>) · [LC|NC](<url>)` line per number, reading
the path from disk and the title/URL from the file's own docstring header (falling back to
the tracker). The agent runs it and pastes the output — it is structurally impossible to
emit a wrong path.

Per the intervention ladder in `.claude/memory/feedback_self_evaluation.md`:
source fix > hook > CLAUDE.md step > memory file. This is the top rung, matching
`new_problem.py`'s `report_links()`; the Stop hook `problem_link_reminder.py` is the backup.

Usage:
    python scripts/links.py 269 853 424
    python scripts/links.py 853               # single problem
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The `·` separator and any glyph in a problem title is unmappable on a stock Windows
# console (cp1252) and would render as `?` or, from the git hook, crash the run. Force
# UTF-8 stdout the same way every other script here does.
import _console

_console.force_utf8()

# Repo root is two levels up from scripts/ — the base the chat renderer resolves against,
# which is the whole point: paths printed here are ALWAYS repo-root-relative.
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = "dsa/leetcode"
TRACKER = REPO_ROOT / "docs" / "foundations" / "dsa" / "mastery" / "dsa_progress.md"

# Header line: `853. Car Fleet   ·   https://leetcode.com/problems/car-fleet/`. The `·`
# and the URL are optional — a legacy file may carry only `853. Car Fleet`.
HEADER = re.compile(r"^\s*(\d{1,4})\.\s+(.+?)(?:\s+·\s+(https?://\S+))?\s*$")
# Tracker row cell: `[49. Group Anagrams](https://leetcode.com/problems/group-anagrams/)`.
TRACKER_CELL = re.compile(r"\[(\d{1,4})\.\s*([^\]]+?)\]\((https?://[^)]+)\)")


def source_roots() -> list[Path]:
    """Solution roots from cse.config.yml, defaulting to dsa/leetcode.

    Mirrors new_problem.py's source_root(), but returns ALL roots — a problem could live
    under any of them, and matching on the number is what identifies it.
    """
    cfg = REPO_ROOT / "cse.config.yml"
    if cfg.exists():
        m = re.search(r"roots:\s*\[([^\]]*)\]", cfg.read_text(encoding="utf-8"))
        if m:
            roots = [r.strip().strip("'\"") for r in m.group(1).split(",") if r.strip()]
            if roots:
                return [REPO_ROOT / r for r in roots]
    return [REPO_ROOT / DEFAULT_ROOT]


def find_file(number: str) -> Path | None:
    """The solution file for `number`, or None. The NUMBER is the identity (same rule as
    new_problem.py's twin check), so glob `<root>/*/<number>_*.py` across every root.

    On the rare twin (a forked history), warn and take the first — the caller still gets a
    working link, and the fork is a separate problem flagged loudly.
    """
    hits: list[Path] = []
    for root in source_roots():
        hits.extend(sorted(root.glob(f"*/{number}_*.py")))
    if not hits:
        return None
    if len(hits) > 1:
        joined = ", ".join(p.relative_to(REPO_ROOT).as_posix() for p in hits)
        print(f"WARNING: {number} matches {len(hits)} files ({joined}); using the first.",
              file=sys.stderr)
    return hits[0]


def header_title_url(path: Path) -> tuple[str | None, str | None]:
    """(title, url) from the file's docstring header line, each None if absent.

    The header is the authoritative source: it carries the true slug even when the filename
    disagrees (229_majority_element_2 vs .../majority-element-ii) and it is the only place
    that records a premium (neetcode.io) link. Scan only the first docstring block.
    """
    text = path.read_text(encoding="utf-8")
    parts = text.split('"""')
    block = parts[1] if len(parts) >= 2 else text
    for line in block.splitlines():
        m = HEADER.match(line)
        if m:
            return m.group(2).strip(), (m.group(3).rstrip(".,;)") if m.group(3) else None)
    return None, None


def tracker_title_url(number: str) -> tuple[str | None, str | None]:
    """(title, url) for `number` from the tracker — the fallback when the file has no
    header, and the only source when there is no file at all."""
    try:
        lines = TRACKER.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None, None
    for line in lines:
        for num, title, url in TRACKER_CELL.findall(line):
            if num == number:
                return title.strip(), url.rstrip("/") + "/" if url else None
    return None, None


def link_line(number: str) -> str | None:
    """The `[file] · [LC|NC]` line for `number`, or None if nothing on disk knows it.

    Path is ALWAYS repo-root-relative (the fix). Title/URL prefer the file header, then the
    tracker. A problem with no file yields no file link — that is new_problem.py's job (it
    prints LINKS: on the scaffold), so we say so rather than invent a path.
    """
    path = find_file(number)
    file_title, file_url = header_title_url(path) if path else (None, None)
    track_title, track_url = tracker_title_url(number)

    title = file_title or track_title
    url = file_url or track_url

    if path is None:
        if url:
            label = "NC" if "neetcode" in url else "LC"
            print(f"NOTE: {number} has no solution file yet — scaffold it with new_problem.py "
                  f"for the file link. Problem-page link only:", file=sys.stderr)
            return f"[{number}{(' ' + title) if title else ''}]() · [{label}]({url})"
        print(f"WARNING: nothing on disk knows problem {number} (no file, no tracker row).",
              file=sys.stderr)
        return None

    rel = path.relative_to(REPO_ROOT).as_posix()
    name = f"{number} {title}" if title else number
    if not url:
        print(f"WARNING: {number} has no problem-page URL in its header or the tracker; "
              f"emitting the file link alone.", file=sys.stderr)
        return f"[{name}]({rel})"
    label = "NC" if "neetcode" in url else "LC"
    return f"[{name}]({rel}) · [{label}]({url})"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Print the [file] · [LC/NC] link pair for one or more problem numbers.")
    ap.add_argument("numbers", nargs="+", help="problem number(s), e.g. 269 853 424")
    args = ap.parse_args()

    missing = 0
    for number in args.numbers:
        if not number.isdigit():
            print(f"WARNING: '{number}' is not a problem number; skipping.", file=sys.stderr)
            missing += 1
            continue
        line = link_line(number)
        if line is None:
            missing += 1
            continue
        print(line)

    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
