"""Price a study day in effort units instead of counting problems.

The daily cap used to be an integer: "at most N problems." That cannot tell a
five-minute 🟢 Easy from a 🔴 Hard, so three days in the same week were all "7
problems" while measuring 5.5, 8.0 and 10.5 units of actual work. Every weekly
schedule note reading "Saturday is the heaviest day by some margin" was a human
correcting for that by hand, in prose, one week at a time.

This script is the source fix for that: it prints the number, so the number does
not have to be remembered or re-derived. Per the intervention ladder in
.claude/memory/feedback_self_evaluation.md — a tool that emits the right value
outranks a rule that asks someone to compute it.

    units = comfort_units × difficulty      (weights live in cse.config.yml)

Usage:
    python scripts/effort_budget.py                     # demand, floor, ceiling, due queue
    python scripts/effort_budget.py --day 19 110 42     # price a specific day
    python scripts/effort_budget.py --day 269 560 --sd  # ... including one SD lane slot
    python scripts/effort_budget.py --due 2026-08-08    # what is due on a date, priced
"""
from __future__ import annotations

import argparse
import datetime as dt
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRACKER = REPO / "docs/foundations/dsa/mastery/dsa_progress.md"
CONFIG = REPO / "cse.config.yml"

# Weights are keyed by the comfort GLYPH, never by the words blank/shaky/clean/graduated
# — see the note in cse.config.yml. Those words collide with update_review_dates.py's
# fallback config scrape and, in this file's first draft, silently rewrote three review
# dates by being read as intervals.
# Streak -> interval for a 🟢. Non-clean comforts have a flat interval.
CLEAN_INTERVAL = {0: 10, 1: 30, 2: 60}
FLAT_INTERVAL = {"🔴": 2, "🟡": 10, "🎓": 180}

ROW = re.compile(
    r"\|\s*(?P<diff>Easy|Medium|Hard)\s*\|\s*"
    r"\[(?P<num>\d+)\.\s*(?P<title>[^\]]+)\]\([^)]*\)\s*\|\s*"
    r"(?P<comfort>🔴|🟡|🟢|🎓)\s*\|\s*(?P<streak>\d+)\s*\|\s*"
    r"(?P<due>\d{4}-\d{2}-\d{2})"
)


def load_config() -> dict:
    """Read the effort_budget block, falling back to the documented defaults.

    Deliberately tolerant: a missing or malformed config must not stop the script
    from pricing a day, because the weights are a judgment call recorded in the
    doc and the defaults here are that same judgment.
    """
    defaults = {
        "comfort_units": {"🔴": 3.0, "🟡": 2.0, "🟢": 1.0, "🎓": 0.5},
        "difficulty": {"Easy": 0.5, "Medium": 1.0, "Hard": 1.5},
        "ceiling": 9.0,
        "floor_min": 3.0,
        "sd_lane_units": 2.0,
    }
    try:
        import yaml  # noqa: PLC0415
        loaded = (yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {})
        cfg = loaded.get("effort_budget") or {}
    except Exception:  # noqa: BLE001 — no config is a normal state, not an error
        return defaults
    for key, val in defaults.items():
        if key not in cfg:
            cfg[key] = val
        elif isinstance(val, dict):
            cfg[key] = {**val, **(cfg[key] or {})}
    return cfg


def parse_rows() -> list[dict]:
    rows = []
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            rows.append({**m.groupdict(), "streak": int(m.group("streak"))})
    return rows


def interval(row: dict) -> int:
    if row["comfort"] in FLAT_INTERVAL:
        return FLAT_INTERVAL[row["comfort"]]
    return CLEAN_INTERVAL.get(row["streak"], 60)


def units(row: dict, cfg: dict) -> float:
    base = cfg["comfort_units"][row["comfort"]]
    return base * cfg["difficulty"][row["diff"]]


def label(row: dict) -> str:
    streak = f" s{row['streak']}" if row["comfort"] == "🟢" else ""
    return f"{row['comfort']}{streak} {row['diff'][0]}"


def report_demand(rows: list[dict], cfg: dict, today: dt.date) -> None:
    reps = sum(1 / interval(r) for r in rows)
    cost = sum(units(r, cfg) / interval(r) for r in rows)
    floor = max(cfg["floor_min"], math.ceil(cost))
    overdue = [r for r in rows if dt.date.fromisoformat(r["due"]) < today]

    print(f"{len(rows)} rows · demand {reps:.2f} reps/day = "
          f"{cost:.2f} units/day ({cost * 7:.1f}/week)")
    print(f"advisory floor {floor:.0f} u/day (= ceil demand, min {cfg['floor_min']:.0f}) "
          f"· hard ceiling {cfg['ceiling']:.0f} u/day")
    if cost > cfg["ceiling"]:
        # Say it plainly: this is arithmetic, not a discipline problem, and the only
        # fixes are maturation (🟢 s1->s2->🎓) or shrinking the library.
        print(f"⚠ demand ({cost:.1f}) EXCEEDS the ceiling ({cfg['ceiling']:.0f}) — the "
              f"backlog grows no matter how the days are arranged.")
    print(f"overdue: {len(overdue)} rows, "
          f"{sum(units(r, cfg) for r in overdue):.1f} units to clear")


def price_day(nums: list[str], rows: list[dict], cfg: dict, sd: bool) -> None:
    by_num: dict[str, list[dict]] = {}
    for r in rows:
        by_num.setdefault(r["num"], []).append(r)

    total = 0.0
    for num in nums:
        found = by_num.get(num)
        if not found:
            # An untracked number is a NEW problem: no row, no history. Price it as a
            # Blank Medium, because that is what a first exposure usually costs.
            guess = cfg["comfort_units"]["🔴"] * cfg["difficulty"]["Medium"]
            total += guess
            print(f"  {num:>5}  {guess:4.1f}  (untracked — priced as a new 🔴 Medium)")
            continue
        if len(found) > 1:
            # Multi-variant problem (e.g. 130 BFS and 130 Union-Find). Which variant is
            # scheduled is not recoverable from the number, so price the dearest and say so.
            worst = max(found, key=lambda r: units(r, cfg))
            total += units(worst, cfg)
            variants = ", ".join(f"{label(r)}" for r in found)
            print(f"  {num:>5}  {units(worst, cfg):4.1f}  {label(worst)}  "
                  f"⚠ {len(found)} variants ({variants}) — priced the dearest")
            continue
        row = found[0]
        total += units(row, cfg)
        print(f"  {num:>5}  {units(row, cfg):4.1f}  {label(row)}  {row['title'][:44]}")

    if sd:
        total += cfg["sd_lane_units"]
        print(f"  {'SD':>5}  {cfg['sd_lane_units']:4.1f}  one lane slot")

    ceiling = cfg["ceiling"]
    verdict = "OVER" if total > ceiling else "ok"
    print(f"\n  TOTAL {total:.1f} / {ceiling:.0f} units — {verdict}"
          + (f" by {total - ceiling:.1f}" if total > ceiling else
             f" ({ceiling - total:.1f} spare)"))
    if total > ceiling:
        print("  Trim the CHEAPEST items last: dropping a 🟢 Easy saves 0.5, dropping a "
              "🟡 saves 2.0. Never trim the active block.")


def report_due(rows: list[dict], cfg: dict, day: dt.date) -> None:
    due = [r for r in rows if dt.date.fromisoformat(r["due"]) <= day]
    due.sort(key=lambda r: (r["due"], -units(r, cfg)))
    total = 0.0
    for r in due:
        total += units(r, cfg)
        print(f"  {r['due']}  {units(r, cfg):4.1f}  {label(r):8} {r['num']:>5} "
              f"{r['title'][:40]}")
    print(f"\n  {len(due)} due on/before {day} · {total:.1f} units "
          f"= {total / cfg['ceiling']:.1f} days at the ceiling")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--day", nargs="+", metavar="NUM",
                    help="price a day built from these problem numbers")
    ap.add_argument("--sd", action="store_true",
                    help="with --day: add one SD lane slot to the total")
    ap.add_argument("--due", metavar="YYYY-MM-DD",
                    help="list everything due on or before this date, priced")
    ap.add_argument("--today", metavar="YYYY-MM-DD",
                    help="override today's date (default: system date)")
    args = ap.parse_args()

    cfg = load_config()
    rows = parse_rows()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    if args.day:
        price_day(args.day, rows, cfg, args.sd)
    elif args.due:
        report_due(rows, cfg, dt.date.fromisoformat(args.due))
    else:
        report_demand(rows, cfg, today)


if __name__ == "__main__":
    main()
