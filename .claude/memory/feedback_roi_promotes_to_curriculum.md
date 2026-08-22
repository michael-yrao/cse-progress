---
name: feedback-roi-promotes-to-curriculum
description: NC150 is the STARTING point for high-ROI, not the ceiling — anything with genuine interview ROI belongs in the study guide curriculum, never parked in the Knowledge Expansion Queue
metadata:
  type: feedback
reconciled: 2026-08-21
---

**Set by the learner Jul 26, 2026.** The Knowledge Expansion Queue is for material that is
**below the Interview-ROI line** — depth, enrichment, competitive-programming reach. It is **not**
a holding pen for things that are genuinely interview-relevant but happen to sit outside NC150.

**The rule:** when something surfaces that has real interview ROI, **add it to the study guide's
phase curriculum**, even if it isn't in NC150. NC150 is the *floor* of the high-ROI set, not its
boundary.

**Why:** NC150 is a curated starting list, not a complete map of what gets asked. Treating it as the
boundary means a genuinely common interview topic gets filed next to segment trees and Aho-Corasick —
material deliberately deferred as *low* ROI — and the queue's "pull when the phase opens" gating then
guarantees it never gets scheduled. The learner caught this when Floyd-Warshall (the missing fourth
of the shortest-path family, ~5 lines to write) was parked in the queue purely because it isn't an
NC150 problem. Parking is a statement about ROI; making it for the wrong reason mis-prices the topic.

**How to apply:**

1. **Triage on ROI, not on list membership.** Ask "would a strong candidate be expected to know this?"
   not "is this in NC150?"
2. **Promote into the phase it belongs to** in `docs/foundations/dsa/study_guide.md` (phase table +
   any per-phase notes), and update that phase's **new-problem count** so the intake cap arithmetic
   and the phase-completion bar ("N of M 🎓 Graduated") stay honest.
3. **Curriculum scope ≠ schedule timing.** Promoting something into a phase says it is *in scope*;
   it does **not** override the difficulty-tiered intake cap ([[feedback_difficulty_tiered_intake]]).
   A promoted item still waits for a real slot. Say the new count out loud when promoting — a phase
   quietly growing from 7 to 9 moves the completion bar.
4. **Say what you did NOT promote and why.** The rule is "worthy ROI gets added," which only means
   something if the bar is applied honestly in both directions. Redundant-with-something-already-done
   is the most common reason to decline.
5. The queue keeps its two legitimate jobs: **below-the-line depth**, and **phase-gated 🔴s**
   ([[feedback_phase_gated_blanks]]).

Related: [[feedback_method_variant_promotion]] (a second *method* on a solved problem is still gated
on the base retiring — that gate is about rep economics, not ROI, and this rule does not loosen it).
