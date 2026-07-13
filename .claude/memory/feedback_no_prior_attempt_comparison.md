---
name: feedback_no_prior_attempt_comparison
description: When giving feedback on an attempt, judge today's code on its own; never read or reference the folded PRIOR ATTEMPTS region
metadata:
  type: feedback
---

When the user asks "what's the issue with my implementation?", point at the bug **in the code they wrote today** and stop. Do **not** open, read, or cite the `# region ⚠ PRIOR ATTEMPTS — SPOILERS` block — not to compare approaches, not to say "your last attempt had this right," not as evidence for a comfort rating.

**Why:** The region is folded by design so a retry is recall from a blank page (see [[feedback_no_spoilers]]). Narrating what the old solution did drags the spoiler back into the conversation and turns feedback into a diff against an answer the user was deliberately not looking at. The user's words: *"When I ask what the issues are, you help me point in the right direction — this is the whole point of the hint feedback."* Feedback is a hint aimed forward, not a comparison aimed backward.

**How to apply:** Read only from the dated attempt stub down to the region marker. Diagnose with a **failing case** ("on `[1,2,3]` this returns 5, not 6") and let the user find the fix. The comfort rating is inferred from today's session — hints given, bugs self-caught — never from resemblance to a previous solution. Instance of [[feedback_operating_principles]] P2 (the user owns the thinking).
