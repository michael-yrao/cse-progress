"""Tests for effort_budget.py's row cap and unproven-overdue backstop.

    python -m pytest scripts/test_effort_budget.py -q
"""
from __future__ import annotations

import datetime as dt
import unittest

import effort_budget as eb

_CFG = eb.load_config()
_MIN_STREAK = _CFG["carry_forward_min_streak"]
_PAUSE_AT = _CFG["intake_pause_overdue_unproven"]
_TODAY = dt.date(2026, 10, 6)
_OVERDUE = "2026-10-01"


def _tracker_row(comfort: str, streak: int) -> dict:
    return {"comfort": comfort, "streak": streak, "due": _OVERDUE}


class CountRowsTests(unittest.TestCase):
    def test_counts_every_row_but_complexity_and_separators(self):
        lines = [
            "| [5 A](x.py) · [LC](y) | 🟢 s2 | | | Greedy |",
            "| ~~[6 B](x.py) · [LC](y)~~ | 🟢 s2 | 🟢 | 2026-12-01 | Greedy |",
            "| 4 cold complexity probes | 🎯 | | | Complexity |",
            "|---|:-:|:-:|:-:|---|",
            "| → [7 C](x.py) · [LC](y) | 🟢 s2 | | 2026-12-01 | Greedy |",
        ]
        cases = [
            ("plain row counts", lines[:1], 1),
            ("struck row counts", lines[1:2], 1),
            ("complexity row does not", lines[2:3], 0),
            ("separator does not", lines[3:4], 0),
            ("moved row does not", lines[4:], 0),
            ("all together", lines, 2),
        ]
        for name, block, expected in cases:
            with self.subTest(name):
                items = [it for it in map(eb.parse_sched_line, block) if it is not None]
                self.assertEqual(eb.count_rows(items), expected)


class IsUnprovenTests(unittest.TestCase):
    def test_unproven_below_carry_streak_proven_at_or_above(self):
        cases = [
            ("green below min streak", "🟢", _MIN_STREAK - 1, True),
            ("green at min streak", "🟢", _MIN_STREAK, False),
            ("graduated", "🎓", 0, False),
        ]
        for name, comfort, streak, expected in cases:
            with self.subTest(name):
                self.assertEqual(eb.is_unproven(comfort, streak, _CFG), expected)


class UnprovenOverdueTests(unittest.TestCase):
    def test_backstop_triggers_at_the_pause_threshold(self):
        cases = [
            ("one under", _PAUSE_AT - 1, False),
            ("at threshold", _PAUSE_AT, True),
        ]
        for name, count, expected_triggered in cases:
            with self.subTest(name):
                rows = [_tracker_row("🔴", 0)] * count
                self.assertEqual(eb.unproven_overdue(rows, _CFG, _TODAY),
                                 (count, expected_triggered))


if __name__ == "__main__":
    unittest.main()
