"""Tests for links.py — the judge-label helper and link_line's use of it.

Stdlib unittest, same style as test_gamify.py / test_remaining.py:

    python scripts/test_links.py
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import links


class JudgeLabelTests(unittest.TestCase):
    """The four named judges, plus the bare-hostname fallback for anything else."""

    def test_leetcode(self):
        self.assertEqual(links.judge_label("https://leetcode.com/problems/two-sum/"), "LC")

    def test_neetcode(self):
        self.assertEqual(links.judge_label("https://neetcode.io/problems/two-sum"), "NC")

    def test_kattis(self):
        self.assertEqual(
            links.judge_label("https://open.kattis.com/problems/shortestpath3"), "Kattis")

    def test_cses(self):
        self.assertEqual(
            links.judge_label("https://cses.fi/problemset/task/1673"), "CSES")

    def test_unknown_host_falls_back_to_hostname(self):
        self.assertEqual(
            links.judge_label("https://codeforces.com/problemset/problem/4/A"),
            "codeforces.com")

    def test_leading_www_is_stripped(self):
        # A judge fronted by "www." (unlike the four named hosts above) still reports its
        # bare hostname, not the "www." prefix.
        self.assertEqual(
            links.judge_label("https://www.spoj.com/problems/TEST/"), "spoj.com")


class LinkLineJudgeLabelTests(unittest.TestCase):
    """link_line() on a Kattis-sourced problem prints the `Kattis` label, not `LC`.

    Builds a scratch tree — `<tmp>/dsa/leetcode/graphs/9001_x.py` — and monkeypatches the
    module's repo-relative constants to point at it, so nothing here touches the real repo.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self._tmpdir.name)
        graphs_dir = self.repo_root / "dsa" / "leetcode" / "graphs"
        graphs_dir.mkdir(parents=True)
        self.solution = graphs_dir / "9001_x.py"
        self.solution.write_text(
            '"""\n'
            "9001. Single Source Shortest Path, Negative Weights   ·   "
            "https://open.kattis.com/problems/shortestpath3\n"
            'Pattern: graphs\n'
            '"""\n'
            "class Solution:\n"
            "    pass\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_kattis_problem_gets_kattis_label(self):
        with mock.patch.object(links, "REPO_ROOT", self.repo_root), \
             mock.patch.object(links, "source_roots", return_value=[self.repo_root / "dsa" / "leetcode"]), \
             mock.patch.object(links, "TRACKER", self.repo_root / "no_such_tracker.md"):
            line = links.link_line("9001")

        self.assertIsNotNone(line)
        self.assertTrue(
            line.endswith("· [Kattis](https://open.kattis.com/problems/shortestpath3)"),
            line,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
