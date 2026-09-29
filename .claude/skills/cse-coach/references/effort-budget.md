<!-- reconciled: 2026-09-28 -->
# Daily load is an effort budget, not a problem count

**Open this** at the weekly build, before accepting any overflow pull, and when re-pricing
mid-week. **Not for** the review ladder (that's `spaced-repetition.md`). **Not for**
producing a number — every unit calculation (which command, one pricing basis, moving a row,
reading the warnings) is the [`effort-units`](../../effort-units/SKILL.md) skill.

**All weights, the ceiling, and the floor live** in [`cse.config.yml`](cse.config.yml) under
`effort_budget:`. Read them there or run the script; never restate a number here.

## The unit model

A day is budgeted in **units**, not problems:
`units = base(comfort, streak) × difficulty(tier, demoted?) × attempt_factor`. A worse comfort
and a harder problem each cost more, so five 🟢 Easies and five 🔴 Hards are not the same day.

**Familiarity discounts (Sep 3, 2026):** a proven 🟢 decays with its streak. A proven problem
prices one difficulty tier easier. A chronic 🔴/🟡 (≥5 attempts) gets a bounded discount. A
well-worn Hard no longer bills like a cold one, while a fresh blank keeps full conversion
pressure. The three layers and their guardrails live in `effort_budget:`.

## ⚠️ SD is NOT priced (Aug 16, 2026) — the budget is DSA-only

The ceiling was lowered *because* SD moved off-board: it is the honest DSA-only number,
deliberately sized so **the leftover evening is SD's**. Do not add an SD slot to a day's total —
the lowered ceiling already accounts for it; charging both bills it twice. `system_design.cadence`
still decides how many SD slots a week gets (placed at the weekly build); only the cost is gone.
`effort_budget.py --sd` adds 0 and says so.

## 🎯 Complexity re-asks are NOT priced (Sep 28, 2026)

A row whose Technique is `Complexity` is a cold re-ask of time and space on code that already
exists, not a rep. It adds 0 units, and `--schedule-day` lists it at 0.0.
`decisions.yml` `complexity-reask-unpriced`.

## The ceiling is the daily goal (Sep 28, 2026)

Build each day as close to the ceiling (`effort_budget.ceiling`) as possible. It is the daily goal, and a small overshoot is fine. Raising the ceiling itself to catch up is still off the table. `decisions.yml` `daily-goal-is-the-ceiling-sep28`.

## ⚠️ Never raise the ceiling to catch up on a backlog

On a Medium row a 🟡 bills ~12× what a 🟢 s2 does. A rep rushed into a 🟡 costs 12× *forever*, so
chasing a deficit with a higher ceiling *increases* future demand. **Demand sets the floor**; the
ceiling is a quality judgment and stays put. Fri Aug 7: the board was at ceiling. The pull that
overran it was the single dearest item available, and it came back 🟡 with four bugs.

## Why the two pricing modes never mix

Which mode answers which question is in the `effort-units` skill. The why: on Aug 18, 2026,
`--day` was handed only the remaining rows and re-read their current comfort, and a day at the
ceiling was reported with 5.0 units spare. On Sep 28, 2026, `--schedule-day` priced 25 streakless
🟢 Start cells at streak 0, and a 7.4-unit day read as "8.0, header matches".

## Re-price mid-week — a build's verdict expires as results land

After logging the day's results, re-run `python scripts/effort_budget.py`. The weekly build's
"what does not fit" can be wrong by the next session. Aug 17, 2026: demand fell 7.16 → 5.58
units/day in one morning off a single 🔴→🟢 conversion. **If headroom opened**, re-seat from the
slip list, oldest first, in the same edit. Say what changed.

- ⚠️ **Weekly headroom does not seat an indivisible item** — check the DAY, not just the week. A
  single 4.5-unit Hard doesn't fit days sitting at 7.5–8.0 with a largest single-day spare of 0.5,
  even when weekly slack looks ample.
- ⚠️ **Headroom resting on a provisional 🟢 is contingent** — spend it on deferrable work
  (🟢 backlog, an unseen problem), never permanent new demand.

full rule: [`docs/foundations/effort_budget.md`](docs/foundations/effort_budget.md) (dated
derivation — read for the *why*, never the values); `decisions.yml` `effort-budget-replaces-count`,
`sd-unpriced`, `ceiling-lowered`, `familiarity-discounting`, `midweek-reprice`;
[`feedback_midweek_reprice.md`](.claude/memory/feedback_midweek_reprice.md).
