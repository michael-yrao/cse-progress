"""Tests for check_schedule_integrity.py's check 4 — header_vs_rows (the header/Goal-vs-rows
build-drift check).

Stdlib unittest, mirrors test_check_timeline_gaps.py's runner style. header_vs_rows() is pure
(Path in, findings out) but DOES read the filesystem — unlike gamify's pure functions, a
schedule week is a whole markdown file, not a plain dict, so each fixture is written to the
test's own temp dir rather than depending on a real (and mutable) schedule file.

False positives are the whole difficulty this check exists to survive (see the module
docstring), so the fixtures below are built directly from the traps a real week's prose
contains: a date, a decimal unit count, an approximate rep count, a plain intake count, a
"+N" interval suffix, and a bare-numbered 🆕 intake row with no link/bold before its number.

    python scripts/test_check_schedule_integrity.py
"""
from __future__ import annotations

import datetime as dt
import tempfile
import unittest
from pathlib import Path

import check_schedule_integrity as csi
import effort_budget as eb

# A minimal, valid Daily Schedule table header + separator — every fixture's rows sit below it.
_TABLE_HEAD = "| Problem | S | E | Next | Technique |\n|---|:-:|:-:|:-:|---|\n"

# The real Sep 14 drift this check exists for: the Goal paragraph promises TWO backtracking
# intakes (22, then 78) but the Daily Schedule only ever seats a row for 22.
FIXTURE_POSITIVE_DRIFT = f"""# Week of September 14 - 20, 2026

**Goal:** clear the 🔴 re-rep and open Backtracking with exactly **2 intakes** (22 Generate
Parentheses, then 78 Subsets — no primer, learner's call).

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Mon Sep 14** · 5.0 units — 22 🔴 re-rep |  |  |  |  |
| [22 Generate Parentheses](../../../dsa/leetcode/backtracking/22_generate_parentheses.py) · [LC](https://leetcode.com/problems/generate-parentheses/) | 🔴 | | | Backtracking |
"""

# A clean week packing every trap from the module docstring right next to genuine mentions
# that DO all have rows: a date ("Sep 21"), a decimal unit count ("6.8 units"), an approximate
# rep count ("~26 reps"), a bare intake count ("2 backtracking intakes"), "+2" interval
# suffixes, and a "·"-separated number list (55 · 332 · 34).
FIXTURE_NEGATIVE_CLEAN = f"""# Week of September 21 - 27, 2026

**Goal:** a review-heavy week by demand (not light by choice — ~26 reps come due). NEW intake
is held to the learner's floor of **2 backtracking intakes**. Primary: clear the two 🔴
re-reps (22 Generate Parentheses +2, 1552 Magnetic Force +2) and drain the conversion backlog
(55 · 332 · 34).

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Mon Sep 21** · 6.8 units — 22 🔴 re-rep + 1552 🔴 re-rep |  |  |  |  |
| [22 Generate Parentheses](../../../dsa/leetcode/backtracking/22_generate_parentheses.py) · [LC](https://leetcode.com/problems/generate-parentheses/) | 🔴 | | | Backtracking |
| [1552 Magnetic Force Between Two Balls](../../../dsa/leetcode/binary_search/1552_magnetic_force_between_two_balls.py) · [LC](https://leetcode.com/problems/magnetic-force-between-two-balls/) | 🔴 | | | Binary-search |
| [55 Jump Game](../../../dsa/leetcode/greedy/55_jump_game.py) · [LC](https://leetcode.com/problems/jump-game/) | 🟡 | | | Greedy |
| [332 Reconstruct Itinerary](../../../dsa/leetcode/graphs/332_reconstruct_itinerary.py) · [LC](https://leetcode.com/problems/reconstruct-itinerary/) | 🟡 | | | Graph |
| [34 Find First and Last Position](../../../dsa/leetcode/binary_search/34_find_first_and_last_position_of_element_in_sorted_array.py) · [LC](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | 🟢 | | | Binary-search |
"""

# The 🆕-row trap: a NEW intake's Problem cell carries no `[`/`**` before its number (no local
# solution file exists yet to link), so MENTION alone would both under-extract the row AND
# (via schedule_rows()'s own filter) drop it from the board entirely. A clean week naming 39
# and 46 in the Goal paragraph, each seated as a bare 🆕 row, must report nothing.
FIXTURE_BARE_NEW_ROW = f"""# Week of September 21 - 27, 2026

**Goal:** NEW intake is held to the learner's floor of **2 backtracking intakes** (39
Combination Sum, 46 Permutations).

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Wed Sep 23** · 7.6 units — Backtracking intake 1 |  |  |  |  |
| 🆕 39 Combination Sum · [LC](https://leetcode.com/problems/combination-sum/) | 🆕 | | | Backtracking |
| |  |  |  |  |
| ▸ **Fri Sep 25** · 6.9 units — Backtracking intake 2 |  |  |  |  |
| 🆕 46 Permutations · [LC](https://leetcode.com/problems/permutations/) | 🆕 | | | Backtracking |
"""

# The pre-Daily-Schedule masking trap: a Capacity table BEFORE "## Daily Schedule" that
# happens to share the Daily table's 5-column shape, with the number sitting in ITS first
# cell too — the exact position week_row_numbers() reads. Unscoped, this reads as a seated
# row and silences the real 78-Subsets-shaped drift the check exists to catch; scoped to
# "## Daily Schedule" onward, it must still report both numbers as missing.
FIXTURE_PRE_DAILY_SCHEDULE_TABLE = f"""# Week of September 21 - 27, 2026

**Goal:** NEW intake is held to the learner's floor of **2 backtracking intakes** (39
Combination Sum, 46 Permutations).

---

## Capacity

| **39** Combination Sum | x | y | z | w |
| **46** Permutations | x | y | z | w |

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Wed Sep 23** · 7.6 units — Backtracking intake |  |  |  |  |
"""

# The emphasised-tag-row trap: a DONE (struck) or bolded 🆕/🎯 row, where `~~`/`**` wraps the
# tag glyph too. Unstripped, `_row_number` returns None for a row that IS seated, which in
# check 4 reads as a genuine problem going FALSE POSITIVE (a seated row reported missing) —
# the failure the module docstring says is unacceptable, worse than under-extraction.
FIXTURE_EMPHASISED_TAG_ROW = f"""# Week of September 21 - 27, 2026

**Goal:** NEW intake is held to the learner's floor of **2 backtracking intakes** (39
Combination Sum, 46 Permutations).

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Wed Sep 23** · 7.6 units — Backtracking intake 1 |  |  |  |  |
| ~~🆕 39 Combination Sum · [LC](https://leetcode.com/problems/combination-sum/)~~ | 🆕 | 🟢 | 2026-10-01 | Backtracking |
| |  |  |  |  |
| ▸ **Fri Sep 25** · 6.9 units — Backtracking intake 2 |  |  |  |  |
| **🆕 46 Permutations** | 🆕 | | | Backtracking |
"""

# The post-Daily-Schedule masking trap: mirrors FIXTURE_PRE_DAILY_SCHEDULE_TABLE, but the
# 5-column lookalike table sits AFTER "## Daily Schedule" (a Waiting Room / next-week
# preview shape) instead of before it. Unscoped past the section's own end, this reads as
# seated rows and silences the drift; bounded to the section, it must still report both.
FIXTURE_POST_DAILY_SCHEDULE_TABLE = f"""# Week of September 21 - 27, 2026

**Goal:** NEW intake is held to the learner's floor of **2 backtracking intakes** (39
Combination Sum, 46 Permutations).

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Wed Sep 23** · 7.6 units — Backtracking intake |  |  |  |  |

---

## Waiting Room

| **39** Combination Sum | x | y | z | w |
| **46** Permutations | x | y | z | w |
"""

# The non-header "units —" trap: a capacity/build-note line that happens to contain the
# literal text "units —" (DAY_LABEL's only trigger) without being an actual "▸" day header.
# Its numbers must NOT be read as a build promise.
FIXTURE_NON_HEADER_UNITS_LINE = f"""# Week of September 21 - 27, 2026

**Goal:** a light week, nothing special.

```
9.0 units — ALL placed (355 · 18)
```

---

## Daily Schedule

{_TABLE_HEAD}| ▸ **Mon Sep 21** · 6.8 units — green batch |  |  |  |  |
"""


class HeaderVsRowsTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write(self, name: str, text: str) -> Path:
        path = Path(self._tmpdir.name) / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_goal_names_a_problem_with_no_row_is_flagged(self):
        path = self._write("20260914_schedule.md", FIXTURE_POSITIVE_DRIFT)
        findings = csi.header_vs_rows(path)
        self.assertEqual(len(findings), 1)
        self.assertIn("78", findings[0])

    def test_clean_week_full_of_trap_text_reports_nothing(self):
        path = self._write("20260921_schedule.md", FIXTURE_NEGATIVE_CLEAN)
        self.assertEqual(csi.header_vs_rows(path), [])

    def test_bare_numbered_new_intake_row_satisfies_its_own_goal_mention(self):
        path = self._write("20260921_schedule.md", FIXTURE_BARE_NEW_ROW)
        self.assertEqual(csi.header_vs_rows(path), [])

    def test_a_5_column_table_before_daily_schedule_does_not_mask_a_real_drift(self):
        path = self._write("20260921_schedule.md", FIXTURE_PRE_DAILY_SCHEDULE_TABLE)
        findings = csi.header_vs_rows(path)
        self.assertEqual(len(findings), 2)
        joined = " ".join(findings)
        self.assertIn("39", joined)
        self.assertIn("46", joined)

    def test_a_5_column_table_after_daily_schedule_does_not_mask_a_real_drift(self):
        path = self._write("20260921_schedule.md", FIXTURE_POST_DAILY_SCHEDULE_TABLE)
        findings = csi.header_vs_rows(path)
        self.assertEqual(len(findings), 2)
        joined = " ".join(findings)
        self.assertIn("39", joined)
        self.assertIn("46", joined)

    def test_struck_or_bolded_tag_row_is_still_recognised_as_seated(self):
        path = self._write("20260921_schedule.md", FIXTURE_EMPHASISED_TAG_ROW)
        self.assertEqual(csi.header_vs_rows(path), [])


class TrapExtractionTests(unittest.TestCase):
    """Direct pins on week_named_numbers()/week_row_numbers(), the two extraction halves
    header_vs_rows() diffs — narrower than the end-to-end fixtures above, so a future
    regression in just one half points straight at the broken side.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write(self, text: str) -> Path:
        path = Path(self._tmpdir.name) / "20260921_schedule.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_date_decimal_count_and_interval_suffix_are_not_named(self):
        path = self._write(FIXTURE_NEGATIVE_CLEAN)
        named = csi.week_named_numbers(path, eb.DAY_HEADER)
        # Traps that must NOT surface as a required mention.
        for trap in (21, 26, 2, 8):
            self.assertNotIn(trap, named)
        # Genuine mentions that must.
        for real in (22, 1552, 55, 332, 34):
            self.assertIn(real, named)

    def test_bare_new_row_still_yields_its_number(self):
        path = self._write(FIXTURE_BARE_NEW_ROW)
        self.assertEqual(csi.week_row_numbers(path, eb.SCHED_ROW), {39, 46})

    def test_row_scan_ignores_a_5_column_table_before_daily_schedule(self):
        path = self._write(FIXTURE_PRE_DAILY_SCHEDULE_TABLE)
        self.assertEqual(csi.week_row_numbers(path, eb.SCHED_ROW), set())

    def test_row_scan_ignores_a_5_column_table_after_daily_schedule(self):
        path = self._write(FIXTURE_POST_DAILY_SCHEDULE_TABLE)
        self.assertEqual(csi.week_row_numbers(path, eb.SCHED_ROW), set())

    def test_struck_and_bolded_tag_rows_still_yield_their_number(self):
        self.assertEqual(csi._row_number("~~🆕 39 Combination Sum · [LC](https://x)~~"), 39)
        self.assertEqual(csi._row_number("**🆕 46 Permutations**"), 46)
        # The stacked form that really occurs in this repo's archive.
        self.assertEqual(csi._row_number("~~**🎯 211 Add and Search Words**~~"), 211)

    def test_non_header_units_line_is_not_read_as_a_day_header_promise(self):
        path = self._write(FIXTURE_NON_HEADER_UNITS_LINE)
        named = csi.week_named_numbers(path, eb.DAY_HEADER)
        self.assertNotIn(355, named)
        self.assertNotIn(18, named)


class LiveCurrentWeekTests(unittest.TestCase):
    """A soft check against the repo's real current-week schedule, not a fixture. Skips
    rather than fails when the schedule tree isn't present (e.g. a checkout of just this
    script) — the fixture tests above are the ones that must always run.
    """

    def test_live_current_week_is_silent(self):
        path = csi.current_schedule(dt.date.today())
        if path is None or not path.exists():
            self.skipTest("no live schedule tree in this checkout")
        findings = csi.header_vs_rows(path)
        self.assertEqual(findings, [], f"live week {path.name} has header-vs-rows drift: {findings}")


class CurrentScheduleTests(unittest.TestCase):
    """current_schedule() picks the week that SPANS `today`, not just the newest file —
    the Sunday-close-out case: next week's Monday file already exists (built ahead of
    time), but a `today` still inside THIS week must keep resolving to THIS week's file.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        tmp_dir = Path(self._tmpdir.name)
        # Both the primary lookup (eb.find_schedule, which reads effort_budget's OWN
        # SCHEDULES constant) and the fallback glob (this module's SCHEDULE_DIR) must
        # point at the same fixture directory.
        self._orig_eb_schedules = eb.SCHEDULES
        self._orig_schedule_dir = csi.SCHEDULE_DIR
        eb.SCHEDULES = tmp_dir
        csi.SCHEDULE_DIR = tmp_dir

    def tearDown(self):
        eb.SCHEDULES = self._orig_eb_schedules
        csi.SCHEDULE_DIR = self._orig_schedule_dir
        self._tmpdir.cleanup()

    def _write_week(self, monday: str) -> Path:
        path = csi.SCHEDULE_DIR / f"{monday}_schedule.md"
        path.write_text(
            f"# Week of {monday}\n\n## Daily Schedule\n\n"
            "| Problem | S | E | Next | Technique |\n|---|:-:|:-:|:-:|---|\n",
            encoding="utf-8")
        return path

    def test_picks_this_week_when_next_weeks_monday_already_exists(self):
        this_week = self._write_week("20260921")  # Mon Sep 21
        self._write_week("20260928")  # Mon Sep 28, built ahead by the Sunday close-out
        today = dt.date(2026, 9, 24)  # Thu Sep 24 — inside this week, not next week
        self.assertEqual(csi.current_schedule(today), this_week)

    def test_falls_back_to_newest_when_no_file_spans_today(self):
        self._write_week("20260907")
        newest = self._write_week("20260914")
        today = dt.date(2026, 10, 1)  # past both weeks' spans
        self.assertEqual(csi.current_schedule(today), newest)


if __name__ == "__main__":
    unittest.main()
