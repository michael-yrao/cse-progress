"""Tests for .claude/hooks/kickoff_scaffold_reminder.py (kickoff vs scoped-start triggers).

Run with: python .claude/hooks/tests/test_kickoff_scaffold_reminder.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "kickoff_scaffold_reminder.py"
KICKOFF_MARK = "session KICKOFF"
SCOPED_MARK = "is starting problem"


def run_hook(prompt: str) -> str:
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": prompt}),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


class KickoffScaffoldReminderTests(unittest.TestCase):
    def test_prompt_routes_to_kickoff_scoped_or_neither(self):
        cases = [
            ("doing 332 from tomorrow", False, True, "332"),
            ("im confused, I am doing 332 right now", False, True, "332"),
            ("let's do 235", False, True, "235"),
            ("332 next", False, True, "332"),
            ("in 2 minutes I'm doing 332", False, True, "332"),
            ("what's the bug in 332", False, False, None),
            ("close monday session", False, False, None),
            ("start saturday session", True, False, None),
            ("start session, 332 first", True, False, None),
            ("it ran in 2026", False, False, None),
        ]
        for prompt, is_kickoff, is_scoped, number in cases:
            with self.subTest(prompt):
                out = run_hook(prompt)
                self.assertEqual(KICKOFF_MARK in out, is_kickoff)
                self.assertEqual(SCOPED_MARK in out, is_scoped)
                if number:
                    self.assertIn(f"starting problem {number} now", out)


if __name__ == "__main__":
    unittest.main()
