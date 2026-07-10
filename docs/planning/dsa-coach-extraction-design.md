# Design Doc: Extracting cse-review into a Reusable DSA Coach

**Status:** Draft for review
**Author:** Claude (with michael-yrao)
**Date:** 2026-07-09
**Decision baseline:** Ship a **new separate repo** (`dsa-coach`). `cse-review` stays 100% intact — no refactors, no data moved out. The new repo mirrors the cse-review workflow as closely as possible so an engineer who adopts it gets *your* system, not a diluted version.

---

## 1. Problem statement

`cse-review` is a working, opinionated spaced-repetition DSA coaching system. Its value is not the data — it's the **machinery + the coaching behavior**:

- A Comfort→interval spaced-repetition engine (`scripts/update_review_dates.py`)
- A version-controlled git hook that runs it automatically on commit
- A rigorous agent workflow (ask Clean/Shaky/Blank → log → schedule → never spoil)
- A documented study scaffold (study guide, weekly schedules, progress tracker, stuck log, pattern library)

Today all of this is fused to one person: your NC150 Jun–Dec 2026 roadmap, your filled schedules, your progress rows, your career folder, and — critically — behavior that lives in **your personal `~/.claude` memory**, which no one else inherits.

**Goal:** produce `dsa-coach`, a repo any engineer can adopt in <10 minutes and get the identical system seeded to their own start date and track, with the coaching behavior traveling *with the repo* rather than depending on a personal memory store.

**Non-goals:** changing the algorithm, redesigning the doc structure, or "improving" the workflow. This is an **extraction + parameterization** effort, not a rewrite. Fidelity to cse-review is the success bar.

---

## 2. What's reusable vs. what's personal

The single most important architectural act is drawing this line cleanly.

### 2a. Reusable engine (ships as-is or lightly parameterized)

| Asset | cse-review location | Change needed |
|-------|---------------------|---------------|
| Interval engine | `scripts/update_review_dates.py` | Read intervals + globs from config (§4) |
| Pre-commit hook | `.githooks/pre-commit` | Path-generalize; keep verbatim otherwise |
| Progress tracker format | `docs/foundations/dsa/mastery/dsa_progress.md` | Ship the header/notes + **one seed row**, no real data |
| Stuck log format | `docs/.../mastery/stuck_log.md` | Ship empty with template block |
| Pattern library | `docs/.../patterns/**` | Ship as-is — this is generically valuable reference material |
| Big-O / fundamentals | `docs/.../fundamentals/**` | Ship as-is |
| CLAUDE.md workflow rules | `CLAUDE.md` | Generalize paths + dates; keep the workflow verbatim |

### 2b. Coaching behavior — currently trapped in personal memory (the crux)

These `.claude/memory/feedback_*.md` files **are the product**. They must be promoted into **committed, shippable form** so every adopter inherits them:

| Memory file | Generalizable? | Destination in `dsa-coach` |
|-------------|----------------|-----------------------------|
| `feedback_operating_principles.md` (close the loop; user owns thinking/code) | ✅ Core | Skill body |
| `feedback_no_spoilers.md` | ✅ Core | Skill body |
| `feedback_no_code_edits.md` | ✅ Core | Skill body |
| `feedback_proactive_scheduling.md` | ✅ Core | Skill body |
| `feedback_daily_cap.md` | ✅ Core | Skill body (cap value from config) |
| `feedback_new_vs_retry.md` | ✅ Core | Skill body |
| `feedback_method_variant_promotion.md` | ✅ Core | Skill body |
| `feedback_schedule_mistakes.md` | ✅ Core | Skill body |
| `feedback_end_of_session_push.md` | ✅ Core | Skill body |
| `feedback_end_of_week_schedule.md` | ✅ Core | Skill body |
| `feedback_schedule_markdown.md` | ✅ Core (tooling quirk) | Skill body |
| `feedback_session_dating.md` | ✅ Core | Skill body |
| `feedback_git_commit.md` | ✅ Core | Skill body |
| `feedback_self_evaluation.md` + `self_eval_log.md` | ⚠️ Personal mechanism | Ship the *mechanism* (empty log + rule), not your entries |

**Key decision:** these become a **committed skill** (`.claude/skills/dsa-coach/SKILL.md`) inside the template repo, so they load for anyone working in an adopter's repo — no dependency on personal `~/.claude/memory`. Adopters can still layer their own private memory on top; the baseline behavior is guaranteed.

### 2c. Strictly personal (never ships)

- `career/**` (resume, performance reviews, trajectory)
- Your populated `dsa_progress.md` rows, filled `schedules/*.md`, real `stuck_log.md` entries
- Your NC150 Jun–Dec 2026 dated roadmap (becomes a *generated* artifact, see §5)
- `.claude/memory/user_profile.md`, `career_trajectory.md`, and anything MS/fintech-specific

---

## 3. Distribution shape

`dsa-coach` is **both** a GitHub *template repository* and the carrier of a *portable skill* — the "Both" model, achieved with one repo:

- **Turnkey path:** engineer clicks **Use this template** → runs bootstrap → has their own tracker.
- **Drop-in path:** the same repo's `.claude/skills/dsa-coach/` + `scripts/` can be copied into an existing practice repo; a `dsa-init` skill scaffolds the docs/hook there.

One repo, one source of truth for the script, two adoption routes. No second codebase to keep in sync.

```
dsa-coach/
├── README.md                       ← engineer-facing onboarding + philosophy
├── CLAUDE.md                       ← generalized workflow (paths/dates parameterized)
├── dsa.config.yml                  ← THE personalization surface (§4)
├── .githooks/pre-commit            ← generalized copy of yours
├── scripts/
│   ├── update_review_dates.py      ← config-driven (§4)
│   └── bootstrap.py                ← interactive setup (§5)
├── .claude/
│   └── skills/
│       ├── dsa-coach/SKILL.md      ← the coaching behavior (from §2b)
│       └── dsa-init/SKILL.md       ← scaffold-into-existing-repo command
├── docs/foundations/dsa/
│   ├── study_guide.md              ← roadmap templated, not hardcoded
│   ├── mastery/
│   │   ├── dsa_progress.md         ← header + ONE seed row
│   │   ├── stuck_log.md            ← empty + template
│   │   └── self_eval_log.md        ← empty + template
│   ├── schedules/                  ← empty; week 1 generated by bootstrap
│   └── patterns/**, fundamentals/**← shipped as-is (generic reference)
└── tracks/                         ← curriculum presets (§5)
    ├── nc150.yml
    └── blind75.yml
```

---

## 4. Config layer — the personalization surface

Today the engine hardcodes intervals, paths, and a Python-only solution glob. Introduce **one** config file the script and skill both read.

```yaml
# dsa.config.yml
learner: "Your Name"
start_date: 2026-07-13
track: nc150            # nc150 | blind75 | custom
daily_cap: 5

intervals:              # days until next review, by Comfort + streak
  clean:  { streak1: 30, streak2: 60, retired: 180 }
  shaky:  10
  blank:  2
retire_at_streak: 3

solutions:
  # language-agnostic discovery; you practice Java + Python
  roots: ["dsa/leetcode"]
  globs: ["*.py", "*.java", "*.js", "*.ts", "*.cpp"]
  filename_pattern: "{number}_{name}"   # 19_remove_nth_node.py
```

**Script changes (surgical, behavior-preserving):**

- Replace module constants `MARKDOWN_PATH`, `SOURCE_ROOT`, and the interval numbers in `compute_next_review_date()` with values loaded from `dsa.config.yml` (fallback to current defaults so cse-review-style behavior is the default).
- Generalize `SOURCE_FILE_RE` and `discover_source_problems()` from `.py`-only to the configured `globs`. The regex `(?P<number>\d+)_(?P<name>.+)\.py$` becomes extension-agnostic.
- Everything else — diff parsing, staged-only mode, summary table, sort-by-latest, legacy migration — stays untouched.

**Test hook:** add a tiny `tests/` with a fixture `dsa_progress.md` + a golden output, so adopters (and CI) can verify the engine after edits. cse-review has none today; the template should, since strangers will modify it.

---

## 5. Bootstrap & curriculum presets

The NC150 Jun–Dec 2026 table in your `study_guide.md` is the hardest-to-generalize asset — it's a *dated* plan. Solution: separate **curriculum** (ordered problem list, undated) from **schedule** (dates), and generate the dated view.

- `tracks/nc150.yml` / `tracks/blind75.yml`: ordered phases + problem lists + per-phase pacing, **no dates**. This is a faithful port of your roadmap's *content* minus the calendar.
- `scripts/bootstrap.py` (also invocable via the `dsa-init` skill) asks:
  1. Name, start date, track (nc150/blind75/custom), daily cap, solution language(s).
  2. Writes `dsa.config.yml`.
  3. Projects the chosen track's phases onto real dates from `start_date` using the pacing rules → writes a personalized `study_guide.md` roadmap table + the **week-1 schedule file** (`docs/.../schedules/<YYYYMMDD>_schedule.md`).
  4. Resets `dsa_progress.md` to header + seed row; empties logs.
  5. Runs `git config core.hooksPath .githooks`.
  6. Prints the daily loop and "how to log a result" cheat sheet.

After bootstrap the adopter's repo is behaviorally identical to cse-review on day 1.

---

## 6. The coaching skill (`.claude/skills/dsa-coach/SKILL.md`)

This is where cse-review's soul lives. It encodes, from §2b:

- **Operating principles first:** close the loop completely & proactively; the learner owns thinking and writes all code — the agent coaches, reads, explains, never edits solution source.
- **The review workflow:** on any problem mention → mark schedule → ask "Clean, Shaky, or Blank?" (with your exact definitions) → update `dsa_progress.md` → run the script (or let the hook) → proactively slot the computed next-review date into the right week's schedule.
- **Guardrails:** no spoilers/approaches unless stuck or asked; never recap approach on a retry; strict comfort bar; daily cap from config; schedule-integrity rule (never drop a problem without re-slotting it); new-vs-retry distinction; method-variant promotion rule.
- **Cadence rules:** session dating, end-of-session push, end-of-week schedule generation.

Because it's committed to the repo, `CLAUDE.md` just points at it — every adopter, on every machine, gets the behavior with zero personal-memory setup. This is the fix for the core "trapped in your memory" problem.

---

## 7. Migration / build plan (phased)

1. **Scaffold repo** — new `dsa-coach` repo, directory skeleton, licenses, README stub.
2. **Port engine** — copy `update_review_dates.py` + hook; add config loading; keep defaults = current behavior; add golden-file test.
3. **Port docs scaffold** — patterns/fundamentals as-is; blank templated tracker/logs/schedules.
4. **Author curriculum presets** — `nc150.yml` (faithful content port), `blind75.yml`.
5. **Write bootstrap** — interactive setup + date projection.
6. **Extract coaching skill** — consolidate the generalizable memory files into `SKILL.md`; wire `CLAUDE.md` to it.
7. **README + a `docs/PHILOSOPHY.md`** — the Interview-ROI line, comfort system, daily loop, backlog recovery, all currently implicit.
8. **Dogfood** — run a mock adopter flow end-to-end; verify a logged result flows through hook → tracker → schedule exactly as in cse-review.

Each phase is independently reviewable. `cse-review` is never touched.

---

## 8. Open questions for you

1. **Curriculum fidelity:** port only NC150, or also seed Blind75 (and/or a "custom/empty" track) at launch?
2. **Solution languages in the default preset:** you practice Java + Python. Ship the default glob as both, or language-pick at bootstrap only?
3. **How opinionated should the shipped skill be?** Full cse-review rigor (strict comfort bar, no-spoilers, daily cap) as non-negotiable defaults, or expose a few of these as config toggles for adopters with different philosophies?
4. **Repo home & visibility:** public GitHub template under your account, or private first? Name — `dsa-coach`, `leetcode-spaced-rep`, something else?
5. **The `self_eval_log` meta-review loop:** ship it as a default coaching mechanism, or treat it as an advanced/optional add-on?

---

## 9. What this explicitly does NOT do

- Does not modify, refactor, or migrate `cse-review`.
- Does not change the spaced-repetition math or the doc structure.
- Does not auto-publish anything public without your go-ahead on §8.4.
