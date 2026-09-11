# cse-progress

<!-- reconciled: 2026-09-10 -->

This is a personal spaced-repetition practice log + coaching workflow (DSA, with a System
Design pillar). **The coaching engine is a skill; this file carries only the always-on
normative rules + pointers.**

## The coaching engine lives in a skill

All coaching behavior — the review workflow, scaffolding, the comfort scale, the effort
budget, the weekly build, technique coverage, and the System Design mocks — is defined in
[`.claude/skills/cse-coach/SKILL.md`](.claude/skills/cse-coach/SKILL.md) and its
`references/`. **Load it at any coaching moment:** the learner mentions, starts, reviews, or
finishes a problem or an SD mock; asks what to work on; scaffolds; the weekly close-out; or
session start/end. `SKILL.md` is a lean spine that points to the reference file for the
moment at hand — open only that slice.

**Other agents (Copilot, caveman) can't invoke skills** — see [`AGENTS.md`](AGENTS.md); they
read `SKILL.md` + `references/` directly as plain markdown.

**The structural principle behind the split:** CLAUDE.md is *always* injected; the skill and
`.claude/memory/*.md` are *opt-in reads*. A rule that must fire **unprompted** cannot live
only in an opt-in read — so the always-on gates below stay here (and in the SessionStart
hook), while moment-triggered engine detail lives in the skill, loaded when its moment
arrives. If a standing rule keeps lapsing, ask: **is it a step in an executable list, or
merely a paragraph?** — or, in tier terms, *is it in too cold a tier?* The full model (the four
tiers, the "which tier?" routing rule, the compaction loop) is [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Always-on gates — bound to a MOMENT, not a topic

Each fires unprompted; the SessionStart hook re-states them and the Stop hooks enforce two of
them. The *how* is in the named skill reference.

1. **About to propose a comfort rating?** The **complexity gate** is already overdue — time
   AND space, each with an itemized why-clause, before the rating. (`review-workflow.md` §1;
   enforced by `rating_gate.py`.)
2. **Before any solution code?** The **recognition gate** — learner states shape → technique →
   the feature that picks it; you name only shape cues, never candidate techniques.
   (`review-workflow.md` §0.)
3. **Learner says they're stuck?** Read their solution file **before hinting** — one free
   call. (`review-workflow.md` §2.)
4. **Mentioning a problem by number/name?** It must be a markdown link. (Enforced by
   `problem_link_reminder.py`.)
5. **Something got corrected — by you or the learner?** Append a dated entry to
   `.claude/memory/self_eval_log.md` **in the same turn**, and climb the intervention ladder
   (source fix > hook > skill/CLAUDE.md step > memory file). (`feedback_self_evaluation.md`.)
6. **Deferring/dropping a problem?** Assign a new specific slot in the same edit — a deferred
   problem with no new date is a missed problem. (`review-workflow.md` schedule integrity.)
7. **Last session of the week?** Archive this week's schedule AND generate next week's, before
   the commit — both, or neither counts. (`weekly-build.md`.)
8. **Asked to commit or push?** ⚠️ **Ask first, every time. No exceptions.** Make the edits,
   say what is staged, and stop; accumulate edits and let them land in one commit when the
   learner says so. (`feedback_commit_discipline.md`.)

## Two registers: latitude when thinking, stringency when executing (Aug 21, 2026)

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

## Agent Memory

Persistent behavioral preferences live in `.claude/memory/`. At session start, read
`.claude/memory/MEMORY.md` (the index), then load files relevant to the task. **Save new
memories to `.claude/memory/` in this repo** (not `~/.claude/projects/`) and index them in
`MEMORY.md`, so they sync across machines via git.

## Single source of truth for tuned values

**Every tuned number — review intervals, the effort ceiling/floor, comfort/difficulty
weights, `graduate_at_streak` — is stated in [`cse.config.yml`](cse.config.yml) and NOWHERE
else. Prose points at it; prose never copies it.** The failure is always silent, and it is
always the copy nobody executes from that rots.

| | |
|---|---|
| **Changing a value** | edit `cse.config.yml`, and nothing else. A second file updated was already a bug |
| **Writing prose** | name the key and point at the config; never write the number |
| **Writing code** | read the config. A `DEFAULT_CONFIG` fallback is allowed only where the tool must run before a config exists, and must announce loudly when it fires |
| **Recording history** | a dated entry stating what a number *was* is correct; mark it `single-source-ok` so the checker skips it |

### ⚠️ The one DELIBERATE exception: rules live in layers

Values, history and evidence are single-sourced. **Rules are not** — the normative sentence
sits here (or in a skill reference for a coaching-moment rule) *and* the reasoning sits in a
`.claude/memory/feedback_*.md`. This is accepted: this file is injected every turn, so moving
each rule's full derivation here would carry it forever.

> **The rule sentence in the always-injected/loaded layer is NORMATIVE and WINS. A memory file
> carries the why, the evidence and the occurrence log — and must never be the only place a
> rule is stated.**

So a rule change lands in CLAUDE.md (or the skill reference) in the same edit, always. `reconcile.py`
covers this file and the skill, forcing a re-read when a decision is recorded — the affordable
90% of keeping the layers agreeing.

### Enforced, not remembered

```sh
python scripts/check_single_source.py           # report
python scripts/check_single_source.py --check    # exit 1 on drift
```

Runs from the pre-commit hook. Script-defaults-vs-config is an exact hard finding; prose
restating a value is heuristic and advisory.

## Decisions are dated, and rules are reconciled against them

**[`decisions.yml`](decisions.yml) is the dated record of when the MODEL changed.**
`cse.config.yml` says what values *are*; this says when they became that. **Record a decision
there in the same edit that makes it.** Rules go stale when their PREMISE expires, not when
their words drift — so the check is temporal, not lexical: every rule file carries
`reconciled: YYYY-MM-DD`; a file predating a decision has not been read against it.

⚠️ **CLAUDE.md and the skill files are IN SCOPE.** This file is always injected, so when it and
a memory file disagree this is the copy that gets obeyed — a stale rule here is strictly worse
than anywhere else.

```sh
python scripts/reconcile.py                      # what has not been read against what
python scripts/reconcile.py --file <path> ...    # "I read these; they are right or now fixed"
```

Bump the date only after actually reading the file (it asserts a judgement, not an edit);
never derive it from `git log`. The pre-commit hook runs it, report-only, when `decisions.yml`
is staged.

## Token discipline (efficiency by default)

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

## Repo setup

One one-time step on a fresh clone — see [`docs/SETUP.md`](docs/SETUP.md): the git hooks path
(`git config core.hooksPath .githooks`). `.claude/settings.json` is committed and syncs; only
`.claude/settings.local.json` (personal permission overrides) stays per-machine.

**Caveman → `lite`** (`/caveman lite` at session start); never `full`/`ultra`/`wenyan`, which
strip the explanation coaching depends on. Compress mechanical output; keep the teaching full.
