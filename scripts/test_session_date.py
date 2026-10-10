"""Tests for session_date.resolve_datetime's --date override announcement.

Run with: python scripts/test_session_date.py
"""
from __future__ import annotations

import contextlib
import io
import os
import sys
import unittest
from datetime import datetime
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import session_date  # noqa: E402  (import after sys.path setup)

SMALL_HOURS = datetime(2026, 10, 10, 0, 40)
DAYTIME = datetime(2026, 10, 10, 14, 0)
OVERRIDE_LINE = (
    "--date 2026-10-10 overrides the detected session date 2026-10-09 "
    "(working tree is dirty — a session is in progress, so it started yesterday); "
    "the override is for a wrong detection, not for re-deciding which day has started."
)


class ResolveDatetimeOverrideTests(unittest.TestCase):
    def test_override_line_only_when_explicit_contradicts_a_reasoned_detection(self):
        cases = [
            ("explicit equals detected, small hours, dirty", "2026-10-09", SMALL_HOURS, ""),
            ("explicit differs, small hours, dirty", "2026-10-10", SMALL_HOURS, OVERRIDE_LINE),
            ("explicit differs from now, daytime", "2026-10-09", DAYTIME, ""),
        ]
        for name, explicit, now, expected in cases:
            with self.subTest(name):
                out = io.StringIO()
                with mock.patch.object(session_date, "has_uncommitted_changes", return_value=True), \
                        contextlib.redirect_stdout(out):
                    session_date.resolve_datetime(explicit, now=now)
                self.assertEqual(out.getvalue().strip(), expected)


if __name__ == "__main__":
    unittest.main()
