---
name: feedback_end_of_week_schedule
description: Generate the next week's schedule file before closing out the last session of the week
metadata:
  type: feedback
reconciled: 2026-08-31
---

At the end of the last session of the week (or whenever the user closes out a week), generate the next week's schedule file at `docs/foundations/schedules/<YYYYMMDD>_schedule.md` before pushing.

**Why:** User noticed the Jun 29 week schedule was never created — the week started with no schedule file. The weekly schedule is the primary daily driver; it must exist before the week begins.

**How to apply:** When closing out a week's final session, check if next week's schedule file exists. If not, build it using:
1. The current week's preview section (carries forward shakys, retries, overdue backlog)
2. `dsa_progress.md` — scan for all problems with `Next Review Date` falling in the coming week
3. The phase plan (from `study_guide.md`) for active block topics
4. Daily load: priced in **units** against the ceiling in `cse.config.yml` (`scripts/effort_budget.py`), not as a problem count
4b. **Refresh the technique comfort audit — `python scripts/technique_comfort_audit.py`** (added to
   this list Aug 30, 2026; the step shipped in CLAUDE.md on Aug 22 and this file was never updated).
   Its top "Needs work" callout is the **pull-order source** for the whole build:
   **zero-green conversions and their coverage siblings > overdue 🟢 cleans > thin-green fills +
   probes.** Fill any why-line the script flags. See `decisions.yml` `technique-comfort-audit`.
4c. **Fill under-ceiling days toward the ceiling with weak-technique work rather than deferring it**
   (Aug 23, 2026) — same priority order as 4b, and prefer a NEW sibling over pulling an existing
   review forward. A coverage sibling's candidate pool is a **company frequency pull first**
   (`pull_interview.py --technique <t>`), hand-picked only if the pull yields too little — say so in
   the build when it does. See `decisions.yml` `fill-capacity-with-weak-coverage` and
   `coverage-sibling-pulled-not-authored`, and [[feedback_surplus_triggered_intake]]
5. Sunday = the SD **mock** (the three-lane "sprint" was retired Aug 13, 2026 — [[project_sd_mock_model]]).
   ⚠️ **Place it, never price it**: SD has been unpriced since Aug 16, 2026 and the 8.0 ceiling is
   DSA-only, sized so the leftover evening is SD's. `system_design.cadence` decides how many slots a
   week gets. *(Caught Aug 21, 2026 during the reconcile pass — this step still said "sprint".)*

At the same time, archive the current week's schedule by moving it to `docs/foundations/schedules/archive/`. Both happen together — archive current, generate next — in a single commit before pushing.
