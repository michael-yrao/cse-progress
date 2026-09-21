"""Tests for gamify.py — the honest-progress contract generator.

Stdlib unittest on purpose: this repo has no pytest/CI, and a test that needs an
uninstalled framework is a test that never runs. Run it with:

    python scripts/test_gamify.py

The functions under test are pure (they take plain dicts), so nothing here touches
the filesystem — the point is to pin the streak math, the timeline reconstruction,
and the badge triggers, which are the parts most likely to drift silently.
"""
from __future__ import annotations

import datetime as dt
import tempfile
import unittest
from pathlib import Path

import gamify


def _row(num, comfort, streak, diff="Medium", due="2026-12-01", reps=""):
    return {"num": str(num), "title": f"P{num}", "diff": diff, "comfort": comfort,
            "streak": streak, "due": due, "reps": reps}


class StreakTests(unittest.TestCase):
    TODAY = dt.date(2026, 9, 20)

    def _days(self, *iso):
        return [dt.date.fromisoformat(d) for d in iso]

    def test_empty(self):
        s = gamify.compute_streak([], allowance=1, today=self.TODAY)
        self.assertEqual((s["current"], s["longest"], s["studyDays"]), (0, 0, 0))

    def test_perfect_consecutive_run(self):
        days = self._days("2026-09-18", "2026-09-19", "2026-09-20")
        s = gamify.compute_streak(days, allowance=1, today=self.TODAY)
        self.assertEqual(s["current"], 3)
        self.assertEqual(s["longest"], 3)

    def test_rest_day_within_allowance_does_not_break(self):
        # A single skipped day (gap of 2) is tolerated at allowance=1.
        days = self._days("2026-09-16", "2026-09-18", "2026-09-20")
        s = gamify.compute_streak(days, allowance=1, today=self.TODAY)
        self.assertEqual(s["current"], 3)

    def test_gap_beyond_allowance_breaks(self):
        # A 3-day gap (Sep 16 -> Sep 20) exceeds allowance=1, so only today counts.
        days = self._days("2026-09-16", "2026-09-20")
        s = gamify.compute_streak(days, allowance=1, today=self.TODAY)
        self.assertEqual(s["current"], 1)

    def test_current_zero_when_last_day_stale(self):
        # Longest run is preserved, but the streak is not live if the last study day
        # is beyond the allowance window from today.
        days = self._days("2026-09-01", "2026-09-02", "2026-09-03")
        s = gamify.compute_streak(days, allowance=1, today=self.TODAY)
        self.assertEqual(s["current"], 0)
        self.assertEqual(s["longest"], 3)

    def test_study_days_counts_distinct_dates(self):
        days = self._days("2026-09-19", "2026-09-20")
        s = gamify.compute_streak(days, allowance=1, today=self.TODAY)
        self.assertEqual(s["studyDays"], 2)
        self.assertEqual(s["lastStudyDay"], "2026-09-20")


class PipelineTests(unittest.TestCase):
    def test_counts_and_green_streak_split(self):
        rows = [_row(1, "🔴", 0), _row(2, "🟡", 0), _row(3, "🟢", 0),
                _row(4, "🟢", 1), _row(5, "🟢", 2), _row(6, "🟢", 5), _row(7, "🎓", 3)]
        retired = [{"lcNumber": 704}]
        pl = gamify.pipeline(rows, retired)
        self.assertEqual(pl["blank"], 1)
        self.assertEqual(pl["shaky"], 1)
        self.assertEqual(pl["clean"]["total"], 4)
        self.assertEqual(pl["clean"]["s0"], 1)
        self.assertEqual(pl["clean"]["s1"], 1)
        self.assertEqual(pl["clean"]["s2plus"], 2)   # streak 2 and streak 5
        self.assertEqual(pl["graduated"], 1)
        self.assertEqual(pl["retired"], 1)

    def test_difficulty_mix(self):
        rows = [_row(1, "🟢", 1, "Easy"), _row(2, "🟢", 1, "Hard"), _row(3, "🟡", 0, "Hard")]
        self.assertEqual(gamify.difficulty_mix(rows), {"Easy": 1, "Medium": 0, "Hard": 2})

    def test_on_schedule_overdue_and_due(self):
        today = dt.date(2026, 9, 20)
        rows = [_row(1, "🟢", 1, due="2026-09-19"),   # overdue
                _row(2, "🟢", 1, due="2026-09-20"),   # due today
                _row(3, "🟢", 1, due="2026-10-01")]   # future
        os = gamify.on_schedule(rows, today)
        self.assertEqual(os["overdue"], 1)
        self.assertEqual(os["dueToday"], 1)
        self.assertEqual(os["totalActive"], 3)


class TimelineTests(unittest.TestCase):
    def test_reconstruction_and_anchor(self):
        rows = [_row(763, "🟡", 0, reps="2026-09-09, 2026-09-19")]
        sched = {"2026-09-09": {763: "🔴"}, "2026-09-19": {763: "🟡"}}
        problems = gamify.build_problems(rows, sched, {763: "greedy"},
                                         {763: "https://leetcode.com/problems/partition-labels/"})
        tl = problems[0]["timeline"]
        self.assertEqual([p["comfort"] for p in tl], ["🔴", "🟡"])
        self.assertEqual([p["level"] for p in tl], [0, 1])
        self.assertEqual(problems[0]["category"], "greedy")
        self.assertEqual(problems[0]["url"], "https://leetcode.com/problems/partition-labels/")

    def test_unknown_rep_is_activity_dot_but_last_anchors_to_current(self):
        rows = [_row(206, "🎓", 3, reps="2026-04-23, 2026-09-19")]
        sched = {}  # pre-archive: nothing known
        problems = gamify.build_problems(rows, sched, {}, {})
        tl = problems[0]["timeline"]
        self.assertIsNone(tl[0]["comfort"])            # activity dot, never fabricated
        self.assertEqual(tl[-1]["comfort"], "🎓")       # last point anchors to current comfort
        self.assertEqual(tl[-1]["level"], 3)

    def test_multi_variant_number_does_not_fabricate(self):
        # Two rows share number 21 (Recursion vs Iterative). The schedule index is keyed by
        # number and cannot say which variant a rep was, so reconstructed comfort must degrade
        # to activity dots (null) — only the final point anchors to each row's own comfort.
        rows = [_row(21, "🎓", 3, reps="2026-09-19"),
                _row(21, "🟢", 1, reps="2026-09-19")]
        sched = {"2026-09-19": {21: "🎓"}}  # would wrongly apply to BOTH without the guard
        problems = gamify.build_problems(rows, sched, {}, {})
        self.assertEqual(problems[0]["timeline"][-1]["comfort"], "🎓")   # anchored to its own
        self.assertEqual(problems[1]["timeline"][-1]["comfort"], "🟢")   # not the other variant

    def test_had_turnaround(self):
        blank_then_clean = [{"date": "1", "comfort": "🔴"}, {"date": "2", "comfort": "🟢"}]
        clean_only = [{"date": "1", "comfort": "🟢"}, {"date": "2", "comfort": "🟢"}]
        self.assertTrue(gamify._had_turnaround([{"timeline": blank_then_clean}]))
        self.assertFalse(gamify._had_turnaround([{"timeline": clean_only}]))


class BadgeTests(unittest.TestCase):
    CFG = {"streak_milestones": [7, 30], "trophy_milestones": [1, 10]}

    def _stats(self, graduated=0, retired=0, clean_total=0, longest=0, no_green=1):
        return {
            "pipeline": {"graduated": graduated, "retired": retired,
                         "clean": {"total": clean_total}},
            "streak": {"longest": longest},
            "coverage": {"noGreen": no_green, "started": 56, "total": 56},
        }

    def test_locked_when_nothing_earned(self):
        badges = gamify.compute_badges(self._stats(), [], self.CFG)
        earned = {b["id"] for b in badges if b["earned"]}
        self.assertEqual(earned, set())

    def test_graduation_and_trophy_milestones(self):
        stats = self._stats(graduated=12, retired=0, clean_total=5, no_green=0)
        problems = [{"difficulty": "Hard", "comfort": "🎓", "timeline": []}]
        badges = {b["id"]: b["earned"] for b in gamify.compute_badges(stats, problems, self.CFG)}
        self.assertTrue(badges["first-graduate"])
        self.assertTrue(badges["trophies-1"])
        self.assertTrue(badges["trophies-10"])       # 12 >= 10
        self.assertTrue(badges["first-hard-clean"])  # a Hard at 🎓
        self.assertTrue(badges["all-green"])         # noGreen == 0
        self.assertFalse(badges["first-retire"])     # 0 retired

    def test_streak_badges_use_longest(self):
        stats = self._stats(longest=30)
        badges = {b["id"]: b["earned"] for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertTrue(badges["streak-7"])
        self.assertTrue(badges["streak-30"])


class ParseTechniquesTests(unittest.TestCase):
    """parse_techniques() against a small fixture table, not the live repo file — pins the
    Problems-cell parsing (count vs. the parenthetical LC list) against the tricky tokens
    the real table actually contains (*+Nv*, em-dash, tilde-strikeout elsewhere)."""

    FIXTURE = """## Coverage

| Technique | Family | Problems | Best | 🟢 | Variants | Gaps |
|---|---|---:|:---:|:---:|---|---|
| Hierholzer (Eulerian path) | advanced_graphs | 2 *+1v* (332, 2097) | 🟢 | ✅ | pre-sorted adjacency ×1 | thin (2/3) |
| Bellman-Ford | advanced_graphs | 1 (787) | 🟢 | ✅ | — | thin (1/3) |
| Dijkstra | advanced_graphs | 1 (778) | 🟢 | ✅ | **Min-over-max ×0** | variant: **Min-over-max** |
| Frequency Counting | arrays_and_hash | 2 (49, 242) | 🎓 | ✅ | — | — |
| Not Started Technique | some_family | — | — | — | — | — |

## Vocabulary maintenance

- some unrelated bullet
"""

    def setUp(self):
        self._orig_coverage = gamify.COVERAGE
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(self.FIXTURE)
        tmp.close()
        gamify.COVERAGE = Path(tmp.name)

    def tearDown(self):
        gamify.COVERAGE.unlink(missing_ok=True)
        gamify.COVERAGE = self._orig_coverage

    def test_variant_rep_annotation_does_not_pollute_count_or_problems(self):
        rows = {r["name"]: r for r in gamify.parse_techniques()}
        row = rows["Hierholzer (Eulerian path)"]
        self.assertEqual(row["problemCount"], 2)
        self.assertEqual(row["problems"], [332, 2097])
        self.assertEqual(row["family"], "advanced_graphs")
        self.assertEqual(row["bestComfort"], "🟢")
        self.assertTrue(row["hasGreen"])
        self.assertTrue(row["thin"])
        self.assertFalse(row["hasVariantGap"])

    def test_simple_single_problem_row(self):
        rows = {r["name"]: r for r in gamify.parse_techniques()}
        row = rows["Bellman-Ford"]
        self.assertEqual(row["problemCount"], 1)
        self.assertEqual(row["problems"], [787])

    def test_variant_gap_flag(self):
        rows = {r["name"]: r for r in gamify.parse_techniques()}
        self.assertTrue(rows["Dijkstra"]["hasVariantGap"])

    def test_em_dash_row_is_zero_and_empty_not_a_crash(self):
        rows = {r["name"]: r for r in gamify.parse_techniques()}
        row = rows["Not Started Technique"]
        self.assertEqual(row["problemCount"], 0)
        self.assertEqual(row["problems"], [])
        self.assertIsNone(row["bestComfort"])
        self.assertFalse(row["hasGreen"])
        self.assertFalse(row["thin"])
        self.assertFalse(row["hasVariantGap"])

    def test_header_and_separator_rows_excluded(self):
        names = {r["name"] for r in gamify.parse_techniques()}
        self.assertNotIn("Technique", names)
        self.assertEqual(len(gamify.parse_techniques()), 5)

    def test_missing_file_fails_soft(self):
        gamify.COVERAGE = Path(tempfile.gettempdir()) / "no-such-coverage-file.md"
        self.assertEqual(gamify.parse_techniques(), [])


class SummaryOfTests(unittest.TestCase):
    def _payload(self):
        return {
            "schemaVersion": 1,
            "generatedAt": "2026-09-20",
            "totals": {"problems": 1, "solutions": 1, "reps": 2},
            "pipeline": {"blank": 0, "shaky": 0,
                         "clean": {"s0": 0, "s1": 0, "s2plus": 0, "total": 0},
                         "graduated": 1, "retired": 1},
            "difficulty": {"Easy": 0, "Medium": 1, "Hard": 0},
            "streak": {"current": 3, "longest": 5, "lastStudyDay": "2026-09-20",
                       "studyDays": 10, "restDayAllowance": 1},
            "coverage": {"total": 56, "started": 40, "noGreen": 2, "thin": 3, "variantGaps": 1},
            "onSchedule": {"totalActive": 10, "dueToday": 1, "overdue": 2},
            "trophyCase": {
                "graduated": [{"lcNumber": 206, "title": "Reverse Linked List",
                               "difficulty": "Easy", "url": "https://x", "comfort": "🎓",
                               "level": 3, "streak": 3, "nextReview": "2026-10-01",
                               "repDates": ["2026-01-01"], "timeline": [{"date": "2026-01-01"}]}],
                "retired": [{"lcNumber": 704, "title": "Binary Search",
                             "retiredOn": "2026-08-01"}],
            },
            "badges": [{"id": "first-graduate", "title": "First Graduation", "earned": True}],
            "techniques": [{"name": "Bellman-Ford", "family": "advanced_graphs",
                            "problemCount": 1, "problems": [787], "bestComfort": "🟢",
                            "hasGreen": True, "thin": True, "hasVariantGap": False}],
            # One date far outside the summary's rolling window (well over
            # SUMMARY_STUDY_DAYS_WINDOW days before generatedAt) plus two recent ones —
            # exercises the cap in summary_of() without touching the lifetime count, which
            # comes from streak.studyDays (10 above), never from len(this list).
            "studyDays": ["2025-01-01", "2026-09-19", "2026-09-20"],
            "problems": [{"lcNumber": 206, "title": "Reverse Linked List", "comfort": "🎓"}],
        }

    def test_no_problems_key(self):
        summary = gamify.summary_of(self._payload())
        self.assertNotIn("problems", summary)

    def test_keeps_core_aggregates(self):
        summary = gamify.summary_of(self._payload())
        for key in ("streak", "pipeline", "badges", "coverage", "totals",
                    "onSchedule", "difficulty", "schemaVersion", "generatedAt",
                    "techniques", "studyDays"):
            self.assertIn(key, summary)
        self.assertEqual(summary["streak"]["current"], 3)
        self.assertEqual(summary["badges"][0]["id"], "first-graduate")

    def test_techniques_pass_through_unchanged(self):
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["techniques"],
                         [{"name": "Bellman-Ford", "family": "advanced_graphs",
                           "problemCount": 1, "problems": [787], "bestComfort": "🟢",
                           "hasGreen": True, "thin": True, "hasVariantGap": False}])

    def test_study_days_capped_to_the_rolling_window(self):
        # 2025-01-01 is far more than SUMMARY_STUDY_DAYS_WINDOW days before generatedAt
        # (2026-09-20) and must be dropped; the two recent dates stay.
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["studyDays"], ["2026-09-19", "2026-09-20"])

    def test_study_days_cap_does_not_touch_the_lifetime_count(self):
        # The lifetime total lives in streak.studyDays/streak.longest, untouched by the cap
        # on the summary's date LIST.
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["streak"]["studyDays"], 10)
        self.assertEqual(summary["streak"]["longest"], 5)

    def test_trophy_case_graduated_is_compact(self):
        summary = gamify.summary_of(self._payload())
        graduated = summary["trophyCase"]["graduated"]
        self.assertEqual(len(graduated), 1)
        self.assertEqual(graduated[0], {"lcNumber": 206, "title": "Reverse Linked List",
                                        "difficulty": "Easy"})
        self.assertNotIn("timeline", graduated[0])
        self.assertNotIn("repDates", graduated[0])

    def test_trophy_case_retired_passes_through(self):
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["trophyCase"]["retired"],
                         [{"lcNumber": 704, "title": "Binary Search", "retiredOn": "2026-08-01"}])


class PayloadTests(unittest.TestCase):
    def test_build_payload_is_wellformed_and_never_raises(self):
        # Runs against the live repo files; asserts the contract's required keys exist.
        payload, _warnings = gamify.build_payload(dt.date(2026, 9, 20))
        for key in ("schemaVersion", "generatedAt", "totals", "pipeline", "streak",
                    "problems", "badges"):
            self.assertIn(key, payload)
        self.assertEqual(payload["schemaVersion"], gamify.SCHEMA_VERSION)
        self.assertIsInstance(payload["problems"], list)
        self.assertIsInstance(payload["badges"], list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
