---
name: feedback-execution-workflow
description: Tech lead plans, Opus team leads supervise Sonnet engineers who implement, tech lead reviews + runs advisor before any commit/push — GLOBAL, three-tier pyramid at a 2:1 spawn ratio, for all non-trivial work (evidence/why for the always-on gate in ~/.claude/rules/execution-workflow.md)
metadata:
  type: feedback
reconciled: 2026-09-21
---
**NORMATIVE SSOT is the always-on global rule** `~/.claude/rules/execution-workflow.md` (auto-injected
in every repo), enforced by the global `UserPromptSubmit` hook
`~/.claude/hooks/execution_workflow_reminder.py`. This file is the *why/evidence/occurrence* layer only —
it must never be the only place the rule is stated.

**Widened 2026-09-21 (later the same day) by the learner — three-tier pyramid:** tech lead = the
orchestrating session (Fable on Max, Opus otherwise), Opus team leads at a 2:1 engineer:lead ratio
(ceil(n/2) leads, ≤ 2 engineers per lead, 1 engineer → the tech lead supervises direct), Sonnet engineers.
Roles are enforced as custom agent definitions — `~/.claude/agents/team-lead.md` and `engineer.md`
(model pinned, `disallowedTools` blocks Write/Edit on the lead) — not prose only. **Subagents are never
Fable** — Fable stays the orchestrating session; leads are Opus, engineers are Sonnet, pinned explicitly
(never `model: inherit`, never a Fable override on an Agent call). **Why:** the Max plan removes the cost
pressure that kept the tree flat; a lead per 2 engineers keeps review close to the diff while the session
stays on judgement; pinning the model and removing the editing tools in the definitions is stronger than
a prose "never writes" — but the lead keeps Bash for test runs, so the no-writing rule is part enforced
(the tools are gone) and part convention (Bash could still write; the lead just doesn't). See `decisions.yml`
`execution-workflow-pyramid-sep21`.

**Broadened 2026-09-21 by the learner:** from the gamification/site-integration scope to **all
non-trivial work, across every repo** (global), **strongly enforced** (gate + reminder hook), triggered
on **non-trivial work only** (trivial one-liners/typos/reads run inline). See `decisions.yml`
`execution-workflow-global-sep21`.

**Refined 2026-09-21:** the Opus role never writes implementation — it plans/supervises/advises/reviews/
integrates only; all edits go to Sonnet engineer subagents (spawn as many as needed).

**Set 2026-09-20 by the learner** for the gamification / site-integration work (cse-progress
`progress.json` + the progressiveoverflow.com dashboard).

| Tier | Model | What |
|---|---|---|
| Tech lead | the session (Fable on Max, Opus otherwise) | explore, design, write the plan, get approval, review every diff, run `advisor`, integrate |
| Team lead | Opus (`team-lead` agent) | own one plan slice, brief/supervise ≤ 2 engineers, review their diffs, report up |
| Engineer | Sonnet (`engineer` agent) | execute a brief — edits, tests, build; report the diff |

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
