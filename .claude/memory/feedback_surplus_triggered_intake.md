---
name: feedback-surplus-triggered-intake
description: Review demand is a rate (sum of 1/interval), not a headcount — measure surplus in UNITS against the effort ceiling at every schedule build and gate pulls/extra intake on it, never on "NC150 is finished"
metadata:
  type: feedback
reconciled: 2026-08-21
---

**Established Jul 26, 2026** when the learner asked whether the schedule runs out of problems as
intervals lengthen near the end of NC150. It does — and the old date-based rule would have missed it.

<!-- single-source-ok: DERIVATION — the intervals are inputs to `1 / interval`. -->
**The model:** each tracked row generates `1 / interval` reps per day. 🔴 +2 → 0.50/day · 🟡 +10 →
0.10 · 🟢 s1 +30 → 0.033 · 🟢 s2 +60 → 0.017 · 🎓 +180 → 0.006. **A graduated problem generates 1/83rd
the load of a Blank** — retirement removes a problem from the schedule, it doesn't just label it.

⚠️ **Capacity is now UNITS, not problem-slots (Aug 7, 2026).** The retired formula was
*"≈ 28 problem-slots/week — 7 × 2 warmup slots × ~2 problems, −6 for the three SD lanes,
+6 active blocks"*, and all three of its inputs are now gone:
the problem count was replaced by the effort budget, the three SD lanes were retired Aug 13, and
SD stopped being charged against the day on Aug 16. **Don't hand-compute it — `scripts/effort_budget.py`
prints demand and capacity in units** from the config's own ceiling. The demand model below is
unchanged and is exactly what that script sums.

**Calibrated Jul 26, 2026:** demand ≈ 35.6/wk vs 28 → **−8 over-subscribed.** That deficit *is* the
23-item stale 🟢 pile. Worth saying to the learner when it comes up: the backlog is **arithmetic, not
neglect**, and diligence cannot drain it while demand exceeds capacity. Only maturation or more
capacity closes it.

**The finding:** the hole opens **after** NC150, not before. During the roadmap, new intake keeps
feeding streak-1 rows at +30 (a heavy rate) and demand tracks capacity. When intake stops and the
population matures to +60/+180, demand falls to ~7/wk by late 2027 — **75% idle**.

**How to apply:**

1. **At every weekly schedule build, run `scripts/effort_budget.py` before slotting anything.** It sums
   `1/interval` across the tracker and prices it against the ceiling — the arithmetic this rule used to
   describe by hand as "×7, subtract from 28".
2. **Then write the per-day row — the surplus measures the WEEK, not the DAY.** A negative weekly
   surplus does *not* mean every day is full; the SD slot and doubled warmups land unevenly, so a
   deficit week routinely holds days well under the ceiling. **Slipping reviews off a week that still
   has slack days is a false shortage and costs real reps.** Any under-cap day absorbs items back off
   the slip list, preferring ones **already due that day** (those aren't pulled forward at all — they
   just stop slipping). Only then is the slip list final. *Found Jul 27, 2026: a −7.3 build slipped
   12 🟢 while Wed carried 1 problem and Sun carried 2; four came straight back. The arithmetic was
   right and the conclusion drawn from it was wrong — **an aggregate is not a schedule.***
3. **Gate pulls and extra intake on that number, never on a date.** This supersedes *"no application
   pulls during the NC150 milestone"* — correct only while over-subscribed, and silently wrong once
   demand crosses below capacity (projected Oct–Dec 2026, with two phases still open).
4. **Fill order:** ≤0 → reviews only · 1–5 → [[feedback_consolidation_reps]] · 6–12 → + application
   pulls · 13+ → + open Tier 1 advanced early.
5. **Consolidation reps fill first** — NC150 supplies 1–2 problems per technique where 3–4 are needed,
   so that queue is large, aimed at [[feedback_phase_exit_per_algorithm]], and higher-ROI than reaching
   for Tier 2 material early.
6. **Don't read a shrinking review list as being ahead.** It's the intervals doing their job, and it
   means capacity needs redirecting, not banking.
