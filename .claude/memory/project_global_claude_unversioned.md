---
name: project-global-claude-unversioned
description: CLOSED 2026-09-21 — the execution-workflow enforcement layer in ~/.claude/ is now versioned in the private repo michael-yrao/claude-dotfiles (whitelist .gitignore, in-place, no sync script)
metadata:
  type: project
reconciled: 2026-09-21
---
The enforcement layer for the execution workflow lives in `~/.claude/`: the normative SSOT
`rules/execution-workflow.md`, the reminder hook `hooks/execution_workflow_reminder.py`, the agent
definitions `agents/team-lead.md` + `agents/engineer.md`, and `settings.json` (which wires the hook).

**Resolved 2026-09-21:** `~/.claude/` was made a git repo IN PLACE with a whitelist `.gitignore`
(`*` then re-include `rules/`, `agents/`, `hooks/`, `settings.json`), pushed to the private repo
`https://github.com/michael-yrao/claude-dotfiles`. Credentials, `projects/`, history, caches, and the
third-party plugin dump (`agents.disabled/`, `commands.disabled/`, `scripts/`, the ECC README files) are
never tracked. Chosen over "commit copies into cse-progress + sync script" because that creates a second
copy of the rule — the single-source failure the repo's own architecture warns about.

**Standing obligation:** any edit to a file under `~/.claude/rules|agents|hooks` or to `settings.json`
needs a commit + push in `~/.claude/` too — it is a separate repo, and the pre-commit sweep in
cse-progress does not see it. Check with `git -C ~/.claude status -sb`.

**Restore on a fresh machine:** `git init -b main` in `~/.claude`, add the remote, `git fetch origin`,
`git checkout -b main origin/main`. See [[feedback-execution-workflow]].
