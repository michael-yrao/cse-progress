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


class IsSeatedTests(unittest.TestCase):
    """Direct pins on is_seated(), check 3's seating decision — pure, so no fixture files
    are needed. The two masking shapes it exists to fix (see check_schedule_integrity's
    module docstring, check 3): a second tracker row for the same LC number whose only
    board mention is a struck rep for the OTHER method, and a single row's own struck rep
    keeping its number "listed" while its next (already-due) rep seats nowhere.
    """

    SUNDAY = dt.date(2026, 9, 27)

    KRUSKAL_ROW = {"num": "1584", "title": "Min Cost to Connect All Points (Kruskal)",
                   "due": "2026-08-26"}  # overdue
    PRIMS_ROW = {"num": "1584", "title": "Min Cost to Connect All Points (Prim's MST)",
                 "due": "2026-11-24"}  # not due this week

    def test_pending_board_mentions_excludes_struck_rows(self):
        struck = "~~[1584 Min Cost to Connect All Points](x)~~ · [LC](y)"
        unstruck = "**1584** Min Cost to Connect All Points (Kruskal) re-rep"
        board_rows = [
            (struck, True, ["🟢", "🟢", "2026-11-24"]),
            (unstruck, False, ["", "", ""]),
        ]
        pending = csi.pending_board_mentions(board_rows)
        self.assertEqual(pending.get(1584), [unstruck])

    def test_two_rows_one_number_only_struck_board_row_is_flagged(self):
        # board has only a STRUCK row for 1584 -> pending_board_mentions drops it, so no
        # unstruck mention ever reaches is_seated.
        board_rows = [
            ("~~[1584 Min Cost to Connect All Points](x)~~ · [LC](y)", True,
             ["🟢", "🟢", "2026-11-24"]),
        ]
        pending = csi.pending_board_mentions(board_rows)
        seated = csi.is_seated(self.KRUSKAL_ROW, [self.KRUSKAL_ROW, self.PRIMS_ROW],
                                pending.get(1584, []), self.SUNDAY)
        self.assertFalse(seated)

    def test_two_rows_one_number_unstruck_row_naming_its_own_method_is_not_flagged(self):
        pending = ["**1584** Min Cost to Connect All Points (Kruskal) re-rep"]
        seated = csi.is_seated(self.KRUSKAL_ROW, [self.KRUSKAL_ROW, self.PRIMS_ROW],
                                pending, self.SUNDAY)
        self.assertTrue(seated)

    def test_two_rows_one_number_unstruck_row_naming_the_other_method_is_flagged(self):
        pending = ["**1584** Min Cost to Connect All Points (Prim's MST) re-rep"]
        seated = csi.is_seated(self.KRUSKAL_ROW, [self.KRUSKAL_ROW, self.PRIMS_ROW],
                                pending, self.SUNDAY)
        self.assertFalse(seated)

    def test_single_row_due_this_week_only_struck_board_row_is_flagged(self):
        row = {"num": "22", "title": "Generate Parentheses", "due": "2026-09-24"}
        board_rows = [
            ("~~[22 Generate Parentheses](x)~~ · [LC](y)", True, ["🔴", "🟢", "2026-10-24"]),
        ]
        pending = csi.pending_board_mentions(board_rows)
        seated = csi.is_seated(row, [row], pending.get(22, []), self.SUNDAY)
        self.assertFalse(seated)

    def test_single_row_due_this_week_unstruck_board_row_is_not_flagged(self):
        row = {"num": "22", "title": "Generate Parentheses", "due": "2026-09-24"}
        pending = ["**22** Generate Parentheses re-rep"]
        seated = csi.is_seated(row, [row], pending, self.SUNDAY)
        self.assertTrue(seated)

    def test_unstruck_row_with_no_method_text_seats_the_sole_due_variant(self):
        due_row = {"num": "39", "title": "Combination Sum (BFS)", "due": "2026-09-24"}
        other_row = {"num": "39", "title": "Combination Sum (Union-Find)",
                     "due": "2026-11-01"}  # not due this week -> due_count is 1, unambiguous
        pending = ["**39** Combination Sum"]  # no method text at all
        seated = csi.is_seated(due_row, [due_row, other_row], pending, self.SUNDAY)
        self.assertTrue(seated)


class DoneRowFindingsTests(unittest.TestCase):
    """Check 1 on the UNNUMBERED mock row shape (`🎤 Mock interview (Medium)`: no `[N`/`**N`
    for MENTION to match), read through schedule_rows() so the test also proves its
    "Mock" whitelist -- without it the row is dropped before check 1 ever sees it."""

    def test_struck_mock_row_with_blank_end_is_flagged_and_unstruck_is_not(self):
        cases = [
            ("| ~~🎤 Mock interview (Medium)~~ | 🎤 |  | 2026-10-21 | Mock |", 1),
            ("| 🎤 Mock interview (Medium) | 🎤 |  |  | Mock |", 0),
        ]
        for row, expected_findings in cases:
            with self.subTest(row=row):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "20261004_schedule.md"
                    path.write_text(_TABLE_HEAD + row + "\n", encoding="utf-8")
                    findings = csi.done_row_findings(csi.schedule_rows(path))
                self.assertEqual(len(findings), expected_findings)


_CFG = {"carry_forward_min_streak": 2, "intake_per_week": 2,
        "intake_pause_overdue_unproven": 2}
_MONDAY = dt.date(2026, 10, 5)
_TODAY = dt.date(2026, 10, 6)


def _day(*items: dict) -> dict[dt.date, list[dict]]:
    return {_MONDAY: list(items)}


class RowCapFindingsTests(unittest.TestCase):
    """Check 5: a day block over the cap, Complexity rows excluded."""

    def test_over_cap_only_when_more_than_cap_non_complexity_rows(self):
        plain = {"is_complexity": False}
        complexity = {"is_complexity": True}
        cap = 3
        cases = [
            ("at cap", [plain] * cap, 0),
            ("one over", [plain] * (cap + 1), 1),
            ("complexity excluded", [plain] * cap + [complexity], 0),
        ]
        for name, items, expected in cases:
            with self.subTest(name):
                self.assertEqual(len(csi.row_cap_findings(_day(*items), cap)), expected)


class DueRowCarriedSectionTests(unittest.TestCase):
    """Check 3 with the carried section: only a proven row may be carried."""

    SUNDAY = dt.date(2026, 10, 11)
    CARRIED_SECTION = ("## ⏭️ Carried to next week (row cap)\n\n"
                       "- [5 Title](x.py) · 🟢 s2 · due 2026-10-05 · carried from Sat\n")

    def _findings(self, streak: int, section: str) -> list[str]:
        row = {"num": "5", "title": "Title", "due": "2026-10-05",
               "comfort": "🟢", "streak": streak}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "20261005_schedule.md"
            path.write_text("## Daily Schedule\n\n" + section, encoding="utf-8")
            carried = csi.carried_numbers(path)
        return csi.due_row_findings([row], {}, carried, self.SUNDAY, "20261005_schedule.md", _CFG)

    def test_carried_row_accepted_only_when_proven(self):
        cases = [
            ("s2 carried accepted", 2, self.CARRIED_SECTION, None),
            ("s1 carried flagged", 1, self.CARRIED_SECTION, "cannot be carried (unproven)"),
            ("absent flagged", 2, "", "seated on no day"),
        ]
        for name, streak, section, expected in cases:
            with self.subTest(name):
                findings = self._findings(streak, section)
                if expected is None:
                    self.assertEqual(findings, [])
                else:
                    self.assertEqual(len(findings), 1)
                    self.assertIn(expected, findings[0])


class IntakeFindingsTests(unittest.TestCase):
    """Check 6: the week's 🆕 count vs intake_per_week, or 0 when the backstop triggers."""

    def test_new_row_count_against_expected(self):
        new = {"is_new": True, "deferred_to": None}
        overdue = {"comfort": "🔴", "streak": 0, "due": "2026-10-01"}
        triggering = [overdue] * _CFG["intake_pause_overdue_unproven"]
        per_week = _CFG["intake_per_week"]
        cases = [
            ("at the rate", [new] * per_week, [], 0),
            ("one over", [new] * (per_week + 1), [], 1),
            ("zero when triggered", [], triggering, 0),
        ]
        for name, items, tracker_rows, expected in cases:
            with self.subTest(name):
                findings = csi.intake_findings(_day(*items), tracker_rows, _CFG, _TODAY)
                self.assertEqual(len(findings), expected)


def _week_lines(mon_rows: list[str], wed_header: str = "7.8 units", mon_header: str = "5.0 units",
                wed_rows: list[str] | None = None) -> list[str]:
    """A two-day week (Mon Oct 5 started, Wed Oct 7 future) as schedule lines."""
    return ([f"| ▸ **Mon Oct 5** · {mon_header} — label |  |  |  |  |"] + mon_rows
            + ["|  |  |  |  |  |", f"| ▸ **Wed Oct 7** · {wed_header} — label |  |  |  |  |"]
            + (wed_rows or []))


def _row(num: int, method: str | None = None, struck: bool = False, moved: bool = False) -> str:
    title = f"{num} Title" + (f" ({method})" if method else "")
    cell = f"~~[{title}](x.py)~~ · [LC](y)" if struck else f"[{title}](x.py) · [LC](y)"
    return f"| {'→ ' if moved else ''}{cell} | 🟢 s2 | | {'2026-10-09' if moved else ''} | Graphs |"


class DroppedRowFindingsTests(unittest.TestCase):
    """Check 7: a numbered row on a started day at HEAD must survive in the working file."""

    def test_started_day_rows_must_survive(self):
        mock = "| 🎤 Mock interview | 🎤 | | | Mock |"
        cases = [
            ("kept and struck", [_row(1462)], [_row(1462, struck=True)], 0, None),
            ("kept as moved", [_row(1462)], [_row(1462, moved=True)], 0, None),
            ("deleted on started day", [_row(1462)], [], 1, "1462"),
            ("two variants, one deleted", [_row(1631, "Dijkstra"), _row(1631, "Prim")],
             [_row(1631, "Prim")], 1, "(Dijkstra)"),
            ("numberless mock becomes numbered", [mock], [_row(7, struck=True)], 0, None),
        ]
        for name, head_rows, work_rows, expected, naming in cases:
            with self.subTest(name):
                findings = csi.dropped_row_findings(
                    _week_lines(head_rows), _week_lines(work_rows), _MONDAY, _TODAY)
                self.assertEqual(len(findings), expected)
                if naming:
                    self.assertIn(naming, findings[0])
        with self.subTest("deleted on future day"):
            head = _week_lines([], wed_rows=[_row(1462)])
            self.assertEqual(csi.dropped_row_findings(head, _week_lines([]), _MONDAY, _TODAY), [])


class PlannedFigureFindingsTests(unittest.TestCase):
    """Check 8: a planned figure is never lowered or removed, and is pinned when built drops."""

    def test_planned_never_lowered_and_pinned_when_built_drops(self):
        def mon(units: str) -> list[str]:
            return _week_lines([], mon_header=units)

        def wed(units: str) -> list[str]:
            return _week_lines([], wed_header=units)

        cases = [
            ("drop with pin", mon("6.6 units"), mon("3.8 units · planned 6.6 units"), 0, None),
            ("drop, no pin, started", mon("6.6 units"), mon("3.8 units"), 1,
             "add '· planned 6.6 units'"),
            ("drop on a future day", wed("6.6 units"), wed("3.8 units"), 0, None),
            ("lowered", mon("3.8 units · planned 6.6 units"),
             mon("3.8 units · planned 5.0 units"), 1, "lowered 6.6 → 5.0"),
            ("removed", mon("3.8 units · planned 6.6 units"), mon("3.8 units"), 1,
             "removed (was 6.6)"),
            ("even swap", mon("7.8 units"), mon("7.8 units"), 0, None),
        ]
        for name, head, work, expected, naming in cases:
            with self.subTest(name):
                findings = csi.planned_figure_findings(head, work, _MONDAY, _TODAY)
                self.assertEqual(len(findings), expected)
                if naming:
                    self.assertIn(naming, findings[0])


class LiveCurrentWeekTests(unittest.TestCase):
    """A soft check against the repo's real current-week schedule, not a fixture. Skips
    rather than fails when the schedule tree isn't present (e.g. a checkout of just this
    script) — the fixture tests above are the ones that must always run.
    """

    def test_live_current_week_is_silent(self):
        path = eb.current_schedule(dt.date.today())
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
        self._orig_eb_schedules = eb.SCHEDULES
        eb.SCHEDULES = tmp_dir

    def tearDown(self):
        eb.SCHEDULES = self._orig_eb_schedules
        self._tmpdir.cleanup()

    def _write_week(self, monday: str) -> Path:
        path = eb.SCHEDULES / f"{monday}_schedule.md"
        path.write_text(
            f"# Week of {monday}\n\n## Daily Schedule\n\n"
            "| Problem | S | E | Next | Technique |\n|---|:-:|:-:|:-:|---|\n",
            encoding="utf-8")
        return path

    def test_picks_this_week_when_next_weeks_monday_already_exists(self):
        this_week = self._write_week("20260921")  # Mon Sep 21
        self._write_week("20260928")  # Mon Sep 28, built ahead by the Sunday close-out
        today = dt.date(2026, 9, 24)  # Thu Sep 24 — inside this week, not next week
        self.assertEqual(eb.current_schedule(today), this_week)

    def test_falls_back_to_newest_when_no_file_spans_today(self):
        self._write_week("20260907")
        newest = self._write_week("20260914")
        today = dt.date(2026, 10, 1)  # past both weeks' spans
        self.assertEqual(eb.current_schedule(today), newest)


if __name__ == "__main__":
    unittest.main()
