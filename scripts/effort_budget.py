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
    python scripts/effort_budget.py --schedule-day      # today, AS BUILT (done vs left)
    python scripts/effort_budget.py --schedule-day 2026-08-18
    python scripts/effort_budget.py --day 19 110 42     # price a HYPOTHETICAL day
    python scripts/effort_budget.py --day 269 560       # (--sd is retired: SD is unpriced)
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
    # The tail is OPTIONAL on purpose: a malformed or legacy row must still price,
    # it just cannot participate in the already-repped-today guard below.
    r"(?:\s*\|\s*(?P<latest>\d{4}-\d{2}-\d{2})\s*\|\s*(?P<reps>[^|]*))?"
)

SCHEDULES = REPO / "docs/foundations/schedules"

# A day header in a weekly schedule: "| ▸ **Tue Aug 18** · 8.0 units |  |  |  |  |"
DAY_HEADER = re.compile(
    r"\|\s*▸\s*\*\*(?P<wd>\w{3})\s+(?P<mon>\w{3})\s+(?P<day>\d{1,2})\*\*"
    r"(?:[^|]*?·\s*(?P<units>[\d.]+)\s*units)?"
)
# Any 5-column row of the daily table.
SCHED_ROW = re.compile(r"^\|(?P<c1>[^|]*)\|(?P<c2>[^|]*)\|(?P<c3>[^|]*)\|(?P<c4>[^|]*)\|(?P<c5>.*)\|\s*$")
# The problem number is the first digits following a "[" or a "**" in the first cell.
SCHED_NUM = re.compile(r"(?:\[|\*\*)(\d+)")
GLYPH = re.compile(r"[🔴🟡🟢🎓]")


def load_config() -> dict:
    """Read the effort_budget block, falling back to the documented defaults.

    Deliberately tolerant: a missing or malformed config must not stop the script
    from pricing a day, because the weights are a judgment call recorded in the
    doc and the defaults here are that same judgment.
    """
    defaults = {
        "comfort_units": {"🔴": 3.0, "🟡": 2.0, "🟢": 1.0, "🎓": 0.5},
        "difficulty": {"Easy": 0.5, "Medium": 1.0, "Hard": 1.5},
        # Fallback only — used when PyYAML is missing and cse.config.yml cannot be read.
        # It must track the config, or a machine without PyYAML silently prices every day
        # against the wrong ceiling and calls over-full days "ok". Was 9.0 until Aug 16, 2026.
        "ceiling": 8.0,
        "floor_min": 3.0,
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


def price_day(nums: list[str], rows: list[dict], cfg: dict, sd: bool,
              today: dt.date | None = None) -> None:
    by_num: dict[str, list[dict]] = {}
    for r in rows:
        by_num.setdefault(r["num"], []).append(r)

    # --- guard: this flag is a LIVE PRICER, not a ledger -----------------------
    # Comfort in the tracker is the comfort a row EARNED at its last rep. Units are
    # billed on the comfort a row carried GOING IN. Those agree only until a rep is
    # logged -- after that, pricing the same number here understates it, silently and
    # always in the same direction. Compounded with handing this flag the REMAINING
    # items and reading the total as the day's total, that invented 5.0 units of spare
    # capacity on a day already at the ceiling (Aug 18, 2026).
    if today is not None:
        stale = [n for n in nums
                 for r in by_num.get(n, []) if repped_on(r, today)]
        blind = [n for n in nums
                 for r in by_num.get(n, []) if not rep_dates_readable(r)]
        if blind:
            print(f"  !! could not read the Rep Dates column for "
                  f"{', '.join(sorted(set(blind)))} -- those numbers were NOT checked "
                  f"for a rep dated {today}.")
            print("     Treat the total below as unverified and use --schedule-day.")
            print()
        if stale:
            print(f"  !! {', '.join(sorted(set(stale)))} already have a rep dated "
                  f"{today} -- they are priced here at the comfort they EARNED,")
            print("     not the one they were BILLED at, so this total UNDERSTATES the "
                  "day as built.")
            print("     For a day in progress use --schedule-day, which prices from the "
                  "schedule's Start column.")
            print()

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
        # SD IS NOT PRICED (Aug 16, 2026). The budget used to add an SD slot to the day's
        # total; the model changed and the flag did not. SD moved to a separate repo, is
        # self-directed, and is OFF-BOARD — so the ceiling was lowered 9.0 -> 8.0 to be the
        # honest DSA-only number, and SD takes the leftover evening. Pricing SD into the day
        # AND holding the lowered ceiling would charge for it twice.
        #
        # The flag still parses, and says this, rather than being deleted: silently dropping
        # 3.0 units from a total someone expected it in is how a day gets over-filled without
        # anyone noticing. Accepting it and explaining is the only version that cannot
        # mislead.
        print("  SD     —    not priced: SD is off-board since Aug 16, 2026. The 8.0 "
              "ceiling is\n         DSA-only and already sized so SD fits the leftover "
              "evening. --sd adds nothing.")

    ceiling = cfg["ceiling"]
    verdict = "OVER" if total > ceiling else "ok"
    print(f"\n  TOTAL {total:.1f} / {ceiling:.0f} units — {verdict}"
          + (f" by {total - ceiling:.1f}" if total > ceiling else
             f" ({ceiling - total:.1f} spare)"))
    if total > ceiling:
        print("  Trim the CHEAPEST items last: dropping a 🟢 Easy saves 0.5, dropping a "
              "🟡 saves 2.0. Never trim the active block.")


def repped_on(row: dict, day: dt.date) -> bool:
    """Did this row get a rep on `day`?

    Reads the tracker's own Rep Dates column. Used only by the --day guard: a row
    already repped today has ALREADY been paid for, and its comfort in the tracker
    is now the comfort it EARNED, not the one it was billed at.
    """
    return day.isoformat() in (row["reps"] or "")


def rep_dates_readable(row: dict) -> bool:
    """Could the Rep Dates column be read at all for this row?

    ⚠️ The tail of ROW is optional, so a row whose Latest/Rep Dates cells do not match
    comes back with reps=None -- and `repped_on` would then answer "no rep today" for a
    row it never actually read. A guard that quietly declines to fire is worse than no
    guard, so the caller reports these rather than treating them as clean.
    """
    return row["reps"] is not None


def find_schedule(day: dt.date) -> Path | None:
    """The weekly schedule file whose 7-day span contains `day`.

    Searches the live folder first, then archive/, so an audit still works on a week
    that has already been closed out.
    """
    best: tuple[dt.date, Path] | None = None
    for folder in (SCHEDULES, SCHEDULES / "archive"):
        if not folder.is_dir():
            continue
        for path in folder.glob("*_schedule.md"):
            stamp = path.name.split("_")[0]
            if len(stamp) != 8 or not stamp.isdigit():
                continue
            try:
                start = dt.date(int(stamp[:4]), int(stamp[4:6]), int(stamp[6:]))
            except ValueError:
                continue
            if start <= day < start + dt.timedelta(days=7):
                if best is None or start > best[0]:
                    best = (start, path)
    return best[1] if best else None


def parse_schedule_day(path: Path, day: dt.date) -> tuple[list[dict], float | None]:
    """Pull one day's block out of a weekly schedule's daily table.

    Returns (items, stated_units). Each item carries the problem number, the START
    comfort glyph as written at build time, and whether the row is struck through.

    The START column is the whole point of this function. It is written once, at the
    weekly build, and never mutated -- so it survives a rep being logged, which the
    tracker's Comfort column does not. Pricing a day from the tracker AFTER reps land
    charges the comfort the rows EARNED instead of the one they were BILLED at, and
    therefore always understates the day.
    """
    week_start = dt.date(int(path.name[:4]), int(path.name[4:6]), int(path.name[6:8]))
    wanted = None
    for offset in range(7):
        d = week_start + dt.timedelta(days=offset)
        if d == day:
            wanted = (d.strftime("%a"), d.strftime("%b"), d.day)
            break
    if wanted is None:
        return [], None

    items: list[dict] = []
    stated: float | None = None
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        header = DAY_HEADER.search(line)
        if header:
            hit = (header["wd"], header["mon"], int(header["day"])) == wanted
            if hit:
                inside = True
                stated = float(header["units"]) if header["units"] else None
            elif inside:
                break          # the next day's header ends this day's block
            continue
        if not inside:
            continue
        if not line.lstrip().startswith("|"):
            break              # the daily table ended.
                               # ⚠️ On the LAST day of the week there is no next day
                               # header to break on, so without this the scan runs to
                               # EOF and any later 5-column table is priced into Sunday.
                               # A total that silently absorbs rows is the same class of
                               # error this whole flag exists to prevent.
        m = SCHED_ROW.match(line)
        if not m:
            continue
        cell = m["c1"]
        if not cell.strip() or set(cell.strip()) <= {"-", ":"}:
            continue           # blank separator row, or a markdown rule
        num = SCHED_NUM.search(cell)
        glyph = GLYPH.search(m["c2"] or "")
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)
        # Strip markdown emphasis wherever it sits, not just at the ends: the strike
        # wraps the LINK (`~~[496 ...](...)~~ · [LC](...)`), so trailing-only stripping
        # leaves a stray `~~` in the middle of the printed title.
        text = re.sub(r"~~|\*\*", "", text)
        items.append({
            "num": num.group(1) if num else None,
            "start": glyph.group(0) if glyph else None,
            "done": "~~" in cell,
            "text": re.sub(r"\s+", " ", text).strip(" ·*"),
        })
    return items, stated


def price_schedule_day(day: dt.date, rows: list[dict], cfg: dict) -> None:
    """Price a scheduled day as BUILT, splitting done from remaining.

    This exists because --day cannot do it. --day takes a list of numbers from a
    human, so it prices exactly what it is handed -- and mid-session the natural
    thing to hand it is the REMAINING items, whose total then reads as the day's
    total. That error (Aug 18, 2026) invented 5.0 units of spare capacity on a day
    already sitting at the ceiling, and a discretionary rep got seated on it. Here
    the tool defines the day, so there is nothing to mis-hand it.
    """
    path = find_schedule(day)
    if path is None:
        print(f"no weekly schedule covers {day} (looked in {SCHEDULES} and archive/)")
        return
    items, stated = parse_schedule_day(path, day)
    if not items:
        print(f"{day} has no block in {path.name} -- nothing scheduled, or the day "
              f"header is not in the form this parser expects.")
        return

    by_num: dict[str, list[dict]] = {}
    for r in rows:
        by_num.setdefault(r["num"], []).append(r)

    done_total = rest_total = 0.0
    guessed = 0
    done_lines: list[str] = []
    rest_lines: list[str] = []
    unpriced: list[str] = []

    for it in items:
        if not it["num"]:
            unpriced.append(it["text"][:62])
            continue
        tracked = by_num.get(it["num"])
        if it["start"] and tracked:
            # START comfort (build time) x difficulty (a stable property of the problem).
            diff = tracked[0]["diff"]
            cost = cfg["comfort_units"][it["start"]] * cfg["difficulty"][diff]
            note = f"{it['start']} {diff[0]}"
        elif tracked:
            worst = max(tracked, key=lambda r: units(r, cfg))
            cost = units(worst, cfg)
            note = f"{label(worst)} !! no Start glyph -- priced from the tracker"
        else:
            cost = cfg["comfort_units"]["\U0001f534"] * cfg["difficulty"]["Medium"]
            note = "NEW !! untracked -- guessed as a new Blank Medium"
            guessed += 1
        line = f"  {it['num']:>5}  {cost:4.1f}  {note}  {it['text'][:44]}"
        if it["done"]:
            done_total += cost
            done_lines.append(line)
        else:
            rest_total += cost
            rest_lines.append(line)

    built = done_total + rest_total
    print(f"{day:%a %b %d} - {path.name}\n")
    if done_lines:
        print("  DONE")
        print("\n".join(done_lines))
    if rest_lines:
        print("\n  REMAINING")
        print("\n".join(rest_lines))
    if unpriced:
        print("\n  UNPRICED (no problem number -- primer, probe, or free-text row)")
        for u in unpriced:
            print(f"    {u}")

    ceiling = cfg["ceiling"]
    # A total that silently omits rows is the exact failure this whole flag exists to
    # prevent, so say what could NOT be priced BEFORE saying the number.
    partial = len(unpriced) + guessed
    floor_note = "  (FLOOR -- see below)" if partial else ""
    print(f"\n  built {built:.1f}{floor_note} / done {done_total:.1f} "
          f"/ remaining {rest_total:.1f} / ceiling {ceiling:.0f}")
    if partial:
        bits = []
        if unpriced:
            bits.append(f"{len(unpriced)} row(s) carry no problem number "
                        f"(primer / probe / free text)")
        if guessed:
            bits.append(f"{guessed} untracked row(s) guessed at Blank Medium -- a new "
                        f"HARD really costs 1.5x that")
        print(f"     !! this total is a LOWER BOUND: {'; '.join(bits)}.")
    if built > ceiling:
        print(f"  !! the day as BUILT is OVER by {built - ceiling:.1f}")
    elif not partial:
        print(f"  {ceiling - built:.1f} spare against the day as built")
    else:
        print(f"  at most {ceiling - built:.1f} spare -- less once the rows above price")

    # Catch a build-time arithmetic slip too: the header states a total, and until now
    # nothing had ever checked it against the rows underneath it. Only assert a real
    # mismatch when EVERY row was priced from a Start glyph against a tracked row --
    # otherwise the difference is just the part this parser admits it cannot see, and
    # crying wrong on that is how a check stops being read.
    if stated is None:
        print("  !! the day header states no unit total -- add it so it can be checked")
    elif abs(stated - built) <= 0.05:
        print(f"  header says {stated:.1f} -- matches")
    elif partial:
        print(f"  header says {stated:.1f}, priced rows sum to {built:.1f} "
              f"(difference {stated - built:+.1f}) -- CANNOT VERIFY while rows are "
              f"unpriced or guessed. Check that difference is what those rows are worth.")
    else:
        print(f"  !! HEADER SAYS {stated:.1f}, rows sum to {built:.1f} -- every row "
              f"priced exactly, so one of them is wrong")



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
                    help="price a HYPOTHETICAL day built from these problem numbers. "
                         "A live pricer, not a ledger -- for a day already in progress "
                         "use --schedule-day")
    ap.add_argument("--schedule-day", nargs="?", const="", metavar="YYYY-MM-DD",
                    help="price a scheduled day AS BUILT from the weekly schedule file "
                         "(Start column = the comfort each row was billed at), split "
                         "into done vs remaining. Defaults to today")
    ap.add_argument("--sd", action="store_true",
                    help="RETIRED — SD is off-board and unpriced since Aug 16, 2026. "
                         "Accepted so the flag explains itself; adds 0 units")
    ap.add_argument("--due", metavar="YYYY-MM-DD",
                    help="list everything due on or before this date, priced")
    ap.add_argument("--today", metavar="YYYY-MM-DD",
                    help="override today's date (default: system date)")
    args = ap.parse_args()

    cfg = load_config()
    rows = parse_rows()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    if args.schedule_day is not None:
        target = dt.date.fromisoformat(args.schedule_day) if args.schedule_day else today
        price_schedule_day(target, rows, cfg)
    elif args.day:
        price_day(args.day, rows, cfg, args.sd, today)
    elif args.due:
        report_due(rows, cfg, dt.date.fromisoformat(args.due))
    else:
        report_demand(rows, cfg, today)


if __name__ == "__main__":
    main()
