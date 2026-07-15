---
name: feedback_difficulty_tiered_intake
description: New-problem intake is tiered by category difficulty, not flat 5/week — hard/algorithm-dense categories cap at 4/week, DP at 3
metadata:
  type: feedback
---

New-problem intake is **difficulty-tiered**, not a flat 5/week:

- **Moderate** (Standard Graphs, Heap, Tries, Sliding Window, Stack, Intervals+Greedy, Bit-Math): **4–5/week**
- **Hard, algorithm-dense** (Advanced Graphs, Backtracking): **4/week — not 5**
- **DP phases** (1D, 2D): **3/week**

**Why:** the *blank tax*. A hard-category new problem introduces a new algorithm per problem
(Dijkstra, Bellman-Ford, MST, Eulerian…), so the first attempt almost always logs 🔴, and every 🔴
spawns a +2-day retry that consumes a warmup slot. Empirically each new hard problem is a ~3-slot
commitment over its first fortnight (1 active + ~2–3 retry warmups), not 1 slot. At 5/week that
cascade eats ~40% of the 28 weekly warmup slots servicing *recent* material, starving the backlog —
which is why the 🟢 pile sat at 35 and wouldn't drain. Established Jul 14, 2026 after Advanced Graphs
(mis-bucketed as "moderate") produced back-to-back 🔴 on 743 Dijkstra + 787 Bellman-Ford in one week.

**How to apply:** when building a weekly schedule (see [[feedback_end_of_week_schedule]]) for a hard-cat
or DP phase, cap new intake at the tier above and route the freed active-block slot to a coded backlog
burn-down. Defer the lowest-interview-ROI new problem first, re-slotting it in the same edit
([[feedback_daily_cap]] schedule-integrity). Source of truth: `study_guide.md` Pace Targets.
