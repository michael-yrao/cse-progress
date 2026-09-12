# AI Engineering — parked roadmap

> **Status: PARKED** (2026-09-12). This is the ready-to-go spec; the pillar is **not running yet**.
> It activates at a weekly build when DSA lightens — see the trigger below and
> [`.claude/memory/project_ai_pillar.md`](../../../.claude/memory/project_ai_pillar.md) for the
> standing state. Decision of record: `decisions.yml` `ai-pillar-revived-deferred` (supersedes
> `ai-track-removed`). Read this + the project memory and you can start section 00 without
> re-deriving anything.

**Resource:** [calmrocks/ai-engineer-notebooks](https://github.com/calmrocks/ai-engineer-notebooks)
— ~35–40 runnable, framework-free, eval-driven Colab notebooks across 12 sections. Runs free on
Groq/Colab; backend/full-stack background assumed, no prior ML needed.

**Goal:** interview prep (AI/ML-engineering and agent-focused roles) — so the path front-loads the
high-leverage interview sections, it does **not** march 00→12.

## Why this won't repeat the first AI track's death

The original AI track was removed as *"a plan nobody executed."* Three structural defenses:
1. **Every rep is active and scored**, not a reading checkbox (see "What a rep is" below).
2. **The activation trigger fires from the weekly-build checklist**, not from remembering to check.
3. **The path is a prioritized subset**, so there is never a 40-notebook backlog to bounce off.

## Activation trigger (measured, not a date)

Activate at a **weekly build** when BOTH hold:
1. DP/Backtracking phases have **closed** on the roadmap, and
2. `python scripts/effort_budget.py` shows **≥2 days/week well under the ceiling for 2 consecutive
   weeks** (real evening headroom — re-derived each week, never a fixed calendar date).

Until then: parked. Do not nudge.

## The pillar shape (mirrors System Design)

Same template as [`references/system-design.md`](../../../.claude/skills/cse-coach/references/system-design.md):

- **Off-board and UNPRICED** — AI takes the evening slot, it does **not** charge the DSA effort
  ceiling (same as SD since `sd-unpriced`). `system_design.cadence` has a sibling `ai_engineering`
  cadence *added to `cse.config.yml` only at activation* (single-source: no key until it holds a value).
- **Learner does the work; coach assesses.** The learner runs the notebooks; the coach runs cold
  probes and scores them. No lectures; teaching on request, off-schedule, unrated.
- **Own tracker** (`mastery/ai_progress.md`, created at activation) — section/notebook, comfort,
  spaced next-touch. Reuses the comfort→interval engine.

### What a "rep" is

Not "read notebook N." A rep is: **run the notebook, then produce a small assessed artifact** —

- a **cold explanation** of the mechanism (whiteboard, no notes), plus
- **one modification exercise**: change the eval and predict the score shift; add a tool to the agent
  loop; break RAG retrieval and diagnose it; tighten a prompt's structured-output contract.

The coach probes it cold, reusing the SD drills — `feedback_quantify_qualify` (a number on every
claim), `feedback_hld_altitude` (stay at system altitude), `feedback_expand_acronyms`. Comfort rating
+ spaced re-touch as usual; a concept is re-probed cold later, like an SD open-question.

## The interview-prioritized path

| Order | Section | Why this rank (interview prep) |
|---|---|---|
| 1 | `00-setup` | One-time env + cost setup. Nearly free. |
| 2 | `01-model-apis` | Foundation for everything: prompting, structured output, tool calling, streaming, context management. |
| 3 | `02-evals-basics` + `04-evals` | Eval-driven dev is the resource's spine **and** the top differentiator in AI-eng interviews (golden sets, LLM-as-judge, regression). |
| 4 | `03-rag` | The most-asked AI system-design topic. |
| 5 | `05-agents` | Agent loops, tool design, guardrails, MCP, skills — the hottest current interview area. |
| 6 | `10-ml-system-design` | The **bridge** to the SD pillar; pairs with the surviving ChatGPT design row on HelloInterview's Hard tier. |
| 7+ | `07-security`, `08-operations`, `06-adaptation`, `09-serving-inference`, `11-customer-craft`, `12-case-studies-and-capstone` | Depth as capacity allows; `12` capstone is the integration payoff. |

## The two-pillar cadence ramp (on activation)

| Phase | DSA state | SD cadence | AI cadence |
|---|---|---|---|
| Now → trigger | DP/Backtracking heavy | hold (starved in practice) | **parked** |
| Activation | DP winding down, headroom confirmed | ramp back toward twice_weekly | **1 notebook/wk**, alternating the evening slot with SD |
| DSA maintenance | mostly review/graduated | full twice_weekly | up to 2/wk as the evening allows |

SD recovers **first** (mid-flight and starved); AI is additive only once SD is healthy. The ramp is a
weekly-build decision re-derived from the live budget.

## Activation-day checklist (deferred — do NOT do now)

When the trigger fires and the learner agrees to start:
1. Create `mastery/ai_progress.md` (tracker) from the SD tracker's shape.
2. Add the `ai_engineering` cadence key to `cse.config.yml`.
3. Author `.claude/skills/cse-coach/references/ai-engineering.md` (the rep mechanics + drills), and
   point `SKILL.md` at it for the AI coaching moment.
4. Seat section `00`/`01` into the week's build; record the activation as a dated decision.
