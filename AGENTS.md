# AGENTS.md — running cse-progress on any agent

<!-- reconciled: 2026-09-23 -->

cse-progress is a personal spaced-repetition practice log + coaching workflow (DSA, with a
System Design pillar). **This file is the single always-on hub** — the always-on gates,
repo-maintenance rules, and pointers, in agent-neutral wording, for whichever agent is
driving this repo (Claude Code, GitHub Copilot, Cursor, or anything else). **The coaching
engine itself is a skill**, not this file: [`.claude/skills/cse-coach/SKILL.md`](.claude/skills/cse-coach/SKILL.md)
and its `references/` are the source of truth for the review workflow, the comfort scale,
the guardrails, and the schedule rules. Load it at any coaching moment — the learner
mentions, starts, reviews, or finishes a problem or an SD mock; asks what to work on;
scaffolds; the weekly close-out; or session start/end.

> **Open work on this hub:** [`docs/cse-coach/AGENT_PORTABILITY_PLAN.md`](docs/cse-coach/AGENT_PORTABILITY_PLAN.md)
> is what made this file the hub (Phase 1) and tracks the hook bridges (Phase 2) and the
> live-probe verification (Phase 3) still ahead. Its Status line says which phase is next;
> §0 there is how to pick it up.

## 1. Which agent reads what

Per each agent's own docs (checked 2026-09-22): skill discovery and the always-on file are
documented to need no file move; unverified until Phase 3. No hook tier exists yet on
Copilot or Cursor (a bridge is planned, Phase 2), so every gate in §3 is prose-only there
until one lands and passes Phase 3. Full event-by-event map:
[`docs/cse-coach/AGENT_PORTABILITY_PLAN.md`](docs/cse-coach/AGENT_PORTABILITY_PLAN.md) §1.

| | Claude Code | Copilot (VS Code / CLI / cloud) | Cursor |
|---|---|---|---|
| **Skill dirs scanned** | `.claude/skills/` only | `.github/skills`, `.claude/skills`, `.agents/skills` | `.cursor/skills`, `.agents/skills`, `.claude/skills`, `.codex/skills` |
| **Always-on file** | `CLAUDE.md` (`@path` imports inlined) | this file + `.github/copilot-instructions.md` (VS Code: `chat.useAgentsMdFile: true`; CLI/cloud reads `AGENTS.md` natively) | this file, natively; `.cursor/rules/*.mdc` for Cursor-only rules |
| **Hook config** | `.claude/settings.json` | `.github/hooks/*.json` | `.cursor/hooks.json` |
| **Hook events (can inject / can block)** | all events can inject; stop also blocks (has a transcript) | same shape as Claude Code; stop (`agentStop`) also blocks | session start & post-tool can inject; **prompt submit cannot** (`continue`/`user_message` only); stop has no transcript, returns a `followup_message` instead of blocking |

## 2. The coaching engine lives in a skill

All coaching behavior — the review workflow, scaffolding, the comfort scale, the effort
budget, the weekly build, technique coverage, and the System Design mocks — is defined in
[`.claude/skills/cse-coach/SKILL.md`](.claude/skills/cse-coach/SKILL.md) and its
`references/`. `SKILL.md` is a lean spine that points to the reference file for the moment
at hand — open only that slice. Claude Code loads it as a skill (its `description` matches
a coaching moment); per §1, Copilot and Cursor may already auto-load it the same way
(documented, not verified) — any agent can also just read `SKILL.md` + `references/`
directly as plain markdown regardless.

**The structural principle behind the split:** this file is *always* injected (on every
agent that supports an always-on layer); the skill and `.claude/memory/*.md` are *opt-in
reads*. A rule that must fire **unprompted** cannot live only in an opt-in read — so the
always-on gates below stay here (restated by the SessionStart hook where one exists),
while moment-triggered engine detail lives in the skill, loaded when its moment arrives.
If a standing rule keeps lapsing, ask: **is it a step in an executable list, or merely a
paragraph?** — or, in tier terms, *is it in too cold a tier?* The full model (the four
tiers, the "which tier?" routing rule, the compaction loop, and how a tier degrades when
an agent has no hook infrastructure) is [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## 3. Always-on gates — bound to a MOMENT, not a topic

Each must fire unprompted, on any agent. On Claude Code: `session_start_memory.py`
(SessionStart) restates the set; `rating_gate.py` and `problem_link_reminder.py` (Stop)
block gates 1 and 4; `kickoff_scaffold_reminder.py` (UserPromptSubmit) warns for gate 9. On
Copilot/Cursor no hook bridge exists yet (Phase 2, planned but unverified — see §1), so
every gate below is prose-only there until one lands and passes its Phase 3 probe. The *how*
for each is in the named skill reference.

1. **About to propose a comfort rating?** The **complexity gate** is already overdue — time
   AND space, each with an itemized why-clause, before the rating. (`review-workflow.md` §1
   · hook: `rating_gate.py` (Claude Code).)
2. **Before any solution code?** The **recognition gate** — learner states shape → technique
   → the feature that picks it; you name only shape cues, never candidate techniques.
   (`review-workflow.md` §0 · no hook — trust-based, via the learner's own top-of-method
   comment.)
3. **Learner says they're stuck?** Read their solution file **before hinting** — one free
   call. (`review-workflow.md` §2 · no hook.)
4. **Mentioning a problem by number/name?** It must be a markdown link (`[file] · [LC]`) —
   **except a recognition probe, which carries its LOCAL file link only, never LC/NC** (the
   problem page spoils the technique call). (Hook: `problem_link_reminder.py` (Claude Code),
   backed up by `scaffold_links_reminder.py` at scaffold time.)
5. **Something got corrected — by you or the learner?** Append a dated entry to
   `.claude/memory/self_eval_log.md` **in the same turn**, and climb the intervention ladder
   (source fix > hook > skill/AGENTS.md step > memory file). (`feedback_self_evaluation.md`
   · no hook appends the entry; the SessionStart banner is a backstop reminder only.)
6. **Deferring/dropping a problem?** Assign a new specific slot in the same edit — a
   deferred problem with no new date is a missed problem. (`review-workflow.md` schedule
   integrity · no hook.)
7. **Last session of the week?** Archive this week's schedule AND generate next week's,
   before the commit — both, or neither counts. (`weekly-build.md` · no hook.)
8. **Asked to commit or push?** ⚠️ **Ask first, every time — EXCEPT on an explicit
   close-out-and-publish instruction** (*"close out the day/session/week"*, *"wrap up and
   commit/push"*): that phrase IS standing authorization to commit AND push with no further
   confirmation — do the pre-commit sweep (`git status` · `restore_history.py` ·
   `update_review_dates`), then **report what landed**. The trigger is the learner's explicit
   phrase, never your own read of a "good breakpoint" (that judgement is what caused the
   31-commit run). Still **hold and ask** if anything is pending: an unrated/uncertain rep, an
   unsettled schedule/structural decision, a weekly close-out whose build isn't done (gate 7
   first), an odd git state, or **any irreversible action beyond an ordinary commit+push**
   (deletions, force-push, history rewrite). A vague close-out (*"call it a night"*) only
   reports done → still ask. Otherwise accumulate edits into one commit when the learner says
   so. (`feedback_commit_discipline.md` · no hook.)
9. **Learner asks to start the day / a session (a kickoff)?** Scaffold the **whole day's
   board** — every problem on today's schedule, active block AND both warmup slots — BEFORE
   presenting the board. A message naming a specific problem is **not** a kickoff (scaffold
   only that). (`scaffolding.md` scope § · hook: `kickoff_scaffold_reminder.py` warns, does
   not block (Claude Code) · Cursor can never get this hook — its prompt hook can't inject.)

## 4. Two registers: latitude when thinking, stringency when executing (Aug 21, 2026)

*"Don't bottleneck the agent when it's thinking, planning, researching and teaching; be
stringent when implementing and pulling basic details."*

| | **DELIBERATIVE** — thinking · planning · researching · teaching · interviewing | **MECHANICAL** — implementing · bookkeeping · pulling a stated detail |
|---|---|---|
| **Content** | unbounded — depth, alternatives, a worked trace *are* the product | exactly what was asked; no improvisation, no unrequested scope |
| **Rules that bind** | the **packaging** ones only — turn economy, register, no-spoilers, answer-length | **all of them, as hard gates** — if a step exists, walk it |
| **Failure to fear** | thin coaching dressed up as discipline | a silently wrong artifact — a bad date, a missed link, an unasked commit |

**The test:** would a second competent agent, given the same inputs, produce the same
artifact? Yes → mechanical, follow the checklist exactly. No → it's judgement, and judgement
is what you were asked for. ⚠️ This does **not** license skipping a gate mid-teach (the gates
above govern the *record*, not the thinking), nor terse coaching (the answer-length cap is
about *an answer*, never explanation or a `stuck_log` entry). ⭐ Push mechanical work OUT of
the session: hook > subagent (bounded sweep) > inline; never send a teach or a rep to a
subagent. full rule: [`project_agent_latitude_modes.md`](.claude/memory/project_agent_latitude_modes.md).

## 5. Agent Memory

Persistent behavioral preferences live in `.claude/memory/`, for every agent — the
`.claude/` prefix is history, not a dependency (D4 of the portability plan). At session
start, read `.claude/memory/MEMORY.md` (the index), then load files relevant to the task.
**Save new memories to `.claude/memory/` in this repo** (not an agent-specific location)
and index them in `MEMORY.md`, so they sync across machines and agents via git.

## 6. Single source of truth, and dated decisions

**Every tuned number — review intervals, the effort ceiling/floor, comfort/difficulty weights,
`graduate_at_streak` — lives in [`cse.config.yml`](cse.config.yml) and NOWHERE else. Prose points at
the key; prose never copies the number.** (Silent failure: the copy nobody executes from is the one
that rots — rationale in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).)

| | |
|---|---|
| **Changing a value** | edit `cse.config.yml`, nothing else — a second file updated was already a bug |
| **Writing prose** | name the key and point at the config; never write the number |
| **Writing code** | read the config; a `DEFAULT_CONFIG` fallback only where the tool runs before a config exists, and it must announce when it fires |
| **Recording history** | a dated entry stating what a number *was* is fine — mark it `single-source-ok` |

**Rules are the one deliberate exception — they live in two layers:** the normative sentence in the
always-injected/loaded layer (here, or a skill reference for a coaching-moment rule), the *why/evidence*
in a `.claude/memory/feedback_*.md`.

> The always-injected/loaded sentence is NORMATIVE and WINS. A memory file carries the why, the evidence
> and the occurrence log — and must never be the only place a rule is stated.

So a rule change lands in this file (or the skill reference) in the **same edit**, always.

**[`decisions.yml`](decisions.yml) dates when the MODEL changed** (`cse.config.yml` says what values
*are*; this says when they became that) — record a decision there in the same edit. Staleness is checked
*temporally, not lexically*: every rule file carries a `reconciled: YYYY-MM-DD` marker; a file predating a
decision hasn't been read against it. ⚠️ **This file and the skill files are IN SCOPE** — always injected
(where an agent supports one), so a stale rule here is obeyed over a correct one anywhere else.

```sh
python scripts/check_single_source.py --check    # exit 1 on a copied value (script-vs-config = hard; prose = advisory)
python scripts/reconcile.py                       # what hasn't been read against which decision
```

Both run report-only from the pre-commit hook. Bump a `reconciled:` date only after actually re-reading
the file — never derive it from `git log`.

## 7. Token discipline (efficiency by default)

Be lean: answer the thing, skip preamble, don't restate what's visible. The coaching voice,
spine-first explanation, one-job-per-turn, procedure-first teaching, and the caveman `lite`
pin live in the skill (`SKILL.md` §1).

### ⚠️ A HARD CAP: an answer to a question is ONE SMALL PARAGRAPH (Aug 17, 2026)

| | |
|---|---|
| **Answering a question** | one small paragraph, then **stop** and ask which part to expand |
| **Explaining what you did** | state it unprompted and in full — never make the learner ask for an account of work that already happened |

The cap is on **length, not formatting** — when an answer has more than ~two parts, use
bullets or a small table (structure is free). ⚠️ Don't offer to explain your own work — just
explain it. **Not capped:** comfort-rating rationale (propose + why), concept explanations
when stuck/asked, `stuck_log`/debrief/memory writing, and reporting what an action did.
⭐ Push depth into the file, not the chat. full rule: `decisions.yml` `answer-length-cap`,
[`feedback_explanation_register.md`](.claude/memory/feedback_explanation_register.md).

**On any low-credit / low-token setup** (the `caveman` skill on Claude Code, or an
equivalent low-verbosity mode elsewhere): terse output, compressed problem statements, no
recaps. The rules above never change — only verbosity drops.

## 8. Repo setup

One one-time step on a fresh clone, on any agent — see [`docs/SETUP.md`](docs/SETUP.md): the
git hooks path (`git config core.hooksPath .githooks`). Agent-specific config
(`.claude/settings.json`, `.vscode/settings.json`, a future `.github/hooks/*.json` or
`.cursor/hooks.json`) is committed and syncs on clone/pull; only per-machine permission
overrides (e.g. `.claude/settings.local.json`) stay gitignored.

## Key files

- `.claude/skills/cse-coach/SKILL.md` + `references/` — the coaching engine (read first)
- `CLAUDE.md` — Claude-Code-specific detail (skill auto-load, hook wiring, caveman lite); imports this file
- `cse.config.yml` — engine settings
- `scripts/update_review_dates.py` — Comfort→interval engine (runs on commit)
- `docs/foundations/dsa/mastery/dsa_progress.md` — the DSA tracker
- the SD tracker moved Aug 15, 2026 → [`sd-progress`](https://github.com/michael-yrao/sd-progress) `mastery/design_progress.md` (same engine, its own copy)
- `docs/foundations/schedules/<YYYYMMDD>_schedule.md` — the week's plan (all tracks)
