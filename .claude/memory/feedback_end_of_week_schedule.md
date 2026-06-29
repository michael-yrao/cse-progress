---
name: feedback_end_of_week_schedule
description: Generate the next week's schedule file before closing out the last session of the week
metadata:
  type: feedback
---

At the end of the last session of the week (or whenever the user closes out a week), generate the next week's schedule file at `docs/foundations/schedules/<YYYYMMDD>_schedule.md` before pushing.

**Why:** User noticed the Jun 29 week schedule was never created — the week started with no schedule file. The weekly schedule is the primary daily driver; it must exist before the week begins.

**How to apply:** When closing out a week's final session, check if next week's schedule file exists. If not, build it using:
1. The current week's preview section (carries forward shakys, retries, overdue backlog)
2. `dsa_progress.md` — scan for all problems with `Next Review Date` falling in the coming week
3. The phase plan (from `study_guide.md`) for active block topics
4. Daily cap: 4 warmup slots + 1 active block = 5 problems max per day
5. Sunday = system design sprint (no active block)

Commit and push the new schedule file along with the rest of the end-of-session commit.
