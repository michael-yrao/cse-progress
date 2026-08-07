# System Design — Senior/Staff (L6) Interview Ramp

> **Created Aug 6, 2026; re-aimed the same session.** **Target: big tech / MANGA-adjacent** (Meta, Apple,
> Netflix, Google, Amazon + the tier around them), **senior/staff (L6)** given ~10 years' experience.
> **Fintech and other domain roles are paid waypoints, not the target** — the plan optimizes for the
> big-tech end goal and uses the midpoints as practice/income, never bending toward them.
>
> This is the SD analogue of the DSA roadmap: a **sequence with exit gates, not a calendar of deadlines**
> (per [[feedback_phase_dates_are_advisory]]). The week bands below are *advisory* — you advance a phase
> when its **gate** is met, not when a date arrives. A phase that runs long carries forward; that is a
> normal outcome.

## Target & emphasis — L6 at big tech (depth over breadth)

~10 years in ⟹ the bar is **Staff-adjacent (L6)**, and the emphasis is **depth over breadth.** At L6 the
interviewer assumes you can produce a competent design and spends the round trying to **break** it —
requirements ambiguity, cross-cutting concerns (multi-region, data migration, zero-downtime rollout, cost,
failure domains), and relentless "why not X / what happens at 100× / how do you evolve this." So:

- **Rubric checkpoint #7 — Evolve & operate** (migration / multi-region / zero-downtime rollout / cost &
  failure-domain reasoning, raised unprompted). At L6 a design banks 🟢 only with **#5, #6, AND #7**.
- **The gate is depth, not count:** *"a handful of designs I can defend 2–3 levels deep under sustained
  Socratic pushback + a live curveball requirement change,"* not "N designs banked." Keep drilling more
  designs for coverage; the **gate** is depth-per-design.
- **Design set is general big-tech, not domain-specific — no fintech weighting.** The canonical set MANGA
  loops pull from: news feed, chat/messenger, YouTube/video, typeahead, web crawler, Google Docs, rate
  limiter, URL shortener, distributed cache, notification service, proximity/nearby, ad-click aggregation.

## Why this exists

DSA is on track but **not done** (DP is still ahead — below); **system design is the binding constraint
for L5+.** At senior/staff, SD is 1–2 scored rounds plus deep tradeoff probing, and a strong-DSA/weak-SD
candidate gets leveled down. Starting state (Aug 6): only Redis drilled (🟡), Postgres note built but
undrilled, first design (URL shortener) mid-flight, Vitess not started. Everything else 🔴.

> **⚠️ DSA is not finished — DP is the back half of NC150** (the learner caught this; it corrects the
> earlier "DSA already at bar" premise). **1D DP** (Oct 12–Nov 8, 12 problems) and **2D DP** (Nov 9–Dec 6,
> 11 problems) are still ahead and heavily tested at big tech. **DSA reaches maintenance ~Dec, not at the
> Advanced Graphs close (~Aug 16).**

## The scoreboard — how SD becomes measurable

SD's fair complaint is that it isn't obviously pass/fail like a LeetCode problem. Fix: **the unit is a
timed ~45-min cold mock, self-scored against a fixed rubric, logged as a comfort rating in
[`mastery/design_progress.md`](mastery/design_progress.md)** (role = `Design`; rows added by hand — that
tracker has no source-discovery, so no phantom-row risk). Same +30/+10/+2 engine as DSA.

**Rubric — each checkpoint pass/fail, scored right after the mock:**

| # | Checkpoint | Pass test |
|---|---|---|
| 1 | Requirements | functional + non-functional + scale numbers, pinned unprompted |
| 2 | Estimation | QPS / storage / bandwidth, correct order of magnitude |
| 3 | API + data model | core entities, API surface, schema |
| 4 | High-level architecture | components + data flow, coherent |
| 5 | **Forks defended** | 3–4 biggest forks: trigger → choice → one-line why → **breaks at 10×** |
| 6 | **Failure modes** | named SPOF / bottleneck / race **before** being asked |
| 7 | **Evolve & operate** | migration / multi-region / zero-downtime rollout / cost & failure-domain, unprompted |

**Rating:**
- 🟢 — #1–4 solid **AND #5, #6, #7 all pass** (the senior signal).
- 🟡 — skeleton (#1–4) solid, #5–7 shaky.
- 🔴 — couldn't drive the framework cold.

**The senior gate is baked into the rating:** #1–4 are *assumed* at L6, so the score lives in tradeoff
defense, naming your own failure modes, and evolve/operate — not in drawing boxes. **Headline metric:
# of designs you can defend 2–3 levels deep under pushback** (depth, not raw count).

## Capacity — the parallel model (revised Aug 6)

The original plan freed the DSA active block *"after graphs close (~Aug 16)"* to fund a 2nd design
sprint/week. **That trigger was wrong** — DSA isn't done at Aug 16 (DP runs to ~Dec), so the block isn't
free. Replaced by:

- **`daily_cap` raised 5 → 7** (in `cse.config.yml`); **new-problem intake stays capped** at the
  difficulty tiers (moderate 5 / hard 4 / DP 3). The **+2/day (+14/week) is review/backlog throughput** —
  it drains the ~−9.6 surplus and the 🟢 pile, it does **not** add new intake (the blank-tax discipline
  holds).
- **DSA keeps its active block through DP (~Dec)** on the NC150 roadmap — it does **not** drop to
  maintenance at the graphs close.
- **SD ramps in parallel**, funded by its existing lanes (Sunday design ③ + two midweek warmup-swap lanes
  ①②) plus the breathing room the cap raise buys — **not** by stealing the DSA active block.
- **Reassess a 2nd weekly design sprint once DSA actually reaches maintenance (~Dec).**

Honest trade: DSA-completion and the SD ramp both proceed, neither at absolute max. The cap raise is what
makes *parallel* feasible instead of forcing a strict sequence.

## Design sourcing & the prerequisite-tech gate (Aug 6)

- **Source → [systemdesign.io](https://systemdesign.io/).** Each design session pulls one problem from
  there (weighted to the canonical big-tech set above), rather than a fixed hardcoded list.
- **Prerequisite-tech gate — cover *before* you design (bar: off 🔴, confirmed by the learner).** Before a
  design that needs a core technology not yet at **off 🔴**, cover that tech first: build/drill its
  `technologies/<tech>.md` note to at least one clean-ish sprint. This is stricter than the old
  *"hit the block cold mid-design, learn it after"* — a deliberate shift, because walking into a design on
  a tech you've only *read* wastes the mock.
  - **Current tech status:** **Redis 🟡** (usable) · **Postgres** note built but **undrilled** → drill to
    off-🔴 before a Postgres-heavy design · **Vitess** no note → build before any sharded-MySQL design ·
    everything else 🔴.

---

## Phase A — Framework fluency + data layer (advisory: ~Aug → Sep)

**Goal:** make the framework skeleton (rubric #1–4) automatic, so later mocks spend their 45 min on forks,
failure modes, and evolve/operate instead of remembering the steps. Drill the cheap/canonical designs
where the framework itself is the thing being practiced. **Order easiest-framework-rep first.**

- **Designs — walk systemdesign.io's tiers, one design = one row = one session** (weekly-loop retired;
  the tracker's `Design (tier)` rows are the concrete unit, like LeetCode numbers). **Finish the open arcs
  first**, then the **Easy tier** in order:
  1. **URL Shortener** *(in flight — Sunday)* · 2. **Rate Limiter** *(close the Mastery arc, 🟡; it's
     systemdesign.io-Hard but this is a closing re-rep, not a cold learn)* →
  then Easy: **Pastebin → Instagram → Twitter → Top-K (App Store Rankings) → Job Scheduler → Document Mgmt
  (Notion) → FB Likes w/ live updates.** *(Skip the low-ROI easies — Weather, Price-Alert, Parts-Compat.)*
- **Lane ① tech fluency — the data-store trio (highest leverage):** **Postgres** (note built → drill to
  🟢) → **Cassandra** → **DynamoDB**. **Vitess** (sharded MySQL) pulled in when a design demands it. Per the
  **prereq-tech gate**, a design's core tech must be off 🔴 before its session.
- **Lane ② concepts fallback:** the six front-loaded cards (percentiles, Little's Law, utilization,
  sketches, retry storms, quorum math) as the pull queue allows.

**Exit gate:** framework skeleton (#1–4) scores clean on **3+ different designs**, AND the data-store trio
is each **off 🔴**. Until both hold, stay in Phase A.

## Phase B — Senior signals (advisory: ~Sep → Oct)

**Goal:** where L6 is won — **forks, failure modes, and evolve/operate (#5/#6/#7).** Re-run Phase-A designs
at Mastery timing scored *specifically* on #5–7, and add the harder canonical set.

- **Designs — systemdesign.io's Medium tier:** **Dropbox/Google Drive · Messenger/WhatsApp · YouTube/
  Netflix · Key-Value Store · Web Crawler · News Feed · Google Calendar.** Same one-row/one-session unit;
  re-run the Phase-A Easy designs at Mastery timing scored *specifically* on #5–7 alongside.
- **Lane ① tech fluency — streaming + coordination tier:** **Kafka** → **Flink** (exactly-once,
  watermarks), **Elasticsearch**, **API Gateway**, **ZooKeeper**.
- **Lane ② concepts:** quorum math, consistency levels (strong→eventual), LSM vs B-tree, idempotency.
- **Interactive drills:** run **Socratic pushback** + a **failure-mode drill** on each banked design —
  exactly what the L6 interviewer does.

**Exit gate:** a **handful (~4+) of designs defended 2–3 levels deep under sustained pushback** (including
#7 evolve/operate), across varied domains; all Tier-1 core techs off 🔴.

## Phase C — Simulation + calibration → **the application trigger** (advisory: ~Oct+, overlaps DP)

**Goal:** convert bank into interview reflexes; calibrate against real loops.

- **Full cold 45-min mocks** on random designs from the bank, strict timing.
- **Add systemdesign.io's Hard / Very-Hard tier** as the depth material: **Typeahead · Notification Service ·
  Metrics Collection**, then **Yelp/Nearby · Credit-Card Processing** *(the last is a fintech-waypoint
  design — do it only if a fintech loop is imminent)*. Same one-row/one-session unit.
- **Deep-dive rounds:** pick 2–3 systems, go two levels deeper (senior loops often spend a full 45 min
  drilling *one* system rather than breadth).
- **Live-fire calibration:** apply to **1–2 lower-priority companies** (fintech waypoints are fine here) —
  real onsites are the best SD stress test, and these are companies you don't mind spending.

**SD exit gate (this ramp owns the mechanics; the apply *decision* lives in
[`../career_strategy.md`](../career_strategy.md) §4 Gate 3, which also requires DSA in maintenance / DP done):**
- a **handful of designs defended deep under pushback** (incl. #7),
- **all Tier-1 core technologies off 🔴**,
- can drive a **cold 45-min mock end-to-end** without prompting.

**The trigger is the gate, not the calendar** — same discipline as the comfort→interval engine. Phone
screens are pure DSA and you'll be ready once DP is in, so nothing is lost holding applications until SD is
real. See `career_strategy.md` for the full tier route (fintech calibration → data-platform → big tech).

---

## The scoreboard at a glance (fill as you go)

| Metric | Now (Aug 6) | Phase A gate | Phase B gate | Apply trigger |
|---|---|---|---|---|
| Designs defended-deep (incl. #7) | 0 | skeleton on 3 | ~4 under pushback | handful under pushback |
| Core techs off 🔴 | 1 (Redis 🟡) | +3 (data-store trio) | all Tier-1 | all Tier-1 |
| Cold 45-min mock | no | — | — | **yes** |
