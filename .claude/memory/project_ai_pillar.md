---
name: project_ai_pillar
description: AI Engineering is a planned THIRD pillar, PARKED behind a measured trigger (DSA must lighten first); active/scored/spaced like SD, interview-prioritized, ~1 notebook/wk on activation.
metadata:
  type: project
reconciled: 2026-09-12
---

**Status: PARKED (set 2026-09-12).** AI Engineering returns as a planned third pillar after
[[project_sd_mock_model]]-style rebuild thinking, but it is **not started** — it activates only when
DSA capacity frees up. Revives the AI half that was voided in `retired/project_curriculum_additions_pending`;
see `decisions.yml` `ai-pillar-revived-deferred` (supersedes `ai-track-removed`).

**Why parked, not running:** Backtracking opened Sep 14 and DP runs Oct–Nov — the heaviest DSA phase —
and the SD pillar already fills the starved "evening" slot. A third pillar now would be additive load
with nowhere to go. The original AI track died as *"a plan nobody executed"*; the defense is to not
start it until there is real room, and to make it active+scored when it does.

## Activation trigger (measured, not a date)

Activate at a **weekly build** when BOTH hold:
1. DP/Backtracking phases have **closed** on the roadmap, and
2. `effort_budget.py` shows **≥2 days/week well under the ceiling for 2 consecutive weeks** (real
   evening headroom — re-derived, not guessed; same ethos as [[feedback_midweek_reprice]] and
   [[feedback_gate_on_internal_state]]).

The weekly-build checklist carries the firing step ("if AI still parked, test the trigger"). Until
then: **do not nudge AI** (same discipline as SD study-mode in [[project_sd_mock_model]]).

## On activation — the two-pillar cadence ramp

| Phase | DSA state | SD cadence | AI cadence |
|---|---|---|---|
| Now → trigger | DP/Backtracking heavy | hold (starved in practice) | **parked** |
| Activation | DP winding down, headroom confirmed | ramp back toward twice_weekly | **1 notebook/wk**, alternating the evening slot with SD |
| DSA maintenance | mostly review/graduated | full twice_weekly | up to 2/wk as the evening allows |

SD recovers **first** (mid-flight and starved); AI is additive only once SD is healthy. The ramp is a
weekly-build decision re-derived from the live budget, never a fixed date.

## The design (for activation day — full spec in `docs/foundations/ai_engineering/ROADMAP.md`)

Mirrors the SD pillar: **off-board, UNPRICED** (takes the evening, not the DSA ceiling),
cadence-driven, learner-does-the-work / coach-assesses, own tracker.

- **A "rep" is active, not reading:** run the notebook, then produce a small **assessed artifact** — a
  cold explanation of the mechanism + one modification (change the eval, add a tool to the agent loop,
  break RAG retrieval and fix it). Coach probes it cold reusing the SD drills ([[feedback_quantify_qualify]],
  [[feedback_hld_altitude]], [[feedback_expand_acronyms]]). Comfort + spaced re-touch reuse the existing engine.
- **Interview-prioritized path** (goal = interview prep): `00-setup` → `01-model-apis` → `02/04-evals`
  → `03-rag` → `05-agents` → `10-ml-system-design` (the bridge to SD) → then depth (`07/08/06/09/11/12`).
- **Home:** in-repo under `docs/foundations/ai_engineering/` — the resource
  (github.com/calmrocks/ai-engineer-notebooks) is public, so no sd-progress-style privacy split.

**NOT built until activation** (avoid premature scaffold): the `references/ai-engineering.md` skill
reference, an `ai_progress.md` tracker, and any `cse.config.yml` cadence key (single-source: add the
key only when it holds a live value). Ties to [[project_interview_goal]].
