# Career Strategy — the North Star (single source of truth)

> **This is the one home for the overarching goal: the target, the company route, and the apply gates.**
> It is **cross-track** — it governs DSA, System Design, and AI alike, which is why it sits at
> `docs/foundations/` beside `schedules/` rather than inside any one track. The track guides describe
> *how* to study; this describes *where it's going and when to apply.* Everything else links here — do not
> restate the goal elsewhere (that's how three stale copies of "Staff fintech" happened on Aug 6, 2026).
>
> Recall pointer: [[project_interview_goal]] (memory) is a compact summary of this file.

## 1. The end goal

**Big tech / MANGA-adjacent** (Meta, Apple, Netflix, Google, Amazon + the tier around them), at
**senior/staff (L6)** given ~10 years' experience. **Re-aimed Aug 6, 2026** — big tech is the *destination*,
not "the move after." **Fintech and any specific-domain role are paid waypoints** — they pay and teach, but
the plan optimizes for the big-tech end goal and never bends toward them.

**Binding constraint = System Design.** DSA is on track but **not done** — DP (1D Oct 12–Nov 8, 2D Nov 9–
Dec 6) is the back half of NC150 and DSA reaches maintenance ~Dec, not at the Advanced Graphs close. SD is
the weak lane and the top priority; L6 emphasis is **depth over breadth**. SD execution plan lives in
[`system_design/senior_ramp.md`](../../https://github.com/michael-yrao/sd-progress/blob/main/senior_ramp.md).

## 2. The route — company tiers (the path to the end goal)

The tiers are the **route to big tech**, not competing destinations. Fintech = calibration, data-platform =
the next actual hop, big tech = where the route terminates.

| Tier | Companies | Role | When |
|------|-----------|------|------|
| **Fintech** | Stripe, Robinhood, Citadel, Bloomberg, Goldman Sachs, JPMorgan | **Calibration** — interview to practice, not to land | Interview *first*, apply ~mid-Sept 2026. First: Bloomberg, Stripe, Citadel. The reconciliation/ledger moat carries these loops — the safe place to burn early reps |
| **Data platform / infra** | **Snowflake**, Databricks, **Datadog** (entry point), Confluent, MongoDB | **Next hop** toward big tech (decided Jul 26, 2026) | Apply once at-scale SD reaches Transition/Mastery, ~2–3 months behind fintech. SD is distributed-storage flavored (query engines, partitioning, columnar storage, consistency), not social-feed |
| **Big tech / MANGA** ⭐ | Google, Amazon, Meta, Microsoft, Apple, Netflix | **THE END GOAL** | Where the hops above lead. The plan optimizes for **here**; SD readiness driven by [`senior_ramp.md`](../../https://github.com/michael-yrao/sd-progress/blob/main/senior_ramp.md), gated not dated |
| **Supplementary** | Uber, Airbnb, DoorDash, LinkedIn | Pattern variety only | Rotate in for problem coverage; not an interview target this cycle |

**SD design prep is general big-tech, not fintech-weighted** — payment/ledger is one design among many
(useful for a fintech *waypoint* loop, not prioritized). See the ramp for the canonical design set.

## 3. Why this route — the hop-count reasoning (preserved from Jul 26, 2026)

The constraint is **hop count**: too many moves before big-tech-adjacent reads as churn on a resume already
carrying a title stuck at Senior since 2017. So the next move has to *count* — one hop that lands closer to
big tech, not a lateral into another bank. Fintech was the earlier plan's *destination* because the
reconciliation/ledger moat covers the design gap there; that property is now why it's the **practice** tier —
loops you can walk into on domain strength are the right place to spend early reps, and a fintech offer you
decline costs nothing.

**The honest cost: the readiness bar went up, not down.** The data-platform tier's SD round is at-scale
distributed data — the weakest lane on the board. Leading the Snowflake + Serenity migration at Morgan
Stanley is a *ran-your-product-at-scale-in-a-regulated-bank* story and real referral/recruiter-screen
leverage, but be exact: **it gets you the screen, not the offer.** Expect an easy funnel top and a hard
onsite. Databricks sits here for the same reason — same round shape, prep transfers.

**Don't collapse the gap.** Calibration only works if the fintech loops *finish* before the Snowflake
applications go out, and application→onsite runs 4–8 weeks each side — that's what puts data-platform ~2–3
months behind mid-Sept. Ready-enough-to-learn beats ready-enough-to-win for the fintech loops; a loop run
too late to inform the real target is just an offer you decline.

**Datadog is the entry point — interview there first.** Round shape overlaps ~60% with Snowflake/Databricks
(metrics ingestion, time-series storage, high-cardinality aggregation, alerting; the non-overlap is query
engines + SQL semantics). But there's **no product-familiarity story** (cold application) and the bar/comp
sit a rung lower — both reasons to go there *first*, rehearsing the ingestion/storage round at lower stakes,
NYC-HQ. Calibration aimed at infra, not a disposable rep.

## 4. The apply gates — cross-track, gate not date

Each tier gates on its own readiness bar. **The trigger is always a repo-evaluable gate, never an offer or
interview outcome** ([[feedback_gate_on_internal_state]]); dates are advisory ([[feedback_phase_dates_are_advisory]]).

**Prerequisite for *any* apply — phone screens are pure DSA.** Ready once **DP is in** (~Dec); nothing is
lost holding applications until SD is real.

- **Gate 1 — fintech / calibration (~mid-Sept 2026).** (1) DSA roadmap through the hard blocks on track,
  low 🔴/🟡; (2) SD fintech-relevant designs at Transition/Mastery — rate limiter + payment/ledger + 2–3
  canonicals, payment/ledger owned cold (the moat). Deliberately *not* raised now these are practice loops —
  run them while winnable on domain strength — but not dropped either.
- **Gate 2 — data platform / next hop (~2–3 months later).** (1) Gate 1 loops actually *run* and get
  debriefed into the SD tracker (calibration is this gate's input, so unfinished loops hold it); (2)
  at-scale distributed-data SD at Transition/Mastery — ingestion, time-series/columnar storage, partitioning,
  consistency. The weak lane sets the date, not the calendar. Burning Snowflake on an unprepped design round
  is the expensive failure — no third tier behind it this cycle.
- **Gate 3 — big tech / end goal.** The [`senior_ramp.md`](../../https://github.com/michael-yrao/sd-progress/blob/main/senior_ramp.md) **Phase-C apply
  gate**: a handful of designs defended 2–3 levels deep under pushback (incl. rubric #7 evolve/operate), all
  Tier-1 core techs off 🔴, and a clean cold 45-min mock. Plus DSA fully in maintenance (DP done). The ramp
  owns the SD gate mechanics; this file owns the *decision to apply* that consumes them.

---

*Execution lives elsewhere, by design:* DSA study mechanics → [`dsa/study_guide.md`](dsa/study_guide.md) ·
SD roadmap → [`system_design/senior_ramp.md`](../../https://github.com/michael-yrao/sd-progress/blob/main/senior_ramp.md) · SD mock mechanics →
[`system_design/study_guide.md`](../../docs/foundations/system_design/study_guide.md).

*(The AI System Engineering track was removed Aug 13, 2026 — never started, no sessions, no trigger to
restore it. Its one interview-relevant design survives as the **ChatGPT** row on the SD board.)*
