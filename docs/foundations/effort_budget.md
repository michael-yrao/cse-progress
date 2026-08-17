# The effort budget — replacing the daily problem cap

**Status: ADOPTED Aug 7, 2026.** Live in `cse.config.yml` under `effort_budget`; `daily_cap: 7` is kept
only as a fallback and nothing reads it. Computed by [`scripts/effort_budget.py`](../../scripts/effort_budget.py).

```sh
python scripts/effort_budget.py                    # demand, floor, ceiling, overdue cost
python scripts/effort_budget.py --day 560 912 235 88 100 20   # price a day
python scripts/effort_budget.py --day 721 105                  # (--sd retired — SD is unpriced)
python scripts/effort_budget.py --due 2026-08-14              # everything due by a date, priced
```

**Decisions (learner, Aug 7):** `x` = **3.0** hard minimum · SD lane = **2.0** units · `q` = **one
binding number for every day**, not per-day, starting at **9.0**.

> ⚠️ **Two of those three numbers have since changed. This document is the ORIGINAL Aug 7 record and
> is deliberately not rewritten** — it is how the model was reasoned out, and back-dating it would
> destroy the reasoning. The live numbers are in [`cse.config.yml`](../../cse.config.yml):
>
> - **`q` = 8.0**, not 9.0 (lowered Aug 16, 2026).
> - **The SD lane is NOT PRICED AT ALL** (Aug 16, 2026). It went 2.0 → 3.0 on Aug 9 and was then
>   retired outright: SD moved off-board to a separate repo, so the ceiling was lowered to be the
>   honest **DSA-only** number and **the leftover evening is SD's**. Pricing SD *and* holding the
>   lowered ceiling would charge for it twice. `--sd` now adds 0 and says so.
> - `x` = 3.0 is unchanged.
>
> Everything below this line is the Aug 7 derivation. Read it for the *why*, never for the *values*.

**What it replaces:** a single integer, `daily_cap`, counting *problems per day*.

---

## Why the count cap is wrong

**A problem is not a unit of work.** On Fri Aug 7 the board held 7 problems and ran light, because
four of them were five-minute 🟢 Easy sweeps. Saturday Aug 8 holds 7 problems and is the hardest day
of the week — four 🟡s back to back. The cap says these are the same day. They are not close:

| Day | Problems | Effort units (below) |
|---|---:|---:|
| Thu Aug 6 | 7 | **5.5** |
| Fri Aug 7 (board) | 7 | **8.0** |
| Sat Aug 8 (as built) | 7 | **10.5** |

**Same count, nearly double the load.** That spread is invisible to `daily_cap` and it is exactly what
the cap exists to control. Every schedule note that says *"Saturday is the heaviest day by some margin"*
or *"Sun holds 6, not 7"* is a human correcting for this by hand, in prose, every week.

**And the failure it causes is measurable.** Friday ran to 8 by pulling 269 forward. The first seven
(8.0 units) went 6🟢/1🟡. The eighth was 🟡 Hard — 3.0 units on its own, more than the whole first slot —
and came back 🟡 with four bugs. The count said "one more problem." The effort said "you are adding 38%
to the day."

---

## The unit table

```
units = comfort_base × difficulty_factor

comfort_base:  🔴 3.0   🟡 2.0   🟢 1.0   🎓 0.5
difficulty:    Easy 0.5   Medium 1.0   Hard 1.5
```

So a 🟢 Easy is **0.5** and a 🔴 Hard is **4.5** — a 9× spread, which is about right: a Blank on a Hard
problem is most of a session, and a 🟢 Easy is five minutes.

Calibration notes, so these are not arbitrary:
- **🟡 = 2× 🟢** because a 🟡 rep is a rep *plus* a diagnosis conversation plus a stuck-log entry.
- **🔴 = 3× 🟢** and the schedule already says so in prose: *"a Blank costs its own slot plus 2–3
  follow-up warmups."* This just writes it down as a number.
- **🎓 = 0.5** — a spot check on a graduated problem is a confirmation, not a rep.
- **Difficulty from the tracker's own column**, so nothing new has to be maintained.

**Rate by the comfort the row carries *going in*,** never the one it earns. The budget is built before
the day runs, and a rep that turns out badly is precisely the thing you could not have known.

---

## The floor comes from demand; the ceiling never does

Measured today (110 rows):

```
demand   4.28 reps/day   =   6.25 units/day   =   43.8 units/week
mean cost per rep: 1.46 units
```

**The floor is `ceil(demand_units)` — currently 7 units/day.** That is the steady-state: do less and
the backlog grows by arithmetic, regardless of effort.

**The ceiling is a quality judgment and must NOT be derived from demand.** This is the load-bearing
claim of the whole proposal:

> A rushed rep returns 🟡 instead of 🟢. On a Medium, 🟡 bills **73 units/year** and 🟢 s2 bills **6.1**
> — the row costs **12× more** for having been rushed. So raising the ceiling to catch up on a deficit
> *increases* future demand. It is a positive feedback loop, and the deficit wins.

Annual cost per Medium row, for reference:

| State | Interval | Units/year |
|---|---:|---:|
| 🟡 | +10 | **73.0** |
| 🟢 s1 | +30 | 12.2 |
| 🟢 s2 | +60 | 6.1 |
| 🎓 | +180 | 1.0 |

This is also why today mattered more than it looked: six s1→s2 conversions and one graduation took
weekly demand from **37.6 → 30.0 reps** and overdue from **30 → 16**, in one day, without shrinking the
library.

---

## The rule

```
budget_today = clamp(planned_units, floor, ceiling)

floor    = max(x, ceil(demand_units_per_day))     # x = hard minimum, learner-set
ceiling  = q                                       # quality ceiling, calibrated (below)
```

- **`x`** is the "I always do something" floor. Suggest **3 units** — one Medium 🟡, or a couple of
  easies. Survives a bad day without a zero.
- **`q`** is the real cap. Suggest starting at **9 units/day**, and *not* deriving it from anything:
  it is a claim about how much focused work a day holds, which only evidence can settle.

**Calibrating `q` from data you already have.** The tracker records difficulty and comfort per attempt,
and the schedules record which day each rep ran on. So the question *"does comfort degrade as the day's
accumulated units rise?"* is answerable directly — group reps by the units already spent that day when
they started, and compare 🟢 rates. Set `q` at the point where the 🟢 rate falls off. Until there is
enough data, 9 is a guess anchored to two observations: Thu (5.5 units) went 5🟢/2🟡 and Fri's board
(8.0 units) went 6🟢/1🟡, both fine; the 11.0-unit version of Friday produced the day's worst rep.

---

## What changes in practice

1. **`cse.config.yml`**: `daily_cap: 7` → `effort_budget: {floor_min: 3, ceiling: 9}`.
2. **The weekly build (§9a)** already computes the surplus; it would now also print the **per-day unit
   row** next to the per-day count row. The existing rule — *an aggregate is not a schedule* — gets
   sharper, because a day at 5 problems/10.5 units is now visibly full while a day at 7 problems/5.5
   units is visibly not.
3. **Overflow pulls** stop being "you have room for one more" and become "you have 2.5 units left,"
   which naturally selects an Easy 🟢 rather than a Hard 🟡 — the exact call that went wrong tonight.
4. **The daily-cap guardrail** in the coach skill changes from a count comparison to a unit comparison.
   Nothing else about it moves; it is still a ceiling, still never cut into the 45-min active block.

---

## Resolved (Aug 7, 2026)

- **Does the SD lane consume units?** **Yes, flat 2.0.** Sunday is exactly where over-scheduling has
  been flagged twice, and the design session is real work competing for the same evening.
  - ⚠️ **REVERSED Aug 16, 2026 — SD consumes NO units.** The premise held (SD competes for the same
    evening); what changed is *where* that gets accounted. Lowering the ceiling 9.0 → 8.0 charges the
    competition **once, on every day**, instead of only on days carrying an SD slot — which is more
    honest, since self-directed SD study is not confined to the scheduled slot.
- **Is `q` one number, or per-day?** **One number, and it binds.** A per-day multiplier is deferred
  until the data shows one rather than assumed up front.
- **Should the floor bind?** The advisory floor (`ceil(demand)`, 7 u/day today) reports; **`floor_min`
  = 3.0 is the hard one.** A bad day still lands somewhere, but nothing forces a full day.

## Known limitation — retroactive pricing drifts

The script prices from the tracker's **current** state, so re-pricing a day that already ran gives the
*outcome* cost, not the going-in cost. Friday Aug 7 priced 8.0 units when it was built and re-prices at
7.8 now, because 110 has since become 🎓 (0.25) instead of 🟢 Easy (0.5). Harmless for the actual use —
budgeting a **future** day reads exactly the state that day will start from — but do not treat a
re-priced past day as the number that day was built against.

Multi-variant problems (130 BFS vs 130 Union-Find) are priced at **the dearer variant**, because which
one is scheduled is not recoverable from the number alone. The script says so on the line.

## First run against the live board

```
110 rows · demand 4.28 reps/day = 6.25 units/day (43.8/week)
advisory floor 7 u/day · hard ceiling 9 u/day · overdue: 16 rows, 12.5 units

Fri Aug 7 board (7 problems) ..........  7.8 / 9   ok, 1.2 spare
Fri Aug 7 as actually run (+269) ......  10.8 / 9  OVER by 1.8
Sat Aug 8 (6 problems) ................  7.5 / 9   ok, 1.5 spare
Sun Aug 9 (6 problems + SD lane) ......  8.5 / 9   ok, 0.5 spare
```

**The first line is the whole argument.** Friday's seven-problem board had room for one more *cheap*
problem — 1.2 spare buys two 🟢 Easies. What got pulled instead was a 🟡 Hard at 3.0 units, which is the
single most expensive item on the entire board, and it came back 🟡 with four bugs. Under the count cap
that pull read as "one over seven." Under the budget it reads as **20% over the ceiling**, and the
script names the cheaper alternative in the same breath.

---

*Companion: [`feedback_surplus_triggered_intake`](../../.claude/memory/feedback_surplus_triggered_intake.md)
computes demand as a rate; this doc computes its **cost**. Same arithmetic, different unit.*
