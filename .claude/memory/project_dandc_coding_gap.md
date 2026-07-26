---
name: project_dandc_coding_gap
description: Learner understands D&C conceptually but has a recurring gap CODING the recursion; the framing that unlocked it (Jul 25)
metadata:
  type: project
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

**Why / how to apply:** this is a recurring, never-durably-encoded gap — reach for these exact
framings when D&C code stalls (procedure-first, [[feedback_procedure_first]]). The Jul 25 rep was
a **teaching session, unrated** ([[feedback_recognition_gate]] not the issue — this is §2a
teach-then-measure); the **rated** measure is the 912 merge-sort re-rep **Jul 29**. If that comes
back shaky, the structure still hasn't stuck — teach the same framing, don't just re-rep.
