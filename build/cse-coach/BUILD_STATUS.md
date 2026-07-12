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
| 7 | Write bootstrap — args/interactive intake, `reach_beyond ≥ 1` floor, projects NC150 → dated roadmap + week-1 schedule, installs hook. Tested end-to-end | ✅ done |
| 8 | Extract coaching skill — SKILL.md in place + CLAUDE.md wired | ✅ done |
| 9 | README (coach voice, interaction model) + `docs/PHILOSOPHY.md` | ✅ done |
| 10 | Dogfood — full mock adopter flow verified (bootstrap → scaffold → log DSA Clean +30 → log SD blind-sprint Shaky +10, all via the git hook) | ✅ done |
| 11 | Publish — **private repo live at https://github.com/michael-yrao/cse-coach** (main, 66 files) | ✅ done |

**BUILD COMPLETE — all 11 steps done.** The staged copy under `build/cse-coach/`
is the source of the initial commit; future work should happen in the standalone
repo. This staging tree can be removed from the design branch once you're settled in.

## How to test the staged build

Copy it out of the design branch and drive it (don't run bootstrap in-place — it
writes personal files):

```sh
cp -r build/cse-coach /tmp/cse-coach && cd /tmp/cse-coach && git init -q
python scripts/bootstrap.py --name You --start 2026-07-13 --non-interactive
python scripts/new_problem.py --number 1 --title "Two Sum" --pattern arrays_and_hash
python tests/test_engine.py            # 5 engine tests
git add -A && git commit -m wip        # pre-commit hook recomputes trackers
```

Then open it in Claude Code and just talk to the coach ("start today", solve,
report Clean/Shaky/Blank). Bootstrap prompts interactively if you omit the flags.

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
