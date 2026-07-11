# cse-coach — build status

Staging build of the `cse-coach` repo (design: `../../docs/planning/cse-coach-extraction-design.md`).
Lives under `build/cse-coach/` on the `cse-review` design branch until it's solid,
then gets pushed to its own private GitHub repo (Q4: private first).

Tracking the §7 phased build plan:

| # | Step | Status |
|---|------|--------|
| 1 | Scaffold repo — skeleton (3 pillars), license, README, CLAUDE.md, config example, hook, skill in place | ✅ done |
| 2 | Port engine — config-driven `update_review_dates.py` (intervals/root/globs from `cse.config.yml`, stdlib-only) + tests | ✅ done |
| 3 | Port DSA scaffold — patterns/fundamentals (copied clean), blank tracker/logs, `solution_template.py` + `new_problem.py` scaffolder (tested: create/retry/discovery) | ✅ done |
| 4 | Port System Design pillar — study guide, both templates, rate_limiter + io/stream seeds, blank `design_progress.md`; engine now multi-tracker (`--tracker`, no discovery) + hook wired; tests pass | ✅ done |
| 5 | Build AI Engineering pillar — study guide, build template, `vector_search` component seed, blank `ai_progress.md`; all 3 trackers idempotent | ✅ done |
| 6 | Author curriculum + backlog pools — DSA milestone (18 phases / 150 problems), Tier 1/2 expansion, interview + competitive backlog; SD & AI tiers. All YAML valid | ✅ done |
| 7 | Write bootstrap — intake (all-at-once) + date projection; enforce `reach_beyond ≥ 1`; seed logs | ⏳ next |
| 8 | Extract coaching skill — SKILL.md in place (done), wire CLAUDE.md (done) | ◑ partial |
| 9 | README (done) + `docs/PHILOSOPHY.md` | ◑ partial |
| 10 | Dogfood — mock adopter flow for all pillars end-to-end | ☐ |
| 11 | Publish — create private GitHub repo, push | ☐ |

## Notes
- Much study content can be **ported from `cse-review`** (patterns, fundamentals,
  SD study guide/templates, AI pillar, competitive backlog) with personal data stripped.
- The skill (`.claude/skills/cse-coach/SKILL.md`) and README are already the real
  drafted versions, moved in during step 1.
- **Engine (step 2):** zero external deps (stdlib only; no PyYAML). Config parsed
  with targeted regex over the documented `cse.config.yml` subset. Defaults exactly
  reproduce cse-review behavior. `DISCOVERY_SKIP_NUMBERS` emptied (the `{76}` was
  cse-review-personal). Run tests: `python tests/test_engine.py`.
- **Multi-pillar tracker iteration** (step 4): added `recompute_simple()` +
  `--tracker` — recompute/re-sort a same-format tracker with NO source discovery;
  the DSA `main()` is untouched (its tests still pass). Hook passes `--tracker` for
  the SD/AI trackers. Verified idempotent (2nd run = no-op) on real trackers.
- **Seed rows must use the engine's canonical format** — empty fields are TWO
  spaces (`|  |`), not one. Hand-written single-space empties mis-parse. Both seed
  rows normalized; the DSA tracker carries its auto-summary block.
