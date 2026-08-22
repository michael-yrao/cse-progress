---
name: feedback-consolidation-reps
description: A technique needs MULTIPLE problems, not one — near-identical siblings are the training signal (their minor differences are what recognition grades), and they don't count against the new-algorithm intake cap
metadata:
  type: feedback
reconciled: 2026-08-21
---

**Set by the learner Jul 26, 2026:** *"we need multiple problems of the same flavor for users to
actually knock down the technique, even if they look similar enough — users need the repetition and
be able to recognize the minor differences."*

**The rule:** intake has **two classes**, and the difficulty-tiered cap governs only the first.

| Class | Definition | Expected | Cascade | Against the cap? |
|---|---|---|---|---|
| **New-technique** | first problem of an algorithm | 🔴 | ~2–3 warmup slots over a fortnight | **yes** (3/4/5 by tier) |
| **Consolidation rep** | another problem in a technique already at 🟡+ | 🟡/🟢 | none | **no** — separate ≤2/week budget |

**Why:** one problem per technique trains **recall of that problem's solution**, not the technique —
there's no variation to generalize across, so what's learned is "743 is the Dijkstra one," a lookup
rather than a skill. Transfer requires multiple surface forms of one underlying idea, and the **minor
differences between near-identical problems are the training signal, not redundancy**: cost-as-max vs
cost-as-sum, multiplicative vs additive relaxation, hop-capped vs unbounded. That discrimination is
exactly what the [[feedback_recognition_gate]] front-gate grades, and it is untrainable from a single
instance.

**The cap never applied to these anyway** — its own stated rationale is the *blank tax*: "a 🔴 costs 1
active slot plus ~2–3 follow-up warmup slots as its Blank-interval retries settle." That is the cost of learning an
algorithm. A sibling in a known technique produces no 🔴 and no cascade, so charging it against a
new-algorithm budget was a category error ([[feedback_difficulty_tiered_intake]] still holds, unchanged,
for its actual class).

**How to apply:**

1. **"Similar to one already done" is an argument FOR scheduling it, not against.** This reverses the
   usual redundancy instinct — check that instinct whenever declining a problem.
2. **Gate: base technique must be 🟡 or better.** Siblings consolidate a half-formed technique (that's
   the point — interleaving while it settles is what makes it stick), but against a 🔴 they just
   double-blank. Teach first, then consolidate.
3. **Slot them lighter than new-technique problems** — closer to a review of a technique than an intake
   of one. Active block if the problem is Hard, generous warmup otherwise.
4. **Aim for ~3–4 problems per technique** before treating it as covered, spanning the meaningful
   variations rather than repeating the same shape.
5. Distinct from [[feedback_method_variant_promotion]]: that is *many techniques on one problem* and is
   gated on the base retiring. This is *one technique across many problems*, gated only at 🟡. Different
   axis, different gate — don't apply one rule's gate to the other.
