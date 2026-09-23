# cse-progress — GitHub Copilot instructions

This file is a **shim**, not a second copy of the rules — a stale prior version of it
(restated review intervals, called `CLAUDE.md` "the full workflow", still listed a retired
pillar) is the reason a shim replaced it.

## Read this first

[`AGENTS.md`](../AGENTS.md) is the single always-on hub for every agent, Copilot included —
the nine gates, the two registers, agent memory, single source of truth, and the
token-discipline cap. Read it before acting; it wins on any conflict. For the current state
of Copilot support specifically, see
[`docs/cse-coach/AGENT_PORTABILITY_PLAN.md`](../docs/cse-coach/AGENT_PORTABILITY_PLAN.md).

## The coaching engine

The review workflow, comfort scale, scaffolding, effort budget, weekly build, and System
Design mocks all live in
[`.claude/skills/cse-coach/SKILL.md`](../.claude/skills/cse-coach/SKILL.md) and its
`references/`. Per Copilot's own skill-discovery documentation it scans `.claude/skills/`
too, so this may already auto-load there the same way it does on Claude Code — that is
**documented, not yet verified** (Phase 3 of the portability plan is the live-probe
checklist). Until it's confirmed, read `SKILL.md` and its `references/` directly as plain
markdown; that always works regardless of whether auto-discovery does.

## Hooks

On Claude Code, some of `AGENTS.md`'s gates are enforced by hooks
(`.claude/settings.json`). A bridge that runs those same hook scripts against Copilot's own
events — `.github/hooks/*.json` — is **planned** for Phase 2 of the portability plan, but
nothing is built or verified yet. Until a bridge lands and passes its live probe, every gate
is prose-only here, carried by `AGENTS.md` alone, exactly as `AGENTS.md` §1/§3 say.

## Everything else

Repo layout and file-naming conventions: the top-level [`README.md`](../README.md).
One-time setup: [`docs/SETUP.md`](../docs/SETUP.md). Neither is restated here, on purpose —
one canonical copy of every rule, the same principle the hub itself follows.
