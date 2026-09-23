# cse-progress

<!-- reconciled: 2026-09-23 -->

@AGENTS.md

This repo's always-on rules — the nine gates, the two registers, agent memory, single
source of truth, and the token-discipline cap — live in [`AGENTS.md`](AGENTS.md), imported
above (Claude Code inlines `@path` imports, so everything there is already in this file's
injected context, every turn). This file carries only what is specific to running the repo
on **Claude Code**; an agent-neutral reader should start at `AGENTS.md` instead.

## Claude Code specifics

### The skill loads automatically

Claude Code scans `.claude/skills/` and loads a skill's `SKILL.md` when its `description`
matches the current moment (see `AGENTS.md` §2 for the structural reasoning). No manual
invocation is needed; a `references/` file loads only when `SKILL.md` points at it for that
moment.

### Hooks (`.claude/settings.json`)

The gates in `AGENTS.md` §3 that carry Claude Code enforcement are wired here, mapped onto
Claude's own event names:

| Event | Script | Gate(s) |
|---|---|---|
| `SessionStart` | `session_start_memory.py` | restates the gate set + the `MEMORY.md` index |
| `UserPromptSubmit` | `kickoff_scaffold_reminder.py` | gate 9 (warn-only, does not block) |
| `PostToolUse` (Bash/PowerShell) | `scaffold_links_reminder.py` | gate 4 backup, at scaffold time |
| `Stop` | `problem_link_reminder.py`, then `rating_gate.py` | gates 4 and 1 (block) |

Every other gate in `AGENTS.md` §3 has no hook on Claude Code either — it is enforced there
by this file's presence in context, same as on any other agent. Activation, the
`python3`/`python` probing convention, and per-hook history are in
[`docs/SETUP.md`](docs/SETUP.md).

### Caveman → `lite`

`/caveman lite` at session start; never `full`/`ultra`/`wenyan`, which strip the explanation
coaching depends on. Compress mechanical output; keep the teaching full.
