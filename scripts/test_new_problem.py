"""Tests for new_problem.py's premium-problem link resolver (decision
`problem-link-order-sep27`: LeetCode -> NeetCode -> HelloInterview -> LeetCode paywalled).

Stdlib unittest, same fixture style as test_links.py: mock.patch.object over the module's
own path constants, with a tempfile-backed neetcode.yml/hellointerview.yml — never the
live repo files, never the network.

    python scripts/test_new_problem.py
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import new_problem


class LoadHelloInterviewMapTests(unittest.TestCase):
    """load_hellointerview_map(): valid entries, a missing file, and a malformed entry."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write_map(self, text: str) -> Path:
        p = self.tmp_path / "hellointerview.yml"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_valid_entries(self):
        p = self._write_map(
            "problems:\n"
            "  - {leetcode_slug: meeting-rooms, "
            "path: /learn/code/intervals/can-attend-meetings}\n"
        )
        with mock.patch.object(new_problem, "HELLOINTERVIEW_MAP_PATH", p):
            result = new_problem.load_hellointerview_map()
        self.assertEqual(
            result, {"meeting-rooms": "/learn/code/intervals/can-attend-meetings"})

    def test_missing_file_returns_empty_map_no_exception(self):
        missing = self.tmp_path / "no_such_file.yml"
        with mock.patch.object(new_problem, "HELLOINTERVIEW_MAP_PATH", missing):
            result = new_problem.load_hellointerview_map()  # must not raise
        self.assertEqual(result, {})

    def test_ignores_malformed_entry(self):
        p = self._write_map(
            "problems:\n"
            "  - {leetcode_slug: meeting-rooms, "
            "path: /learn/code/intervals/can-attend-meetings}\n"
            "  - {leetcode_slug: no-path-here}\n"
            "  - {path: /learn/code/no-slug-here}\n"
            "  - just-a-string\n"
        )
        with mock.patch.object(new_problem, "HELLOINTERVIEW_MAP_PATH", p):
            result = new_problem.load_hellointerview_map()
        self.assertEqual(
            result, {"meeting-rooms": "/learn/code/intervals/can-attend-meetings"})


class LoadNeetcodeSlugsTests(unittest.TestCase):
    """load_neetcode_slugs(): valid entries, a missing file (-> None, UNKNOWN), a
    readable-but-empty file (-> empty frozenset), and a malformed entry."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write_map(self, text: str) -> Path:
        p = self.tmp_path / "neetcode.yml"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_valid_entries(self):
        p = self._write_map(
            "problems:\n"
            "  - {leetcode_slug: two-sum, number: 1, premium: false}\n"
            "  - {leetcode_slug: meeting-rooms, number: 252, premium: true}\n"
        )
        with mock.patch.object(new_problem, "NEETCODE_MAP_PATH", p):
            result = new_problem.load_neetcode_slugs()
        self.assertEqual(result, frozenset({"two-sum", "meeting-rooms"}))

    def test_missing_file_returns_none_not_empty_set(self):
        missing = self.tmp_path / "no_such_file.yml"
        with mock.patch.object(new_problem, "NEETCODE_MAP_PATH", missing):
            result = new_problem.load_neetcode_slugs()  # must not raise
        self.assertIsNone(result)

    def test_readable_but_empty_returns_empty_frozenset(self):
        p = self._write_map("problems: []\n")
        with mock.patch.object(new_problem, "NEETCODE_MAP_PATH", p):
            result = new_problem.load_neetcode_slugs()
        self.assertEqual(result, frozenset())
        self.assertIsNotNone(result)

    def test_ignores_malformed_entry(self):
        p = self._write_map(
            "problems:\n"
            "  - {leetcode_slug: two-sum, number: 1, premium: false}\n"
            "  - {number: 999, premium: false}\n"
            "  - just-a-string\n"
        )
        with mock.patch.object(new_problem, "NEETCODE_MAP_PATH", p):
            result = new_problem.load_neetcode_slugs()
        self.assertEqual(result, frozenset({"two-sum"}))


class ResolvePremiumLinkTests(unittest.TestCase):
    """resolve_premium_link(): the four-step order (NeetCode -> HelloInterview ->
    LeetCode), and the None-vs-empty NeetCode-list distinction."""

    HI_MAP = {"meeting-rooms": "/learn/code/intervals/can-attend-meetings"}

    def test_neetcode_wins_even_when_also_in_hellointerview_map(self):
        # The order test: meeting-rooms sits in BOTH maps; NeetCode must win.
        link = new_problem.resolve_premium_link(
            "meeting-rooms", frozenset({"meeting-rooms"}), self.HI_MAP)
        self.assertEqual(link.url, "https://neetcode.io/problems/meeting-rooms")
        self.assertEqual(link.judge, "NeetCode")

    def test_neetcode_url_honors_neetcode_renames(self):
        # alien-dictionary -> foreign-dictionary is a real NEETCODE_RENAMES entry.
        link = new_problem.resolve_premium_link(
            "alien-dictionary", frozenset({"alien-dictionary"}), {})
        self.assertEqual(link.url, "https://neetcode.io/problems/foreign-dictionary")
        self.assertEqual(link.judge, "NeetCode")

    def test_hellointerview_wins_when_only_there(self):
        link = new_problem.resolve_premium_link("meeting-rooms", frozenset(), self.HI_MAP)
        self.assertEqual(
            link.url,
            "https://www.hellointerview.com/learn/code/intervals/can-attend-meetings",
        )
        self.assertEqual(link.judge, "HelloInterview")

    def test_leetcode_fallback_when_in_neither(self):
        link = new_problem.resolve_premium_link("some-other-problem", frozenset(), {})
        self.assertEqual(link.url, "https://leetcode.com/problems/some-other-problem/")
        self.assertEqual(link.judge, "LeetCode")
        self.assertIn("neither NeetCode nor HelloInterview", link.reason)

    def test_unreadable_neetcode_list_falls_back_to_neetcode_mirror_unverified(self):
        # None (unreadable/unknown), not an empty set, must NOT fall through to
        # HelloInterview even though it has the slug — an unknown list is not an
        # absent one.
        link = new_problem.resolve_premium_link("meeting-rooms", None, self.HI_MAP)
        self.assertEqual(link.url, "https://neetcode.io/problems/meeting-rooms")
        self.assertEqual(link.judge, "NeetCode")
        self.assertIn("unverified", link.reason)

    def test_readable_empty_neetcode_list_falls_through_to_hellointerview(self):
        # An empty-but-READABLE list is a real "NeetCode does not list it" answer, so
        # it falls through normally (unlike the None/unreadable case above).
        link = new_problem.resolve_premium_link("meeting-rooms", frozenset(), self.HI_MAP)
        self.assertEqual(link.judge, "HelloInterview")

    def test_reason_names_the_same_judge_as_the_url_host(self):
        cases = [
            new_problem.resolve_premium_link("meeting-rooms", frozenset({"meeting-rooms"}), {}),
            new_problem.resolve_premium_link("meeting-rooms", frozenset(), self.HI_MAP),
            new_problem.resolve_premium_link("some-other-problem", frozenset(), {}),
            new_problem.resolve_premium_link("meeting-rooms", None, {}),
        ]
        for link in cases:
            with self.subTest(url=link.url):
                self.assertIn(link.judge, link.reason)
                self.assertIn(link.judge.split(".")[0].lower(), link.url.lower())


class EndToEndPremiumResolutionTests(unittest.TestCase):
    """The loaders and the resolver composed, the way both premium call sites use them."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_missing_neetcode_file_falls_back_to_neetcode_mirror(self):
        missing = self.tmp_path / "absent.yml"
        with mock.patch.object(new_problem, "NEETCODE_MAP_PATH", missing):
            neetcode_slugs = new_problem.load_neetcode_slugs()  # must not raise -> None
            link = new_problem.resolve_premium_link("two-sum", neetcode_slugs, {})
        self.assertEqual(link.url, "https://neetcode.io/problems/two-sum")
        self.assertEqual(link.judge, "NeetCode")


if __name__ == "__main__":
    unittest.main(verbosity=2)
