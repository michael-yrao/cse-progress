# Design Doc: Extracting cse-review into a Reusable Mastery Coach (DSA + System Design + AI)

**Status:** Draft for review
**Author:** Claude (with michael-yrao)
**Date:** 2026-07-09
**Decision baseline:** Ship a **new separate repo** (`cse-coach`). `cse-review` stays 100% intact — no refactors, no data moved out. The new repo mirrors the cse-review workflow as closely as possible so an engineer who adopts it gets *your* system, not a diluted version.

---

## 1. Problem statement

`cse-review` is a working, opinionated spaced-repetition DSA coaching system. Its value is not the data — it's the **machinery + the coaching behavior**:

- A Comfort→interval spaced-repetition engine (`scripts/update_review_dates.py`)
- A version-controlled git hook that runs it automatically on commit
- A rigorous agent workflow (ask Clean/Shaky/Blank → log → schedule → never spoil)
- A documented study scaffold (study guide, weekly schedules, progress tracker, stuck log, pattern library)

Today all of this is fused to one person: your NC150 Jun–Dec 2026 roadmap, your filled schedules, your progress rows, your career folder, and — critically — behavior that lives in **your personal `~/.claude` memory**, which no one else inherits.

**Goal:** produce `cse-coach`, a repo any engineer can adopt in <10 minutes and get the identical system seeded to their own start date and track, with the coaching behavior traveling *with the repo* rather than depending on a personal memory store.

**Scope is multi-pillar, not DSA-only.** cse-review runs three pillars off the same engine and philosophy, **all shipping in v1** (Q6 DECIDED):

- **Pillar 1 — DSA** (`docs/foundations/dsa/`): coded LeetCode problems, code-file-driven spaced repetition.
- **Pillar 2 — System Design** (`docs/foundations/system_design/`): whole-system designs and building blocks, template-driven reps, blind-sprint review on the Sunday slot. Has its own ROI-line study guide, `templates/`, `components/`, `fundamentals/`, and a Design Practice Backlog.
- **Pillar 3 — AI System Engineering** (study-guide Phase 3): vector search, context/token management, agentic orchestration, eval/guardrails. Extends Pillar 2's model (study guide + tracker + templates).

All three pillars share **one spaced-repetition engine, one ROI-line curriculum model, one comfort scale, and one weekly schedule** — Phase 2 is a *mode switch* (the 45-min block shifts from DSA to design; DSA stays warm via the 15-min maintenance flashcard), and Phase 3 (AI) extends the same model. `cse-coach` (name **DECIDED**, echoing `cse-review`) ships **all three pillars in v1**, unified by the shared engine.

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

| Memory file | Generalizable? | Destination in `cse-coach` |
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
| `feedback_self_evaluation.md` + `self_eval_log.md` | ✅ Core (Q5 DECIDED: default) | Skill body + empty `self_eval_log.md`; ships ON for every adopter, not your entries |

**Key decision:** these become a **committed skill** (`.claude/skills/cse-coach/SKILL.md`) inside the template repo, so they load for anyone working in an adopter's repo — no dependency on personal `~/.claude/memory`. Adopters can still layer their own private memory on top; the baseline behavior is guaranteed.

### 2c. Strictly personal (never ships)

- `career/**` (resume, performance reviews, trajectory)
- Your populated `dsa_progress.md` rows, filled `schedules/*.md`, real `stuck_log.md` entries
- Your NC150 Jun–Dec 2026 dated roadmap (becomes a *generated* artifact, see §5)
- `.claude/memory/user_profile.md`, `career_trajectory.md`, and anything MS/fintech-specific

---

## 3. Distribution shape

`cse-coach` is **both** a GitHub *template repository* and the carrier of a *portable skill* — the "Both" model, achieved with one repo:

- **Turnkey path:** engineer clicks **Use this template** → runs bootstrap → has their own tracker.
- **Drop-in path:** the same repo's `.claude/skills/cse-coach/` + `scripts/` can be copied into an existing practice repo; a `cse-init` skill scaffolds the docs/hook there.

One repo, one source of truth for the script, two adoption routes. No second codebase to keep in sync.

```
cse-coach/
├── README.md                       ← engineer-facing onboarding + philosophy
├── CLAUDE.md                       ← generalized workflow (paths/dates parameterized)
├── cse.config.yml                  ← THE personalization surface (§4)
├── .githooks/pre-commit            ← generalized copy of yours
├── scripts/
│   ├── update_review_dates.py      ← config-driven (§4)
│   └── bootstrap.py                ← interactive setup (§5)
├── .claude/
│   └── skills/
│       ├── cse-coach/SKILL.md      ← the coaching behavior (from §2b), all pillars
│       └── cse-init/SKILL.md       ← scaffold-into-existing-repo command
├── docs/foundations/
│   ├── dsa/                        ← PILLAR 1
│   │   ├── study_guide.md          ← roadmap templated, not hardcoded
│   │   ├── mastery/
│   │   │   ├── dsa_progress.md     ← header + ONE seed row
│   │   │   ├── stuck_log.md        ← empty + template
│   │   │   └── self_eval_log.md    ← empty + template
│   │   ├── templates/solution_template.py ← dated skeleton, scaffolded before coding (§6b)
│   │   ├── schedules/              ← empty; week 1 generated by bootstrap (SHARED across pillars)
│   │   └── patterns/**, fundamentals/** ← shipped as-is (generic reference)
│   ├── system_design/              ← PILLAR 2 (§6a)
│   │   ├── study_guide.md          ← ROI-line tiers + Bootstrap/Transition/Mastery cadence
│   │   ├── mastery/design_progress.md ← comfort tracker; unit=system, review=blind sprint
│   │   ├── templates/{case_study,component}_template.md ← the scaffold IS the rep
│   │   ├── components/**, fundamentals/** ← reference seeds (rate_limiter, …)
│   │   └── case_studies/           ← filled from templates as adopter progresses
│   └── ai_engineering/             ← PILLAR 3 (§6c) — ships in v1
│       ├── study_guide.md          ← ROI-line tiers: RAG/vector search → serving → agents → eval
│       ├── mastery/ai_progress.md  ← comfort tracker; unit=capability/build, review=blind rebuild
│       └── templates/**, components/** ← template-driven, mirrors the SD pillar
└── curriculum/                     ← ONE layered progression per pillar, not swappable lists (§5)
    ├── dsa/{milestone,expansion_tier1,expansion_tier2}.yml
    ├── dsa/backlog/{interview_sourced,competitive_style}.yml
    ├── system_design/{tier1_interview_core,tier2_architect_depth}.yml  ← + Design Practice Backlog
    └── ai_engineering/{tier1_core,tier2_depth}.yml
```

---

## 4. Config layer — the personalization surface

Today the engine hardcodes intervals, paths, and a Python-only solution glob. Introduce **one** config file the script and skill both read.

```yaml
# cse.config.yml
learner: "Your Name"
start_date: 2026-07-13
target: competitive      # DEFAULT. the mission-level goal. fintech_interview | faang_interview | competitive
reach_beyond: 1          # tiers PAST the target so it's hit with margin. MIN 1, enforced — 0 is rejected (see §5)
daily_cap: 5

pillars:                 # which pillars to run and how to weight focus (§5a)
  priority: [dsa, system_design, ai_engineering]   # ordered emphasis; adopter's choice
  # readiness gates are RECOMMENDED, not hard locks — the coach warns on front-running,
  # a fluent senior can override. Defaults below (mastery-based, not week-based):
  gates:
    system_design_primary:            # earliest to make SD the main 45-min block
      recommend_after: "dsa.milestone >= 60% retired AND {hashing, heap, trees, graphs} comfortable"
      # (SD's light Sunday on-ramp has NO gate — encouraged from week 1)
    ai_engineering:                   # earliest to start the AI pillar
      recommend_after: "system_design.tier1 majority retired"

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

- Replace module constants `MARKDOWN_PATH`, `SOURCE_ROOT`, and the interval numbers in `compute_next_review_date()` with values loaded from `cse.config.yml` (fallback to current defaults so cse-review-style behavior is the default).
- Generalize `SOURCE_FILE_RE` and `discover_source_problems()` from `.py`-only to the configured `globs`. The regex `(?P<number>\d+)_(?P<name>.+)\.py$` becomes extension-agnostic.
- Everything else — diff parsing, staged-only mode, summary table, sort-by-latest, legacy migration — stays untouched.

**Test hook:** add a tiny `tests/` with a fixture `dsa_progress.md` + a golden output, so adopters (and CI) can verify the engine after edits. cse-review has none today; the template should, since strangers will modify it.

### 4a. Configurability contract (DECIDED: pedagogy locked, logistics configurable)

The pedagogy is *why the system works*; loosening it produces a weaker product wearing the same name. So the line is drawn once, explicitly:

**🔒 Locked — non-negotiable, not exposed as config; enforced by the coaching skill:**

- Strict comfort bar (🟢 Clean only from a blank page, correct complexity, zero hints; "mostly remembered" = 🟡 Shaky)
- **Coding is required for Clean (DSA).** A 🟢 Clean is only earned by *coding the solution* from a blank page. A no-code blueprint/verbal walk-through **can never land Clean** — it caps at 🟡 Shaky no matter how flawless. This is a **deliberate divergence from cse-review**, which lets a flawless no-code warmup log Clean; the owner prefers coding to be the default rep and the sole path to Clean. (See §4b for the no-code opt-in.)
- No spoilers / no approach hints unless the learner is stuck or explicitly asks; never recap approach on a retry
- No code edits by the agent — the learner writes every line
- **Whiteboard fidelity** — no shared boilerplate/`datamodel` library; the learner writes the *full* solution from scratch every time, including `ListNode`/`TreeNode` definitions, as on an interview whiteboard (§6b)
- Phase-completion = every associated problem 🏆 Retired (§5)
- Reach-beyond posture — the curriculum always overshoots the target (§5)

**⚙️ Configurable — situational logistics, exposed in `cse.config.yml`:**

- `daily_cap`, time cap (45-min default), `intervals` (Clean/Shaky/Blank days), `retire_at_streak`
- `target` + `reach_beyond` (which tiers are in scope; `reach_beyond` floored at 1)
- `solutions` globs/roots (language)
- **`pillars.priority`** — which pillar leads (DSA / System Design / AI); the readiness gates are *recommendations* the coach warns on, not locks (§5a)
- **`rep_mode` per session: `code` (default) or `no_code` opt-in** — see §4b

Adopters tune *when and how much* they study; they cannot dilute *the standard*. A future `--strict=false` escape hatch is explicitly rejected here — if someone wants a lenient tracker, this isn't it.

### 4b. DSA rep mode — code by default, no-code is an opt-in that can't reach Clean

cse-review leans on a **no-code blueprint** format for its 15-min warmup/maintenance slots (state the complexity + core trick out loud, verify against past code). The owner is **not a fan of that as the DSA default** — most DSA reps should be *actually coded*. So `cse-coach` inverts the emphasis:

- **Default rep = code it.** New problems and reviews alike default to writing the solution from a blank page. This is the normal path and the only one that can earn 🟢 Clean.
- **No-code is opt-in, per session.** A learner *may* choose a no-code blueprint rep (useful when time-boxed, or for a light maintenance touch), but it's an explicit choice, not the default.
- **Hard ceiling on no-code.** A no-code rep is capped at 🟡 Shaky — it keeps the problem warm and updates the review clock, but it **cannot advance a streak toward retirement**, because retirement (§5) requires repeated *coded* Cleans. The coaching skill enforces this: if the learner reports "Clean" on a session they didn't code, the coach records 🟡 Shaky and says why.
- **System Design is unaffected** — its rep is template-fill + blind sprint (§6a); "coding" doesn't apply there. This rule is DSA-pillar-specific.

---

## 5. Curriculum model — reach beyond the target so you always hit it

**This is the heart of cse-review and the part I got wrong the first time.** The mission is *not* "finish NC150." Per `study_guide.md`, the mission is to become a **competent competitive programmer**, and **interview readiness is a milestone on that path, not the finish line.** The whole plan is organized around the **Interview-ROI Line**, and it deliberately trains *past* the interview target so the target itself is cleared with margin. Aim beyond → reliably hit.

So `cse-coach` must NOT model curriculum as swappable problem lists (NC150 vs Blind75 — that was the mistake; Blind75 is a *subset*, not a reach-beyond). It models **one layered progression** with the ROI line as its spine:

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

**The overshoot rule (config-driven, floor enforced):** the adopter declares a `target` (the milestone they must hit) and a `reach_beyond` margin. **Default target is `competitive`** — the mission-level goal, not an interview checkpoint — because reaching for competitive depth is *how* the interview target is cleared with margin in the first place. The curriculum they receive is *everything up to their target, plus `reach_beyond` tiers past it* — so even a "faang_interview" target with `reach_beyond: 1` still pulls Tier-1 advanced into rotation. This is exactly your Post-NC150 steady state (Maintenance · Application-*pull-not-push* · deliberate Expansion) generalized: knowledge always reaches one layer beyond the immediate goal.

**`reach_beyond: 0` is rejected (DECIDED).** Reaching for the end is non-negotiable — the same spirit as the locked pedagogy (§4a). The minimum margin is **1**; bootstrap and the engine refuse `0` and clamp to 1 with a note. There is no interview-only, no-overshoot mode; "always reach for the end goal" is the whole point of the tool.

**Application backlog pools (the "pull, not push" thread).** Learning problems are only half the curriculum. Each phase has an associated **curated backlog pool** of application problems — sourced from real interviews and gated by the patterns already learned — that you *pull* from to build speed and transfer. cse-review already curated a large **interview-sourced backlog** used *during* the knowledge-expansion phase (post-NC150). The generalized model extends this symmetrically: a second, **competitive-style backlog pool** for the phase *after* knowledge expansion (Tier 2 / competitive), so the pull-not-push mechanic keeps running past the ROI line. Pools are curriculum data, not schedule data — the coach pulls from the pool that matches the learner's current tier, never marching a list top-to-bottom.

| Phase | Learning content | Application backlog pool |
|-------|------------------|--------------------------|
| Milestone (NC150) | roadmap phases | (light; roadmap is the work) |
| Expansion Tier 1 (post-NC150, above ROI line) | segment tree, KMP, XOR trie, … | **interview-sourced backlog** (curated) |
| Expansion Tier 2 (below ROI line) | max-flow, Mo's, suffix automaton, … | **competitive-style backlog** (curated) |

**Phase-completion definition (concrete, tied to retirement).** A phase is **fully complete only when every problem associated with that phase is 🏆 Retired** (Streak 3+ Clean) — *not* when each has been attempted or solved once. This binds curriculum progress directly to the spaced-repetition state already tracked in `dsa_progress.md`: a phase's learning problems *and* its pulled backlog problems must all reach retirement before the phase counts as done. The coach reports phase progress as "N of M problems retired" and does not advance the learner's headline phase until the count is complete. This becomes an explicit rule in the coaching skill (§6).

**Curriculum vs. schedule split (still needed for date-independence):** the NC150 Jun–Dec 2026 table is a *dated* artifact — the hardest thing to generalize. Separate the **curriculum** (ordered phases + problem lists + backlog pools + pacing, undated, in `curriculum/*.yml`) from the **schedule** (real dates), and generate the dated view per adopter.

- `curriculum/milestone.yml`, `expansion_tier1.yml`, `expansion_tier2.yml`: faithful port of your roadmap's *content and ordering*, minus the calendar, tagged by ROI-line tier and pacing (e.g. DP phases drop to 3/week). Each carries its associated `backlog_pool` (interview-sourced for Tier 1, competitive-style for Tier 2).
- `scripts/bootstrap.py` (also invocable via the `cse-init` skill) runs a short intake. **Present ALL questions at once** — a single warm, well-framed block the learner answers in one pass, not a slow one-at-a-time interrogation. **Tone matters: warm, brief, a sentence of *why* where it helps, plain language.** It gathers, in one shot:
  1. Name; start date; **target** milestone; **reach_beyond** (mostly handled *for* the learner — note it's ≥1 and non-negotiable rather than asking a "margin" number); daily cap; solution language; **pillar priority** (which pillar leads).
  1b. *After* the learner submits, if the chosen priority leads with SD/AI, deliver the readiness gate as gentle push-back (not a block): name the prerequisite in human terms ("heaps/graphs are the same ideas as priority queues and replication, just wearing a suit"), offer the light on-ramp, proceed only on explicit override.
  2. Writes `cse.config.yml`.
  3. Assembles the curriculum = milestone → target → `+reach_beyond` tiers, projects its phases onto real dates from `start_date` using each phase's pacing rules → writes a personalized `study_guide.md` roadmap table + the **week-1 schedule file** (`docs/.../schedules/<YYYYMMDD>_schedule.md`), with the ROI line and the reach-beyond section preserved.
  4. Resets `dsa_progress.md` to header + seed row; empties logs.
  5. Runs `git config core.hooksPath .githooks`.
  6. Signs off in the same voice: names tomorrow's first problem, and reminds the learner the *only* reporting ever asked is "Clean, Shaky, or Blank?"

**Voice guideline (applies to the whole coach, not just bootstrap):** the coach speaks like a supportive human mentor — encouraging, concise, honest. It explains the *why* behind a rule in a sentence, pushes back kindly when a learner front-runs, and never reads like a CLI prompt or a compliance checklist. A reference sample of the intake dialogue lives in the README/`docs/PHILOSOPHY.md` so the tone is pinned, not left to chance.

After bootstrap the adopter's repo is behaviorally identical to cse-review on day 1 — including the reach-beyond posture, not just an interview checklist.

---

## 5a. Pillar priority & readiness gates (adopter chooses; coach advises)

Adopters **choose which pillar to prioritize** (`pillars.priority` in the config). Priority is *logistics* (configurable, per §4a) — but ordering is not free of consequences, because each later pillar reasons in the vocabulary of the earlier one. So the coach ships **recommended readiness gates**: it doesn't hard-block, it **warns when a learner front-runs a prerequisite** and lets a fluent senior override.

**Recommended earliest uptake (mastery-based, not week-based — consistent with phase = retired):**

| Pillar | Earliest to make it the *primary* focus | Why this gate |
|--------|------------------------------------------|---------------|
| **DSA** | Immediately — default first priority for anyone who can't yet code the fundamental patterns cold. | It's the base vocabulary everything else borrows. |
| **System Design — light on-ramp** (Sunday sprint, Bootstrap stage) | **Week 1, no gate.** Encouraged from the start. | Zero-cost, builds vocabulary; the "trace a user journey" sketch needs no DSA. |
| **System Design — primary** (Phase-2 mode-switch, the 45-min block) | **DSA milestone core ~60%+ 🏆 retired, and {hashing, heap, trees, graphs} comfortable cold.** | SD reasoning leans on exactly these: hashmaps → indexes/sharding keys, heaps → priority queues/scheduling, graphs/trees → dependency & replication topologies. Front-running dilutes both. |
| **AI System Engineering** | **System Design Tier 1 (interview core) majority 🏆 retired** — building blocks (LB, caching, queues, CDN), data layer (SQL/NoSQL, sharding, replication, consistency), and the interview framework. | AI infra *is* system design specialized for ML/LLM serving. Vector DBs, token/context management, GPU batching, RAG, eval/guardrails all assume fluency in caching, queues, sharding, API design. Starting earlier = learning distributed-systems fundamentals and AI-specific concerns at once. |

**Two speeds for System Design (important nuance):** the *light Sunday on-ramp* is ungated and encouraged immediately; only *SD-as-primary-focus* carries the DSA-retirement gate. This mirrors cse-review, which runs the Sunday sprint during Phase 1 while DSA is still the weekday main event.

**Coach behavior at a gate:** if a learner sets `priority` to lead with SD or AI before the recommended mastery, the coach (a) states the recommended prerequisite and *why*, (b) offers to start the light on-ramp instead where one exists, and (c) proceeds anyway if the learner confirms — recording that they overrode. It never silently blocks, and never silently lets them skip the warning.

---

## 6. The coaching skill (`.claude/skills/cse-coach/SKILL.md`)

> **A full draft of this skill exists: [`cse-coach-skill-draft.md`](cse-coach-skill-draft.md).** It moves to `.claude/skills/cse-coach/SKILL.md` in the new repo at build time (§7 step 8). The bullets below are the outline; the draft is the operative text.

This is where cse-review's soul lives. It encodes, from §2b:

- **Operating principles first:** close the loop completely & proactively; the learner owns thinking and writes all code — the agent coaches, reads, explains, never edits solution source.
- **Voice:** speak like a supportive human mentor — warm, concise, honest; a sentence of *why* behind each rule; kind push-back, never a CLI prompt or compliance checklist (see §5 voice guideline + the pinned intake sample).
- **The review workflow:** on any problem mention → mark schedule → ask "Clean, Shaky, or Blank?" (with your exact definitions) → update `dsa_progress.md` → run the script (or let the hook) → proactively slot the computed next-review date into the right week's schedule.
- **Coding-for-Clean rule (DSA):** the default rep is coding; no-code is an explicit opt-in and is hard-capped at 🟡 Shaky. If a learner reports "Clean" on a session they didn't code, record 🟡 Shaky and say why. (§4b)
- **Scaffold-first rule (DSA):** when a problem is started, generate the empty dated skeleton from `solution_template.py` (path, URL, pattern, `Attempt N · <today>` banner, `pass` stub) *before* the learner codes — but never write solution logic or data-structure definitions (§6b, respects the §4a lock).
- **Guardrails:** no spoilers/approaches unless stuck or asked; never recap approach on a retry; strict comfort bar; daily cap from config; schedule-integrity rule (never drop a problem without re-slotting it); new-vs-retry distinction; method-variant promotion rule.
- **Phase-completion rule:** a phase is complete only when *every* associated problem (learning + pulled backlog) is 🏆 Retired. Report "N of M retired"; never advance the headline phase early. (§5)
- **Application pull rule:** during a tier, pull backlog problems from that tier's pool gated by learned patterns — never march a list top-to-bottom; a 🟡/🔴 pull is a diagnostic, not a cue to learn something ad-hoc.
- **System-design review workflow (§6a):** on a design session → drive it through the right template → ask Clean/Shaky/Blank on the *blind sprint* → update `design_progress.md` → slot the next blind sprint. Same comfort scale, different unit and rep.
- **Self-eval meta-loop (ships ON, Q5):** on any correction from the learner, append it to `self_eval_log.md`; run a weekly meta-review to promote recurring corrections into standing rules. This is a default coaching mechanism for every adopter, not an add-on.
- **Readiness-gate advisory (§5a):** honor the adopter's `pillars.priority`, but when they lead with System Design or AI before the recommended DSA/SD retirement, state the prerequisite + why, offer the light on-ramp where one exists, and proceed only on explicit override (recording it). Warn, never silently block or silently skip.
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

**Engine implication:** generalize the script from one hardcoded tracker to a small list of **pillar configs** (DSA, System Design, AI — §6c), each with its own `tracker_path`, `discovery` rule (source-file glob for DSA; template/backlog for SD & AI), and shared intervals. Behavior-preserving for DSA (it's just pillar #1). This is the only non-trivial code change the multi-pillar scope adds — and it's written once for all three pillars.

**Templates are first-class.** Ship `case_study_template.md` and `component_template.md` as-is — the coaching skill enforces "drive every practice session through the template; filling the scaffold *is* the rep, don't just read."

---

## 6b. DSA solution-file template & scaffolding (the scaffold before you start)

Observed convention in cse-review (to standardize, not reinvent):

- Path: `dsa/leetcode/<category>/<number>_<snake_name>.py` — matches the engine's `{number}_{name}` discovery + `filename_pattern`.
- One `class Solution` holds **dated method variants** (e.g. `removeNthFromEnd`, `removeNthFromEndRecursion`). Dating isn't consistent today — **this template is where the "date my classes/methods" convention gets standardized going forward.**
- **No difficulty token line.** (An early cse-review experiment; the owner has dropped it.) Difficulty is set on the tracker row at log time by the coach, not parsed from the source file. The engine's `extract_difficulty_from_source()` stays as a harmless no-op fallback but the template does **not** carry a difficulty line.
- **No shared data-model imports.** Each solution declares its own `ListNode` / `TreeNode` / etc. from scratch — see the whiteboard-fidelity rule below.

**The shipped template** (`docs/foundations/dsa/templates/solution_template.py`), placeholders filled at scaffold time:

```python
"""
{number}. {Title}   ·   https://leetcode.com/problems/{slug}/
Pattern: {category}              # e.g. linked_list, arrays_and_hash

<paste the LeetCode problem statement here>
"""
from typing import Optional, List


class Solution:
    # ── Attempt 1 · {YYYY-MM-DD} ──────────────────────────────────────
    def {methodName}(self, ...) -> ...:
        # your approach in plain English first, then code
        pass
```

Any data structures a problem needs (`ListNode`, `TreeNode`, `TrieNode`, `Node`, …) are **written by the learner inside the file**, not imported — that's deliberate (below).

**Whiteboard fidelity — write the full code from scratch (LOCKED pedagogy, §4a).** No shared `datamodel.py`, no boilerplate library. The learner writes *everything* — including the `ListNode`/`TreeNode` class definitions — every time, exactly as they would on a whiteboard in an interview. Re-deriving the scaffolding is part of the rep, not friction to optimize away. This is why the template ships lean and imports nothing beyond `typing`.

**The dating convention (baked in).** Every attempt is a **dated banner** inside `class Solution`. On a spaced-repetition revisit, the learner **adds a new dated attempt below** rather than overwriting — preserving the history that mirrors the tracker's `Attempt Dates` column and enabling the method-variant promotion rule (§2b). Retirement means several dated, coded Cleans stacked in one file.

**Scaffolding flow — "set up before I start."** When a learner begins a problem, the coach (via the `cse-init` skill / a `new-problem` action) **generates the empty skeleton first**: correct path + filename, URL/slug, pattern, and the `Attempt 1 · <today>` banner with an empty `pass` stub. The learner then writes the body *and* any data-structure definitions it needs.

**Reconciliation with the "no code edits by the agent" lock (§4a).** Scaffolding an **empty, algorithm-free skeleton** (docstring, `typing` import, dated banner, stub signature ending in `pass`) is *not* writing the solution — it's setting the table. The lock still holds: **the agent never writes solution logic or data-structure definitions; the learner writes every line inside the method body and every helper class.**

---

## 6c. The AI System Engineering pillar (ships in v1)

Phase 3 of the study guide becomes the third pillar, built on the **same engine + template model as System Design** (§6a) — it is *not* a new mechanism, just a new subject:

- **ROI-line tiers.** Tier 1 (interview/practitioner core): retrieval & vector search (chunking, embeddings, HNSW/IVF), context-window & token management (ranking, compression, semantic caching), agentic orchestration & tool use (deterministic function calling, structured JSON, state), evaluation & guardrails (programmatic evals, hallucination checks, safety proxies). Tier 2 (depth): serving internals, GPU scheduling/batching, retrieval-quality research, eval frameworks. Same "reach beyond" overshoot.
- **Unit = a capability/build; rep = fill a template + a blind rebuild.** Mirrors SD exactly: `ai_progress.md` is a parallel comfort tracker; the review is designing/rebuilding the capability cold and comparing. Same 🟢/🟡/🔴 scale, same interval engine, same phase = retired rule.
- **Cadence.** Slots into the existing Phase-3 study-guide structure; runs on the same weekly schedule as a mode-switch subject, not a separate calendar.
- **Templates + curriculum.** Ship `ai_engineering/templates/` and `components/` seeds plus `curriculum/ai_engineering/{tier1_core,tier2_depth}.yml`, tier-tagged.

Because it reuses SD's machinery wholesale, the marginal cost of shipping it in v1 is authoring content (study guide + curriculum + a couple of seed templates), not new engine work.

---

## 7. Migration / build plan (phased)

1. **Scaffold repo** — new **private** `cse-coach` repo, directory skeleton (all three pillars), licenses, README stub.
2. **Port engine (multi-pillar)** — copy `update_review_dates.py` + hook; add config loading; generalize from one hardcoded tracker to a list of pillar configs (DSA = pillar #1, behavior-preserving); keep defaults = current behavior; add golden-file test.
3. **Port DSA scaffold** — patterns/fundamentals as-is; blank templated tracker/logs/schedules; **ship the lean `solution_template.py` (no difficulty token, no datamodel import) and the `new-problem` scaffolder** (§6b) that stamps path/URL/pattern/dated banner before coding.
4. **Port System Design pillar** — SD `study_guide.md` (ROI-line tiers + cadence), `templates/` and `components`/`fundamentals` seeds as-is; new blank `design_progress.md`; Design Practice Backlog.
5. **Build AI Engineering pillar (§6c)** — `ai_engineering/study_guide.md` (ROI-line tiers), `ai_progress.md`, seed templates/components. Reuses SD machinery — content authoring, not engine work.
6. **Author the layered curriculum + backlog pools** — DSA `milestone`/`expansion_tier1`/`expansion_tier2` + backlog pools (interview-sourced, competitive-style); SD `tier1_interview_core`/`tier2_architect_depth` + Design Practice Backlog; AI `tier1_core`/`tier2_depth`. All ROI-line-tagged.
7. **Write bootstrap** — interactive setup + date projection across all pillars (weekday DSA + Sunday SD sprint + AI mode-switch); enforce `reach_beyond ≥ 1`; seed empty `self_eval_log.md`.
8. **Extract coaching skill** — move the drafted [`cse-coach-skill-draft.md`](cse-coach-skill-draft.md) to `.claude/skills/cse-coach/SKILL.md`, incl. the SD/AI review workflows and the self-eval meta-loop (default ON); wire `CLAUDE.md` to it.
9. **README + a `docs/PHILOSOPHY.md`** — the README ([draft](cse-coach-readme-draft.md)) **must teach the interaction model first: this is a coach you talk to, not a tracker you edit.** Lead with "start a problem / ask questions / report Clean-Shaky-Blank," a sample conversation, and "your only job is the reps + honest grading." PHILOSOPHY holds the Interview-ROI line (all pillars), comfort system, daily loop, mode-switch to Phases 2–3, backlog recovery.
10. **Dogfood** — run a mock adopter flow end-to-end for all pillars; verify a logged DSA result *and* a blind-sprint result each flow through hook → tracker → schedule exactly as in cse-review.
11. **Publish** — keep the repo **private** through dogfooding; flip to a public GitHub template once the pillars are proven (Q4).

Each phase is independently reviewable. `cse-review` is never touched.

---

## 8. Open questions for you — ALL DECIDED

1. ~~**Overshoot defaults**~~ — **DECIDED: default `target: competitive`; `reach_beyond` minimum 1, `0` rejected/clamped. Reaching for the end goal is non-negotiable (§5).**
2. ~~**Solution languages in the default preset**~~ — **DECIDED: default Python-only (`globs: ["*.py"]`); engine stays language-agnostic so adopters can widen at bootstrap.**
3. ~~**How opinionated should the shipped skill be?**~~ — **DECIDED: pedagogy locked, logistics configurable (see §4a Configurability contract).**
4. ~~**Repo name, visibility**~~ — **DECIDED: name `cse-coach` (echoes `cse-review`); ship **private first**, flip to a public GitHub template once the pillars are dogfooded.**
5. ~~**The `self_eval_log` meta-review loop**~~ — **DECIDED: ships **ON by default** as a built-in coaching mechanism (§6), empty log seeded for every adopter.**
6. ~~**AI System Engineering pillar (Phase 3)**~~ — **DECIDED: ships in **v1** as the third pillar (study guide + tracker + templates), same shared engine.**

*(No open questions remain — this section is the decision log. Next step is the phased build in §7.)*

---

## 9. What this explicitly does NOT do

- Does not modify, refactor, or migrate `cse-review`.
- Does not change the spaced-repetition math or the doc structure.
- Does not auto-publish anything public without your go-ahead on §8.4.
