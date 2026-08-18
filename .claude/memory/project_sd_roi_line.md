---
name: project_sd_roi_line
description: The L6 big-tech ROI bar for SD questions and how to apply it — the board is now HelloInterview's 35 questions (Aug 13, 2026); the old systemdesign.io triage survives only as a compressed decline list
metadata:
  type: project
reconciled: 2026-08-17
---

⚠️ **Superseded in part, Aug 13, 2026.** The board is no longer systemdesign.io — SD is now mock
interviews on **HelloInterview's 35 questions** ([[project_sd_mock_model]]). The *bar* below still governs
every add/decline; the 55-question triage is now a compressed decline table at the bottom of
`senior_ramp.md`. **Do not re-derive that catalog.**

**The bar, verbatim:** *would a strong L6 candidate at Meta/Apple/Netflix/Google/Amazon be expected to
handle this in a 45-minute round?* Three consequences do most of the sorting: **depth over breadth**
(redundancy is the most common decline, not difficulty) · **distributed-systems altitude only** (an LLD
question rehearses [[feedback_hld_altitude]], the learner's known failure) · **no domain weighting**
(fintech is a waypoint per [[project_interview_goal]], so Payment System and Robinhood sit off the
rotation behind `waypoint_loop:fintech` even though HelloInterview rates them Hard).

⚠️ **Two deferral bins, and the distinction is whether a trigger CAN exist** — not quality. Corrected the
day it was written: the two fintech designs were filed beside IoC/DI and Botnet, and the learner
challenged it. They are *the right thing aimed at the wrong employer* — a state with a real trigger —
while off-altitude declines can never fire. **If you want to write a trigger on a declined item, it is
misfiled.**

**Still live under the new board:** the designs HelloInterview does not cover are parked in
`design_progress.md` with trigger `board:hard-tier-open` — typeahead · key-value store · Google Calendar ·
distributed tracing · A/B testing · **data migration** (rubric #7 as an entire design; protect it) ·
stream-processing. Twitter and Pastebin were declined outright as redundant.

**The "why not just do the easy ones" argument, worth reusing verbatim:** the instinct is right (Phase A
orders questions easiest-framework-rep first on purpose), but one question = one session ≈ one Sunday, so
an easy question is a *displaced* canonical one rather than extra practice, and **the Phase A gate is not
a count** — it is *#1–4 passing on 3+ questions*. *"It's still good to know"* is true and is not the test:
**the line rations Sundays, not knowledge.**

**How to apply:**
- **Before adding an SD question, check it isn't already placed** — the HelloInterview board is the menu,
  and the parked list carries triggers.
- **Before declining one, write the reason in the same edit.** A dateless, reasonless decline is the
  failure this exists to fix ([[feedback_roi_promotes_to_curriculum]]: the bar only means something
  applied in both directions).
- **Evaluate triggers at every weekly build** — fired means slotted that week or re-deferred *in writing*
  ([[feedback_gate_on_internal_state]]).
- **Never report row count as progress.** 35 rows is a menu; the gate is a handful defended 2–3 levels
  deep including rubric #7, plus one 🟢 on a no-write-up question.

## The ownership rule (Aug 8) — still in force, and the reason for it survived the rework

`study_guide.md`, `senior_ramp.md` and `design_progress.md` had held **three competing design lists** and
two stale status tables. Each thing now has exactly one owner: **state** → `mastery/design_progress.md` ·
**the plan** (order, phases, gates, 7-point rubric) → `senior_ramp.md` · **the mechanics** (the split, the
slots, the mock protocol, the debrief) → `study_guide.md` · **the syllabus** → HelloInterview, with
`coverage_map.md` as the pattern→question cross-walk.

⚠️ **If the engine can compute it, do not write it down in prose.** Every stale item found in that
reconciliation was a hand-written date or ✅ duplicating tracker state. Deleting the duplicate beats
remembering to update it — [[feedback_self_evaluation]]'s ladder: **source fix over reminder.**

**One finding worth not rediscovering:** *distributed cache* was absent from systemdesign.io entirely, and
that source gap is now closed — HelloInterview has it as a Medium. Designing a cache is a different rep
from using one (consistent hashing, eviction, replication, invalidation), which is why a Redis note was
never a substitute.
