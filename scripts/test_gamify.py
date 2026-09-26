"""Tests for gamify.py — the honest-progress contract generator.

Stdlib unittest on purpose: this repo has no pytest/CI, and a test that needs an
uninstalled framework is a test that never runs. Run it with:

    python scripts/test_gamify.py

The functions under test are pure (they take plain dicts), so nothing here touches
the filesystem — the point is to pin the streak math, the timeline reconstruction,
and the badge triggers, which are the parts most likely to drift silently.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import effort_budget as eb
import gamify
import links


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

    @staticmethod
    def _default_techniques():
        """One green, one not — the ordinary "some breadth, not full" shape."""
        return [{"name": "A", "hasGreen": True}, {"name": "B", "hasGreen": False}]

    def _stats(self, graduated=0, retired=0, clean_total=0, longest=0, no_green=1,
               techniques=None):
        techs = techniques if techniques is not None else self._default_techniques()
        return {
            "pipeline": {"graduated": graduated, "retired": retired,
                         "clean": {"total": clean_total}},
            "streak": {"longest": longest},
            "coverage": {"noGreen": no_green, "started": 56, "total": len(techs)},
            "techniques": techs,
        }

    def test_locked_when_nothing_earned(self):
        badges = gamify.compute_badges(self._stats(), [], self.CFG)
        earned = {b["id"] for b in badges if b["earned"]}
        self.assertEqual(earned, set())

    def test_graduation_and_trophy_milestones(self):
        stats = self._stats(graduated=12, retired=0, clean_total=5)
        problems = [{"difficulty": "Hard", "comfort": "🎓", "timeline": []}]
        badges = {b["id"]: b["earned"] for b in gamify.compute_badges(stats, problems, self.CFG)}
        self.assertTrue(badges["first-graduate"])
        self.assertTrue(badges["trophies-1"])
        self.assertTrue(badges["trophies-10"])       # 12 >= 10
        self.assertTrue(badges["first-hard-clean"])  # a Hard at 🎓
        self.assertFalse(badges["first-retire"])     # 0 retired
        # New criterion (Sep 26, 2026): all-green needs a green in EVERY
        # technique on the roadmap, not just the started ones — one
        # ungreened technique keeps it locked even with a loaded pipeline.
        self.assertFalse(badges["all-green"])

    def test_all_green_locked_despite_no_green_zero(self):
        """noGreen==0 (the OLD "every started technique" signal) no longer drives
        all-green on its own — only a green in every techniques.yml entry does."""
        stats = self._stats(no_green=0)
        badges = {b["id"]: b["earned"] for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertFalse(badges["all-green"])

    def test_all_green_earned_when_every_technique_has_green(self):
        techs = [{"name": "A", "hasGreen": True}, {"name": "B", "hasGreen": True}]
        stats = self._stats(techniques=techs)
        badges = {b["id"]: b for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertTrue(badges["all-green"]["earned"])
        self.assertEqual(badges["all-green"]["progress"], {"current": 2, "target": 2})

    def test_all_green_locked_when_no_techniques_at_all(self):
        stats = self._stats(techniques=[])
        badges = {b["id"]: b for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertFalse(badges["all-green"]["earned"])
        self.assertEqual(badges["all-green"]["progress"], {"current": 0, "target": 0})

    def test_streak_badges_use_longest(self):
        stats = self._stats(longest=30)
        badges = {b["id"]: b["earned"] for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertTrue(badges["streak-7"])
        self.assertTrue(badges["streak-30"])

    def test_progress_on_counter_badges_absent_on_event_badges(self):
        stats = self._stats(graduated=1, longest=30)
        badges = {b["id"]: b for b in gamify.compute_badges(stats, [], self.CFG)}
        self.assertEqual(badges["streak-7"]["progress"], {"current": 30, "target": 7})
        self.assertEqual(badges["trophies-1"]["progress"], {"current": 1, "target": 1})
        self.assertIn("progress", badges["all-green"])
        self.assertNotIn("progress", badges["comeback"])
        self.assertNotIn("progress", badges["first-retire"])

    def test_trophies_description_pluralization(self):
        badges = {b["id"]: b["description"]
                  for b in gamify.compute_badges(self._stats(), [], self.CFG)}
        self.assertIn("1 problem graduated", badges["trophies-1"])
        self.assertIn("10 problems graduated", badges["trophies-10"])


class ParseTechniquesTests(unittest.TestCase):
    """parse_techniques() against a small fixture table, not the live repo file — pins the
    Problems-cell parsing (count vs. the parenthetical LC list) against the tricky tokens
    the real table actually contains (*+Nv*, em-dash, tilde-strikeout elsewhere), the Tier
    column + the started/*not started* Gaps marker (Sep 21, 2026), and (round 3) the Min
    column -> minProblems."""

    FIXTURE = """## Coverage

| Technique | Family | Tier | Min | Problems | Best | 🟢 | Variants | Gaps |
|---|---|---|---:|---:|:---:|:---:|---|---|
| Hierholzer (Eulerian path) | advanced_graphs | core | 3 | 2 *+1v* (332, 2097) | 🟢 | ✅ | pre-sorted adjacency ×1 | thin (2/3) |
| Bellman-Ford | advanced_graphs | core | 3 | 1 (787) | 🟢 | ✅ | — | thin (1/3) |
| Dijkstra | advanced_graphs | core | 3 | 1 (778) | 🟢 | ✅ | **Min-over-max ×0** | variant: **Min-over-max** |
| Frequency Counting | arrays_and_hash | core | 2 | 2 (49, 242) | 🎓 | ✅ | — | — |
| Knapsack | dynamic_programming | dp | 3 | 0 (—) | — | ❌ | — | *not started* |

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
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Hierholzer (Eulerian path)"]
        self.assertEqual(row["problemCount"], 2)
        self.assertEqual(row["problems"], [332, 2097])
        self.assertEqual(row["family"], "advanced_graphs")
        self.assertEqual(row["bestComfort"], "🟢")
        self.assertTrue(row["hasGreen"])
        self.assertTrue(row["thin"])
        self.assertFalse(row["hasVariantGap"])

    def test_started_technique_has_tier_core_and_started_true(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Bellman-Ford"]
        self.assertEqual(row["tier"], "core")
        self.assertTrue(row["started"])

    def test_not_started_technique_has_its_declared_tier_and_started_false(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Knapsack"]
        self.assertEqual(row["tier"], "dp")
        self.assertFalse(row["started"])

    def test_min_problems_read_from_the_min_column(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        self.assertEqual(rows["Bellman-Ford"]["minProblems"], 3)
        self.assertEqual(rows["Frequency Counting"]["minProblems"], 2)

    def test_not_started_technique_still_carries_its_declared_min_problems(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Knapsack"]
        self.assertEqual(row["minProblems"], 3)
        self.assertEqual(row["problemCount"], 0)

    def test_simple_single_problem_row(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Bellman-Ford"]
        self.assertEqual(row["problemCount"], 1)
        self.assertEqual(row["problems"], [787])

    def test_variant_gap_flag(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        self.assertTrue(rows["Dijkstra"]["hasVariantGap"])

    def test_em_dash_row_is_zero_and_empty_not_a_crash(self):
        rows = {r["name"]: r for r in gamify.parse_techniques([])}
        row = rows["Knapsack"]
        self.assertEqual(row["problemCount"], 0)
        self.assertEqual(row["problems"], [])
        self.assertIsNone(row["bestComfort"])
        self.assertFalse(row["hasGreen"])
        self.assertFalse(row["thin"])
        self.assertFalse(row["hasVariantGap"])

    def test_header_and_separator_rows_excluded(self):
        names = {r["name"] for r in gamify.parse_techniques([])}
        self.assertNotIn("Technique", names)
        self.assertEqual(len(gamify.parse_techniques([])), 5)

    def test_missing_file_fails_soft(self):
        gamify.COVERAGE = Path(tempfile.gettempdir()) / "no-such-coverage-file.md"
        self.assertEqual(gamify.parse_techniques([]), [])


class ParseTechniquesWrongColumnCountTests(unittest.TestCase):
    """An older technique_coverage.py emitting a 7-column table (no Min / no 🟢 columns)
    must not silently yield [] with no signal — it warns and returns []."""

    FIXTURE = """## Coverage

| Technique | Family | Min | Problems | Best | Variants | Gaps |
|---|---|---:|---:|:---:|---|---|
| Bellman-Ford | advanced_graphs | 3 | 1 (787) | 🟢 | — | thin (1/3) |
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

    def test_wrong_column_count_returns_empty(self):
        self.assertEqual(gamify.parse_techniques([]), [])

    def test_wrong_column_count_warns_with_the_actual_count(self):
        warnings: list[str] = []
        gamify.parse_techniques(warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIn("7 columns", warnings[0])
        self.assertIn("expected 9", warnings[0])


def _tech_row(name, problems=None):
    return {"name": name, "family": "f", "tier": "core", "started": True,
            "minProblems": 3, "problemCount": len(problems or []),
            "problems": problems or [], "bestComfort": None, "hasGreen": False,
            "thin": True, "hasVariantGap": False}


def _yaml_entry(name, builds_on=None):
    return {"name": name, "builds_on": builds_on}


def _problem(num, comfort):
    return {"lcNumber": num, "comfort": comfort}


class EnrichTechniquesTests(unittest.TestCase):
    """enrich_techniques() against plain-dict fixtures (parse_techniques()'s row shape and
    techniques.yml's own entry shape) — never the live repo file. Pins: builds_on copies
    through; defaults to []; an unknown name is dropped with a warning; a self-edge is
    dropped with a warning; a 2-cycle is detected and one edge dropped; graduatedCount
    counts 🎓 and 🏆 but not 🟢; enrich_techniques never mutates its inputs."""

    def test_builds_on_copies_through(self):
        rows = [_tech_row("B")]
        entries = [_yaml_entry("A"), _yaml_entry("B", ["A"])]
        out = gamify.enrich_techniques(rows, entries, {}, [])
        self.assertEqual(out[0]["buildsOn"], ["A"])

    def test_builds_on_defaults_to_empty_list(self):
        rows = [_tech_row("Root")]
        entries = [_yaml_entry("Root")]
        out = gamify.enrich_techniques(rows, entries, {}, [])
        self.assertEqual(out[0]["buildsOn"], [])

    def test_unknown_name_dropped_with_warning(self):
        rows = [_tech_row("B")]
        entries = [_yaml_entry("B", ["Nonexistent"])]
        warnings: list[str] = []
        out = gamify.enrich_techniques(rows, entries, {}, warnings)
        self.assertEqual(out[0]["buildsOn"], [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("Nonexistent", warnings[0])

    def test_self_edge_dropped_with_warning(self):
        rows = [_tech_row("A")]
        entries = [_yaml_entry("A", ["A"])]
        warnings: list[str] = []
        out = gamify.enrich_techniques(rows, entries, {}, warnings)
        self.assertEqual(out[0]["buildsOn"], [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("itself", warnings[0])

    def test_two_cycle_detected_and_one_edge_dropped(self):
        rows = [_tech_row("A"), _tech_row("B")]
        entries = [_yaml_entry("A", ["B"]), _yaml_entry("B", ["A"])]
        warnings: list[str] = []
        out = gamify.enrich_techniques(rows, entries, {}, warnings)
        by_name = {r["name"]: r["buildsOn"] for r in out}
        # exactly one of the two edges survives — the DFS back-edge is dropped
        total_edges = len(by_name["A"]) + len(by_name["B"])
        self.assertEqual(total_edges, 1)
        self.assertTrue(any("cycle" in w for w in warnings))

    def test_graduated_and_retired_count_graduated_streak_and_clean_do_not(self):
        rows = [_tech_row("T", problems=[1, 2, 3, 4])]
        entries = [_yaml_entry("T")]
        comfort_by_number = {1: "🎓", 2: "🏆", 3: "🟢", 4: "🟡"}
        out = gamify.enrich_techniques(rows, entries, comfort_by_number, [])
        self.assertEqual(out[0]["graduatedCount"], 2)

    def test_untracked_problem_number_does_not_count(self):
        rows = [_tech_row("T", problems=[99])]
        entries = [_yaml_entry("T")]
        out = gamify.enrich_techniques(rows, entries, {}, [])
        self.assertEqual(out[0]["graduatedCount"], 0)

    def test_does_not_mutate_inputs(self):
        row = _tech_row("B")
        entry = _yaml_entry("B", ["A"])
        rows, entries = [row], [_yaml_entry("A"), entry]
        gamify.enrich_techniques(rows, entries, {}, [])
        self.assertNotIn("buildsOn", row)
        self.assertNotIn("graduatedCount", row)

    def test_comfort_by_number_malformed_glyph_does_not_raise_or_count(self):
        # build_problems() itself is fail-soft (LEVEL.get(r["comfort"]), never LEVEL[...]),
        # so _comfort_by_number must be too: a tracker cell outside LEVEL's five glyphs
        # must never raise build_payload out of its "never raises" contract.
        problems = [_problem(1, "?")]
        comfort_by_number = gamify._comfort_by_number(problems, retired=[])
        self.assertNotIn(1, comfort_by_number)

        rows = [_tech_row("T", problems=[1])]
        entries = [_yaml_entry("T")]
        out = gamify.enrich_techniques(rows, entries, comfort_by_number, [])
        self.assertEqual(out[0]["graduatedCount"], 0)


class ParseCurrentWeekScheduleTests(unittest.TestCase):
    """parse_current_week_schedule() against a small fixture week (not the live repo file)
    — pins the Today's-board slice: a plain row, a struck/done row (glyph swap-out and
    title cleanup on a `~~[...]~~` cell), a bare-number 🆕 row (lcNumber via the fallback,
    url via the row's own [LC] link, kind "new"), a row whose own [LC] link wins over a
    (deliberately different) urls.get() value, a 🔤 concept-primer row mirroring the
    archived real one (kind "primer", no lcNumber/url at all), a row struck AHEAD of its
    tag glyph (`~~🆕 39 ...~~`, real archived history — pins tags/kind survive emphasis
    ahead of the glyph, and done stays true), and the three Sunday `🎯 ... | Complexity`
    rows (kind "complexity" beats the 🎯 tag) — together the five `kind` values are all
    covered. Also pins `_schedule_item_url`'s full 3-way precedence: an NC-only row WITH
    a tracker entry (the tracker join wins over the row's own NC link) and an NC-only row
    with NO tracker entry (the NC link is used as the last resort). Also pins the
    tracker-joined `difficulty` — including the honest null for a number the tracker
    doesn't have yet."""

    FIXTURE = (
        "## Daily Schedule\n\n"
        "| Problem | S | E | Next | Technique |\n"
        "|---|:-:|:-:|:-:|---|\n"
        "| ▸ **Mon Sep 21** · 6.8 units — Test day one |  |  |  |  |\n"
        "| ⚠️🔥 [22 Generate Parentheses](../../../dsa/leetcode/backtracking/22_generate_parentheses.py)"
        " · [LC](https://leetcode.com/problems/generate-parentheses/) | 🔴 | | | Backtracking |\n"
        "| ~~[100 Same Tree](../../../dsa/leetcode/trees/100_same_tree.py)~~"
        " · [LC](https://leetcode.com/problems/same-tree/) | 🟢 | 🎓 | 2026-10-01 | Tree-DFS |\n"
        "| [55 Jump Game](../../../dsa/leetcode/greedy/55_jump_game.py)"
        " · [LC](https://leetcode.com/problems/jump-game/) | 🟡 | | | Greedy |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Tue Sep 22** · 5.0 units — Test day two |  |  |  |  |\n"
        "| 🆕 39 Combination Sum · [LC](https://leetcode.com/problems/combination-sum/)"
        " | 🆕 | | | Backtracking |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Thu Sep 24** · 3.0 units — Test day three |  |  |  |  |\n"
        "| [77 Word Break](../../../dsa/leetcode/dp/77_word_break.py)"
        " · [LC](https://leetcode.com/problems/word-break/) | 🟡 | | | DP |\n"
        # Mirrors the archived 🔤 row shape (see docs/foundations/schedules/archive/
        # 20260907_schedule.md's "Backtracking primer" row): a bare **Bold Title** with no
        # digit after `**` (so eb.SCHED_NUM finds nothing and the bare-number fallback also
        # finds nothing, since the title itself starts with a letter, not a number), 🔤 in
        # both the Problem cell and the S column, and a free-form Technique cell that is
        # NOT "Complexity" — the only kind/tag branch no other fixture row exercises.
        "| 🔤 **Two Pointers primer** — before the phase opens Oct 5"
        " | 🔤 | | | concept overview, no LC number |\n"
        # Emphasis-before-glyph: several archived weeks strike (or bold, or both) the
        # WHOLE row ahead of its tag glyph rather than plain — this exact shape is real
        # history (20260824_schedule.md's struck 🆕 rows), not a hypothetical.
        "| ~~🆕 39 Combination Sum · [LC](https://leetcode.com/problems/combination-sum/)~~"
        " | 🆕 | | | Backtracking |\n"
        "| |  |  |  |  |\n"
        # NC-only rows (no [LC] at all) — _schedule_item_url's 3-way precedence, per-case:
        "| ▸ **Fri Sep 25** · 4.0 units — Test day four |  |  |  |  |\n"
        # 200 IS in the tracker: the tracker join (precedence 2) must win over this row's
        # own [NC] link (precedence 3) — an NC url must never beat a real LC one.
        "| [200 Number of Islands](../../../dsa/leetcode/graphs/200_number_of_islands.py)"
        " · [NC](https://neetcode.io/problems/number-of-islands) | 🟡 | | | BFS |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Sat Sep 26** · ~4.0 units — Test day five |  |  |  |  |\n"
        # 269 is NOT in the tracker: nothing outranks the row's own [NC] link, so it's
        # used as the last resort rather than leaving url null.
        "| [269 Alien Dictionary](../../../dsa/leetcode/graphs/269_alien_dictionary.py)"
        " · [NC](https://neetcode.io/problems/foreign-dictionary) | 🟡 | | | Topological Sort |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Sun Sep 27** · 2.0 units — Complexity day |  |  |  |  |\n"
        "| 🎯 [226 Invert Binary Tree](../../../dsa/leetcode/trees/226_invert_binary_tree.py)"
        " · [LC](https://leetcode.com/problems/invert-binary-tree/) — complexity re-ask (time)"
        " | 🎯 | | | Complexity |\n"
        "| 🎯 [98 Validate BST](../../../dsa/leetcode/trees/98_validate_bst.py)"
        " · [LC](https://leetcode.com/problems/validate-binary-search-tree/) — complexity re-ask (space)"
        " | 🎯 | | | Complexity |\n"
        "| 🎯 [543 Diameter of Binary Tree](../../../dsa/leetcode/trees/543_diameter_of_binary_tree.py)"
        " · [LC](https://leetcode.com/problems/diameter-of-binary-tree/) — complexity re-ask (time)"
        " | 🎯 | | | Complexity |\n"
    )

    # Joined by lcNumber into the schedule items above: 22 -> Medium, 100 -> Easy,
    # 200 -> Medium. 39 (the 🆕 row), 77, and 269 are deliberately ABSENT — 39 must
    # resolve to null (no tracker entry yet); 77 pins that difficulty and url are joined
    # independently (77 gets its url from its own [LC] link despite no tracker row); 269
    # (NC-only, no tracker row) pins the honest-null-turned-NC-last-resort case.
    TRACKER_FIXTURE = (
        "| Medium | [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) "
        "| 🔴 | 0 | 2026-12-01 |\n"
        "| Easy | [100. Same Tree](https://leetcode.com/problems/same-tree/) "
        "| 🎓 | 3 | 2026-12-05 |\n"
        "| Medium | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) "
        "| 🟡 | 1 | 2026-11-01 |\n"
    )

    # Joined by lcNumber into the schedule items above, mirroring TRACKER_FIXTURE's own
    # markdown links (problem_urls() reads the same file). 55 and 39 are deliberately
    # absent — the honest-null / own-link-only cases pinned below. 77's entry is
    # deliberately a DIFFERENT url than its row's own [LC] link, to pin that the row's own
    # [LC] link wins (see _schedule_item_url) rather than this tracker join. 200's entry
    # pins the OPPOSITE precedence case: this tracker join must win over 200's own [NC]
    # link (an NC url must never outrank a real LC one). 269 is deliberately absent from
    # both TRACKER_FIXTURE and here — its own [NC] link is the only source available.
    URLS = {22: "https://leetcode.com/problems/generate-parentheses/",
            100: "https://leetcode.com/problems/same-tree/",
            77: "https://leetcode.com/problems/STALE-SLUG-DO-NOT-PREFER/",
            200: "https://leetcode.com/problems/number-of-islands/"}

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._orig_schedules = eb.SCHEDULES
        self._orig_tracker = eb.TRACKER
        self._orig_gamify_tracker = gamify.TRACKER
        sched_dir = Path(self._tmpdir.name)
        (sched_dir / "20260921_schedule.md").write_text(self.FIXTURE, encoding="utf-8")
        eb.SCHEDULES = sched_dir
        tracker_path = sched_dir / "dsa_progress.md"
        tracker_path.write_text(self.TRACKER_FIXTURE, encoding="utf-8")
        eb.TRACKER = tracker_path
        gamify.TRACKER = tracker_path

    def tearDown(self):
        eb.SCHEDULES = self._orig_schedules
        eb.TRACKER = self._orig_tracker
        gamify.TRACKER = self._orig_gamify_tracker
        self._tmpdir.cleanup()

    def test_all_seven_days_emitted_with_correct_dates(self):
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        self.assertIsNotNone(result)
        self.assertEqual(result["weekOf"], "2026-09-21")
        self.assertEqual(len(result["days"]), 7)
        self.assertEqual(result["days"][0]["date"], "2026-09-21")
        self.assertEqual(result["days"][6]["date"], "2026-09-27")

    def test_monday_items_and_done_row_parsed(self):
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        mon = result["days"][0]
        self.assertEqual(mon["weekday"], "Monday")
        self.assertEqual(mon["units"], 6.8)
        self.assertEqual(mon["label"], "Test day one")
        # An approximate price ("~4.0 units") is still a price — the `~` must not null the units
        # (Sat Sep 26's "~11.1 units" header hid the dashboard's workload bar, found 2026-09-25).
        self.assertEqual(result["days"][5]["units"], 4.0)
        self.assertEqual(len(mon["items"]), 3)

        plain, done, untracked = mon["items"]
        self.assertEqual(plain, {"lcNumber": 22, "title": "Generate Parentheses",
                                 "technique": "Backtracking", "startComfort": "🔴",
                                 "difficulty": "Medium",
                                 "url": "https://leetcode.com/problems/generate-parentheses/",
                                 "file": None,
                                 "tags": ["protected", "backfill"], "kind": "rep",
                                 "done": False,
                                 "endComfort": None, "endNote": None, "nextReview": None})
        # The 100 row's E cell is "🎓" (no trailing note) and Next is "2026-10-01" — pins
        # endComfort/nextReview are emitted, and a glyph with nothing following it yields
        # endNote null rather than an empty string.
        self.assertEqual(done, {"lcNumber": 100, "title": "Same Tree",
                                "technique": "Tree-DFS", "startComfort": "🟢",
                                "difficulty": "Easy",
                                "url": "https://leetcode.com/problems/same-tree/",
                                "file": None,
                                "tags": [], "kind": "rep",
                                "done": True,
                                "endComfort": "🎓", "endNote": None, "nextReview": "2026-10-01"})
        # 55 has a real lcNumber but is deliberately absent from TRACKER_FIXTURE — the
        # honest-null case for `difficulty` (a number the tracker doesn't have yet). `url`
        # is NOT null, though: 55's row carries its own [LC] link, which _schedule_item_url
        # reads directly, independently of the (absent) tracker join.
        self.assertEqual(untracked, {"lcNumber": 55, "title": "Jump Game",
                                     "technique": "Greedy", "startComfort": "🟡",
                                     "difficulty": None,
                                     "url": "https://leetcode.com/problems/jump-game/",
                                     "file": None,
                                     "tags": [], "kind": "rep",
                                     "done": False,
                                     "endComfort": None, "endNote": None, "nextReview": None})

    def test_new_intake_row_gets_lcnumber_from_fallback_and_url_from_own_link(self):
        # 🆕 39 has no `[`/`**` before its number, so eb.SCHED_NUM (by design) finds
        # nothing — but _schedule_item_lc_number's bare-digits fallback still recovers 39
        # from the tag-stripped title, and _schedule_item_url reads its url straight off
        # the row's own [LC] link (39 has no TRACKER_FIXTURE/URLS entry at all).
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        tue = result["days"][1]
        self.assertEqual(len(tue["items"]), 1)
        self.assertEqual(tue["items"][0], {"lcNumber": 39, "title": "Combination Sum",
                                           "technique": "Backtracking", "startComfort": None,
                                           "difficulty": None,
                                           "url": "https://leetcode.com/problems/combination-sum/",
                                           "file": None,
                                           "tags": ["new"], "kind": "new",
                                           "done": False,
                                           "endComfort": None, "endNote": None, "nextReview": None})

    def test_row_own_link_url_wins_over_tracker_join(self):
        # 77's URLS entry is deliberately a different (stale) url — the row's own [LC]
        # link must win, per _schedule_item_url's precedence.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        thu = result["days"][3]
        self.assertEqual(len(thu["items"]), 3)
        self.assertEqual(thu["items"][0], {"lcNumber": 77, "title": "Word Break",
                                           "technique": "DP", "startComfort": "🟡",
                                           "difficulty": None,
                                           "url": "https://leetcode.com/problems/word-break/",
                                           "file": None,
                                           "tags": [], "kind": "rep",
                                           "done": False,
                                           "endComfort": None, "endNote": None, "nextReview": None})

    def test_primer_row_has_no_lcnumber_and_kind_primer(self):
        # The only kind/tag branch ("primer") not otherwise exercised by a real or
        # synthetic row above. No `[`/`**digit` for eb.SCHED_NUM, and the tag-stripped
        # title starts with a letter, not a digit, so the bare-number fallback also comes
        # up empty — lcNumber and url are both honestly null, same as a concept primer
        # with no attached LC problem.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        thu = result["days"][3]
        self.assertEqual(thu["items"][1], {
            "lcNumber": None, "title": "Two Pointers primer — before the phase opens Oct 5",
            "technique": "concept overview, no LC number", "startComfort": None,
            "difficulty": None, "url": None,
            "file": None,
            "tags": ["primer"], "kind": "primer",
            "done": False,
            "endComfort": None, "endNote": None, "nextReview": None})

    def test_emphasis_before_glyph_does_not_blank_out_tags(self):
        # `~~🆕 39 ...~~` (whole row struck AHEAD of its tag glyph) is real archived
        # history (20260824_schedule.md's struck 🆕 rows), not hypothetical — a plain
        # `cell.lstrip()` would see "~~" first and never reach "🆕", yielding tags: []
        # and kind: "rep". done stays keyed off the raw "~~" check either way, so pinning
        # it True here also confirms the emphasis strip in _leading_tags didn't leak into
        # (or otherwise disturb) done detection.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        thu = result["days"][3]
        self.assertEqual(thu["items"][2], {
            "lcNumber": 39, "title": "Combination Sum",
            "technique": "Backtracking", "startComfort": None,
            "difficulty": None,
            "url": "https://leetcode.com/problems/combination-sum/",
            "file": None,
            "tags": ["new"], "kind": "new",
            "done": True,
            "endComfort": None, "endNote": None, "nextReview": None})

    def test_complexity_technique_wins_kind_over_the_probe_tag(self):
        # All three Sunday rows are 🎯-tagged AND carry Technique "Complexity" — kind must
        # come out "complexity" (the more specific fact), not "probe", and tags still
        # records the 🎯 glyph regardless of which kind it resolved to.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        sun = result["days"][6]
        self.assertEqual(len(sun["items"]), 3)
        for item in sun["items"]:
            self.assertEqual(item["kind"], "complexity")
            self.assertEqual(item["tags"], ["probe"])
        self.assertEqual(sun["items"][0]["lcNumber"], 226)
        self.assertEqual(sun["items"][0]["title"], "Invert Binary Tree")
        self.assertEqual(sun["items"][0]["url"],
                          "https://leetcode.com/problems/invert-binary-tree/")

    def test_nc_only_row_loses_to_a_tracker_lc_join(self):
        # 200's row carries only its own [NC] link, but 200 HAS a tracker entry — the
        # tracker join (precedence 2) must win over that row's own NC link
        # (precedence 3): an NC url must never outrank a real LC one.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        fri = result["days"][4]
        self.assertEqual(len(fri["items"]), 1)
        self.assertEqual(fri["items"][0], {
            "lcNumber": 200, "title": "Number of Islands",
            "technique": "BFS", "startComfort": "🟡",
            "difficulty": "Medium",
            "url": "https://leetcode.com/problems/number-of-islands/",
            "file": None,
            "tags": [], "kind": "rep",
            "done": False,
            "endComfort": None, "endNote": None, "nextReview": None})

    def test_nc_only_row_with_no_tracker_entry_uses_nc_as_last_resort(self):
        # 269's row also carries only its own [NC] link, and 269 has NO tracker entry —
        # nothing outranks the NC link here, so it is used rather than leaving url null.
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        sat = result["days"][5]
        self.assertEqual(len(sat["items"]), 1)
        self.assertEqual(sat["items"][0], {
            "lcNumber": 269, "title": "Alien Dictionary",
            "technique": "Topological Sort", "startComfort": "🟡",
            "difficulty": None,
            "url": "https://neetcode.io/problems/foreign-dictionary",
            "file": None,
            "tags": [], "kind": "rep",
            "done": False,
            "endComfort": None, "endNote": None, "nextReview": None})

    def test_day_with_no_block_has_no_items(self):
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS)
        wed = result["days"][2]
        self.assertEqual(wed["items"], [])

    def test_no_current_schedule_file_is_none(self):
        result = gamify.parse_current_week_schedule(dt.date(2030, 1, 1), self.URLS)
        self.assertIsNone(result)

    def test_items_carry_solution_file_from_the_files_map(self):
        # `files` (links.solution_files()) joins each item's own solution path by lcNumber;
        # a number with no file — and a row with no number at all (the 🔤 primer) — is an
        # honest null, never a guessed path.
        files = {22: [gamify.REPO / "dsa/leetcode/backtracking/22_generate_parentheses.py"],
                 100: [gamify.REPO / "dsa/leetcode/trees/100_same_tree.py"]}
        result = gamify.parse_current_week_schedule(dt.date(2026, 9, 21), self.URLS, files)
        plain, done, untracked = result["days"][0]["items"]
        self.assertEqual(plain["file"], "dsa/leetcode/backtracking/22_generate_parentheses.py")
        self.assertEqual(done["file"], "dsa/leetcode/trees/100_same_tree.py")
        self.assertIsNone(untracked["file"])                  # 55: no file yet
        primer = result["days"][3]["items"][1]
        self.assertIsNone(primer["lcNumber"])
        self.assertIsNone(primer["file"])                     # no number → no lookup


class BuildWorkloadTests(unittest.TestCase):
    """gamify.build_workload() — planned-vs-completed effort units per scheduled day,
    scanned across BOTH the live schedules folder and its archive/ subfolder, priced via
    effort_budget.price_day_items() (the extracted pricing core of price_schedule_day()).

    Fixture rows are plain dicts (effort_budget's own row shape, via the module-level
    _row() helper) rather than a tracker markdown file + eb.parse_rows() — build_workload()
    takes `rows` straight from its caller, so nothing here needs the tracker file at all.

    CFG is a minimal, self-contained effort_budget config: no attempt_decay or
    difficulty_demotion block, so price() reduces to base(comfort/streak) x
    difficulty(tier) with no decay/demotion — expected prices below are computed by hand
    against exactly these weights, not against cse.config.yml's (which is free to change).
    """

    CFG = {
        "comfort_units": {"🔴": 3.0, "🟡": 2.0, "🟢": 1.0},
        "difficulty": {"Easy": 0.7, "Medium": 1.0, "Hard": 1.5},
    }

    # Mon Aug 10 2026: a plain 🔴 Medium row (remaining, priced 3.0) and a struck 🟡 Easy
    # row (done, priced 1.4) — the two-row done/remaining split. Thu Aug 13 2026: a
    # number-less 🔤 primer row only — no problem number to price, so `partial` must be
    # true even though built/done both land at 0.0.
    LIVE_FIXTURE = (
        "## Daily Schedule\n\n"
        "| Problem | S | E | Next | Technique |\n"
        "|---|:-:|:-:|:-:|---|\n"
        "| ▸ **Mon Aug 10** · 5.0 units — Test build day |  |  |  |  |\n"
        "| [501 Widget One](../../../dsa/leetcode/arrays/501_widget_one.py)"
        " · [LC](https://leetcode.com/problems/widget-one/) | 🔴 | | | Arrays |\n"
        "| ~~[502 Widget Two](../../../dsa/leetcode/arrays/502_widget_two.py)~~"
        " · [LC](https://leetcode.com/problems/widget-two/) | 🟡 | | | Arrays |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Thu Aug 13** · 3.0 units — Primer day |  |  |  |  |\n"
        "| 🔤 **Some Primer Topic** — no LC number | 🔤 | | | concept overview |\n"
        "| |  |  |  |  |\n"
    )

    # Mon Sep 14 2026: an approximate (`~4.0`) header with no priced rows — pins that
    # `planned` reads the approximate price, not None. Wed Sep 16 2026: a struck 🟢 s1
    # Hard row (done) plus a plain 🟡 Medium row (remaining) — built > done.
    ARCHIVE_FIXTURE = (
        "## Daily Schedule\n\n"
        "| Problem | S | E | Next | Technique |\n"
        "|---|:-:|:-:|:-:|---|\n"
        "| ▸ **Mon Sep 14** · ~4.0 units — Approx day |  |  |  |  |\n"
        "| |  |  |  |  |\n"
        "| ▸ **Wed Sep 16** · 6.0 units — Struck day |  |  |  |  |\n"
        "| ~~[503 Widget Three](../../../dsa/leetcode/arrays/503_widget_three.py)~~"
        " · [LC](https://leetcode.com/problems/widget-three/) | 🟢 s1 | | | Arrays |\n"
        "| [504 Widget Four](../../../dsa/leetcode/arrays/504_widget_four.py)"
        " · [LC](https://leetcode.com/problems/widget-four/) | 🟡 | | | Arrays |\n"
        "| |  |  |  |  |\n"
    )

    # Pre-2026-08-10 one-row-per-day shape: no `▸ **Day**` header this parser recognizes,
    # so every day of this week is stated=None/items=[] and build_workload() must emit
    # nothing for it.
    OLD_FORMAT_FIXTURE = (
        "## Daily Schedule\n\n"
        "| Date | Problem | Comfort |\n"
        "|---|---|---|\n"
        "| 2026-06-01 | 1 Two Sum | 🟢 |\n"
    )

    ROWS = [
        _row(501, "🔴", 0, diff="Medium"),
        _row(502, "🟡", 0, diff="Easy"),
        _row(503, "🟢", 1, diff="Hard"),
        _row(504, "🟡", 0, diff="Medium"),
    ]

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._orig_schedules = eb.SCHEDULES
        sched_dir = Path(self._tmpdir.name)
        (sched_dir / "archive").mkdir()
        (sched_dir / "20260810_schedule.md").write_text(self.LIVE_FIXTURE, encoding="utf-8")
        (sched_dir / "20260601_schedule.md").write_text(self.OLD_FORMAT_FIXTURE, encoding="utf-8")
        (sched_dir / "archive" / "20260914_schedule.md").write_text(
            self.ARCHIVE_FIXTURE, encoding="utf-8")
        eb.SCHEDULES = sched_dir

    def tearDown(self):
        eb.SCHEDULES = self._orig_schedules
        self._tmpdir.cleanup()

    def test_entries_sorted_by_date_across_live_and_archive(self):
        workload = gamify.build_workload(self.ROWS, self.CFG)
        dates = [w["date"] for w in workload]
        self.assertEqual(dates, sorted(dates))
        self.assertEqual(dates, ["2026-08-10", "2026-08-13", "2026-09-14", "2026-09-16"])

    def test_planned_reads_the_approximate_header(self):
        workload = gamify.build_workload(self.ROWS, self.CFG)
        by_date = {w["date"]: w for w in workload}
        self.assertEqual(by_date["2026-09-14"]["planned"], 4.0)

    def test_done_is_the_struck_rows_priced_sum_and_built_covers_all_rows(self):
        workload = gamify.build_workload(self.ROWS, self.CFG)
        by_date = {w["date"]: w for w in workload}
        aug10 = by_date["2026-08-10"]
        self.assertAlmostEqual(aug10["done"], 1.4)     # 502: 🟡 Easy = 2.0 * 0.7
        self.assertAlmostEqual(aug10["built"], 4.4)    # + 501: 🔴 Medium = 3.0 * 1.0
        self.assertGreaterEqual(aug10["built"], aug10["done"])
        sep16 = by_date["2026-09-16"]
        self.assertAlmostEqual(sep16["done"], 1.5)     # 503: 🟢 s1 Hard = 1.0 * 1.5
        self.assertAlmostEqual(sep16["built"], 3.5)    # + 504: 🟡 Medium = 2.0 * 1.0
        self.assertGreaterEqual(sep16["built"], sep16["done"])

    def test_pre_era_headerless_file_contributes_no_entries(self):
        workload = gamify.build_workload(self.ROWS, self.CFG)
        self.assertFalse(any(w["date"].startswith("2026-06") for w in workload))
        self.assertEqual(len(workload), 4)

    def test_partial_true_for_a_numberless_primer_row(self):
        workload = gamify.build_workload(self.ROWS, self.CFG)
        by_date = {w["date"]: w for w in workload}
        self.assertTrue(by_date["2026-08-13"]["partial"])
        self.assertFalse(by_date["2026-08-10"]["partial"])

    def test_price_day_items_splits_done_from_remaining_on_a_two_row_day(self):
        path = eb.SCHEDULES / "20260810_schedule.md"
        items, stated = eb.parse_schedule_day(path, dt.date(2026, 8, 10))
        priced = eb.price_day_items(dt.date(2026, 8, 10), items, self.ROWS, self.CFG)
        self.assertEqual(stated, 5.0)
        self.assertAlmostEqual(priced["done"], 1.4)
        self.assertAlmostEqual(priced["remaining"], 3.0)
        self.assertAlmostEqual(priced["built"], 4.4)


class SolutionFilesTests(unittest.TestCase):
    """links.solution_files() — the map gamify reads: keyed by the file's leading number,
    non-numbered files skipped, roots walked in config order and sorted within each root
    (so a twin's first path is the same one links.find_file returns)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root_a = Path(self._tmp.name) / "a"
        root_b = Path(self._tmp.name) / "b"
        for rel in ("graphs/200_islands.py", "trees/100_same_tree.py", "trees/notes.py",
                    "z_late/1216_twin.py"):
            (root_a / rel).parent.mkdir(parents=True, exist_ok=True)
            (root_a / rel).write_text("", encoding="utf-8")
        (root_b / "dp").mkdir(parents=True)
        (root_b / "dp/1216_twin.py").write_text("", encoding="utf-8")
        self._patches = [
            mock.patch.object(links, "source_roots", return_value=[root_a, root_b]),
            # find_file's twin warning prints paths relative to the repo root; point it at
            # the temp tree so the fixture roots are inside it.
            mock.patch.object(links, "REPO_ROOT", Path(self._tmp.name)),
        ]
        for patch in self._patches:
            patch.start()
        self.root_a, self.root_b = root_a, root_b

    def tearDown(self):
        for patch in self._patches:
            patch.stop()
        self._tmp.cleanup()

    def test_keys_by_leading_number_and_skips_unnumbered_files(self):
        files = links.solution_files()
        self.assertEqual(sorted(files), [100, 200, 1216])
        self.assertEqual(files[100], [self.root_a / "trees/100_same_tree.py"])

    def test_twin_order_is_config_root_order_and_matches_find_file(self):
        files = links.solution_files()
        self.assertEqual(files[1216], [self.root_a / "z_late/1216_twin.py",
                                       self.root_b / "dp/1216_twin.py"])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(links.find_file("1216"), files[1216][0])


class SolutionPathTests(unittest.TestCase):
    """solution_path()/build_problems() — the `file` field: a repo-relative POSIX path from
    the links.solution_files() map, null when absent, and a twin (two files for one number,
    e.g. 1216) takes the FIRST sorted path with exactly one warning per number."""

    FILES = {763: [gamify.REPO / "dsa/leetcode/greedy/763_partition_labels.py"],
             1216: [gamify.REPO / "dsa/leetcode/1d_dynamic_programming/1216_valid_palindrome_iii.py",
                    gamify.REPO / "dsa/leetcode/backtracking/1216_valid_palindrome_iii.py"]}

    def test_path_is_repo_relative_posix(self):
        self.assertEqual(gamify.solution_path(763, self.FILES),
                         "dsa/leetcode/greedy/763_partition_labels.py")

    def test_missing_file_is_none_and_warns_nothing(self):
        warnings: list[str] = []
        self.assertIsNone(gamify.solution_path(999, self.FILES, warnings))
        self.assertEqual(warnings, [])

    def test_twin_takes_first_and_warns_once(self):
        warnings: list[str] = []
        self.assertEqual(gamify.solution_path(1216, self.FILES, warnings),
                         "dsa/leetcode/1d_dynamic_programming/1216_valid_palindrome_iii.py")
        self.assertEqual(len(warnings), 1)
        self.assertIn("1216", warnings[0])
        self.assertIn("2 solution files", warnings[0])

    def test_build_problems_emits_file_and_one_twin_warning_per_number(self):
        rows = [_row(763, "🟡", 0, reps="2026-09-19"),
                _row(1216, "🟡", 0, reps="2026-09-19"),      # twin, two tracker rows
                _row(1216, "🔴", 0, reps="2026-09-19"),
                _row(999, "🟢", 1, reps="2026-09-19")]        # no file
        warnings: list[str] = []
        problems = gamify.build_problems(rows, {}, {}, {}, self.FILES, warnings)
        by_num = {}
        for p in problems:
            by_num.setdefault(p["lcNumber"], []).append(p["file"])
        self.assertEqual(by_num[763], ["dsa/leetcode/greedy/763_partition_labels.py"])
        self.assertEqual(by_num[1216],
                         ["dsa/leetcode/1d_dynamic_programming/1216_valid_palindrome_iii.py"] * 2)
        self.assertEqual(by_num[999], [None])
        self.assertEqual(len(warnings), 1)                    # once per NUMBER, not per row

    def test_build_problems_without_a_files_map_is_all_null(self):
        problems = gamify.build_problems([_row(763, "🟡", 0, reps="2026-09-19")], {}, {}, {})
        self.assertIsNone(problems[0]["file"])


class ScheduleItemOutcomeTests(unittest.TestCase):
    """_schedule_item_outcome(end_cell, next_cell) — pure, no file IO. Pins the real E-cell
    vocabulary (s0/s1/s2/prov/dropped) seen across every week since the Aug 17 format, and
    the glyph-less cells (unrated/—/✅ delivered/empty) that must yield three nulls."""

    def test_glyph_with_streak_note_and_a_full_next_date(self):
        self.assertEqual(gamify._schedule_item_outcome("🟢 s2", "2026-10-21"),
                          {"endComfort": "🟢", "endNote": "s2", "nextReview": "2026-10-21"})

    def test_glyph_with_prov_note_and_no_next_date(self):
        self.assertEqual(gamify._schedule_item_outcome("🟢 prov", ""),
                          {"endComfort": "🟢", "endNote": "prov", "nextReview": None})

    def test_bare_glyph_with_a_next_date(self):
        self.assertEqual(gamify._schedule_item_outcome("🟡", "2026-09-30"),
                          {"endComfort": "🟡", "endNote": None, "nextReview": "2026-09-30"})

    def test_arrow_prefixed_note_is_stripped_to_dropped(self):
        self.assertEqual(gamify._schedule_item_outcome("🟡→dropped", ""),
                          {"endComfort": "🟡", "endNote": "dropped", "nextReview": None})

    def test_unrated_has_no_glyph_so_everything_is_null(self):
        self.assertEqual(gamify._schedule_item_outcome("unrated", ""),
                          {"endComfort": None, "endNote": None, "nextReview": None})

    def test_em_dash_has_no_glyph_so_everything_is_null(self):
        self.assertEqual(gamify._schedule_item_outcome("—", ""),
                          {"endComfort": None, "endNote": None, "nextReview": None})

    def test_checkmark_delivered_has_no_glyph_so_everything_is_null(self):
        self.assertEqual(gamify._schedule_item_outcome("✅ delivered", ""),
                          {"endComfort": None, "endNote": None, "nextReview": None})

    def test_both_cells_empty_is_all_null(self):
        self.assertEqual(gamify._schedule_item_outcome("", ""),
                          {"endComfort": None, "endNote": None, "nextReview": None})

    def test_free_form_next_cell_does_not_full_match_a_date(self):
        self.assertEqual(gamify._schedule_item_outcome("🟢", "Sep 14 phase"),
                          {"endComfort": "🟢", "endNote": None, "nextReview": None})

    def test_note_whitespace_collapsed_and_lowercased(self):
        self.assertEqual(gamify._schedule_item_outcome(" 🟢  S1 ", ""),
                          {"endComfort": "🟢", "endNote": "s1", "nextReview": None})


class ScanWeekEndGlyphFallbackTests(unittest.TestCase):
    """_scan_week still falls back to the Start glyph when the End cell is empty — guards
    the _end_glyph refactor. Only the board slice (_schedule_item_outcome, above) refuses
    that fallback; the comfort timeline still wants SOME glyph recorded per rep."""

    def test_falls_back_to_start_glyph_when_end_cell_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "20260921_schedule.md"
            path.write_text(
                "## Daily Schedule\n\n"
                "| Problem | S | E | Next | Technique |\n"
                "|---|:-:|:-:|:-:|---|\n"
                "| ▸ **Mon Sep 21** · 6.8 units — Test day |  |  |  |  |\n"
                "| [22 Generate Parentheses](../../../dsa/leetcode/backtracking/22_x.py)"
                " | 🔴 | | | Backtracking |\n",
                encoding="utf-8",
            )
            index: dict[str, dict[int, str]] = {}
            gamify._scan_week(path, dt.date(2026, 9, 21), index)
            self.assertEqual(index, {"2026-09-21": {22: "🔴"}})


class ParseProbesTests(unittest.TestCase):
    """parse_probes() against a small fixture Probe log table, not the live repo file —
    pins the Problem-cell number/title split and (the tricky case) a MULTI-glyph Result
    cell (`🔴 → 🟡 (re-rep Sep 16)`), which must score the COLD call (the first glyph), not
    the eventual conversion."""

    FIXTURE = (
        "## 📒 Probe log — the tally\n\n"
        "Some prose above the table.\n\n"
        "| # | Date | Problem | Technique | Result | Tracker row? |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | 2026-08-10 | 977 Squares of a Sorted Array | Two Pointers | 🟢 | — |\n"
        "| 2 | 2026-08-11 | 202 Happy Number | Cycle Detection (iterated seq) | 🟡 | ✅ earned |\n"
        "| 3 | 2026-09-11 | 547 Number of Provinces | Union-Find (connected components) "
        "| 🔴 → 🟡 (re-rep Sep 16) | earned Sep 11 → **dropped Sep 16** |\n\n"
        "**Tally (3 run):** some prose that must not be parsed as a row.\n\n"
        "## 🎣 Queued probe candidates\n\n"
        "unrelated section\n"
    )

    def setUp(self):
        self._orig_probes = gamify.PROBES_README
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(self.FIXTURE)
        tmp.close()
        gamify.PROBES_README = Path(tmp.name)

    def tearDown(self):
        gamify.PROBES_README.unlink(missing_ok=True)
        gamify.PROBES_README = self._orig_probes

    # Joined by lcNumber into the items below — only 977 has a URL, pinning the honest-null
    # case for a probe number the tracker doesn't carry a link for.
    URLS = {977: "https://leetcode.com/problems/squares-of-a-sorted-array/"}

    def test_problem_cell_splits_into_number_and_title(self):
        probes = gamify.parse_probes(self.URLS)
        first = probes["items"][0]
        self.assertEqual(first["lcNumber"], 977)
        self.assertEqual(first["title"], "Squares of a Sorted Array")
        self.assertEqual(first["technique"], "Two Pointers")
        self.assertEqual(first["date"], "2026-08-10")
        self.assertEqual(first["url"], "https://leetcode.com/problems/squares-of-a-sorted-array/")

    def test_multi_glyph_result_scores_the_cold_call_not_the_conversion(self):
        probes = gamify.parse_probes(self.URLS)
        converted = probes["items"][2]
        self.assertEqual(converted["lcNumber"], 547)
        self.assertEqual(converted["result"], "🔴")  # NOT 🟡 — that's the later conversion
        self.assertIsNone(converted["url"])  # absent from URLS — honest null, not a guess

    def test_total_and_clean_rate(self):
        probes = gamify.parse_probes(self.URLS)
        self.assertEqual(probes["total"], 3)
        # 1 of 3 clean (977 is 🟢; 202 is 🟡; 547's COLD call is 🔴).
        self.assertAlmostEqual(probes["cleanRate"], 1 / 3)

    def test_prose_and_next_section_are_not_parsed_as_rows(self):
        probes = gamify.parse_probes(self.URLS)
        self.assertEqual(len(probes["items"]), 3)

    def test_missing_file_is_none(self):
        gamify.PROBES_README = Path(tempfile.gettempdir()) / "no-such-probes-file.md"
        self.assertIsNone(gamify.parse_probes(self.URLS))

    def test_no_table_in_file_is_none(self):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("# Nothing here\n\nJust prose, no Probe log heading at all.\n")
        tmp.close()
        gamify.PROBES_README = Path(tmp.name)
        self.assertIsNone(gamify.parse_probes(self.URLS))
        gamify.PROBES_README.unlink(missing_ok=True)

    # An empty PROBE-log table — the section and its header row exist, but no data rows
    # yet — is a fresh adopter's first-run state, not a defect: it must NOT collapse to
    # the same None the missing-file/missing-section cases above return.
    EMPTY_TABLE_FIXTURE = (
        "## 📒 Probe log — the tally\n\n"
        "| # | Date | Problem | Technique | Result | Tracker row? |\n"
        "|---|---|---|---|---|---|\n"
    )

    def test_present_but_empty_table_is_zero_payload_not_none(self):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(self.EMPTY_TABLE_FIXTURE)
        tmp.close()
        gamify.PROBES_README = Path(tmp.name)
        self.assertEqual(gamify.parse_probes(self.URLS),
                         {"total": 0, "cleanRate": 0.0, "items": []})
        gamify.PROBES_README.unlink(missing_ok=True)

    def test_present_but_empty_table_emits_no_warning(self):
        # Runs the real build_payload() (live repo tracker/schedule/coverage, per the
        # style of PayloadTests) with only PROBES_README swapped, so this exercises the
        # actual warnings-list wiring in main()/build_payload, not just parse_probes().
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(self.EMPTY_TABLE_FIXTURE)
        tmp.close()
        gamify.PROBES_README = Path(tmp.name)
        _payload, warnings = gamify.build_payload(dt.date(2026, 9, 20))
        self.assertFalse(any("Probe log" in w for w in warnings))
        gamify.PROBES_README.unlink(missing_ok=True)

    def test_missing_probe_section_still_warns_from_build_payload(self):
        # The genuinely-wrong case (section header missing entirely) must still warn —
        # confirms the fix didn't silence a real problem along with the false-positive one.
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("# Nothing here\n\nJust prose, no Probe log heading at all.\n")
        tmp.close()
        gamify.PROBES_README = Path(tmp.name)
        _payload, warnings = gamify.build_payload(dt.date(2026, 9, 20))
        self.assertTrue(any("Probe log" in w for w in warnings))
        gamify.PROBES_README.unlink(missing_ok=True)


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
            "techniques": [
                {"name": "Bellman-Ford", "family": "advanced_graphs", "tier": "core",
                 "started": True, "minProblems": 3, "problemCount": 1, "problems": [787],
                 "bestComfort": "🟢", "hasGreen": True, "thin": True, "hasVariantGap": False},
                {"name": "Knapsack", "family": "dynamic_programming", "tier": "dp",
                 "started": False, "minProblems": 3, "problemCount": 0, "problems": [],
                 "bestComfort": None, "hasGreen": False, "thin": False, "hasVariantGap": False},
            ],
            # One date far outside the summary's rolling window (well over
            # SUMMARY_STUDY_DAYS_WINDOW days before generatedAt) plus two recent ones —
            # exercises the cap in summary_of() without touching the lifetime count, which
            # comes from streak.studyDays (10 above), never from len(this list).
            "studyDays": ["2025-01-01", "2026-09-19", "2026-09-20"],
            "schedule": {"weekOf": "2026-09-21", "days": [
                {"date": "2026-09-21", "weekday": "Monday", "label": "Test day", "units": 6.8,
                 "items": [{"lcNumber": 22, "title": "Generate Parentheses",
                           "technique": "Backtracking", "startComfort": "🔴",
                           "difficulty": "Medium", "done": False}]},
            ]},
            # Mirrors studyDays just above: one date far outside the summary's rolling
            # window plus two recent ones, so the cap can be pinned the same way.
            "workload": [
                {"date": "2025-01-01", "planned": 4.0, "done": 4.0, "built": 4.0, "partial": False},
                {"date": "2026-09-19", "planned": 5.0, "done": 5.0, "built": 5.0, "partial": False},
                {"date": "2026-09-20", "planned": 6.0, "done": 3.0, "built": 6.0, "partial": True},
            ],
            "effortCeiling": 8.0,
            "effortFloor": 3.0,
            "probes": {"total": 3, "cleanRate": 1 / 3, "items": [
                {"date": "2026-08-10", "lcNumber": 977, "title": "Squares of a Sorted Array",
                 "technique": "Two Pointers", "result": "🟢"},
            ]},
            "problems": [{"lcNumber": 206, "title": "Reverse Linked List", "comfort": "🎓"}],
        }

    def test_no_problems_key(self):
        summary = gamify.summary_of(self._payload())
        self.assertNotIn("problems", summary)

    def test_keeps_core_aggregates(self):
        summary = gamify.summary_of(self._payload())
        for key in ("streak", "pipeline", "badges", "coverage", "totals",
                    "onSchedule", "difficulty", "schemaVersion", "generatedAt",
                    "techniques", "studyDays", "schedule", "workload", "effortCeiling",
                    "effortFloor", "probes"):
            self.assertIn(key, summary)
        self.assertEqual(summary["streak"]["current"], 3)
        self.assertEqual(summary["badges"][0]["id"], "first-graduate")

    def test_techniques_pass_through_unchanged_incl_tier_started_and_min_problems(self):
        summary = gamify.summary_of(self._payload())
        by_name = {t["name"]: t for t in summary["techniques"]}
        self.assertEqual(by_name["Bellman-Ford"]["tier"], "core")
        self.assertTrue(by_name["Bellman-Ford"]["started"])
        self.assertEqual(by_name["Bellman-Ford"]["minProblems"], 3)
        self.assertEqual(by_name["Knapsack"]["tier"], "dp")
        self.assertFalse(by_name["Knapsack"]["started"])
        self.assertEqual(by_name["Knapsack"]["minProblems"], 3)

    def test_probes_pass_through_unchanged(self):
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["probes"], self._payload()["probes"])
        self.assertAlmostEqual(summary["probes"]["cleanRate"], 1 / 3)

    def test_probes_none_when_no_probe_log(self):
        payload = self._payload()
        payload["probes"] = None
        summary = gamify.summary_of(payload)
        self.assertIsNone(summary["probes"])

    def test_schedule_passes_through_unchanged_and_no_problems_leak(self):
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["schedule"], self._payload()["schedule"])
        self.assertNotIn("problems", summary)

    def test_effort_ceiling_and_floor_pass_through(self):
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["effortCeiling"], 8.0)
        self.assertEqual(summary["effortFloor"], 3.0)

    def test_schedule_none_when_no_current_week_file(self):
        payload = self._payload()
        payload["schedule"] = None
        summary = gamify.summary_of(payload)
        self.assertIsNone(summary["schedule"])

    def test_study_days_capped_to_the_rolling_window(self):
        # 2025-01-01 is far more than SUMMARY_STUDY_DAYS_WINDOW days before generatedAt
        # (2026-09-20) and must be dropped; the two recent dates stay.
        summary = gamify.summary_of(self._payload())
        self.assertEqual(summary["studyDays"], ["2026-09-19", "2026-09-20"])

    def test_workload_capped_to_the_same_rolling_window_as_study_days(self):
        # Same cutoff, same shape of fixture as studyDays above: 2025-01-01 drops,
        # the two recent entries stay.
        summary = gamify.summary_of(self._payload())
        self.assertEqual([w["date"] for w in summary["workload"]],
                         ["2026-09-19", "2026-09-20"])

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

    def test_build_payload_honours_injected_today(self):
        # generatedAt must come from the injected `today`, not the wall clock — this is
        # what makes main()'s session_date resolution (see below) actually take effect
        # rather than being overridden again inside build_payload.
        payload, _warnings = gamify.build_payload(dt.date(2026, 9, 20))
        self.assertEqual(payload["generatedAt"], "2026-09-20")

    def test_every_technique_row_carries_builds_on_and_graduated_count(self):
        # Runs against the live techniques.yml + tracker — this is what actually proves
        # the authored builds_on list in techniques.yml got through gamify, not just that
        # the two keys exist somewhere.
        payload, warnings = gamify.build_payload(dt.date(2026, 9, 20))
        self.assertEqual(warnings, [])
        techs = payload["techniques"]
        self.assertTrue(techs)
        for row in techs:
            self.assertIn("buildsOn", row)
            self.assertIn("graduatedCount", row)
            self.assertIsInstance(row["buildsOn"], list)
            self.assertGreaterEqual(row["graduatedCount"], 0)

    def test_every_builds_on_name_resolves_to_a_live_technique_row(self):
        payload, _warnings = gamify.build_payload(dt.date(2026, 9, 20))
        techs = payload["techniques"]
        names = {t["name"] for t in techs}
        for row in techs:
            for dep in row["buildsOn"]:
                self.assertIn(dep, names)

    def test_live_builds_on_row_count_matches_the_authored_yaml(self):
        # Proves the authored builds_on list in techniques.yml actually reached every
        # row it named — a join that silently dropped rows would still pass the two
        # checks above (both only test the keys/edges that DID come through).
        payload, _warnings = gamify.build_payload(dt.date(2026, 9, 20))
        techs = payload["techniques"]
        yaml_entries = gamify.load_technique_entries([])
        expected = sum(1 for e in yaml_entries if e.get("builds_on"))
        actual = sum(1 for t in techs if t["buildsOn"])
        self.assertEqual(actual, expected)


class MainStdoutCleanTests(unittest.TestCase):
    """main()'s session-date resolution must never leak session_date.resolve_datetime's
    announcement onto stdout: --stdout must still emit parseable JSON and --banner must
    still emit exactly one line. The real detect_session_date heuristic depends on the
    wall clock and git state, so the announcement is FORCED here via a monkeypatched
    resolve_datetime rather than relying on hitting the real heuristic by chance."""

    @staticmethod
    def _announcing_resolve_datetime(explicit=None, *, now=None, announce=True):
        if announce:
            print("Using session date 2026-09-20 (forced for test). "
                  "Override with --date if that's wrong.")
        return dt.datetime(2026, 9, 20)

    def _run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
             mock.patch.object(gamify.session_date, "resolve_datetime",
                               self._announcing_resolve_datetime), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            gamify.main()
        return out.getvalue(), err.getvalue()

    def test_stdout_mode_stays_parseable_json_even_when_session_date_announces(self):
        out, err = self._run_main(["gamify.py", "--stdout"])
        json.loads(out)  # raises if the announcement leaked into stdout
        self.assertIn("Using session date", err)

    def test_banner_mode_emits_exactly_one_line_even_when_session_date_announces(self):
        out, err = self._run_main(["gamify.py", "--banner"])
        self.assertEqual(len(out.splitlines()), 1)
        self.assertIn("Using session date", err)


class MainDateFlagTests(unittest.TestCase):
    """--date is the flag name main() actually documents and session_date.resolve_datetime
    itself references in its announcement ("Override with --date if that's wrong") —
    --today is kept only as a hidden alias so an existing caller of the old name still
    works. Both must reach resolve_datetime's `explicit` param identically."""

    def _captured_explicit(self, argv):
        captured: dict = {}

        def fake_resolve(explicit=None, *, now=None, announce=True):
            captured["explicit"] = explicit
            return dt.datetime(2026, 9, 20)

        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
             mock.patch.object(gamify.session_date, "resolve_datetime", fake_resolve), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            gamify.main()
        return captured["explicit"]

    def test_date_flag_reaches_resolve_datetime(self):
        explicit = self._captured_explicit(["gamify.py", "--stdout", "--date", "2026-09-20"])
        self.assertEqual(explicit, "2026-09-20")

    def test_today_alias_resolves_to_the_same_value_as_date(self):
        explicit = self._captured_explicit(["gamify.py", "--stdout", "--today", "2026-09-20"])
        self.assertEqual(explicit, "2026-09-20")


if __name__ == "__main__":
    unittest.main(verbosity=2)
