---
name: feedback_end_of_week_schedule
description: Generate the next week's schedule file before closing out the last session of the week
metadata:
  type: feedback
reconciled: 2026-08-21
---

At the end of the last session of the week (or whenever the user closes out a week), generate the next week's schedule file at `docs/foundations/schedules/<YYYYMMDD>_schedule.md` before pushing.

**Why:** User noticed the Jun 29 week schedule was never created — the week started with no schedule file. The weekly schedule is the primary daily driver; it must exist before the week begins.

**How to apply:** When closing out a week's final session, check if next week's schedule file exists. If not, build it using:
1. The current week's preview section (carries forward shakys, retries, overdue backlog)
2. `dsa_progress.md` — scan for all problems with `Next Review Date` falling in the coming week
3. The phase plan (from `study_guide.md`) for active block topics
4. Daily load: priced in **units** against the ceiling in `cse.config.yml` (`scripts/effort_budget.py`), not as a problem count
5. Sunday = the SD **mock** (the three-lane "sprint" was retired Aug 13, 2026 — [[project_sd_mock_model]]).
   ⚠️ **Place it, never price it**: SD has been unpriced since Aug 16, 2026 and the 8.0 ceiling is
   DSA-only, sized so the leftover evening is SD's. `system_design.cadence` decides how many slots a
   week gets. *(Caught Aug 21, 2026 during the reconcile pass — this step still said "sprint".)*

At the same time, archive the current week's schedule by moving it to `docs/foundations/schedules/archive/`. Both happen together — archive current, generate next — in a single commit before pushing.
