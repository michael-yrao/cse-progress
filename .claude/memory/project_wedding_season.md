---
name: project_wedding_season
description: Learner is busy with wedding preparation from Oct 5 through Nov 29, 2026; Nov 30, 2026 is the first day out of the wedding season. Do not cut the load; adapt the teaching of Backtracking, 1D DP and 2D DP when a signal shows it is needed.
metadata:
  type: project
reconciled: 2026-10-05
---

Set by the learner Oct 5, 2026, right after the Oct 5 weekly build: *"from now until nov 30th, i will be
quite busy because i am preparing for my wedding. nov 30th is the first day out of my wedding season."*

- **Window:** Oct 5 – Nov 29, 2026. **Nov 30, 2026 is the first normal day.**
- It covers the rest of Backtracking, all of 1D DP (Oct 12 – Nov 8) and the first three weeks of 2D DP.
- **Intake stays at `effort_budget.intake_per_week` (currently 2) through Nov 29; from Nov 30 it can ramp
  back up.** Learner, Oct 10, 2026: *"we are at 2 new per week until nov 30th, then it can ramp back up."*
  The ramp is a decision for the first weekly build on or after Nov 30, priced with
  `backlog_forecast.py --check` as the `scheduling` skill requires, never a pre-emptive edit. Until then
  the phase-table dates in `study_guide.md` (1D DP to Nov 8, 2D DP to Dec 6, Bit-Math to Dec 28) are
  known to run long; do not re-date them for the wedding window, and do not read the slip as a reason
  to raise the rate early.
- [[project_november_breaks]] (two light-maintenance weeks, ~Nov 1–7 and ~Nov 24–30, set Aug 6) sits inside
  this window. That file's dates were approximate; treat Nov 30 as the return day.

**Correction, same day (learner):** *"i don't want to drop problems because of this but i do want to make
you aware so that you can adjust my learning if needed since backtracking, 1DP and 2DP are tough learns."*
The first version of this file read "busy" as "cut the load". That was wrong.

**Why:** the three hardest phases left (Backtracking, 1D DP, 2D DP) land while the learner has less
attention to spare. The learner wants the coach to know that, so the teaching can adapt. The volume is
not the lever.

**How to apply:**
- **Do not drop, thin or pre-emptively defer problems because of this window.** Build each week as usual
  (the ceiling is still the daily goal, `effort-budget.md`). Do not ask "which days are you free" at the
  build. A row moves only when the learner moves it or a day actually slips (gate 6).
- **Adjust the learning, not the count, and only when a signal shows it is needed:** a new pattern that
  comes back 🔴 twice, the same failure category repeating across sibling problems, or sessions running
  long. Then propose one concrete change and let the learner decide. Examples: a concept primer before a
  new DP pattern, a proper teach in place of another cold retry, one more sibling on the pattern just
  learned before the next pattern opens, splitting a teach and its first rated rep across two days.
- The DP rule from [[project_november_breaks]] still holds: no brand-new DP pattern in the 2–3 days before
  a stretch the learner will be away.
- Phase dates in `study_guide.md` are checkpoints, not deadlines ([[feedback_phase_progression]]).
- From Nov 30, 2026 this file is history.
