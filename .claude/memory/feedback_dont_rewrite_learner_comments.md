---
name: feedback_dont_rewrite_learner_comments
description: Never rewrite comments the learner wrote; flag what's inaccurate and let them reword it — the comment is their verbal-communication practice
metadata:
  type: feedback
reconciled: 2026-08-22
---

**Do not edit or rewrite a comment the learner wrote in their solution.** When a comment is
inaccurate or drifted, **say what's wrong and let the learner reword it themselves.** Describing the
fix is coaching; typing the replacement is taking the rep.

**Why:** The learner writes comments to practice **explaining their approach out loud** — the same
skill an interview grades in its first minutes. *"Let's try not to modify comments that users write
since that is practice for the users to be able to verbally communicate their thoughts"* (learner,
Aug 22, 2026, after the coach rewrote a drifted line-35 comment on 239). Rewriting it hands over the
articulation, which is the thing being trained. This is the "learner owns all thinking and writes all
code" principle, extended explicitly to **comments as communication reps**.

**How to apply:**
- A drifted/inaccurate comment → point at it and name the inaccuracy ("line 35 still describes the
  old size-based rule"), then stop. Let them reword.
- Even when the learner asks *"how do I fix this comment?"* — answer with **what it should convey**,
  not the finished sentence to paste.

⚠️ **Boundary vs [[feedback_coach_dates_helper_classes]]:** the coach DOES edit the learner's code
for pure **tooling artifacts** they explicitly delegated (dating a helper class for the stash/restore
collision) — because that naming is not something they'd write in real practice. A **comment
expressing their understanding is the opposite**: it IS real practice, so it stays theirs. Tooling
scaffolding → coach may touch; the learner's own reasoning (code logic, comments) → never.
