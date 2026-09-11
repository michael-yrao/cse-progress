<!-- reconciled: 2026-09-10 -->
# Daily load is an effort budget, not a problem count

**Open this** at the weekly build, before accepting any overflow pull, and when re-pricing
mid-week. **Not for** the review ladder (that's `spaced-repetition.md`). **Not for**
hand-computing a total — the script is the only thing that prices a day; never do the arithmetic
yourself.

**All weights, the ceiling, and the floor live in [`cse.config.yml`](cse.config.yml) under
`effort_budget:`.** Read them there or run the script; never restate a number here.

## The unit model

A day is budgeted in **units**, not problems:
`units = base(comfort, streak) × difficulty(tier, demoted?) × attempt_factor` — a worse comfort
and a harder problem each cost more, so five 🟢 Easies and five 🔴 Hards are not the same day.

**Familiarity discounts (Sep 3, 2026):** a proven 🟢 decays with its streak, a proven problem
prices one difficulty tier easier, and a chronic 🔴/🟡 (≥5 attempts) gets a bounded discount — so
a well-worn Hard no longer bills like a cold one, while a fresh blank keeps full conversion
pressure. The three layers and their guardrails live in `effort_budget:`.

```sh
python scripts/effort_budget.py                       # demand · floor · ceiling · overdue cost
python scripts/effort_budget.py --schedule-day        # TODAY as built: done vs remaining
python scripts/effort_budget.py --day 560 912 235     # a HYPOTHETICAL day (build time only)
```

## ⚠️ SD is NOT priced (Aug 16, 2026) — the budget is DSA-only

The ceiling was lowered *because* SD moved off-board: it is the honest DSA-only number,
deliberately sized so **the leftover evening is SD's**. Do not add an SD slot to a day's total —
the lowered ceiling already accounts for it; charging both bills it twice. `system_design.cadence`
still decides how many SD slots a week gets (placed at the weekly build); only the cost is gone.
`effort_budget.py --sd` adds 0 and says so.

## ⚠️ Never raise the ceiling to catch up on a backlog

On a Medium row a 🟡 bills ~12× what a 🟢 s2 does — a rep rushed into a 🟡 costs 12× *forever*, so
chasing a deficit with a higher ceiling *increases* future demand. **Demand sets the floor; the
ceiling is a quality judgment and stays put.** (Fri Aug 7: the board was at ceiling, the pull that
overran it was the single dearest item available, and it came back 🟡 with four bugs.)

## ⚠️ `--day` is a LIVE PRICER, not a ledger — audit a day in progress with `--schedule-day`

```sh
python scripts/effort_budget.py --schedule-day              # today, AS BUILT
python scripts/effort_budget.py --schedule-day 2026-08-18   # any day, incl. archived weeks
```

`--schedule-day` reads the week's schedule, prices each row from the **`Start` column** (the
comfort written at the build, never mutated), and splits the day into **built · done ·
remaining**. Two things make `--day` wrong mid-session, and they compound:

| | |
|---|---|
| **It prices exactly what it is handed** | mid-day the natural list to hand it is the *remaining* items, and that total then reads as the *day's* total — the already-spent units silently missing |
| **It re-reads CURRENT comfort** | a 🟡 that came back 🟢 re-prices at the 🟢 rate; but units are billed on the comfort a row carried **going in** — the conversion cuts *future* demand, never today's bill |

⭐ The Aug 18, 2026 failure: both errors ran together, both understate, so they never cancel — a
day at exactly the ceiling was reported as having 5.0 units spare, and a discretionary rep was
seated on capacity that did not exist. `--day` now warns on any number whose tracker row already
has a rep dated today; `--schedule-day` reports a day containing a primer/probe/untracked-new as a
**FLOOR** (it won't hide rows it couldn't price), and cross-checks each day header's stated units
against its rows.

## Re-price mid-week — a build's verdict expires as results land

After logging the day's results, re-run `python scripts/effort_budget.py`. The weekly build's
"what does not fit" can be wrong by the next session (Aug 17, 2026: demand fell 7.16 → 5.58
units/day in one morning off a single 🔴→🟢 conversion). **If headroom opened, re-seat from the
slip list — oldest first, in the same edit — and say what changed.**

- ⚠️ **Weekly headroom does not seat an indivisible item — check the DAY, not just the week.** A
  single 4.5-unit Hard doesn't fit days sitting at 7.5–8.0 with a largest single-day spare of 0.5,
  even when weekly slack looks ample.
- ⚠️ **Headroom resting on a provisional 🟢 is contingent** — spend it on deferrable work
  (🟢 backlog, an unseen problem), never permanent new demand.

full rule: [`docs/foundations/effort_budget.md`](docs/foundations/effort_budget.md) (dated
derivation — read for the *why*, never the values); `decisions.yml` `effort-budget-replaces-count`,
`sd-unpriced`, `ceiling-lowered`, `familiarity-discounting`, `midweek-reprice`;
[`feedback_midweek_reprice.md`](.claude/memory/feedback_midweek_reprice.md).
