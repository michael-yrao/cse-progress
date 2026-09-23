---
name: project-multi-agent-portability
description: AGENTS.md is now the single always-on hub for every agent (Claude Code, Copilot, Cursor); CLAUDE.md is a thin Claude-only import; the Copilot shim points at both — what to keep in sync and how not to re-fork the rule text
metadata:
  type: project
reconciled: 2026-09-23
---
**What shipped (Phase 1 of `docs/cse-coach/AGENT_PORTABILITY_PLAN.md`, 2026-09-23):** `AGENTS.md`
carries the full always-on layer in agent-neutral wording — the nine gates, the two registers, agent
memory, single source of truth, and the token cap — plus a "which agent reads what" table. `CLAUDE.md`
shrank to `@AGENTS.md` + a Claude-Code-only section (skill auto-load, the `.claude/settings.json`
hook-to-gate map, caveman lite). `.github/copilot-instructions.md` is now a shim that reads `AGENTS.md`
and states the Copilot hook bridge as planned, not built. `.vscode/settings.json` gained
`chat.useAgentsMdFile: true`. See `decisions.yml` `agents-md-hub-sep22` for the full change list and
[[project-agent-portability]] (the plan-status file) for which phase is next.

**The rule this enforces on future edits:** `AGENTS.md` is now the injected/obeyed copy — the role
`CLAUDE.md` alone used to hold. A rule change goes into `AGENTS.md` (or the skill, for a coaching-moment
rule) FIRST; `CLAUDE.md`'s Claude-only section only ever adds Claude-specific mechanics on top of that,
never a second copy of a gate. `reconcile.py`'s `RULE_GLOBS` and `check_single_source.py`'s `PROSE_GLOBS`
need `AGENTS.md` in their file lists for this to be checked automatically (the companion engineering slice
of this same phase, same `decisions.yml` entry) — if a future audit finds `AGENTS.md` missing from either
list, that is regression, not a design choice.

**What is still unverified — do not upgrade the wording without doing this first:** every Copilot/Cursor
claim in `AGENTS.md`, `.github/copilot-instructions.md`, and `docs/SETUP.md` is phrased as "documented,
not verified" — read from each vendor's own docs, never confirmed by a live run in this repo. Phase 3 of
the plan (§7) is the live-probe checklist; only after it runs on a given agent does a "works on X" /
"enforced on X" sentence become honest. Until then, every hook note for Copilot/Cursor reads "bridge
planned" and every gate there is prose-only.

**A known permanent gap, not a to-do:** the kickoff-scaffold gate (gate 9) has no possible hook bridge on
Cursor — its prompt-submit hook cannot inject context (see `AGENTS.md` §1). Don't file this as an open
item to fix in Phase 2; it stays prose-only there by the vendor's own design, not by an oversight.

Related: [[project-agent-portability]] (phase/status tracker — read its plan-file pointer for what's
next), [[feedback-execution-workflow]] (the roles used to execute this phase).
