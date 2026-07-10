# Design Doc: Extracting cse-review into a Reusable Mastery Coach (DSA + System Design + AI)

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

**Scope is multi-pillar, not DSA-only.** cse-review already runs two parallel pillars off the same engine and philosophy — and a third planned:

- **Pillar 1 — DSA** (`docs/foundations/dsa/`): coded LeetCode problems, code-file-driven spaced repetition.
- **Pillar 2 — System Design** (`docs/foundations/system_design/`): whole-system designs and building blocks, template-driven reps, blind-sprint review on the Sunday slot. Has its own ROI-line study guide, `templates/`, `components/`, `fundamentals/`, and a Design Practice Backlog.
- **Pillar 3 — AI System Engineering** (study-guide Phase 3): vector search, context/token management, agentic orchestration, eval/guardrails. Extends Pillar 2's model.

Both existing pillars share **one spaced-repetition engine, one ROI-line curriculum model, one comfort scale, and one weekly schedule** — Phase 2 is a *mode switch* (the 45-min block shifts from DSA to design; DSA stays warm via the 15-min maintenance flashcard), not a separate system. `dsa-coach` must ship **all pillars**, unified by the shared engine. (Name caveat: "dsa-coach" now undersells the scope — see §8 Q4.)

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
| **SD study guide** | `docs/foundations/system_design/study_guide.md` | Generalize; keep ROI-line tiers + cadence verbatim |
| **SD templates** | `system_design/templates/{case_study,component}_template.md` | Ship as-is — the scaffold *is* the rep |
| **SD components/fundamentals** | `system_design/{components,fundamentals}/**` | Ship as reference seeds (e.g. `rate_limiter.md`) |
| **SD progress tracker** | *(new — §6a)* | Parallel comfort tracker; unit = *system*, review = blind sprint |
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
│       ├── dsa-coach/SKILL.md      ← the coaching behavior (from §2b), all pillars
│       └── dsa-init/SKILL.md       ← scaffold-into-existing-repo command
├── docs/foundations/
│   ├── dsa/                        ← PILLAR 1
│   │   ├── study_guide.md          ← roadmap templated, not hardcoded
│   │   ├── mastery/
│   │   │   ├── dsa_progress.md     ← header + ONE seed row
│   │   │   ├── stuck_log.md        ← empty + template
│   │   │   └── self_eval_log.md    ← empty + template
│   │   ├── schedules/              ← empty; week 1 generated by bootstrap (SHARED across pillars)
│   │   └── patterns/**, fundamentals/** ← shipped as-is (generic reference)
│   └── system_design/              ← PILLAR 2 (§6a)
│       ├── study_guide.md          ← ROI-line tiers + Bootstrap/Transition/Mastery cadence
│       ├── mastery/design_progress.md ← comfort tracker; unit=system, review=blind sprint
│       ├── templates/{case_study,component}_template.md ← the scaffold IS the rep
│       ├── components/**, fundamentals/** ← reference seeds (rate_limiter, …)
│       └── case_studies/           ← filled from templates as adopter progresses
└── curriculum/                     ← ONE layered progression per pillar, not swappable lists (§5)
    ├── dsa/{milestone,expansion_tier1,expansion_tier2}.yml
    ├── dsa/backlog/{interview_sourced,competitive_style}.yml
    └── system_design/{tier1_interview_core,tier2_architect_depth}.yml  ← + Design Practice Backlog
```

---

## 4. Config layer — the personalization surface

Today the engine hardcodes intervals, paths, and a Python-only solution glob. Introduce **one** config file the script and skill both read.

```yaml
# dsa.config.yml
learner: "Your Name"
start_date: 2026-07-13
target: competitive      # DEFAULT. the mission-level goal. fintech_interview | faang_interview | competitive
reach_beyond: 1          # tiers to pursue PAST the target so it's hit with margin (see §5)
daily_cap: 5

intervals:              # days until next review, by Comfort + streak
  clean:  { streak1: 30, streak2: 60, retired: 180 }
  shaky:  10
  blank:  2
retire_at_streak: 3

solutions:
  # DEFAULT is Python-only; engine stays language-agnostic so adopters can widen this
  roots: ["dsa/leetcode"]
  globs: ["*.py"]                        # widen to *.java, *.ts, … at bootstrap if desired
  filename_pattern: "{number}_{name}"   # 19_remove_nth_node.py
```

**Script changes (surgical, behavior-preserving):**

- Replace module constants `MARKDOWN_PATH`, `SOURCE_ROOT`, and the interval numbers in `compute_next_review_date()` with values loaded from `dsa.config.yml` (fallback to current defaults so cse-review-style behavior is the default).
- Generalize `SOURCE_FILE_RE` and `discover_source_problems()` from `.py`-only to the configured `globs`. The regex `(?P<number>\d+)_(?P<name>.+)\.py$` becomes extension-agnostic.
- Everything else — diff parsing, staged-only mode, summary table, sort-by-latest, legacy migration — stays untouched.

**Test hook:** add a tiny `tests/` with a fixture `dsa_progress.md` + a golden output, so adopters (and CI) can verify the engine after edits. cse-review has none today; the template should, since strangers will modify it.

### 4a. Configurability contract (DECIDED: pedagogy locked, logistics configurable)

The pedagogy is *why the system works*; loosening it produces a weaker product wearing the same name. So the line is drawn once, explicitly:

**🔒 Locked — non-negotiable, not exposed as config; enforced by the coaching skill:**

- Strict comfort bar (🟢 Clean only from a blank page, correct complexity, zero hints; "mostly remembered" = 🟡 Shaky)
- No spoilers / no approach hints unless the learner is stuck or explicitly asks; never recap approach on a retry
- No code edits by the agent — the learner writes every line
- Phase-completion = every associated problem 🏆 Retired (§5)
- Reach-beyond posture — the curriculum always overshoots the target (§5)

**⚙️ Configurable — situational logistics, exposed in `dsa.config.yml`:**

- `daily_cap`, time cap (45-min default), `intervals` (Clean/Shaky/Blank days), `retire_at_streak`
- `target` + `reach_beyond` (which tiers are in scope)
- `solutions` globs/roots (language)

Adopters tune *when and how much* they study; they cannot dilute *the standard*. A future `--strict=false` escape hatch is explicitly rejected here — if someone wants a lenient tracker, this isn't it.

---

## 5. Curriculum model — reach beyond the target so you always hit it

**This is the heart of cse-review and the part I got wrong the first time.** The mission is *not* "finish NC150." Per `study_guide.md`, the mission is to become a **competent competitive programmer**, and **interview readiness is a milestone on that path, not the finish line.** The whole plan is organized around the **Interview-ROI Line**, and it deliberately trains *past* the interview target so the target itself is cleared with margin. Aim beyond → reliably hit.

So `dsa-coach` must NOT model curriculum as swappable problem lists (NC150 vs Blind75 — that was the mistake; Blind75 is a *subset*, not a reach-beyond). It models **one layered progression** with the ROI line as its spine:

```
  milestone            interview foundation (NC150 content) + framework lenses
     │                 + cross-cutting pattern docs  ← this alone clears most interviews
     ▼
  expansion tier 1     segment tree, Fenwick, KMP, XOR trie, Manacher's, matrix expo,
     │                 Tarjan's, meet-in-the-middle, difference array, number theory
     │                 ← still shows up in HARD interviews; TOP of the ROI curve
  ═══╪═══ INTERVIEW-ROI LINE ═══════════════════════════════════════════
     ▼
  expansion tier 2     sweep line, max-flow, LCA, Mo's, SOS DP, suffix automaton,
                       Aho-Corasick, persistent structures ← competitive-programming
                       horizon; near-zero interview payoff, pursued for mastery
```

**The overshoot rule (config-driven):** the adopter declares a `target` (the milestone they must hit) and a `reach_beyond` margin. **Default target is `competitive`** — the mission-level goal, not an interview checkpoint — because reaching for competitive depth is *how* the interview target is cleared with margin in the first place. The curriculum they receive is *everything up to their target, plus `reach_beyond` tiers past it* — so even a "faang_interview" target with `reach_beyond: 1` still pulls Tier-1 advanced into rotation. This is exactly your Post-NC150 steady state (Maintenance · Application-*pull-not-push* · deliberate Expansion) generalized: knowledge always reaches one layer beyond the immediate goal.

**Application backlog pools (the "pull, not push" thread).** Learning problems are only half the curriculum. Each phase has an associated **curated backlog pool** of application problems — sourced from real interviews and gated by the patterns already learned — that you *pull* from to build speed and transfer. cse-review already curated a large **interview-sourced backlog** used *during* the knowledge-expansion phase (post-NC150). The generalized model extends this symmetrically: a second, **competitive-style backlog pool** for the phase *after* knowledge expansion (Tier 2 / competitive), so the pull-not-push mechanic keeps running past the ROI line. Pools are curriculum data, not schedule data — the coach pulls from the pool that matches the learner's current tier, never marching a list top-to-bottom.

| Phase | Learning content | Application backlog pool |
|-------|------------------|--------------------------|
| Milestone (NC150) | roadmap phases | (light; roadmap is the work) |
| Expansion Tier 1 (post-NC150, above ROI line) | segment tree, KMP, XOR trie, … | **interview-sourced backlog** (curated) |
| Expansion Tier 2 (below ROI line) | max-flow, Mo's, suffix automaton, … | **competitive-style backlog** (curated) |

**Phase-completion definition (concrete, tied to retirement).** A phase is **fully complete only when every problem associated with that phase is 🏆 Retired** (Streak 3+ Clean) — *not* when each has been attempted or solved once. This binds curriculum progress directly to the spaced-repetition state already tracked in `dsa_progress.md`: a phase's learning problems *and* its pulled backlog problems must all reach retirement before the phase counts as done. The coach reports phase progress as "N of M problems retired" and does not advance the learner's headline phase until the count is complete. This becomes an explicit rule in the coaching skill (§6).

**Curriculum vs. schedule split (still needed for date-independence):** the NC150 Jun–Dec 2026 table is a *dated* artifact — the hardest thing to generalize. Separate the **curriculum** (ordered phases + problem lists + backlog pools + pacing, undated, in `curriculum/*.yml`) from the **schedule** (real dates), and generate the dated view per adopter.

- `curriculum/milestone.yml`, `expansion_tier1.yml`, `expansion_tier2.yml`: faithful port of your roadmap's *content and ordering*, minus the calendar, tagged by ROI-line tier and pacing (e.g. DP phases drop to 3/week). Each carries its associated `backlog_pool` (interview-sourced for Tier 1, competitive-style for Tier 2).
- `scripts/bootstrap.py` (also invocable via the `dsa-init` skill) asks:
  1. Name, start date, **target** milestone, **reach_beyond** margin, daily cap, solution language(s).
  2. Writes `dsa.config.yml`.
  3. Assembles the curriculum = milestone → target → `+reach_beyond` tiers, projects its phases onto real dates from `start_date` using each phase's pacing rules → writes a personalized `study_guide.md` roadmap table + the **week-1 schedule file** (`docs/.../schedules/<YYYYMMDD>_schedule.md`), with the ROI line and the reach-beyond section preserved.
  4. Resets `dsa_progress.md` to header + seed row; empties logs.
  5. Runs `git config core.hooksPath .githooks`.
  6. Prints the daily loop, the overshoot philosophy, and the "how to log a result" cheat sheet.

After bootstrap the adopter's repo is behaviorally identical to cse-review on day 1 — including the reach-beyond posture, not just an interview checklist.

---

## 6. The coaching skill (`.claude/skills/dsa-coach/SKILL.md`)

This is where cse-review's soul lives. It encodes, from §2b:

- **Operating principles first:** close the loop completely & proactively; the learner owns thinking and writes all code — the agent coaches, reads, explains, never edits solution source.
- **The review workflow:** on any problem mention → mark schedule → ask "Clean, Shaky, or Blank?" (with your exact definitions) → update `dsa_progress.md` → run the script (or let the hook) → proactively slot the computed next-review date into the right week's schedule.
- **Guardrails:** no spoilers/approaches unless stuck or asked; never recap approach on a retry; strict comfort bar; daily cap from config; schedule-integrity rule (never drop a problem without re-slotting it); new-vs-retry distinction; method-variant promotion rule.
- **Phase-completion rule:** a phase is complete only when *every* associated problem (learning + pulled backlog) is 🏆 Retired. Report "N of M retired"; never advance the headline phase early. (§5)
- **Application pull rule:** during a tier, pull backlog problems from that tier's pool gated by learned patterns — never march a list top-to-bottom; a 🟡/🔴 pull is a diagnostic, not a cue to learn something ad-hoc.
- **System-design review workflow (§6a):** on a design session → drive it through the right template → ask Clean/Shaky/Blank on the *blind sprint* → update `design_progress.md` → slot the next blind sprint. Same comfort scale, different unit and rep.
- **Cadence rules:** session dating, end-of-session push, end-of-week schedule generation; the **Sunday slot is the system-design sprint** and Phase 2 is a mode-switch (45-min block → design, DSA warm via 15-min flashcard).

Because it's committed to the repo, `CLAUDE.md` just points at it — every adopter, on every machine, gets the behavior with zero personal-memory setup. This is the fix for the core "trapped in your memory" problem.

---

## 6a. The System Design pillar

System design reuses **the same engine and philosophy** as DSA, with three deliberate differences in the *unit* and the *rep*:

| Dimension | DSA pillar | System Design pillar |
|-----------|-----------|----------------------|
| Unit tracked | a coded problem (source file) | a **system** or building block |
| The rep | write the solution from a blank page | **fill a template** (case-study or component); the scaffold *is* the rep |
| Review trigger | re-solve / no-code blueprint | **blind sprint** — design a system from ~2 weeks ago cold, then compare |
| Discovery source | `dsa/leetcode/*.py` files | Design Practice Backlog + `components/` coverage |
| Progress artifact | `dsa_progress.md` | `design_progress.md` (parallel comfort tracker) |

**What stays identical (the point of unifying):**

- **Same ROI-line spine.** SD Tier 1 = Interview Core (fundamentals/estimation, building blocks, data layer, the interview framework, canonical designs). Tier 2 = Architect Depth (DDIA cover-to-cover, consensus, distributed transactions, storage engines, papers). Tier 3 = research horizon. Same "reach beyond the target" overshoot.
- **Same comfort scale + interval engine.** A blind sprint scores 🟢/🟡/🔴 and the *same* `compute_next_review_date()` sets the next sprint. `design_progress.md` uses the same columns; the engine needs a second configured `(tracker_path, discovery)` pair, not new math.
- **Same phase-completion rule.** An SD phase is done only when its systems are 🏆 Retired (repeatedly designed cold and clean), not merely read about once.
- **Same staged cadence** already in the guide: **Bootstrap** (watch → recall → check gaps) → **Transition** (sketch cold → compare) → **Mastery** (~45-min timed mock, self-scored against the framework). These map onto the comfort progression naturally.

**Engine implication:** generalize the script from one hardcoded tracker to a small list of **pillar configs**, each with its own `tracker_path`, `discovery` rule (source-file glob for DSA; template/backlog for SD), and shared intervals. Behavior-preserving for DSA (it's just pillar #1). This is the only non-trivial code change the multi-pillar scope adds.

**Templates are first-class.** Ship `case_study_template.md` and `component_template.md` as-is — the coaching skill enforces "drive every practice session through the template; filling the scaffold *is* the rep, don't just read."

---

## 7. Migration / build plan (phased)

1. **Scaffold repo** — new repo, directory skeleton (both pillars), licenses, README stub.
2. **Port engine (multi-pillar)** — copy `update_review_dates.py` + hook; add config loading; generalize from one hardcoded tracker to a list of pillar configs (DSA = pillar #1, behavior-preserving); keep defaults = current behavior; add golden-file test.
3. **Port DSA scaffold** — patterns/fundamentals as-is; blank templated tracker/logs/schedules.
4. **Port System Design pillar** — SD `study_guide.md` (ROI-line tiers + cadence), `templates/` and `components`/`fundamentals` seeds as-is; new blank `design_progress.md`; Design Practice Backlog.
5. **Author the layered curriculum + backlog pools** — DSA `milestone`/`expansion_tier1`/`expansion_tier2` + backlog pools (interview-sourced, competitive-style); SD `tier1_interview_core`/`tier2_architect_depth` + Design Practice Backlog. All ROI-line-tagged.
6. **Write bootstrap** — interactive setup + date projection across both pillars (weekday DSA + Sunday SD sprint).
7. **Extract coaching skill** — consolidate the generalizable memory files into `SKILL.md`, incl. the SD review workflow; wire `CLAUDE.md` to it.
8. **README + a `docs/PHILOSOPHY.md`** — the Interview-ROI line (both pillars), comfort system, daily loop, mode-switch to Phase 2, backlog recovery — all currently implicit.
9. **Dogfood** — run a mock adopter flow end-to-end for BOTH pillars; verify a logged DSA result *and* a blind-sprint result each flow through hook → tracker → schedule exactly as in cse-review.

Each phase is independently reviewable. `cse-review` is never touched.

---

## 8. Open questions for you

1. **Overshoot defaults:** what `target` options ship at launch (fintech / faang / competitive), and what default `reach_beyond` margin? Do we ever allow `reach_beyond: 0`, or is reaching-past-the-target a non-negotiable that we refuse to let an adopter disable?
2. ~~**Solution languages in the default preset**~~ — **DECIDED: default Python-only (`globs: ["*.py"]`); engine stays language-agnostic so adopters can widen at bootstrap.**
3. ~~**How opinionated should the shipped skill be?**~~ — **DECIDED: pedagogy locked, logistics configurable (see §4a Configurability contract).**
4. **Repo home, visibility & name:** public GitHub template under your account, or private first? **Naming now matters more — the scope is DSA + System Design + (AI), so "dsa-coach" undersells it.** Candidates: `interview-mastery-coach`, `swe-mastery`, `roi-coach`, `cse-coach` (echoing cse-review), something else?
5. **The `self_eval_log` meta-review loop:** ship it as a default coaching mechanism, or treat it as an advanced/optional add-on?
6. **AI System Engineering pillar (Phase 3):** ship it now as a third pillar (study guide + tracker), or stub it and add after the two core pillars are dogfooded?

---

## 9. What this explicitly does NOT do

- Does not modify, refactor, or migrate `cse-review`.
- Does not change the spaced-repetition math or the doc structure.
- Does not auto-publish anything public without your go-ahead on §8.4.
