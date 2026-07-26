---
name: feedback-gate-on-internal-state
description: Never gate a study milestone on an offer, interview result, or application date — every trigger must resolve against something measurable in the repo (rating, streak, surplus, pull rate)
metadata:
  type: feedback
---

**Set by the learner Jul 26, 2026:** *"let's not worry about the offer and worry about the timeline
only. While it is important for me to get an offer financially, for my growth as an engineer for the
purposes of cse-coach and cse-progress, it has no real significance. And it is also too dependent on
outside factors that we cannot predict."*

**The rule:** no milestone in the study system — phase exit, ROI-line crossing, Tier 1 or Tier 2
opening, cadence changes — is **ever** gated on an offer, an interview outcome, or an application
date. Every gate resolves against something **measurable in this repo**: a comfort rating, a streak, a
computed surplus, a pull diagnostic rate, a per-algorithm coverage count.

**Why:** external outcomes are unpredictable and largely outside the learner's control, so a study
trigger hanging on one either stalls indefinitely or lurches for reasons unrelated to what's actually
been learned. It also inverts the purpose — the system exists for engineering growth, and an offer is a
financial event that happens to correlate. Correlation is not a gate.

**How to apply:**

1. When proposing any trigger, ask **"could I evaluate this by reading files in this repo?"** If the
   answer needs a recruiter, a calendar, or someone else's decision, it's the wrong trigger — find the
   internal proxy. (Example: the readiness *behind* an application date is SD lanes reaching
   Transition/Mastery; gate on that, and let the date follow.)
2. **The job search still informs *what* is worth learning** — interview ROI is a legitimate input to
   curriculum priority ([[feedback-roi-promotes-to-curriculum]]). It just never determines **when**
   you're ready to move on.
3. Keep the two separated by file: job-search planning lives in `career/career_trajectory.md` and the
   company-tier tables in the DSA study guide; study gates live with the mechanics they measure.
4. I proposed offer-gating for the ROI-line crossing on Jul 26 and was corrected before it was written
   to disk. Watch for it recurring — it's a tempting framing precisely because the timelines *look*
   like they line up.
