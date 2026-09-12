# cse-progress

A personal, spaced-repetition study system for technical-interview prep. Solutions are written by
hand; a comfort-based schedule decides *what to review when*. Drive it conversationally from
[Claude Code](https://claude.com/claude-code) (recommended), where the coaching engine loads as a
skill — or another agent (Copilot, caveman) via [`AGENTS.md`](AGENTS.md) for a lower-credit option.

## Three pillars

DSA is the primary, actively-scheduled pillar. System Design and AI Engineering **ramp up as the
high-ROI DSA work completes** — so both are light right now.

| Pillar | How it's practised | Status / where it lives |
|---|---|---|
| **DSA** *(primary)* | hand-written solutions + spaced review, scheduled against a daily effort budget | active — [`dsa/`](dsa/), [`docs/foundations/dsa/`](docs/foundations/dsa/) |
| **System Design** | study on [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction); the coach runs cold mock interviews and scores them | study mode now, ramps up after DSA; off-board. Mechanics + tracker [here](docs/foundations/system_design/); premium mock content in private [sd-progress](https://github.com/michael-yrao/sd-progress) |
| **AI Engineering** | work [calmrocks/ai-engineer-notebooks](https://github.com/calmrocks/ai-engineer-notebooks); the coach probes each notebook cold | **parked** — activates once DSA lightens; spec in [`ai_engineering/ROADMAP.md`](docs/foundations/ai_engineering/ROADMAP.md) |

## How the engine works

Each problem gets a **comfort** rating — 🟢 Clean / 🟡 Shaky / 🔴 Blank — inferred from the session
and proposed for you to confirm. Comfort sets a spaced-repetition interval; the weekly build then
schedules everything due against a daily effort budget (demand priced in units, not a problem
count). Non-Clean attempts are logged in `stuck_log.md`, so a retry is a rebuild, not a cold start.

**Every tuned value (intervals, the effort ceiling, weights) lives only in
[`cse.config.yml`](cse.config.yml).** The full coaching engine — review workflow, comfort scale,
guardrails, weekly build — is the `cse-coach` skill:
[`.claude/skills/cse-coach/SKILL.md`](.claude/skills/cse-coach/SKILL.md).

## Layout

```
dsa/leetcode/<type>/*.py     # hand-written solutions (arrays_and_hash, graphs, …)
docs/foundations/
  dsa/                       # study_guide.md · patterns/ · mastery/ (dsa_progress + stuck_log)
  system_design/             # study_guide.md + mastery/ (the SD tracker)
  ai_engineering/            # ROADMAP.md (parked)
  schedules/                 # weekly cross-pillar plans (+ archive/)
scripts/                     # tracker, effort budget, integrity + single-source checks
.claude/                     # the cse-coach skill, agent memory, git hooks
CLAUDE.md · AGENTS.md        # always-on rules · agent-agnostic entry point
```

## Setup (one-time per machine)

```sh
git config core.hooksPath .githooks   # auto-updates the tracker on commit
```

Full notes: [`docs/SETUP.md`](docs/SETUP.md).

## Start here

- [`CLAUDE.md`](CLAUDE.md) — the always-on rules · [`SKILL.md`](.claude/skills/cse-coach/SKILL.md) — the coaching engine
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how the rules are tiered against a context budget
- DSA plan: [`study_guide.md`](docs/foundations/dsa/study_guide.md) · pattern library: [`patterns/README.md`](docs/foundations/dsa/patterns/README.md)
- Template roadmap: [`docs/cse-coach/ROADMAP.md`](docs/cse-coach/ROADMAP.md)

## External resources

- [NeetCode](https://neetcode.io/) — Blind 75, then NeetCode 150 (the ROI floor).
- Company-wise pull pool (once NC150 is solid): [snehasishroy/leetcode-companywise-interview-questions](https://github.com/snehasishroy/leetcode-companywise-interview-questions). Fallback mirrors + the "repos go stale, pick the freshest" caveat are in the DSA study guide's post-NC150 section.
