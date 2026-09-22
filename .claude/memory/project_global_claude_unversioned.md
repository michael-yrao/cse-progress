---
name: project-global-claude-unversioned
description: OPEN — the execution-workflow enforcement layer lives in ~/.claude/, which is not a git repo, so none of it is versioned, backed up, or synced across machines
metadata:
  type: project
reconciled: 2026-09-21
---
The entire enforcement layer for the execution workflow lives in `~/.claude/`: the normative SSOT
`rules/execution-workflow.md`, the reminder hook `hooks/execution_workflow_reminder.py`, and the agent
definitions `agents/team-lead.md` + `agents/engineer.md`. `~/.claude/` is not a git repo — none of this
is versioned, backed up, or synced across machines. The versioned artifact in cse-progress
(`decisions.yml`, `.claude/memory/feedback_execution_workflow.md`) is only the why/evidence layer.

**Consequence:** a machine reinstall or a lost profile silently drops the rule, the hook, and both agent
definitions — the memory file keeps describing a workflow that nothing enforces anymore.

**Fix undecided.** Options: a dotfiles repo for `~/.claude/`, or committing copies into cse-progress with
a sync script. See [[feedback-execution-workflow]].
