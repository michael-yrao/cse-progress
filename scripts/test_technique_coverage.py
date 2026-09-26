"""Tests for technique_coverage.py — the `queued:` key on a `problems:` spec (Sep 26, 2026).

Stdlib unittest, matching test_gamify.py's convention (no pytest in this repo). String
fixtures only: a tiny techniques.yml + a tiny dsa_progress.md, written to temp files with
the module's own path constants monkeypatched — never the live repo files. Run it with:

    python scripts/test_technique_coverage.py

Pins the `queued:` key added alongside the Prim's/Kruskal's split and the Bellman-Ford
external-judge siblings: a `problems:` spec with no matching tracker row and a `queued:`
trigger is reported as a known gap (the Gaps cell + the Action list), never silently
folded into "declared, not queued"; a `queued:` on a spec that DOES match a row is a no-op;
an unqueued unreached spec is still counted AND listed; and the rendered `## Coverage`
table still round-trips through gamify.parse_techniques() with the right `problems` list,
`thin` flag, and no false `hasVariantGap`.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import gamify
import technique_coverage as tc

TECHNIQUES_FIXTURE = """
version: 1
defaults:
  min_problems: 3
techniques:
  - name: Test Tech
    family: test_family
    problems:
      - {number: 100, queued: "ignored-trigger"}
      - {number: 200, queued: "surplus>=1"}
      - {number: 300}
"""

TRACKER_FIXTURE = (
    "| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |\n"
    "|---|---|---|---|---|---|---|\n"
    "| Medium | [100. Test Problem](https://example.com/100) | 🟢 | 1 "
    "| 2026-01-01 | 2026-01-01 | 2026-01-01 |\n"
)


class QueuedProblemTests(unittest.TestCase):
    """resolve()/render() against the fixtures above — never the live repo files.

    100 has a matching tracker row (and its own, irrelevant `queued:` key — it is matched,
    so the key is never consulted). 200 has no tracker row and a `queued:` trigger — a
    known gap. 300 has no tracker row and no `queued:` — plain "declared, not queued".
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        tmp = Path(self._tmpdir.name)
        self._techniques_path = tmp / "techniques.yml"
        self._tracker_path = tmp / "dsa_progress.md"
        self._techniques_path.write_text(TECHNIQUES_FIXTURE, encoding="utf-8")
        self._tracker_path.write_text(TRACKER_FIXTURE, encoding="utf-8")

        self._orig_techniques_yml = tc.TECHNIQUES_YML
        self._orig_tracker_md = tc.TRACKER_MD
        tc.TECHNIQUES_YML = self._techniques_path
        tc.TRACKER_MD = self._tracker_path

        self._orig_gamify_coverage = gamify.COVERAGE

    def tearDown(self):
        tc.TECHNIQUES_YML = self._orig_techniques_yml
        tc.TRACKER_MD = self._orig_tracker_md
        gamify.COVERAGE = self._orig_gamify_coverage
        self._tmpdir.cleanup()

    def _render(self) -> str:
        config = tc.yaml.safe_load(tc.TECHNIQUES_YML.read_text(encoding="utf-8"))
        rows = tc.parse_tracker(tc.TRACKER_MD)
        resolved, claimed = tc.resolve(config, rows)
        return tc.render(resolved, rows, claimed)

    def test_queued_problem_in_gaps_cell_and_action_list_not_in_problems_parens(self):
        report = self._render()
        self.assertIn("queued: 200 `surplus>=1`", report)   # Gaps cell style (bare)
        self.assertIn("queued: 200 (`surplus>=1`)", report)  # Action list style (parens)
        # The Problems cell's parenthetical carries only the MATCHED number.
        self.assertIn("1 (100)", report)
        self.assertNotIn("(100, 200)", report)
        self.assertNotIn("(200)", report)

    def test_unqueued_unreached_problem_counted_and_listed_under_declared_not_queued(self):
        report = self._render()
        self.assertIn("**Declared, not queued (1)**", report)
        self.assertIn(": 300", report)
        self.assertIn("**Queued (1)**", report)

    def test_queued_on_a_matched_spec_is_ignored_with_no_error(self):
        report = self._render()
        # 100 is matched (a tracker row exists) despite its own `queued:` key — it counts
        # as an ordinary solved problem, never as a queued gap, and the key raises nothing.
        self.assertIn("1 (100)", report)
        self.assertNotIn("ignored-trigger", report)

    def test_coverage_table_round_trips_through_gamify_parse_techniques(self):
        report = self._render()
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(report)
        tmp.close()
        gamify.COVERAGE = Path(tmp.name)
        try:
            rows = {r["name"]: r for r in gamify.parse_techniques([])}
        finally:
            Path(tmp.name).unlink(missing_ok=True)
        row = rows["Test Tech"]
        self.assertEqual(row["problems"], [100])
        self.assertEqual(row["problemCount"], 1)
        self.assertTrue(row["thin"])
        self.assertFalse(row["hasVariantGap"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
