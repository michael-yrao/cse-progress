# Agent portability plan — cse-coach on Copilot and Cursor

**Status:** approved 2026-09-22 · Phase 0 DONE (same push) · Phase 1 NOT STARTED · Phase 2 NOT STARTED · Phase 3 NOT STARTED
**Written:** 2026-09-22 · **Owner:** whichever session picks up the next phase (see §0)

## 0. Picking this up (any agent, any session)

This file is the single status record: the **Status** line above and the checkboxes in §7 are the only
places state lives. Update them in the same commit that lands a phase. Nothing about this work is in
chat history, memory, or a ticket — if it is not here, it did not happen.

1. **Read, in order:** this file top to bottom; then `AGENTS.md` and `CLAUDE.md` as they are *now* (Phase
   1 rewrites them, so read the current text before designing the new one); then the files named in the
   brief you are taking.
2. **Take one phase, in order.** Phases are sequential — Phase 2 assumes the hub exists, Phase 3 assumes
   the bridges exist. Within Phase 1 and Phase 2 the two engineer briefs are parallel and touch disjoint
   files, so one team lead can run both at once.
3. **Work on a branch off `main`**, never on `main`. On Claude Code the execution workflow applies as
   written (tech lead plans and reviews, engineers implement); on any other agent, the same split is a
   convention: one pass to implement the brief verbatim, one separate pass to review the diff against the
   brief before committing.
4. **Done means:** every file the brief names is changed; the verification commands in §5/§6 are green;
   the Status line and §7 boxes are updated; a `decisions.yml` entry is recorded when a rule file changed;
   the reviewer read the whole diff. Then commit and push per the commit rule in `AGENTS.md`.
5. **If you find the plan wrong,** change the plan in the same commit and say why in a dated line under
   the affected section — never silently do something different from what is written here.

Entry points that lead here: `.claude/memory/MEMORY.md` → `project_agent_portability.md` (Claude Code
reads the index at session start); the "Open work" line in `AGENTS.md` (Copilot, Cursor, anything else);
`docs/cse-coach/README.md`.
**Scope:** GitHub Copilot (VS Code, CLI, cloud agent) and Cursor. Codex and Gemini CLI are out of scope
for now; the one thing they would need (a `.agents/skills/` copy of the skill) is listed under *Later*.

**Principle:** one canonical copy of every rule. Other agents get *pointers and adapters*, never copies —
the same single-source rule that governs `cse.config.yml`, applied to the rule text itself. The stale
`.github/copilot-instructions.md` (it restates the review intervals, calls CLAUDE.md the full workflow and
still lists the retired AI pillar) is the evidence that a second copy rots.

## 1. What each agent reads (verified against vendor docs, 2026-09-22)

| | Claude Code | Copilot (VS Code / CLI / cloud) | Cursor |
|---|---|---|---|
| **Skill dirs scanned** | `.claude/skills/` only | `.github/skills`, **`.claude/skills`**, `.agents/skills` | `.cursor/skills`, `.agents/skills`, **`.claude/skills`**, `.codex/skills` |
| **Always-on file** | `CLAUDE.md` (`@path` imports are inlined) | `.github/copilot-instructions.md`; `AGENTS.md` (VS Code needs `chat.useAgentsMdFile: true`; the coding agent reads it natively) | `.cursor/rules/*.mdc`; `AGENTS.md` natively |
| **Hook config** | `.claude/settings.json` | `.github/hooks/*.json` | `.cursor/hooks.json` |
| **Session start** | `SessionStart` → `hookSpecificOutput.additionalContext` | `sessionStart` → `additionalContext` | `sessionStart` → `additional_context` |
| **Prompt submitted** | `UserPromptSubmit` (can inject context) | `userPromptSubmitted` | `beforeSubmitPrompt` — **cannot inject context** (`continue`/`user_message` only) |
| **After a tool** | `PostToolUse` → `additionalContext` | `postToolUse` → `additionalContext` | `postToolUse` → `additional_context` |
| **Turn end** | `Stop` (payload has `transcript_path`, can `block` with `reason`) | `agentStop` (payload has `transcriptPath`, returns `decision: block` + `reason`) | `stop` (payload is `status` + `loop_count` only — **no transcript**; returns `followup_message`, auto-submitted as the next user message, `loop_limit` default 5) |
| **Assistant text** | in the transcript | in the transcript | `afterAgentResponse` payload `text` (observe-only) |

Skill frontmatter per the open spec (agentskills.io): `name, description, license, allowed-tools, metadata,
compatibility`. Strict hosts reject any other top-level key. Our `reconciled:` key is non-spec.

**Consequences.** The skill is discoverable by Copilot and Cursor today with no move. The hook tier maps
1:1 onto Copilot. On Cursor the two Stop gates need a *shadow transcript* (see §5) and the prompt-time
kickoff reminder has no equivalent.

## 2. Current-state findings

1. `.claude/skills/cse-coach/` is spec-shaped except for the top-level `reconciled:` key.
2. The always-on layer exists three times and has drifted: `CLAUDE.md` (current), `AGENTS.md` (thin; still
   names the SD tracker at its pre-Aug-15 path), `.github/copilot-instructions.md` (stale, see above).
3. The five hooks read Claude's payload shape (`prompt`, `tool_input`, `transcript_path`, `stop_hook_active`,
   `hookSpecificOutput`) and Claude's JSONL transcript.
4. `docs/cse-coach/ROADMAP.md` Phase 2 already carries *"Generalize CLAUDE.md — split reusable workflow
   conventions from personal preferences."* This plan is that item.
5. This machine has `core.symlinks=false`, so symlinked skill dirs are not an option.
6. Incidental: `rating_gate.py` false-fired on this plan's summary turn — `\bclean\b` matched "spec-clean"
   and the proposal cue matched "approve". Logged in `self_eval_log.md` 2026-09-22; fix is in Phase 1.

## 3. Decisions

- **D1 — Skill stays at `.claude/skills/cse-coach/`, no mirror.** Both target agents read it there.
  Frontmatter goes spec-clean: `reconciled` moves under `metadata:`.
- **D2 — `AGENTS.md` becomes the hub.** It carries today's CLAUDE.md content in agent-neutral wording
  (gates, two registers, memory, single source, token cap, repo setup) plus a "which agent reads what"
  table and a per-agent enforcement note. `CLAUDE.md` shrinks to `@AGENTS.md` + a Claude-Code-only
  section (skill auto-load, `.claude/settings.json` hooks, caveman lite). `.github/copilot-instructions.md`
  becomes a shim. `.vscode/settings.json` gains `chat.useAgentsMdFile: true`. Cursor needs no file.
- **D3 — Hooks port via bridges, not rewrites.** One bridge script per agent normalizes stdin to the
  Claude shape, runs the existing hook unchanged, and translates stdout. Copilot first (1:1 events, but its
  transcript format is undocumented → spike). Cursor second (shadow transcript).
- **D4 — Memory stays at `.claude/memory/`.** Plain markdown; the hub tells every agent to read
  `MEMORY.md` at session start. The `.claude/` prefix is history, not a dependency.
- **D5 — The `advisor` role is retired.** Review is the tech lead's and the team lead's own job. Every
  place that says "run `advisor`" becomes "review the diff yourself" (Phase 0).

## 4. Phase 0 — retire `advisor` (rule edits, two repos) — DONE 2026-09-22

Landed in the same push as this plan (`decisions.yml` `advisor-retired-sep22`; the claude-dotfiles half in
its own commit). The word appeared in exactly these live places (history entries in `decisions.yml` and
`self_eval_archive.md` stay as history):

| Repo | File | Change |
|---|---|---|
| claude-dotfiles | `~/.claude/rules/execution-workflow.md` — tech-lead row; the "Review step is not optional" bullet | drop "run `advisor`"; bullet becomes *"nothing lands unreviewed — the tech lead reviews the consolidated diff and a team lead reviews its engineers' diffs, before any commit/push."* |
| claude-dotfiles | `~/.claude/hooks/execution_workflow_reminder.py` — docstring line 7, reminder text line 102 | same wording |
| cse-progress | `.claude/memory/feedback_execution_workflow.md` — description, table row, two prose lines | same wording; add a dated line: *retired 2026-09-22, learner's call — the reviewer is the lead, not a separate agent* |
| cse-progress | `.claude/memory/MEMORY.md` — the Execution workflow index line | drop "runs `advisor`" |
| cse-progress | `.claude/skills/cse-coach/references/weekly-build.md` line 98 | "review the engineer's diff, then commit/push …" |
| cse-progress | `.claude/memory/project_site_refresh_resume.md` line 45 | the note that `advisor` has no tool behind it becomes "closed by D5" |
| cse-progress | `decisions.yml` | new entry `advisor-retired-sep22`, `affects: [execution_workflow]` |

Trivial one-liners → the tech lead did these inline. The dotfiles repo got its own commit+push; its
working tree carried an unrelated modified `settings.json`, which was left out.

## 5. Phase 1 — the hub + spec-clean skill (two engineers, one team lead)

**E1 — always-on hub and docs** (files: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`,
`.vscode/settings.json`, `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/cse-coach/ROADMAP.md`,
`decisions.yml`, new `.claude/memory/project_multi_agent_portability.md`, `MEMORY.md` index line)
- Rewrite `AGENTS.md` from `CLAUDE.md`: same nine gates in substance, agent-neutral wording; every
  "enforced by `<hook>`" note says on which agents (§1 table); fix the SD tracker path; add the §1 table.
- Shrink `CLAUDE.md` to `@AGENTS.md` + the Claude-only section. Keep its `<!-- reconciled -->` marker.
- Rewrite the Copilot file as a shim: read `AGENTS.md`, the skill auto-loads from `.claude/skills/`, hooks
  live in `.github/hooks/` once Phase 2 lands. No numbers, no layout tree (README has it).
- Merge `chat.useAgentsMdFile: true` into `.vscode/settings.json` (merge, never clobber).
- `docs/SETUP.md`: a per-agent one-time-setup section. `docs/ARCHITECTURE.md`: one paragraph — the four
  tiers per agent; where the hook tier is absent a gate degrades to L1 prose.
- `decisions.yml` `agents-md-hub-sep22`; tick the ROADMAP Phase 2 item; write the memory file.

**E2 — skill frontmatter, script scope, hook fix** (files: `SKILL.md` frontmatter, `scripts/reconcile.py`,
`scripts/check_single_source.py`, `.githooks/pre-commit`, `.claude/hooks/session_start_memory.py`,
`.claude/hooks/rating_gate.py`)
- `SKILL.md`: `reconciled: 2026-09-20` → `metadata: {reconciled: "2026-09-20"}`. `reconcile.py` reads
  `metadata.reconciled` (old top-level form kept as fallback) and stamps into `metadata`.
- Add `AGENTS.md` to `reconcile.py`'s and `check_single_source.py`'s file lists and to the pre-commit
  SSOT trigger regex; both scripts must still pass `--check` on the rewritten files.
- `session_start_memory.py`: gate text that names "CLAUDE.md's …" names `AGENTS.md`.
- `rating_gate.py`: the comfort-word regex must not match a hyphen-joined token (`spec-clean`); add the
  false-fire as a test case beside the existing ones.

**Review:** the team lead reviews both diffs; the tech lead reviews the consolidated diff and runs
`python scripts/check_single_source.py --check`, `python scripts/reconcile.py`, `python -m pytest scripts/`,
then commits and pushes on the worktree branch.

## 6. Phase 2 — hook bridges (spike, then two engineers, one team lead)

**Spike first (tech lead, or one engineer, read-only):** run one Copilot CLI session in the repo with a
throwaway `agentStop` hook that copies its stdin and the file at `transcriptPath` into
`docs/cse-coach/spike/`. Decide from the real format whether `problem_link_reminder.py` and
`rating_gate.py` can read it with a translation step or need a parser branch. No bridge is written
before this file exists.

**E3 — Copilot bridge** (`.github/hooks/cse-coach.json`, `scripts/hooks/copilot_bridge.py`, tests)
- Event map: `sessionStart` → `session_start_memory.py`; `userPromptSubmitted` → `kickoff_scaffold_reminder.py`;
  `postToolUse` (bash/shell tools) → `scaffold_links_reminder.py`; `agentStop` → `problem_link_reminder.py`
  then `rating_gate.py`.
- The bridge translates field names in (`prompt`, `toolName`/`toolArgs` → `tool_name`/`tool_input`,
  `transcriptPath` → `transcript_path`) and out (`hookSpecificOutput.additionalContext` → `additionalContext`;
  Stop `decision: block` + `reason` is already the same shape). `stop_hook_active` is emulated with a
  per-session marker file so a block still fires once, never loops.
- Hook scripts stay byte-identical; if the spike shows the transcript needs a parser branch, that branch
  is keyed on a `transcript_format` field the bridge sets, not on the agent name.

**E4 — Cursor bridge** (`.cursor/hooks.json`, `scripts/hooks/cursor_bridge.py`, tests)
- Shadow transcript: `beforeSubmitPrompt` appends `{"role":"user","text":…}` and `afterAgentResponse`
  appends `{"role":"assistant","text":…}` to a per-session JSONL under the job/temp dir, in Claude's
  transcript shape, so the Stop gates read it unchanged.
- `stop` → run `problem_link_reminder.py` then `rating_gate.py` against the shadow transcript; a `block`
  becomes `followup_message` carrying the gate's `reason` (Cursor auto-submits it; `loop_limit: 1`).
- `sessionStart` → `session_start_memory.py` (`additional_context`). `postToolUse` → `scaffold_links_reminder.py`.
- The kickoff reminder has no Cursor equivalent (prompt hooks can't inject). It stays prose in `AGENTS.md`
  gate 9; the §1 table says so.

## 7. Phase 3 — verification by live probe (the standard set on 2026-09-21)

No claim of "works on X" lands in a rule file until this checklist is run on X and the evidence is pasted
into `decisions.yml`:

- [ ] Copilot CLI in the repo: `/skills` (or equivalent) lists `cse-coach`; a fresh session shows the
      `AGENTS.md` gates in its context; one deliberate rating-without-complexity turn is blocked by the bridge.
- [ ] VS Code Copilot Chat: same skill listing; `AGENTS.md` loads with `chat.useAgentsMdFile`.
- [ ] Cursor: skill listed; `AGENTS.md` loaded; the shadow transcript accumulates; the Stop gate's
      `followup_message` fires exactly once on a deliberate violation.
- [ ] Claude Code: `CLAUDE.md` with `@AGENTS.md` still injects every gate (the SessionStart hook output is
      unchanged) and `reconcile.py --check` / `check_single_source.py --check` are green.

## 8. Later (out of scope now)

- Codex / Gemini CLI: a byte-identical `.agents/skills/cse-coach/` mirror kept by a `sync_skills.py`
  pre-commit check, or a move of the canonical skill to `.agents/` once Claude Code reads that dir
  (anthropics/claude-code#66352). `.gemini/settings.json` `context.fileName: ["AGENTS.md"]`.
- Upstream: once Phase 1–2 soak here, the bridges and the hub layout go to canonical cse-coach via
  `project_upstream_candidates.md`.
