---
name: project_familiarity_engine_revisit
description: OPEN — revisit at the Sep 7 build how the familiarity discount interacts with DAILY packing; discounted units understate the indivisible cost of the next problem.
metadata:
  type: project
reconciled: 2026-09-03
---

**Open design question, raised by the learner Sep 3, 2026 — revisit at the Sep 7 build.**

## The observation

With familiarity discounting live ([[decisions]] `familiarity-discounting`), repricing a near-full day
*downward* surfaces small per-day slack that **cannot actually seat another problem**:

- Sat Sep 5: 8.0 → **7.8** (0.2 spare) · Sun Sep 6: 8.0 → **7.2** (0.8 spare) · Fri Sep 4: 6.5 (1.5 spare).
- The cheapest *useful* add is a 🟢 backlog item at ~0.8–1.0 or a 🟡 at ~2.0. The freed slack is smaller
  than the smallest real unit of work.

Learner: *"diff is not big enough to put in another problem tbh with the new engine."*

## The tension to examine

The discount lowers the **accounting cost** of a familiar rep, but **a problem is still an indivisible
chunk of attention** — repricing it down did not make it take less time to sit and do. So `units-to-ceiling`
now **over-reads as available capacity**: a day can show 0.8 spare while having zero room for the next
indivisible problem. The number is doing two jobs that the discount pulls apart:

| Use of the number | Does the discount help? |
|---|---|
| **Demand-rate / library carrying capacity** (steady-state load, `Σ 1/interval`) | **Yes, genuinely** — familiar reps really do generate less load over time. Demand fell 5.4 → 3.7 u/day honestly. |
| **Packing a single day to the ceiling** | **Questionable** — the ceiling is an *attention* judgment, and a familiar problem's attention cost is not what the discount says. |

## Candidate framings to decide between (Sep 7)

1. **Two prices, two uses.** Keep the discounted price for the demand-rate / capacity calc, but pack a
   *day* against something closer to the **nominal/cold** price — or against the explicit test *"does the
   next indivisible problem fit?"* rather than *"units to ceiling."*
2. **Accept it as correct — freed capacity is a WEEK-level lever, never a cram.** The discount's whole
   point is that familiar days are lighter, so the surplus should be spent at the next **build**
   (intake, slip items), not by adding to a near-ceiling day. Under this reading the fragmented per-day
   slack is a feature: it banks into the next week's larger surplus. This is consistent with the
   existing guardrail *never raise the ceiling to chase a backlog* — [[feedback_midweek_reprice]].
3. **Watch the failure mode either way:** the reprice must never tempt seating a permanent new problem
   into a day just because `units-to-ceiling` grew, when the problem's real attention cost is unchanged.

## Decision for now (Sep 3)

Framing #2 in practice: **did not seat new work into this week's freed per-day slack.** Let the Sep 7
build absorb the week-level surplus. Revisit whether packing should use a separate (cold/nominal or
slot-count) measure then — decide #1 vs #2 explicitly rather than leaving it implicit.

See [[decisions]] `familiarity-discounting`, `docs/foundations/effort_budget.md` (familiarity section).
