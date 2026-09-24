---
name: project-global-claude-unversioned
description: The execution-workflow enforcement layer in ~/.claude/ is versioned in the private repo michael-yrao/claude-dotfiles (whitelist .gitignore, in-place); restored on the Mac 2026-09-24 with a merged settings.json — restore recipe + the merge step
metadata:
  type: project
reconciled: 2026-09-24
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

**2026-09-24 — the Mac had never been restored.** `~/.claude` there was a plain directory: no
`rules/`, `agents/`, `hooks/`, no hook wiring in `settings.json` — so the whole enforcement layer was
absent and the pyramid lapsed on the stage-1 `src`-link work (`self_eval_log.md`, same date). Restored
per the recipe above, with one extra step the recipe lacked: **`settings.json` had diverged** (the
tracked copy carried the Windows machine's 45 permission entries + `C:\...` additionalDirectories; the
Mac's carried 98 entries, Mac paths and a `modelSettings` block, 3 entries shared). A plain checkout
refuses to overwrite it. Resolution: a MERGED file — union of both allow lists, both machines'
additionalDirectories (each side's paths are inert on the other), the tracked hooks/defaultMode, the
local model/theme/modelSettings — committed and pushed, so both machines now converge on it.
**Recipe amendment:** on a machine with an existing `settings.json`, move it aside before the checkout,
then merge (union) rather than pick a side. **Portability caveat:** `additionalDirectories` is
inherently machine-specific; the harness resolves the foreign paths relative to the cwd (harmless
noise). Verified after restore: both hooks fire (`execution_workflow_reminder` on a non-trivial prompt;
`role_gate` warns the tech lead's first write and denies a `team-lead` Edit); 20/20 hook tests pass.
