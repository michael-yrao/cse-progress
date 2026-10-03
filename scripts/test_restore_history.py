"""Tests for restore_history.py's restore_stash(): the stash goes back into its source file,
helpers above `class Solution`, prior attempts at EOF — and an OLD-format stash (no marker)
restores exactly as it always did.

Stdlib unittest, temp dirs with os.chdir only — never the real repo tree:

    python scripts/test_restore_history.py
"""
from __future__ import annotations

import ast
import os
import tempfile
import unittest
from pathlib import Path

import new_problem
import restore_history

STAMP = "20261002"
HEADER = '"""\n7. Demo Problem\n"""\nfrom typing import List\n'
HELPER = "class UF:\n    def __init__(self, n):\n        self.p = list(range(n))\n"
PRIOR = "    def find_20260901(self, n: int) -> int:\n        return n\n"
POINTER = new_problem.POINTER_PREFIX + " in x — restored at session end"


def _source(attempt_body: str) -> str:
    return (f"{HEADER}\n\nclass Solution:\n"
            f"    def find_{STAMP}(self, n: int) -> int:\n{attempt_body}\n\n{POINTER}\n")


class RestoreStashTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)
        self.source = self.tmp_path / new_problem.DEFAULT_ROOT / "demo" / "7_demo_problem.py"
        self.stash = self.tmp_path / new_problem.DEFAULT_ROOT / ".history" / "7_demo_problem.txt"
        self.source.parent.mkdir(parents=True)
        self.stash.parent.mkdir(parents=True)

    def _restore(self, source_text: str, stash_text: str) -> str | None:
        self.source.write_text(source_text, encoding="utf-8")
        self.stash.write_text(stash_text, encoding="utf-8")
        previous_cwd = Path.cwd()
        os.chdir(self.tmp_path)
        try:
            return restore_history.restore_stash(self.stash, STAMP, False, [])
        finally:
            os.chdir(previous_cwd)

    def test_restore_stash(self):
        attempted = "        return n + 1"
        new_format = f"{PRIOR}\n{new_problem.MODULE_SECTION_MARKER}\n{HELPER}"
        old_format_expected = (
            f"{HEADER}\n\nclass Solution:\n"
            f"    def find_{STAMP}(self, n: int) -> int:\n{attempted}\n\n{PRIOR}"
        )

        with self.subTest("old-format stash restores at EOF as before"):
            reason = self._restore(_source(attempted), PRIOR)
            self.assertIsNone(reason)
            self.assertEqual(self.source.read_text(encoding="utf-8"), old_format_expected)
            self.assertFalse(self.stash.exists())

        with self.subTest("new-format stash puts helpers above class Solution"):
            self.setUp()
            reason = self._restore(_source(attempted), new_format)
            restored = self.source.read_text(encoding="utf-8")
            self.assertIsNone(reason)
            self.assertIn(f"{HEADER}\n\n{HELPER}\n\nclass Solution:", restored)
            self.assertTrue(restored.endswith(f"{attempted}\n\n{PRIOR}"))
            self.assertNotIn(new_problem.MODULE_SECTION_MARKER, restored)
            self.assertNotIn(new_problem.POINTER_PREFIX, restored)
            ast.parse(restored)
            self.assertFalse(self.stash.exists())

        with self.subTest("still-empty attempt keeps source and stash untouched"):
            self.setUp()
            empty_source = _source("        pass")
            reason = self._restore(empty_source, new_format)
            self.assertIn("still empty", reason)
            self.assertEqual(self.source.read_text(encoding="utf-8"), empty_source)
            self.assertEqual(self.stash.read_text(encoding="utf-8"), new_format)


if __name__ == "__main__":
    unittest.main(verbosity=2)
