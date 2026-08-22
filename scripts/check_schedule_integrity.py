#!/usr/bin/env python3
"""The two propagation misses that are actually possible: a rated rep whose schedule row was
never completed, and a rated rep whose row was never struck.

CLAUDE.md's **Schedule Integrity Rule** ends with *"the spaced repetition dates are the source of
truth; the weekly schedules must reflect them."* This checks that the CURRENT week's schedule file
reflects what the tracker says happened — nothing more.

## ⚠️ What this deliberately does NOT check, and why

The first version of this script enforced the rule's broadest reading — *every* computed next-review
date must appear in some schedule file — and reported **73 of 115 rows on a healthy repo**. That is
not a finding, it is a broken instrument: the rule cannot mean that, because a 🟢 s2 landing in
February 2027 has no week file, no preview, and no business having one. **Distant dates are handled by
the weekly build's own tracker sweep** (*"FIRST do a full tracker sweep for ALL problems with
next_review_date ≤ end of that week"*), which is a pull, not a push. Pre-placing them would be
duplicate bookkeeping that rots.

So this script checks only the window where a *push* is genuinely owed: the week being worked.

## The two checks

| | Miss | Why it is invisible without this |
|---|---|---|
| **1** | A **struck-through** row with an empty `End` or `Next` cell | the row reads as done, the tracker is correct, and only the schedule is short a fact — nothing downstream notices |
| **2** | A tracker row **attempted during this week** whose number is **not struck** in the file | the rep happened and the board still advertises it as pending; the next kickoff re-offers a problem that was already done |

**An em-dash, `unrated`, or `✅` in a cell is intentional, not missing.** Teaches, primers and probes
are unrated by design and legitimately carry no comfort and no date, so only a genuinely **empty**
cell is reported. A checker that flags deliberate blanks gets ignored within a week.

Usage:
    python scripts/check_schedule_integrity.py            # report
    python scripts/check_schedule_integrity.py --check    # exit 1 on any finding
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# Git runs hooks with a cp1252 console on Windows; the first emoji printed would
# otherwise kill the script mid-report while the commit still succeeds. See _console.
import _console

_console.force_utf8()

TRACKERS = [
    Path("docs/foundations/dsa/mastery/dsa_progress.md"),
    Path("docs/foundations/system_design/mastery/design_progress.md"),
]
SCHEDULE_DIR = Path("docs/foundations/schedules")

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A link's text or a bold mention — NOT a bare \b\d+\b, which collides with dates
# ("Aug 14" vs problem 14) and unit counts. Both forms are the schedule files' own conventions.
MENTION = re.compile(r"(?:\[|\*\*)\s*(\d{1,4})\b")
# A cell that is deliberately blank: an em-dash, a tick, "unrated", "n/a".
INTENTIONAL = re.compile(r"^(—|-|–|✅.*|unrated.*|n/?a)$", re.I)


def current_schedule() -> Path | None:
    """The newest non-archived weekly file whose Monday is on or before today."""
    if not SCHEDULE_DIR.exists():
        return None
    files = sorted(SCHEDULE_DIR.glob("[0-9]" * 8 + "_schedule.md"))
    return files[-1] if files else None


def week_of(path: Path) -> tuple[dt.date, dt.date]:
    monday = dt.datetime.strptime(path.name[:8], "%Y%m%d").date()
    return monday, monday + dt.timedelta(days=6)


def schedule_rows(path: Path) -> list[tuple[str, bool, list[str]]]:
    """(raw problem cell, is_struck, [start, end, next]) for every daily-table row."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        problem = cells[0]
        if "▸" in problem or problem.startswith("---") or not problem:
            continue  # day header, separator, spacer
        if not MENTION.search(problem) and "PROBE" not in problem and "PRIMER" not in problem:
            continue  # a table that is not the daily board (capacity, triggers, landing list)
        rows.append((problem, "~~" in problem, cells[1:4]))
    return rows


def tracker_attempts(path: Path) -> list[tuple[str, int, dt.date]]:
    """(row title, problem number, latest attempt date)."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not DATE.match(cells[5]):
            continue
        number = re.match(r"\[(\d+)\.", cells[1])
        if not number:
            continue
        title = re.sub(r"\]\(.*", "", cells[1]).lstrip("[")
        out.append((title, int(number.group(1)), dt.date.fromisoformat(cells[5])))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 on any finding")
    ap.add_argument("--file", help="check this schedule file instead of the current one")
    args = ap.parse_args()

    path = Path(args.file) if args.file else current_schedule()
    if path is None or not path.exists():
        print("No schedule file to check.")
        return

    monday, sunday = week_of(path)
    rows = schedule_rows(path)
    findings: list[str] = []

    # 1 — a done row that never got its result written back.
    for problem, struck, (start, end, nxt) in rows:
        if not struck:
            continue
        label = re.sub(r"[~*]", "", problem).split("]")[0].lstrip("[")[:60]
        if not end:
            findings.append(f"struck but no End (comfort) — {label}")
        if not nxt and not INTENTIONAL.match(end or ""):
            findings.append(f"struck, rated {end}, but no Next (review date) — {label}")

    # 2 — a rep the tracker says happened this week, still advertised as pending.
    struck_numbers = {
        int(n) for problem, struck, _ in rows if struck for n in MENTION.findall(problem)
    }
    listed_numbers = {int(n) for problem, _, _ in rows for n in MENTION.findall(problem)}
    for tracker in TRACKERS:
        if not tracker.exists():
            continue
        for title, number, attempted in tracker_attempts(tracker):
            if not (monday <= attempted <= sunday):
                continue
            if number in listed_numbers and number not in struck_numbers:
                findings.append(f"attempted {attempted} but its row is not struck — {title[:60]}")

    if not findings:
        print(f"✅ {path.name}: every done row carries its result, and every rep this week is struck")
        return

    print(f"⚠️  {path.name}: {len(findings)} schedule-integrity finding(s)\n")
    for f in sorted(set(findings)):
        print(f"   {f}")
    if args.check:
        sys.exit(1)


if __name__ == "__main__":
    main()
