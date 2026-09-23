---
name: project-agent-portability
description: OPEN — cse-coach on Copilot + Cursor; the approved plan (hub AGENTS.md, spec-clean skill, hook bridges, live-probe checklist) lives in docs/cse-coach/AGENT_PORTABILITY_PLAN.md, which is the single status record
metadata:
  type: project
reconciled: 2026-09-22
---
**State (2026-09-23):** Phases 0–1 done; Phase 2 in progress; Phase 3 not started.
The plan file's Status line is the only status field — read it, never this line, for what is done.

**Where:** [`docs/cse-coach/AGENT_PORTABILITY_PLAN.md`](../../docs/cse-coach/AGENT_PORTABILITY_PLAN.md).
§0 is the pickup procedure (read order, one phase at a time, branch off main, done criteria). §1 is the
verified per-agent table (skill dirs, always-on file, hook events) as of 2026-09-22 — re-verify against
vendor docs before relying on it after ~2 months.

**Why it exists:** the always-on layer had three drifting copies (CLAUDE.md, AGENTS.md,
`.github/copilot-instructions.md`); the fix is one hub file (`AGENTS.md`) with per-agent shims, the same
single-source rule as `cse.config.yml` applied to rule text. Hooks port through bridges that run the
existing scripts unchanged, so the gate logic stays single-source too.

**How to apply:** a session asked to continue this work takes the next NOT STARTED phase from the plan and
follows §0. Do not re-plan; if the plan is wrong, amend it in the same commit with a dated line.
Related: [[feedback-execution-workflow]] (the roles the plan's briefs assume), [[project-upstream-candidates]]
(the bridges go upstream to canonical cse-coach after they soak).
