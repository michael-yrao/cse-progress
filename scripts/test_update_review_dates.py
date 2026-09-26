"""Tests for update_review_dates.py's extract_url_from_source() and its use in
discover_source_problems() — the auto-row URL for a newly-discovered solution file.

Stdlib unittest, same style as test_gamify.py / test_remaining.py. Temp files only,
never the real repo tree:

    python scripts/test_update_review_dates.py

Importing update_review_dates has one cwd-relative side effect worth naming rather than
working around: module load runs `CONFIG = load_config()`, which reads `cse.config.yml`
relative to the current working directory (real values when run from the repo root, the
built-in DEFAULT_CONFIG otherwise) and `_console.force_utf8()` (idempotent, reconfigures
stdout/stderr encoding). Neither touches a fixture or mutates anything on disk, so it is
left as-is rather than patched around.
"""
from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

import update_review_dates as uprd


class ExtractUrlFromSourceTests(unittest.TestCase):
    """extract_url_from_source() reads the header's own URL, scanning only the first
    docstring block — same scope as extract_difficulty_from_source()."""

    def _write(self, body: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8")
        tmp.write(body)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_header_with_kattis_url(self):
        path = self._write(
            '"""\n'
            "9001. Single Source Shortest Path, Negative Weights   ·   "
            "https://open.kattis.com/problems/shortestpath3\n"
            'Pattern: graphs\n'
            '"""\n'
            "class Solution:\n    pass\n"
        )
        self.assertEqual(
            uprd.extract_url_from_source(path),
            "https://open.kattis.com/problems/shortestpath3",
        )

    def test_header_with_no_url_returns_none(self):
        path = self._write(
            '"""\n'
            "39. Combination Sum\n"
            'Pattern: backtracking\n'
            '"""\n'
            "class Solution:\n    pass\n"
        )
        self.assertIsNone(uprd.extract_url_from_source(path))


class DiscoverSourceProblemsUrlTests(unittest.TestCase):
    """discover_source_problems() uses the header URL for the auto-row when one is
    present, and falls back to the LeetCode-slug URL only when it is absent — the
    behavior that was hard-coded to the LeetCode fallback before this change."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.root = Path(self._tmpdir.name)
        # session_now() shells out to git for the *live-session* heuristic — irrelevant
        # to what's under test (the URL field) and unnecessary to exercise here.
        self._session_now_patch = mock.patch.object(
            uprd, "session_now", return_value=datetime(2026, 9, 26))
        self._session_now_patch.start()
        self.addCleanup(self._session_now_patch.stop)
        # Isolate from whatever discovery_skip the real cse.config.yml carries.
        self._skip_patch = mock.patch.object(uprd, "DISCOVERY_SKIP_NUMBERS", set())
        self._skip_patch.start()
        self.addCleanup(self._skip_patch.stop)

    def _write(self, filename: str, body: str) -> Path:
        path = self.root / filename
        path.write_text(body, encoding="utf-8")
        return path

    def test_kattis_header_url_is_used(self):
        path = self._write(
            "9001_single_source_shortest_path_negative_weights.py",
            '"""\n'
            "9001. Single Source Shortest Path, Negative Weights   ·   "
            "https://open.kattis.com/problems/shortestpath3\n"
            'Pattern: graphs\n'
            '"""\n'
            "class Solution:\n    pass\n",
        )
        rows = uprd.discover_source_problems(set(), staged_files=[path])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["url"], "https://open.kattis.com/problems/shortestpath3")

    def test_no_header_url_falls_back_to_leetcode_slug(self):
        path = self._write(
            "39_combination_sum.py",
            '"""\n'
            "39. Combination Sum\n"
            'Pattern: backtracking\n'
            '"""\n'
            "class Solution:\n    pass\n",
        )
        rows = uprd.discover_source_problems(set(), staged_files=[path])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["url"], "https://leetcode.com/problems/combination-sum/")


if __name__ == "__main__":
    unittest.main(verbosity=2)
