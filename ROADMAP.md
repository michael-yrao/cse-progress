# Roadmap: Personal Tool → Reusable Study Framework

**Vision:** turn this repo from a personal spaced-repetition study system into a **template any developer can fork** and use for their own DSA + system-design interview prep — with their own tracker, schedules, and solutions, but the same structure, scripts, and reference library.

**Guiding split** (the whole effort is separating these two):

| Already reusable (the *framework*) | Personal (the *data*) |
|------------------------------------|------------------------|
| `patterns/` (techniques, hubs, cheatsheet) | `mastery/dsa_progress.md` rows |
| `fundamentals/big_o.md` | `mastery/stuck_log.md` entries |
| `system_design/` guides + templates | `schedules/` (my weeks) |
| `scripts/update_review_dates.py` | `dsa/leetcode/**` (my solutions) |
| `.githooks/pre-commit` | study_guide phase dates/goals |
| the comfort/spaced-rep *mechanism* | study_guide's *specific* NC150 plan |

The framework transfers as-is; the data needs a blank-slate path.

---

## Backlog

### Phase 1 — Separate framework from data
- [ ] Add blank starter templates: `dsa_progress.template.md`, `stuck_log.template.md`, a `<YYYYMMDD>_schedule.template.md`.
- [ ] Make `study_guide.md` a *generic* template (roadmap phases, pace, ROI line as fill-ins) + keep the current one as `examples/` reference.
- [ ] Decide the clean-start story: fork + wipe personal data via a seed script, **or** ship data in `examples/` and keep the tracked files empty by default.

### Phase 2 — Onboarding
- [ ] `setup.sh` (or `make setup`): activate `core.hooksPath`, scaffold empty tracker/schedule from templates, sanity-check Python.
- [ ] Human-facing "Getting Started" guide (README already covers structure; add a first-week walkthrough).
- [ ] Generalize `CLAUDE.md` — it's agent-facing and personal; split into (a) reusable workflow conventions, (b) my personal preferences.

### Phase 3 — Genericize hardcoded assumptions
- [ ] Config for cadence/daily-cap/intervals (currently baked into `study_guide.md` + `scripts/`).
- [ ] Language-agnostic note: solutions are Python under `dsa/leetcode/`; document how to adapt the discover-problems logic for other languages.
- [ ] Confirm no personal absolute paths / usernames leak into tracked files.

### Phase 4 — Packaging & distribution
- [ ] `LICENSE` + `CONTRIBUTING.md`.
- [ ] Mark the repo a **GitHub template repository**.
- [ ] Move reference data into `examples/` so `main` is a clean starting point.
- [ ] (Optional) the ECC `opensource-pipeline` skill can sanitize + package a fork when ready.

### Phase 5 — Polish
- [ ] Screenshots / a short walkthrough of a logging cycle.
- [ ] Sample filled-out design (YouTube/LLM) as a worked `system_design/case_studies/` example.
- [ ] Consider a lightweight docs landing page.

---

## How to use this file
Chip at it opportunistically — same as the knowledge-expansion queue. When a task is done, check it off with the commit that did it. New ideas for reusability go here, not in the study guides.
