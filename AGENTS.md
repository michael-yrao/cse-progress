# AGENTS.md — running cse-review on any agent

cse-review is my personal spaced-repetition practice log + coaching workflow (DSA,
with a System Design pillar). This file is the **agent-agnostic entry point** so I can
drive it from GitHub Copilot, the **caveman** skill, or any assistant — not just
Claude Code.

> **Recommended: Claude Code**, which auto-loads memory and the full workflow. Other
> agents: read [`CLAUDE.md`](CLAUDE.md) in full — it is the source of truth for the
> review workflow, the comfort scale, the guardrails, and the schedule rules.

## The contract (essentials)
1. **Comfort = infer, then confirm.** After a problem, infer 🟢 Clean / 🟡 Shaky /
   🔴 Blank from the session and **propose it for confirmation** — don't ask an open
   "how did that feel?", don't log silently. My call is final; flag a dishonest 🟢.
2. **I write all code and do all thinking.** No spoilers unless I'm stuck or ask.
3. **Close the loop unprompted:** mark the schedule, update
   `docs/foundations/dsa/mastery/dsa_progress.md`, let the commit hook recompute the
   next review date, and re-slot it — never defer a problem without a new date.
4. **Log non-Clean** in `stuck_log.md` (🔴 full entry, 🟡 one-liner).
5. **System Design cadence = twice_weekly** (Sunday sprint + one midweek slot); drive
   the design *decisions*, not just the diagram (SD study guide's decision drill).

## Low-token / caveman mode
Under the caveman skill or any low-credit setup: terse output, caveman-compressed
problem statements, no recaps. Rules unchanged — only verbosity drops.

## Key files
- `CLAUDE.md` — full workflow (read first)
- `cse.config.yml` — engine settings
- `scripts/update_review_dates.py` — Comfort→interval engine (runs on commit)
- `docs/foundations/dsa/mastery/dsa_progress.md` — the DSA tracker
- `docs/foundations/system_design/mastery/design_progress.md` — the SD tracker (same engine)
- `docs/foundations/schedules/<YYYYMMDD>_schedule.md` — the week's plan (all tracks)
