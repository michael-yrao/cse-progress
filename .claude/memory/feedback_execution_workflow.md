---
name: feedback-execution-workflow
description: Opus plans, Sonnet 5 implements, Opus reviews + runs advisor before any commit/push — for the gamification / site-integration project AND the weekly EOW schedule build
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

**Extended 2026-09-20 to the weekly EOW schedule build** (learner's call). The Sunday close-out runs the
same split: **Opus** prices/designs the build (capacity, pulls, day placement — the judgement), a
**Sonnet 5 subagent** does the mechanical writeback only (`git mv` the archive, write the next-week
schedule file from the approved plan, run the checker scripts — no commit/push), **Opus** reviews the
diff + runs `advisor`, then commits/pushes. ⭐ Only the mechanical writeback goes to the subagent — never
the planning, and never a teach or a rep. Operational home for the build steps:
`.claude/skills/cse-coach/references/weekly-build.md`. See `decisions.yml` `eow-close-out-process-sep20`.
