---
name: feedback_new_vs_retry
description: When building a weekly schedule, only call a problem "new" if it comes from the study_guide roadmap phase AND has no existing tracker row
metadata:
  type: feedback
---

A weekly schedule's "New Problems This Week" table must contain only genuinely new problems. The source of new problems is the **Study Roadmap phase table** in `docs/foundations/core/study_guide.md` (the `New Problems` column for the phase covering the current dates). Everything else in a schedule — warmups and active blocks alike — is a retry/review pulled from `dsa_progress.md` by next-review due date.

**Litmus test before listing anything as "new":** if the problem already has a row in `dsa_progress.md` with past attempt dates, it is a retry, not new — it belongs in a backlog/vintage table, never in "New Problems."

**Why:** A prior schedule listed 42. Trapping Rain Water as a new problem in the week of Jun 29, even though it was an April-vintage retry already tracked since 2026-04-15 (and was already correctly listed in the same file's "April Vintage Cleared" table). User caught the double-listing and asked where new problems come from.

**How to apply:** When generating a weekly schedule, cross-check every "New Problems" candidate against (1) the roadmap phase list in `study_guide.md` and (2) the absence of an existing `dsa_progress.md` row. If it fails either check, move it to the appropriate backlog/overdue table instead. See [[feedback_schedule_mistakes]] for the related out-of-order detection rule.
