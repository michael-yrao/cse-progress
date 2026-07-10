# cse-coach

This repo is a **spaced-repetition mastery coach** for DSA, System Design, and AI
System Engineering. The learner talks to the coach in plain language; the coach
runs the review engine, protects the schedule, and coaches without spoiling.

## The coaching behavior lives in a skill

All coaching behavior is defined in [`.claude/skills/cse-coach/SKILL.md`](.claude/skills/cse-coach/SKILL.md).
Load it whenever the learner mentions, starts, reviews, or finishes a problem /
design / AI build, asks what to work on, or opens/closes a session. It is the
source of truth for the workflow, the comfort scale, the guardrails, and the voice.

## Config

Learner settings live in `cse.config.yml` (copy from `cse.config.example.yml`;
the bootstrap writes it). The review script and the skill both read it.

## One-time setup (per machine/clone)

```sh
git config core.hooksPath .githooks
```

This activates the pre-commit hook that auto-updates the spaced-repetition
trackers when a tracker or solution file is staged.

## Key files

- `.claude/skills/cse-coach/SKILL.md` — the coaching behavior (read this first)
- `cse.config.yml` — learner settings
- `scripts/update_review_dates.py` — the Comfort→interval engine (config-driven)
- `docs/foundations/dsa/mastery/dsa_progress.md` — DSA spaced-repetition tracker
- `docs/foundations/system_design/mastery/design_progress.md` — SD tracker
- `docs/foundations/ai_engineering/mastery/ai_progress.md` — AI tracker
- `docs/foundations/*/study_guide.md` — per-pillar roadmaps (ROI-line tiers)
- `docs/foundations/dsa/schedules/<YYYYMMDD>_schedule.md` — the current week's plan
