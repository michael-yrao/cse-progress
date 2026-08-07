# System Design — Senior (L5+) Interview Ramp

> **Created Aug 7, 2026**, for a deliberate senior-fintech interview push. This is the SD analogue of
> the DSA roadmap: a **sequence with exit gates**, not a calendar of deadlines. Per the Aug 5 policy
> ([[feedback_phase_dates_are_advisory]]), the week bands below are *advisory* — you advance a phase
> when its **gate** is met, not when a date arrives. A phase that runs long carries forward; that is a
> normal outcome.

> **⚠️ Staff (L6) recalibration — Aug 7, 2026.** The learner is ~10 years in, so the target is
> **Staff-adjacent (L6), not L5.** That shifts the whole emphasis: **depth over breadth.** At L6 the
> interviewer assumes you can produce a competent design and spends the round trying to *break* it —
> requirements ambiguity, cross-cutting concerns (multi-region, data migration, zero-downtime rollout,
> cost, org/ops boundaries), and relentless "why not X, what happens at 100×, how do you evolve this"
> pushback. So:
> - **Add rubric checkpoint #7 — Evolve & operate:** migration / multi-region / zero-downtime rollout /
>   cost & failure-domain reasoning, raised unprompted. At L6 a design banks 🟢 only with **#5, #6, AND
>   #7**.
> - **The apply-trigger changes from breadth to depth.** Not "8 designs banked" but **"3–4 designs I can
>   defend two-to-three levels deep under sustained Socratic pushback + a live curveball requirement
>   change."** Keep drilling more designs for coverage, but the *gate* is depth-per-design.
> - **Fintech domain depth is non-optional at L6:** payment/ledger, idempotency, exactly-once,
>   consistency, reconciliation — expect to go *deep*, not just name them.

## Why this exists

DSA is interview-ready; **system design is the binding constraint for L5+.** At senior level SD is
1–2 scored rounds plus deep tradeoff/domain probing, and a strong-DSA / weak-SD candidate gets
leveled down. Starting state (Aug 7): only Redis drilled (🟡), PostgreSQL note built but undrilled,
first design (URL shortener) mid-flight. Everything else 🔴.

## The scoreboard — how SD becomes measurable

The complaint SD earns fairly: it isn't obviously pass/fail like a LeetCode problem. Fix: **the unit
is a timed ~45-min cold mock, self-scored against a fixed 6-point rubric, logged as a comfort rating
in [`mastery/design_progress.md`](mastery/design_progress.md)** (role = `Design`; rows added by hand —
that tracker has no source-discovery, so there is no phantom-row risk). Same +30/+10/+2 engine as DSA.

**Rubric — each checkpoint pass/fail, scored right after the mock:**

| # | Checkpoint | Pass test |
|---|---|---|
| 1 | Requirements | functional + non-functional + scale numbers, pinned unprompted |
| 2 | Estimation | QPS / storage / bandwidth, correct order of magnitude |
| 3 | API + data model | core entities, API surface, schema |
| 4 | High-level architecture | components + data flow, coherent |
| 5 | **Forks defended** | 3–4 biggest forks: trigger → choice → one-line why → **breaks at 10×** |
| 6 | **Failure modes** | named SPOF / bottleneck / race **before** being asked |

**Rating:**
- 🟢 — 5–6 pass, **including #5 and #6**.
- 🟡 — skeleton (1–4) solid, forks/failure-modes shaky.
- 🔴 — couldn't drive the framework cold.

**The senior gate is baked into the rating:** #1–4 are *assumed* at L5, so a design **banks at 🟢 only
if #5 and #6 are among the passes.** The score lives in tradeoff defense + naming your own failure
modes, not in drawing the boxes. **Your headline metric: # of designs banked at 🟢-with-forks.**

## Capacity — where the time comes from

Current SD load is 3 lanes/week out of DSA warmup capacity (surplus is already ~−9.6). The senior push
needs more design throughput than 1 Sunday/week (that's only ~12 design-reps across the whole window,
with zero room for the required repetition). Source the extra capacity from DSA:

- **After Advanced Graphs closes (~Aug 16), DSA drops to pure maintenance** — no new intake, warmups
  service the review queue only. That frees one 45-min active block.
- **Redirect that block to a 2nd design sprint/week** (midweek Transition/Mastery), giving **2 designs/
  week** from ~Aug 17. Lanes ① (tech fluency) and ② (blocks/concepts) continue unchanged.

This is the honest trade: the 🟢 DSA backlog grows a bit faster for ~10 weeks. Accepted — DSA is at
bar and SD is not, so that is the correct place for the cost to land.

---

## Phase A — Framework fluency + data layer (advisory: ~Aug 7 → early Sep)

**Goal:** make the framework *skeleton* (rubric #1–4) automatic, so later mocks spend their 45 min on
forks and failure modes instead of on remembering the steps. Drill the cheap/canonical designs where
the framework itself is the thing being practiced.

- **Designs (Sunday + 2nd slot once graphs close):**
  1. **URL shortener** — finish it (short-code generation fork + HLD + deep dives are open). *In flight.*
  2. **Rate limiter** — close the open Mastery arc.
  3. **Chat / messenger** — pulls WebSockets, message queues, fan-out.
  4. **News feed** — pulls push-vs-pull fan-out (celebrity problem), CDN.
- **Lane ① tech fluency — the data-store trio (highest leverage, fintech-relevant):**
  **PostgreSQL** (note built — drill to 🟢) → **Cassandra** → **DynamoDB**.
- **Lane ② concepts fallback:** the six front-loaded cards (percentiles, Little's Law, utilization,
  sketches, retry storms, quorum math) as the pull queue allows.

**Exit gate:** framework skeleton (#1–4) scores clean on **3+ different designs**, AND the data-store
trio is each **off 🔴**. Until both hold, stay in Phase A.

## Phase B — Senior signals + fintech domain (advisory: ~early Sep → mid Oct)

**Goal:** this is where L5 is won — forks and failure modes (#5/#6), plus fintech domain depth. Re-run
Phase-A designs at Mastery timing scored *specifically* on #5/#6, and add the domain-heavy set.

- **Designs — add the fintech-weighted canonical set:**
  - **Payment / ledger** ⭐ — the single highest-value fintech design: double-entry, **idempotency**,
    exactly-once, strong consistency, reconciliation, the money-movement state machine. Expect this in
    a fintech loop; over-invest here.
  - **Notification service**, **Typeahead** (ties DSA tries / 208), **YouTube / CDN**,
    **Distributed KV store** (quorum, vector clocks, consistency).
- **Lane ① tech fluency — the streaming + coordination tier:** **Kafka** → **Flink** (exactly-once,
  watermarks — fintech event pipelines & reconciliation), **Elasticsearch**, **API Gateway**,
  **ZooKeeper**.
- **Lane ② concepts:** quorum math, consistency levels (strong→eventual), LSM vs B-tree, idempotency —
  the ones that *back a fintech consistency argument*.
- **Interactive drills** (from the study guide): run **Socratic pushback** + **failure-mode drill** on
  each banked design — that is exactly what the L5 interviewer does.

**Exit gate:** **6+ designs banked at 🟢-with-forks**, one of which is **payment/ledger**, AND you can
survive Socratic pushback + a failure-mode drill cold on any of them. All Tier-1 core techs off 🔴.

## Phase C — Simulation + calibration → **the application trigger** (advisory: ~mid Oct → Nov)

**Goal:** convert bank into interview reflexes; calibrate against real loops.

- **Full cold mocks** on random designs from the bank, strict 45-min timing.
- **Deep-dive rounds:** pick 2–3 systems, go two levels deeper (senior loops often spend a full 45 min
  drilling *one* system rather than breadth).
- **Live-fire calibration:** apply to **1–2 lower-priority fintechs** now — real onsites are the best
  SD stress test, and these are companies you don't mind spending.

**Exit gate = the signal to apply to top-choice fintechs:**
- **≥8 designs banked at 🟢-with-forks** (incl. payment/ledger),
- **all Tier-1 core technologies off 🔴**,
- can drive a **cold 45-min mock end-to-end** without prompting.

When that gate is met, apply to first-choice fintechs and time onsites ~4 weeks out. **The trigger is
the gate, not the calendar** — same discipline as the comfort→interval engine. Phone screens are pure
DSA and you're ready for those today, so nothing is lost by holding the applications until SD is real.

---

## The scoreboard at a glance (fill as you go)

| Metric | Now (Aug 7) | Phase A gate | Phase B gate | Apply trigger |
|---|---|---|---|---|
| Designs 🟢-with-forks | 0 | — (skeleton on 3) | 6 | **8** |
| Core techs off 🔴 | 1 (Redis 🟡) | +3 (trio) | all Tier-1 | all Tier-1 |
| Cold 45-min mock | no | — | — | **yes** |
