---
name: feedback-surplus-triggered-intake
description: Review demand is a rate (sum of 1/interval), not a headcount — measure surplus vs ~28 slots/week at every schedule build and gate pulls/extra intake on it, never on "NC150 is finished"
metadata:
  type: feedback
---

**Established Jul 26, 2026** when the learner asked whether the schedule runs out of problems as
intervals lengthen near the end of NC150. It does — and the old date-based rule would have missed it.

**The model:** each tracked row generates `1 / interval` reps per day. 🔴 +2 → 0.50/day · 🟡 +10 →
0.10 · 🟢 s1 +30 → 0.033 · 🟢 s2 +60 → 0.017 · 🏆 +180 → 0.006. **A retired problem generates 1/83rd
the load of a Blank** — retirement removes a problem from the schedule, it doesn't just label it.

**Capacity ≈ 28 problem-slots/week** (7 × 2 warmup slots × ~2 problems, −6 for the three SD lanes,
+6 active blocks).

**Calibrated Jul 26, 2026:** demand ≈ 35.6/wk vs 28 → **−8 over-subscribed.** That deficit *is* the
23-item stale 🟢 pile. Worth saying to the learner when it comes up: the backlog is **arithmetic, not
neglect**, and diligence cannot drain it while demand exceeds capacity. Only maturation or more
capacity closes it.

**The finding:** the hole opens **after** NC150, not before. During the roadmap, new intake keeps
feeding streak-1 rows at +30 (a heavy rate) and demand tracks capacity. When intake stops and the
population matures to +60/+180, demand falls to ~7/wk by late 2027 — **75% idle**.

**How to apply:**

1. **At every weekly schedule build, compute the surplus before slotting anything**: sum `1/interval`
   across the tracker, ×7, subtract from 28.
2. **Gate pulls and extra intake on that number, never on a date.** This supersedes *"no application
   pulls during the NC150 milestone"* — correct only while over-subscribed, and silently wrong once
   demand crosses below capacity (projected Oct–Dec 2026, with two phases still open).
3. **Fill order:** ≤0 → reviews only · 1–5 → [[feedback_consolidation_reps]] · 6–12 → + application
   pulls · 13+ → + open Tier 1 advanced early.
4. **Consolidation reps fill first** — NC150 supplies 1–2 problems per technique where 3–4 are needed,
   so that queue is large, aimed at [[feedback_phase_exit_per_algorithm]], and higher-ROI than reaching
   for Tier 2 material early.
5. **Don't read a shrinking review list as being ahead.** It's the intervals doing their job, and it
   means capacity needs redirecting, not banking.
