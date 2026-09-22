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

## The four checks

| | Miss | Why it is invisible without this |
|---|---|---|
| **1** | A **struck-through** row with an empty `End` or `Next` cell | the row reads as done, the tracker is correct, and only the schedule is short a fact — nothing downstream notices |
| **2** | A tracker row **attempted during this week** whose number is **not struck** in the file | the rep happened and the board still advertises it as pending; the next kickoff re-offers a problem that was already done |
| **3** | A tracker row **due on or before this week's Sunday** seated on **no day** of the built board | the weekly build's own sweep silently dropped an overdue rep; the 2026-09-14 leak (84, 547) crossed a week boundary and slipped two builds |
| **4** | A day-header label or the week's **Goal** paragraph **names** a problem that appears on **no row** anywhere in the week's Daily Schedule | build prose promised a rep no row carried; the 2026-09-14 (78 Subsets) and 2026-09-20 (1102/1631 Dijkstra) misses both had this shape |

**An em-dash, `unrated`, or `✅` in a cell is intentional, not missing.** Teaches, primers and probes
are unrated by design and legitimately carry no comfort and no date, so only a genuinely **empty**
cell is reported. A checker that flags deliberate blanks gets ignored within a week.

**Check 4's known false-positive shapes, recorded rather than chased.** `PROSE_NUMBER` is tuned
against real weeks, not proven correct — it can still misread `12 🟡 conversions` (a REP COUNT, not
a problem, followed by a comfort glyph) or `by December 2026, the` (four digits immediately before a
comma) as a genuine mention. Check 4 is report-only, so a rare false positive there costs a manual
glance, not a silent miss. **The obvious-looking fix — intersect a candidate with the tracker's known
LC numbers — does NOT work and should not be attempted:** a 🆕 intake is untracked BY DEFINITION (its
whole point is that it has no tracker row yet), so that filter would drop every genuine new-intake
mention while still admitting a tracked date/count number that happens to match a real problem's LC
number.

Usage:
    python scripts/check_schedule_integrity.py            # report
    python scripts/check_schedule_integrity.py --check    # exit 1 on any finding
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import re
import sys
from pathlib import Path

# Git runs hooks with a cp1252 console on Windows; the first emoji printed would
# otherwise kill the script mid-report while the commit still succeeds. See _console.
import _console

_console.force_utf8()

import session_date

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

# ── Check 4: a build PROMISE (a day-header label, or the week's Goal paragraph) named a
# problem no row of the week ever carried — the 2026-09-14 (78 Subsets) and 2026-09-20
# (1102/1631 Dijkstra) leaks. False positives are the whole difficulty here: a schedule's
# own prose packs "Sep 21", "6.8 units", "~26 reps", "2 backtracking intakes", "+2" and
# "743×2" right next to genuine mentions like "39 Combination Sum" — see
# test_check_schedule_integrity.py for the real week this is tuned against.

# A day header's LABEL only — the free text after "units —", up to the next "|". Mirrors
# gamify.py's DAY_LABEL precedent (that script strips the same slice for its own display
# purpose); kept local because the two scripts scan it for unrelated reasons.
DAY_LABEL = re.compile(r"units\s*—\s*(?P<label>[^|]+)")
# The week's Goal paragraph: from "**Goal:**" to the first blank line — the paragraph
# itself never contains one (every current schedule file wraps it as one run of lines).
GOAL_PARAGRAPH = re.compile(r"\*\*Goal:\*\*(?P<body>.*?)\n\s*\n", re.DOTALL)

_MONTH_ABBR = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
PROSE_NUMBER_MIN_DIGITS = 2
PROSE_NUMBER_MAX_DIGITS = 4
# Comfort glyphs AND build-tag glyphs both end a genuine mention ("22 🔴", "🆕 1631
# Dijkstra" reads its glyph before the number, "1489 🟡" reads it after — either shape
# needs to close a match here).
PROSE_FOLLOW_GLYPHS = "🔴🟡🟢🎓🆕🎯⚙️🔥⚠️"
# A number is a genuine MENTION — not a date, a decimal, a rep count, or a "+2"/"×2"
# interval suffix — when it is 2-4 digits, not glued to another digit/decimal-point/`+`/`~`
# or a month abbreviation on its LEFT, and followed by either a Capitalized word, one of
# the glyphs above, or a list separator (`·`, `,`, `)`). Under-extraction (missing a real
# mention, e.g. "743×2") is an acceptable failure mode — see the module docstring's
# broken-instrument warning; a false positive is not.
PROSE_NUMBER = re.compile(
    rf"(?<![\d.+~])(?<!{_MONTH_ABBR}\s)"
    rf"(\d{{{PROSE_NUMBER_MIN_DIGITS},{PROSE_NUMBER_MAX_DIGITS}}})"
    rf"(?!\.\d)"
    rf"(?=\s*[{PROSE_FOLLOW_GLYPHS}·,)]|\s+[A-Z])"
)

# A row's build-time tag glyphs (⚠️ protected · 🔥 backfill · 🆕 new · 🎯 probe · ⚙️
# variant · 🔤 primer · → moved — the legend on any schedule file's "Tags:" line) AND the
# `~~`/`**` emphasis that can wrap them (a struck or bolded 🆕/🎯 row), stripped from the
# front so a bare-numbered row still yields its number. A single repeated alternation
# handles any interleaving (`~~**🎯 …` really occurs in this repo's archive) — stripping
# glyphs and emphasis in two separate passes would miss that stacked form. Without this, a
# row's number goes invisible and check 4 reads a genuinely SEATED row as unseated — a
# false positive, not the under-extraction this module tolerates elsewhere. Kept local:
# gamify.py solves the identical problem with its own `_LEADING_EMPHASIS`, but importing it
# here would couple two independently-owned scripts over an incidental shared string.
ROW_TAG_PREFIX = re.compile(r"^(?:~~|\*\*|[⚠️🔥🆕🎯⚙️🔤→\s])+")
ROW_BARE_NUMBER = re.compile(r"^(\d{1,4})\b")

# The Daily Schedule section's own heading — week_row_numbers() scans ONLY between here
# and the next "## " section heading (see _daily_schedule_slice). Any 5-pipe-delimited
# table elsewhere in the file — a capacity table before it, a Waiting Room/preview table
# after it — would otherwise be read as a row purely because it happens to share the Daily
# table's column count, which can silently mask a real header-vs-rows drift (a number named
# in the Goal paragraph but seated only in such a table would wrongly count as "seated").
DAILY_SCHEDULE_HEADING = re.compile(r"^##\s+Daily Schedule\b", re.MULTILINE)
NEXT_SECTION_HEADING = re.compile(r"^##\s+\S", re.MULTILINE)


def _prose_numbers(text: str) -> set[int]:
    """Every genuine problem mention in one slice of prose — see PROSE_NUMBER."""
    return {int(n) for n in PROSE_NUMBER.findall(text)}


def week_named_numbers(path: Path, day_header: re.Pattern) -> set[int]:
    """Every LC number this week's build PROSE promises: named in a day-header's label,
    or in the **Goal** paragraph. Both are prose, not rows — the whole point of check 4
    is to catch when they disagree with what actually got seated.

    `day_header` (pass `eb.DAY_HEADER`) gates the DAY_LABEL scan to lines that are actually
    a "▸ **Wkd Mon D**" header — `DAY_LABEL` alone only needs literal "units —" text, which
    a capacity/build note ("9.0 units — ALL placed (355 · 18)") can also contain; ungated,
    such a line's numbers would be misread as a day-header promise.
    """
    text = path.read_text(encoding="utf-8")
    named: set[int] = set()
    for line in text.splitlines():
        if not day_header.search(line):
            continue
        label = DAY_LABEL.search(line)
        if label:
            named |= _prose_numbers(label["label"])
    goal = GOAL_PARAGRAPH.search(text)
    if goal:
        named |= _prose_numbers(goal["body"])
    return named


def _row_number(cell: str) -> int | None:
    """A row's LC number: MENTION (linked or bold) first, else a bare leading number once
    the row's build-time tag glyphs are stripped (see ROW_TAG_PREFIX).
    """
    m = MENTION.search(cell)
    if m:
        return int(m.group(1))
    m = ROW_BARE_NUMBER.match(ROW_TAG_PREFIX.sub("", cell))
    return int(m.group(1)) if m else None


def _daily_schedule_slice(text: str) -> str:
    """The text strictly between "## Daily Schedule" and the NEXT "## " section heading
    (Waiting Room, a preview, build notes, …) — falls back to the whole file if the Daily
    Schedule heading is missing (a malformed schedule file), and to EOF if there is no
    later "## " heading at all. Under-scanning on either fallback is the safer failure: it
    can under-report a finding, never fabricate one, matching this module's own
    false-positive-is-the-real-risk stance.
    """
    heading = DAILY_SCHEDULE_HEADING.search(text)
    if not heading:
        return text
    rest = text[heading.end():]
    following = NEXT_SECTION_HEADING.search(rest)
    end = heading.end() + following.start() if following else len(text)
    return text[heading.start():end]


def week_row_numbers(path: Path, sched_row: re.Pattern) -> set[int]:
    """Every LC number seated as a row ANYWHERE in the week's Daily Schedule — any day,
    not just the day a header names it under, since a directed pair can be declared in
    one place (a Goal paragraph, or one day's header) and seated on a different day's row.

    Scoped to just the Daily Schedule section (see _daily_schedule_slice) — a 5-pipe table
    before OR after it would otherwise be read as a row purely because it happens to share
    the Daily table's column count.
    """
    body = _daily_schedule_slice(path.read_text(encoding="utf-8"))
    numbers: set[int] = set()
    for line in body.splitlines():
        if "▸" in line:
            continue  # a day header, not a problem row
        m = sched_row.match(line)
        if not m:
            continue
        num = _row_number((m["c1"] or "").strip())
        if num is not None:
            numbers.add(num)
    return numbers


def header_vs_rows(path: Path) -> list[str]:
    """Check 4, pure: a number the build PROSE names with no matching row anywhere in the
    week. Takes a Path, returns findings, prints nothing — so a test can point it at a
    synthetic fixture and assert on the returned list directly.
    """
    try:
        import effort_budget as eb  # sibling script; a reuse failure must never break this
    except Exception as exc:  # noqa: BLE001 — mirrors main()'s check-3 tolerance
        print(f"   (header-vs-rows check skipped: {exc.__class__.__name__}: {exc})", file=sys.stderr)
        return []
    missing = week_named_numbers(path, eb.DAY_HEADER) - week_row_numbers(path, eb.SCHED_ROW)
    return [
        f"{num} named in a day header or the Goal paragraph but seated on no row of {path.name}"
        for num in sorted(missing)
    ]


def current_schedule(today: dt.date) -> Path | None:
    """The schedule file whose 7-day span actually contains `today`.

    Prefers eb.find_schedule(today) (live schedules/, then archive/): after a Sunday
    close-out has already built NEXT week's file, `today` still falls inside THIS week's
    span, so that lookup keeps returning the week actually being worked rather than the
    newest file on disk. Falls back to the newest live file only when no file's span
    contains `today` (a stale or missing schedule tree) — the prior, pre-eb behaviour.
    """
    try:
        import effort_budget as eb  # sibling script; a reuse failure must never break this
    except Exception as exc:  # noqa: BLE001 — mirrors header_vs_rows's own tolerance
        print(f"   (schedule-selection reuse skipped: {exc.__class__.__name__}: {exc})",
              file=sys.stderr)
    else:
        spanning = eb.find_schedule(today)
        if spanning is not None:
            return spanning

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
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                    help="override the resolved session date used to pick the current week")
    args = ap.parse_args()

    # session_date.resolve_datetime announces a heuristic guess with a bare print() to
    # stdout, the same stream this script's own findings use — redirected to stderr so an
    # announcement (rare: only past-midnight with a dirty tree or a live commit) never
    # turns a clean, no-findings run into non-silent stdout. See gamify.py main()'s
    # identical redirect for --stdout's own reason to keep stdout clean.
    with contextlib.redirect_stdout(sys.stderr):
        today = session_date.resolve_datetime(args.date).date()

    path = Path(args.file) if args.file else current_schedule(today)
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

    # 3 — a row DUE within this week but seated on no day of the built board. This is the
    # 2026-09-14 leak: two overdue 🔴s (84 due Sep 6, 547 due Sep 13) crossed a week boundary
    # and slipped consecutive builds. Checks 1-2 cannot see it — they reconcile rows that ARE
    # on the board, and this failure is a row that is on NO board at all. The weekly build's
    # own rule is "sweep ALL problems with next_review_date <= end of the week"; this asserts
    # the result of that sweep. A row done earlier this week has its due date advanced past
    # sunday, so it is not flagged; a deliberate deferral gets a new future date, so it is not
    # flagged either — only a genuinely-dropped due row surfaces. Reuses effort_budget's row
    # parser (the same rows behind `--due`, which this diffs against the board, per the entry).
    try:
        import effort_budget  # sibling script; import has no side effects
        for r in effort_budget.parse_rows():
            if dt.date.fromisoformat(r["due"]) > sunday:
                continue
            if int(r["num"]) not in listed_numbers:
                findings.append(
                    f"due {r['due']} but seated on no day of {path.name} — "
                    f"{r['num']} {r['title'][:40]} ({r['comfort']})")
    except Exception as exc:  # a reuse failure must never break the integrity check
        print(f"   (overdue-seated check skipped: {exc.__class__.__name__}: {exc})", file=sys.stderr)

    # 4 — a build promise (day-header label / the week's Goal paragraph) with no matching
    # row anywhere in the week. See header_vs_rows for the false-positive guardrails.
    findings.extend(header_vs_rows(path))

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
