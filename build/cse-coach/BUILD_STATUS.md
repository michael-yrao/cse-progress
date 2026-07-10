# cse-coach — build status

Staging build of the `cse-coach` repo (design: `../../docs/planning/cse-coach-extraction-design.md`).
Lives under `build/cse-coach/` on the `cse-review` design branch until it's solid,
then gets pushed to its own private GitHub repo (Q4: private first).

Tracking the §7 phased build plan:

| # | Step | Status |
|---|------|--------|
| 1 | Scaffold repo — skeleton (3 pillars), license, README, CLAUDE.md, config example, hook, skill in place | ✅ done |
| 2 | Port engine (multi-pillar) — config-driven `update_review_dates.py` + golden test | ⏳ next |
| 3 | Port DSA scaffold — patterns/fundamentals, blank trackers/logs/schedules, `solution_template.py` + `new-problem` scaffolder | ☐ |
| 4 | Port System Design pillar — study guide, templates, component/fundamentals seeds, blank `design_progress.md`, backlog | ☐ |
| 5 | Build AI Engineering pillar — study guide, `ai_progress.md`, seed templates/components | ☐ |
| 6 | Author curriculum + backlog pools — DSA/SD/AI tiers, ROI-line-tagged | ☐ |
| 7 | Write bootstrap — intake (all-at-once) + date projection; enforce `reach_beyond ≥ 1`; seed logs | ☐ |
| 8 | Extract coaching skill — SKILL.md in place (done), wire CLAUDE.md (done) | ◑ partial |
| 9 | README (done) + `docs/PHILOSOPHY.md` | ◑ partial |
| 10 | Dogfood — mock adopter flow for all pillars end-to-end | ☐ |
| 11 | Publish — create private GitHub repo, push | ☐ |

## Notes
- Much study content can be **ported from `cse-review`** (patterns, fundamentals,
  SD study guide/templates, AI pillar, competitive backlog) with personal data stripped.
- The skill (`.claude/skills/cse-coach/SKILL.md`) and README are already the real
  drafted versions, moved in during step 1.
