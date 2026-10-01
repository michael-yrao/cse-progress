"""Unit tests for .claude/hooks/session_start_memory.py's DSA-mock banner.

Run with: python .claude/hooks/tests/test_session_start_memory.py
(or: python -m pytest .claude/hooks/tests -q)

Pure-function and temp-fixture tests only -- never the real cse.config.yml, mock log or
schedules.
"""
from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import session_start_memory as ssm  # noqa: E402  (import after sys.path setup)

EVERY_DAYS = 28
FIRST_DUE = dt.date(2026, 10, 11)
LAST_LOGGED = dt.date(2026, 10, 11)
SEATED_FOR_FIRST_DUE = [dt.date(2026, 10, 11)]


class DsaMockDueTests(unittest.TestCase):
    """dsa_mock_due(): fires inside the 7-day window or overdue, unless a mock row is
    already seated on a Sunday of the due week."""

    def test_banner_fires_or_stays_silent(self):
        cases = [
            # (name, today, last_logged, first_due, seated, should_fire)
            ("no log, first_due 7 days out, unseated -> fires",
             dt.date(2026, 10, 4), None, FIRST_DUE, [], True),
            ("no log, first_due 7 days out, seated -> silent",
             dt.date(2026, 10, 4), None, FIRST_DUE, SEATED_FOR_FIRST_DUE, False),
            ("last Oct 11, today Nov 1 (due Nov 8, 7 days) -> fires",
             dt.date(2026, 11, 1), LAST_LOGGED, None, [], True),
            ("last Oct 11, today Nov 15 (overdue), unseated -> fires",
             dt.date(2026, 11, 15), LAST_LOGGED, None, [], True),
            ("today Oct 20, due Nov 8 (19 days out) -> silent",
             dt.date(2026, 10, 20), LAST_LOGGED, None, [], False),
        ]
        for name, today, last, first_due, seated, should_fire in cases:
            with self.subTest(name):
                banner = ssm.dsa_mock_due(today, last, first_due, EVERY_DAYS, seated)
                self.assertEqual(banner is not None, should_fire)
                if should_fire:
                    self.assertTrue(banner.startswith("!! DSA MOCK DUE "))
                    self.assertTrue(banner.isascii())


class DsaMockBannerTests(unittest.TestCase):
    """dsa_mock_banner() is fail-soft: an unparsable log yields '', never an exception.
    The config puts first_due on `today`, so a missing/valid log WOULD fire -- the silence
    below is attributable to the bad log row alone."""

    CONFIG = "dsa_mock:\n  every_days: 28\n  first_due: 2026-11-01\n"

    def test_unparsable_log_date_returns_empty_string(self):
        cases = [
            ("empty log fires", "", True),
            ("unparsable date is fail-soft", "| 1 | 2026-13-45 | 131 | Medium | - | - | - |", False),
        ]
        for name, log_text, should_fire in cases:
            with self.subTest(name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    claude_dir = root / ".claude"
                    claude_dir.mkdir()
                    (root / "cse.config.yml").write_text(self.CONFIG, encoding="utf-8")
                    log = root / "docs" / "foundations" / "dsa" / "mocks" / "README.md"
                    log.parent.mkdir(parents=True)
                    log.write_text(log_text + "\n", encoding="utf-8")
                    banner = ssm.dsa_mock_banner(claude_dir, dt.date(2026, 11, 1))
                self.assertEqual(banner != "", should_fire)


if __name__ == "__main__":
    unittest.main(verbosity=2)
