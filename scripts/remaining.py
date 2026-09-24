"""Print today's UN-STRUCK board — the problems still open on the current day's schedule.

The SOURCE FIX for a recurring miss (self_eval_log 2026-09-17, twice in one session): when
the learner asks "what's left / what else," the coach hand-assembles the lineup from memory
of what was done and DROPS an item. The open set is fully determined by the schedule
(today's block, minus the rows struck through with `~~`), so a tool should derive it — never
memory.

This reads the current week's schedule, finds the day-block for the session date, collects
the rows that are NOT struck through, and prints each as a clean `[file] · [LC/NC]` pair via
`links.py`'s `link_line` (so the paths are repo-root-relative and spoiler-free — name + links
only, exactly what a presented lineup is allowed to carry).

Per the intervention ladder (feedback_self_evaluation.md): source fix > hook > CLAUDE.md step
> memory. A "what's left" lineup now has a tool, matching `links.py` for the link pair itself.

Usage:
    python scripts/remaining.py                 # today's un-struck board (session date)
    python scripts/remaining.py --date 2026-09-18
    python scripts/remaining.py --schedule docs/foundations/schedules/20260914_schedule.md
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import _console

_console.force_utf8()

import session_date
from links import link_line, REPO_ROOT

SCHEDULES = REPO_ROOT / "docs" / "foundations" / "schedules"

# A day-block header: `| ▸ **Thu Sep 17** · 7.7 units — ...`. We match on the date fragment.
DAY_HEADER = re.compile(r"▸\s*\*\*[^*]*\*\*")
# Tag glyphs a row can carry before its number — the schedule's own "Tags:" legend:
# 🔥 backfill · 🎯 probe · ⚙️ variant · 🆕 new · → moved · ⚠️ protected · 🔤 primer.
ROW_TAG_GLYPHS = "🔥🎯⚙️🆕→⚠️🔤"
# A problem row's number: `[N ` for a linked row, with ANY non-bracket prefix allowed in
# front of it (the original, permissive shape — a tag glyph, a review marker like `🔁 `,
# a probe label like `🎯 **PROBE #6** — `, ...): `| [560 Subarray Sum ...](...path...) ·
# [LC](...) | ... |`. Or a bare `N ` for a 🆕 intake with no local file yet to link
# (`| 🆕 39 Combination Sum · [LC](...) | ... |`) — with no bracket to anchor on, this
# branch requires at least ONE of the legend glyphs above, so a plain summary/carry-table
# row (`| 5 overdue rows | 9.0 |`, `| 743 Network Delay Time | Aug 4 |`) is never misread
# as a problem row. Exactly one of the two capture groups fills, depending on which shape
# matched.
ROW_NUMBER = re.compile(
    rf"^\|\s*(?:(?:[^\[\]|]*?\s)?\[(\d{{1,4}})\s|(?:[{ROW_TAG_GLYPHS}]\s*)+(\d{{1,4}})\s)"
)


def current_schedule(session: str) -> Path | None:
    """The week file governing `session` (YYYY-MM-DD): the largest YYYYMMDD_schedule.md whose
    date is <= the session date. Falls back to the newest file if none is <=."""
    stamp = session.replace("-", "")
    files = sorted(SCHEDULES.glob("*_schedule.md"))
    if not files:
        return None
    eligible = [f for f in files if f.name[:8] <= stamp]
    return (eligible or files)[-1]


def day_label(session: str) -> str:
    """`Sep 17` for 2026-09-17 — the fragment that appears in the day-block header."""
    d = datetime.strptime(session, "%Y-%m-%d")
    return f"{d.strftime('%b')} {d.day}"


def unstruck_numbers(schedule: Path, label: str) -> list[str] | None:
    """Problem numbers of the un-struck rows in the day-block whose header contains `label`.
    None if no block matches the label (a day with no schedule / a wrong date)."""
    lines = schedule.read_text(encoding="utf-8").splitlines()
    in_block = False
    found_block = False
    numbers: list[str] = []
    for line in lines:
        header = DAY_HEADER.search(line)
        if header:
            # A new day-block starts. We're in ours only if its bold date names our date —
            # not free text later in the header (a note citing "Sep 23" once matched Fri).
            in_block = re.search(rf"\b{re.escape(label)}\b", header.group(0)) is not None
            if in_block:
                found_block = True
            continue
        if not in_block:
            continue
        m = ROW_NUMBER.match(line)
        if not m:
            continue
        if "~~" in line:  # struck through = done, skip
            continue
        numbers.append(m.group(1) or m.group(2))
    return numbers if found_block else None


def main() -> None:
    ap = argparse.ArgumentParser(description="Print today's un-struck board (name + links only).")
    ap.add_argument("--date", help="session date YYYY-MM-DD (default: detected session date)")
    ap.add_argument("--schedule", help="schedule file to read (default: current week)")
    args = ap.parse_args()

    session = args.date or session_date.resolve()
    schedule = Path(args.schedule) if args.schedule else current_schedule(session)
    if schedule is None or not schedule.exists():
        print("No schedule file found.", file=sys.stderr)
        sys.exit(1)

    label = day_label(session)
    numbers = unstruck_numbers(schedule, label)
    if numbers is None:
        print(f"No day-block for '{label}' in {schedule.relative_to(REPO_ROOT).as_posix()}.",
              file=sys.stderr)
        sys.exit(1)
    if not numbers:
        print(f"Nothing left — every row in the {label} block is struck through. ✅")
        return

    for number in numbers:
        line = link_line(number)
        if line:
            print(line)


if __name__ == "__main__":
    main()
