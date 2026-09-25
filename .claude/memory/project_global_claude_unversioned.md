---
name: project-global-claude-unversioned
description: The execution-workflow enforcement layer in ~/.claude/ is versioned in the private repo michael-yrao/claude-dotfiles (whitelist .gitignore, in-place); since 2026-09-25 a SessionStart hook (hooks/dotfiles_sync.py) converges it automatically — restore recipe for a fresh machine + what the hook does and does not do
metadata:
  type: project
reconciled: 2026-09-25
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

**Restore on a fresh machine (since 2026-09-25): one command.** Clone the repo anywhere, then
`python <clone>/bootstrap.py --repos-dir <dir holding cse-progress etc.>`. It checks out the repo IN PLACE at
`~/.claude` (init + remote + fetch + checkout), backs up any pre-existing `settings.json` to `backups/` and
merges it onto the tracked copy (lists union, local scalars win, tracked `hooks` and `defaultMode` always
win), moves any colliding hand-copied file aside, sets `core.hooksPath .githooks` in every child repo that
ships `.githooks/`, runs the hook tests, verifies the three hooks are wired, and pushes. `--dry-run` prints
the plan; `--no-push` skips the push. Rerunning on a restored machine only fetches. The manual steps it
replaced: `git init -b main` in `~/.claude`, add the remote, `git fetch origin`, `git checkout -b main
origin/main`, then merge `settings.json` by hand. See [[feedback-execution-workflow]].

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

**2026-09-25 — sync is now automatic.** `~/.claude/hooks/dotfiles_sync.py`, wired as a `SessionStart`
hook in the tracked `settings.json`, fetches `origin/main` on every session start (skipped on
`compact`), auto-commits `settings.json` churn as `chore(settings): <host> settings churn`, merges
`origin/main` (a conflict confined to `settings.json` is resolved by a three-way JSON merge:
`allow`/`deny`/`ask`/`additionalDirectories` are order-preserving set unions, everything else is a
scalar three-way merge with local winning on a double change), pushes when ahead, and reports one
`dotfiles:` line per action into the session context. **It never touches a dirty file under `rules/`,
`agents/` or `hooks/`** — those are reported and stay a manual `git -C ~/.claude status` + commit
(the hook pushes that commit on the next start). So the standing obligation above shrinks to: commit
rule/agent/hook edits; settings churn takes care of itself. **The hook cannot help a machine that was
never restored** (no `settings.json` wiring, nothing fires) — the restore recipe above still applies
there, and the two recurrences (Mac 09-24, Windows 09-25) are logged in `self_eval_log.md`.

**Detection (2026-09-25):** cse-progress's own SessionStart hook now runs
`.claude/hooks/global_layer_canary.py`, which prints a `!! GLOBAL LAYER CHECK FAILED` banner when any piece
of the layer is missing on the machine (rule/agent/hook files, the three hook wirings in `settings.json`,
the `~/.claude/.git` checkout, this repo's `core.hooksPath`). A lapse like the Mac's is now loud at the
first session, not discovered days later through a lapsed rule.
