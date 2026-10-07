"""Tests for backlog_forecast.py: tally parser, ladder step, a deterministic 2-week replay.

    python -m pytest scripts/test_backlog_forecast.py -q
"""
from __future__ import annotations

import datetime as dt
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import backlog_forecast as bf  # noqa: E402

LADDER = {"blank": 2, "shaky": 10, "provisional": 10, "streak1": 30, "streak2": 60,
          "graduated": 180, "graduate_at": 3}

SCHEDULE_FIXTURE = """\
| Problem | Start | End | Next | Technique |
|---|---|---|---|---|
| ▸ **Tue Oct 6** · 5.0 units | 🟡 | 🟢 |  |  |
| [1 Two Sum](x) | 🟡 | 🟢 | 2026-10-16 | Hash |
| [2 Add Two](x) | 🟢 | 🟡 | 2026-10-16 | Lists |
| [3 Pending](x) | 🟢 s2 |  |  | Lists |
| 🆕 [4 New](x) | 🆕 | 🔴 | 2026-10-08 | Trees |
"""

CFG = {"max_rows_per_day": 8, "ceiling": 8.0, "carry_forward_min_streak": 2,
       "comfort_units": {"🔴": 3.0, "🟡": 2.0, "🟢": 1.0, "🎓": 0.5},
       "difficulty": {"Easy": 0.5, "Medium": 1.0, "Hard": 1.3},
       "green_streak_units": {0: 1.0, 1: 0.8, 2: 0.6}}


def test_tally_text_classes_bare_green_as_s1_and_skips_header_and_empty_end() -> None:
    assert bf.tally_text(SCHEDULE_FIXTURE) == Counter(
        {("🟡", "🟢"): 1, ("🟢 s1", "🟡"): 1, ("🆕", "🔴"): 1})


def test_ladder_step_table() -> None:
    cases = [
        (("🟢", 1, "🔴"), ("🔴", 0, 2)),
        (("🟢", 1, "🟡"), ("🟡", 0, 10)),
        (("🟡", 0, "🟢"), ("🟢", 0, 10)),
        (("🔴", 0, "🟢"), ("🟢", 0, 10)),
        (("🟢", 0, "🟢"), ("🟢", 1, 30)),
        (("🟢", 1, "🟢"), ("🟢", 2, 60)),
        (("🟢", 2, "🟢"), ("🎓", 3, 180)),
        (("🎓", 3, "🟢"), ("🎓", 4, 180)),
        (("🎓", 3, "🟡"), ("🟡", 0, 10)),
    ]
    for (comfort, streak, outcome), expected in cases:
        assert bf.ladder_step(comfort, streak, outcome, LADDER) == expected, (comfort, streak, outcome)


def test_two_week_replay_with_all_green_sampler() -> None:
    start = dt.date(2026, 10, 6)
    first = start.toordinal()
    rows = [
        {"comfort": "🟢", "streak": 2, "diff": "Easy", "due": first - 1, "attempts": 3},
        {"comfort": "🔴", "streak": 0, "diff": "Medium", "due": first, "attempts": 1},
        {"comfort": "🟡", "streak": 0, "diff": "Medium", "due": first + 30, "attempts": 1},
    ]
    result = bf.simulate(rows, CFG, LADDER, start, 0, 2, lambda cls, rng: "🟢", random.Random(0))
    # Row 1 graduates day 1 (due again +180); row 2 goes 🟢 s0 (+10), then s1 on day 11 is
    # past the 2 weeks; row 3 stays 🟡 and is not yet due.
    assert result["backlog"] == {1: 0, 2: 0}
    assert result["graduated"] == 1
