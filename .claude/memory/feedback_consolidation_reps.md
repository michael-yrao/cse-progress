---
name: feedback-consolidation-reps
description: A technique needs MULTIPLE problems, not one — near-identical siblings are the training signal (their minor differences are what recognition grades), and they don't count against the new-algorithm intake cap
metadata:
  type: feedback
reconciled: 2026-08-28
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
   - ⚠️ **"~3–4" is the DEFAULT, not a cap — the operative clause is *spanning the meaningful
     variations*.** Where a technique genuinely has more distinct flavours than that, the honest bar is
     the flavour count, set per-technique via `min_problems` in `techniques.yml` (the same mechanism that
     drops Dutch National Flag to 1). **Intervals was raised to 5 on Aug 28, 2026** for exactly this
     reason: merge-by-start, insert-into-sorted, schedule-by-end, max-concurrent sweep-line, and
     two-list intersection are five different procedures, not five phrasings of one. A technique sitting
     at "3/3, bar met" while three of its flavours have never been written is the failure this bullet
     exists to prevent — see `decisions.yml` `interval-flavours-declared`.
5. Distinct from [[feedback_method_variant_promotion]]: that is *many techniques on one problem* and is
   gated on the base retiring. This is *one technique across many problems*, gated only at 🟡. Different
   axis, different gate — don't apply one rule's gate to the other.

## ⚠️ Sibling gate is 🟡+, NOT `green:base` (added Aug 23, 2026)

**A thin-technique coverage sibling gates on the standard `🟡+` consolidation gate — never on the base
problem going 🟢 first.** The `green:base` hold (224 waited on `green:150`; the Floyd Fast/Slow variant
on `green:202`) was stricter than this rule and **counterproductive for a thin technique**: a second
problem is another path to the technique's *first* 🟢 and trains the transfer that re-repping one problem
cannot — so gating coverage behind the base going green can **deadlock** a technique stuck at 🟡.

**Why:** the goal for a thin technique is *coverage* (3–4 surface forms). Requiring the single existing
problem to reach 🟢 before a second may enter means a technique that keeps hovering at 🟡 never gets the
second surface form that would actually teach it. The learner's framing (Aug 23): *"for the techniques
without proper coverage, we can drop the gate on another problem being green."*

**How to apply:** a sibling is schedulable once the base is **🟡 or better** (the standard gate). **One
guard retained** — the thing `green:base` was a blunt proxy for:

> A 🟡 that was **heavily coach-guided** (near-🔴 — multiple coach-supplied fixes, per the stuck_log) is
> treated as 🔴 for sibling purposes → convert/teach first, no sibling yet. Against a genuinely-unlearned
> base a sibling just double-blanks (§2a).

**The distinction is 🟡 *quality*, and it is a judgement:** 150 (clean-🟡, recognition hit / execution
slip) → sibling OK; 239 (🟡 after *three* coach fixes Aug 22) → convert first. See
`decisions.yml` `sibling-gate-yellow-not-green`. Related: [[feedback_surplus_triggered_intake]] (when to
spend capacity on this coverage), [[feedback_coverage_gap_ledger]].
