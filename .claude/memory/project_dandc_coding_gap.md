---
name: project_dandc_coding_gap
description: Learner understands D&C conceptually but has a recurring gap CODING the recursion; the framing that unlocked it (Jul 25)
metadata:
  type: project
reconciled: 2026-08-30
---

The learner repeatedly stalls on **coding** divide-and-conquer (merge sort, 912) despite
understanding the approach — *"I know the approach but have no clue how to code it up."* The
block is the recursion structure, not the strategy.

**What unlocked it (Jul 25, 912 teaching session):**
- **Leap of faith** — stop tracing the recursion all the way down; *assume* each recursive
  call returns its sub-array correctly solved. Your only job at this level is the combine step.
- **Uniform return contract** — every call returns the same thing: its input, sorted. Base case
  (len ≤ 1) satisfies it trivially; recursive case satisfies it by merging two sorted halves.
- **"D&C is a strategy, not a framework"** — there's no `divide()` + `conquer()` pair. One
  recursive function does it all: **divides on the way down, merges on the way up** ("one down
  the stack, one up the stack"). The merge is a flat helper only because the weaving logic is long.
- Binary split (2 halves per call, log n deep) — *not* n arrays at once; it's a call stack of
  depth log n.

**RESOLVED Jul 29, 2026 — the teaching worked; the gap is closed.** The rated measurement (912
merge sort, Jul 29) came back **🟡, but for a different reason entirely**: the whole D&C skeleton
was written cold and correct — base case, binary split, recurse both halves, merge the two returns,
uniform return contract. The only defect was `result.append(leftArray[li:])` instead of `extend`,
so `merge([5],[2])` returned `[2, [5], []]`.

**FULLY CLOSED Aug 8, 2026 — 912 came back 🟢 s1 (→ Sep 7), its first clean after three 🟡s.** Skeleton and
Python API both cold and correct; the `extend` slip was sidestepped with explicit drain loops. The
complexity answer was the strongest signal: asked to disambiguate "the recursion is O(n)", the learner
separated **call-stack depth O(log n)** from **retained slices `n + n/2 + n/4 + … = O(n)`** unaided — the
sharp form of the recursion-stack family, not the memorized one.

**The generalizable lesson, which outlives this row:** *three consecutive 🟡s on one problem were three
unrelated defects* (conceptual Jul 25 → Python API Jul 29 → nothing Aug 8), and the same pattern appeared
on **560 the same day** (map contents Jul 29 → lookup sign Aug 8). A repeat non-Clean rating is **not**
evidence of a repeating cause. Diff the stuck-log entries before firing §2a's teach reflex; the trigger is
*the same gap* missed repeatedly, not *the same row* rated low repeatedly. See [[feedback_infer_comfort]].

**Why / how to apply:** the framings above are the ones that landed — reach for them if D&C stalls
again (procedure-first, [[feedback_procedure_first]]). But **do not re-teach D&C to this learner on
the strength of another 🟡 on 912.** The failure mode has moved **conceptual → Python API**, and
§2a's "a repeat 🔴/🟡 means it was never encoded, so teach it" reflex misfires when the *category*
of the error changes. Read the stuck-log entry, not just the rating: three consecutive 🟡s on one
row can be three unrelated defects. Watch list-API slips (`append` vs `extend`, in-place vs
returning) on the next rep, not the recursion.
