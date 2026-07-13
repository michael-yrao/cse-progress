---
name: feedback_phase_gated_blanks
description: A 🔴 Blank on an un-taught technique is a premature attempt — phase-gate it, don't churn it in the +2 retry loop
metadata:
  type: feedback
---

Before treating an overdue 🔴 Blank as urgent, check whether its **technique has actually been taught yet** (i.e. whether its phase in `study_guide.md`'s roadmap has happened).

A Blank on a technique with no foundation is a **premature attempt**, not a spaced-repetition failure. The +2-day loop assumes *forgetting* — but there was never any encoding to forget, so retrying just re-blanks it, resets to +2, and churns forever while inflating the backlog signal.

**Why:** the Jul 12, 2026 backlog audit flagged "5 urgent 🔴s." Two (1216 Valid Palindrome III ×2, attempted May 31) were premature — their phases are Backtracking (Sep 14) and 1D DP (Oct 12). The user caught it: *"they were not re-scheduled since they did not fit the categories we were targeting."* Real 🔴 backlog was 3, not 5.

**How to apply:**
- **Phase-gate it:** move the row out of the review table into the **Knowledge Expansion Queue** with an explicit trigger ("pull into rotation when the <X> phase opens (<date>)"), noting the prior attempt date + 🔴.
- **Do NOT** just set a far-future `Next Review Date` in the review table — `update_review_dates.py` recomputes it as `latest_attempt + interval(comfort)`, so it snaps straight back to permanently-overdue.
- **Check for orphans too:** a problem whose technique appears in **no phase at all** (912 Sort an Array / Merge Sort — there is no sorting or divide-and-conquer phase in the whole Jun–Dec roadmap) will never surface naturally. Either park it in the queue, or close it as a deliberate one-off. User chose to close 912 as a one-off (foundational, ~20 lines, 🔴 since January).
- Same trigger mechanism as [[feedback_method_variant_promotion]].
