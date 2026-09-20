---
name: feedback-execution-workflow
description: For the gamification / progressiveoverflow.com site-integration project — Opus plans, Sonnet 5 implements, Opus reviews + runs advisor before any commit/push
metadata:
  type: feedback
reconciled: 2026-09-20
---
**Set 2026-09-20 by the learner** for the gamification / site-integration work (cse-progress
`progress.json` + the progressiveoverflow.com dashboard).

| Role | Model | What |
|---|---|---|
| Plan | Opus | explore, design, write the plan, get approval |
| Implement | Sonnet 5 (subagent) | execute the approved plan — edits, tests, build; report the diff |
| Review | Opus | review the Sonnet diff + run the `advisor` tool before any commit/push |

**Why:** the learner wants planning/judgement on the stronger model and mechanical execution on the
faster/cheaper one, with an Opus review gate so nothing lands unreviewed. Mirrors the repo's
deliberative-vs-mechanical register split.

**How to apply:** Opus spawns a Sonnet 5 subagent (`model: "sonnet"`) with the approved plan as its
brief; the subagent does NOT commit/push; Opus reviews, runs `advisor`, then commits/pushes per the
standing no-PR instruction.
