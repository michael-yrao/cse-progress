---
name: cse-init
description: >-
  First-run setup / scaffolding for cse-coach. Use when a learner is setting up
  the repo for the first time ("set me up", "/cse-init", no cse.config.yml yet),
  or wants to scaffold cse-coach into an existing practice repo. Runs the
  conversational intake, writes cse.config.yml, generates the roadmap and week-1
  schedule, and installs the git hook.
---

# cse-init — first-run setup & scaffolding

> STUB — full logic lands in build step 6 (bootstrap). The behavior below is the
> contract; `scripts/bootstrap.py` implements the mechanical parts.

When there is no `cse.config.yml`, run setup:

1. **Present all questions at once** (single warm block, coach voice — see the
   cse-coach skill's voice guideline): name, start date, target (default
   `competitive`), daily cap, solution language (default Python), which pillar
   leads. Do **not** ask for a `reach_beyond` number — tell them they'll always
   train at least one tier past their target because that's what makes it stick.
2. After they answer, if they chose to lead with System Design or AI before the
   readiness gate, push back kindly and offer the light on-ramp; proceed only on
   explicit override (record it).
3. Write `cse.config.yml` (from `cse.config.example.yml`).
4. Generate the personalized `study_guide.md` roadmap + the week-1 schedule file
   from the chosen curriculum tiers projected onto `start_date`.
5. Reset the trackers to header + seed row; empty the logs; seed `self_eval_log.md`.
6. Run `git config core.hooksPath .githooks`.
7. Sign off in the same voice: name tomorrow's first problem and remind them the
   only report you ever ask for is "Clean, Shaky, or Blank?"

**Drop-in mode:** to scaffold cse-coach into an existing repo, copy `.claude/`,
`scripts/`, `.githooks/`, `cse.config.example.yml`, and the `docs/foundations/`
scaffold, then run the same setup.
