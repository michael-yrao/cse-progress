---
name: effort-units
description: >-
  Effort-unit calculations for the cse-progress study schedule. Use for ANY number or edit
  involving effort units: pricing a day, a problem or a set of problems; checking a day
  against the ceiling; moving, adding or removing a schedule row (every touched day header
  changes); reseating a deferred rep; the weekly build's day totals; a mid-week re-price; or
  checking the dashboard's workload numbers. Every number comes from
  scripts/effort_budget.py in one named mode — never hand-computed.
---
<!-- reconciled: 2026-10-06 -->
# effort-units — every effort number from one script, on one basis

The unit model, the weights and the policy live elsewhere: the policy (the ceiling is the
daily goal; SD and complexity re-asks are unpriced; never raise the ceiling to catch up) is
in the cse-coach reference [`effort-budget.md`](../cse-coach/references/effort-budget.md),
and the weights are in `cse.config.yml` `effort_budget:`. This skill is the procedure for
producing a number. It never restates a weight.

## Three rules

1. **The script prices.** Every unit figure you state comes from a
   `python scripts/effort_budget.py` run in this turn. A day header equals the script's
   `built`. There are no estimates.
2. **One mode per answer.** Name the mode next to every number ("7.4, `--schedule-day`").
   Never compare, add or subtract numbers from two modes.
3. **A row bills the comfort it carried going in.** A row's price is fixed at the build. A rep
   that converts 🟡 → 🟢 cuts future demand, never today's bill.

## Which command answers which question

| Question | Command | Quote |
|---|---|---|
| What does a day cost as built? What is done, what is left? | `--schedule-day [YYYY-MM-DD]` | `built` · `done` · `remaining` |
| Is a day at the ceiling? How much spare? | `--schedule-day [YYYY-MM-DD]` | the spare line |
| What would these problems cost, for a day not yet started? | `--day N N …` | `TOTAL` |
| Weekly demand, the floor, the overdue cost | no flag | demand · floor |
| What is due by a date, priced? | `--due YYYY-MM-DD` | the total |

⚠️ `--day` reads each problem's CURRENT tracker comfort and prices only the numbers it is
handed. Never use it on a day in progress, on a row already repped, or to price a row that is
moving between days.

## Moving, adding or removing a row

**A day that has started keeps its rows.** A row not done on it stays there, unstruck,
prefixed `→`, with the new date in Next, but it is no longer billed there: the day's header
drops by its price, and `--schedule-day` lists it under MOVED. The copy on the new day is
prefixed `→` and prices there. A swap is therefore even: the row out leaves the bill, the row
in joins it. **A day that has not started is re-planned:** the row moves outright.

1. **Start cell.** Moving: carry the Start cell verbatim. Adding: write it from the tracker —
   the comfort going in, with the streak on a 🟢 (`🟢 s2`), or `🆕` for an unseen problem.
2. **Make the edit.** Both days' headers change in the same edit.
3. **Price each touched day** with `--schedule-day` and set the header to `built`.
4. **Re-run and read the check.** It must read `matches`. `CANNOT VERIFY` means a row is
   unpriced or guessed: fix the row (its number, its difficulty, its Start cell), not the
   header.

## Reading the output

| Line | Meaning | Do |
|---|---|---|
| `header says X -- matches` | every row priced; the header agrees | nothing |
| `!! HEADER SAYS X, rows sum to Y` | every row priced; the header is wrong | set the header to Y |
| `CANNOT VERIFY` | some rows unpriced, guessed, or missing a streak | fix the row |
| `LOWER BOUND` / `FLOOR` | unpriced rows are missing from the total | fix the row |
| `no streak in the Start cell` | a 🟢 row priced at streak 0, the highest 🟢 price | write the streak into the Start cell (`🟢 sN`) |

The last row exists because of Sep 28, 2026: 25 🟢 Start cells had lost their streak, and
`--schedule-day` read Monday as "8.0, header matches" while the build's basis gave 7.4.

## Mid-week

After logging a day's results, run the script with no flag. If headroom opened, reseat from
the slip list in the same edit (policy: `effort-budget.md` "Re-price mid-week").
