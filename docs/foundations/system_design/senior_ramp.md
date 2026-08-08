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
  **All 55 of its questions are now triaged against the L6 bar** — see *The L6 Interview-ROI Line* below.
  ⚠️ **One canonical design the source does not cover: distributed cache.** systemdesign.io has no question
  for it, so it needs a different source or a self-directed session — and Redis's technology note is not a
  substitute (using a cache ≠ designing one: consistent hashing, eviction, replication, invalidation).
- **Prerequisite-tech gate — cover *before* you design (bar: off 🔴, confirmed by the learner).** Before a
  design that needs a core technology not yet at **off 🔴**, cover that tech first: build/drill its
  `technologies/<tech>.md` note to at least one clean-ish sprint. This is stricter than the old
  *"hit the block cold mid-design, learn it after"* — a deliberate shift, because walking into a design on
  a tech you've only *read* wastes the mock.
  - **Current tech status:** **Redis 🟡** (usable) · **Postgres** note built but **undrilled** → drill to
    off-🔴 before a Postgres-heavy design · **Vitess** no note → build before any sharded-MySQL design ·
    everything else 🔴.

---

## The L6 Interview-ROI Line — all 55 systemdesign.io questions, triaged

> **Written Aug 8, 2026**, at the learner's request: *"let's keep in sync with DSA study for system design
> so we have phases with the 55 SD problems split out between high ROI and low ROI… and I want to be clear
> that L6 is the goal so let's have our ROI reflect that."*
>
> **This is the SD analogue of [`dsa/study_guide.md`](../dsa/study_guide.md)'s Interview-ROI Line.** Same
> shape, same discipline: a numbered stack of tiers with **one explicit line drawn through it**, and every
> item on the source list placed on one side of it *with a reason*.

**Why this section exists.** The Aug 6 reseed selected 21 of the catalog's 55 questions and discarded the
other 34 **without recording what or why** — the only trace was a parenthetical naming three of them. That
breaks the rule this repo already has in [[feedback_roi_promotes_to_curriculum]]: *"say what you did NOT
promote and why — the bar only means something if applied in both directions."* Applied in one direction,
"curated by ROI" is indistinguishable from "picked 21 and stopped," and a wrong decline stays invisible
until Phase C, when you'd re-derive the catalog from scratch. It also left SD with no equivalent of DSA's
**two deferral bins**, so a declined design and a design nobody ever read looked identical.

**The bar, stated once, because every call below is an application of it:**

> **Would a strong L6 candidate at Meta / Apple / Netflix / Google / Amazon (or the tier around them) be
> expected to handle this in a 45-minute round?**

Not *"is it a good system"* and not *"is it interesting."* Three things follow from the L6 framing
specifically, and they do most of the sorting:

- **Depth over breadth.** The gate is *a handful of designs defended 2–3 levels deep*, not a large bank.
  So a design earns a place by teaching something no design above it teaches — **redundancy is the most
  common reason to decline**, not difficulty.
- **Distributed-systems altitude only.** At L6 the round is boxes, arrows, forks and failure domains. A
  question whose real content is class design is *actively harmful* here — see [[feedback_hld_altitude]],
  the learner's known default failure.
- **No domain weighting.** Fintech is a paid waypoint, not the target ([[project_interview_goal]]), so
  payments/banking designs sit below the line **even when they are hard and well-known**.

### Above the line — do these, in order

1. **Core canonical set (20)** — the Phase A/B/C designs below. Non-negotiable; this is the SD analogue of
   NC150. Every one of them is a design MANGA loops actually pull from.
2. **Tier 1 advanced (10)** — the **⏳ SD Waiting Room**. High L6 value, but second-order: each is either a
   harder sibling of a core design or a specialty round (streaming, observability, experimentation, ads).
   **Trigger: `phase:B` + the core design it extends is off 🔴.** Pull from here once the core set is
   moving — *not* before, and not top-to-bottom. **Evaluate every trigger at the weekly build.**

**=== L6 INTERVIEW-ROI LINE ===**

3. **Tier 2 — platform & real-world depth (18)** — genuinely good systems, **rarely a generalist L6 round**.
   Mostly redundant with something above the line, or aimed at a specific infra/platform team. Worth
   pursuing *after* the apply trigger, or immediately if a loop is known to target that team.
4. **Tier 3 — off-target (7)** — wrong altitude, wrong domain, or not interview material. These are
   declined outright, not deferred. **A Tier-3 item needs a stated reason to ever move up.**

### Tier 1 advanced — ⏳ SD Waiting Room (above the line)

| # | Question | Tier | Why it's above the line | Extends |
|---|---|---|---|---|
| 11 | [Stream processing system like Kafka](https://systemdesign.io/question/design-a-stream-processing-system-like-kafka) | V.Hard | Designing *the log itself* — partitioning, replication, consumer groups, exactly-once. Kafka is already a Phase-B tech; this is the design that proves you understand it rather than use it | — |
| 55 | [Ads management & display for a social feed](https://systemdesign.io/question/develop-ads-management-and-display-system-for-social-feed) | V.Hard | **Ad serving + click aggregation** — the canonical Meta/Google money-path design, named in this ramp's own canonical set | — |
| 20 | [Google Analytics dashboard & pipeline](https://systemdesign.io/question/design-google-analytics-dashboard-and-pipeline) | Hard | The analytics-pipeline shape (ingest → aggregate → serve) at a gentler slope than #55 | #55 |
| 13 | [K most-shared articles in time windows](https://systemdesign.io/question/identify-k-most-shared-articles-in-time-windows) | Hard | **Windowed** top-K, which the tracked static Top-K does not teach. Directly exercises the sketches card (Count-Min) and Zipfian skew | Top-K |
| 41 | [Distributed tracing system](https://systemdesign.io/question/design-a-distributed-tracing-system) | V.Hard | Observability — flagged in [[project_curriculum_additions_pending]] as added to cse-coach Jul 25 and **never synced here**. Asked at L6 (Dapper/Jaeger lineage) | — |
| 29 | [A/B testing system (Optimizely)](https://systemdesign.io/question/design-an-ab-testing-system-like-optimizely) | Hard | Experimentation platforms are core infrastructure at Meta/Google/Netflix, and this is a real round | — |
| 48 | [Live comments for Facebook](https://systemdesign.io/question/design-a-live-comments-feature-for-facebook) | Hard | Real-time fan-out at scale — the harder, canonical version of the tracked FB-Likes-live-updates | FB Likes |
| 51 | [Migrate large data to Google Cloud](https://systemdesign.io/question/create-a-system-to-migrate-large-data-to-google-cloud) | V.Hard | **Rubric #7 as an entire design.** Migration/zero-downtime/cutover is the checkpoint this ramp says decides L6, and it is the one no other design forces | — |
| 33 | [Count FB likes for high-profile users](https://systemdesign.io/question/count-facebook-likes-especially-for-popular-users) | Med | The **hot-key / celebrity-skew** problem in isolation. Cheap (Medium) and teaches the one thing the plain Likes design skips | FB Likes |
| 10 | [Distributed metrics logging & aggregation](https://systemdesign.io/question/design-a-metrics-logging-and-aggregation-system) | V.Hard | The V.Hard sibling of the tracked Hard metrics-collection design — the natural Phase-C depth re-rep | Metrics Collection |

### Tier 2 — platform & real-world depth (below the line)

| # | Question | Tier | Why it's below the line |
|---|---|---|---|
| 19 | Distributed queue like RabbitMQ | Hard | Broker semantics (ack/redelivery/DLQ) are real, but **#11 Kafka covers queueing at higher L6 frequency**. Do this only if the loop is messaging-infra |
| 34 | Control plane for a distributed database | V.Hard | Excellent, and squarely a **data-platform** round rather than a generalist one. Promote if a data-platform loop lands (the tier route's middle waypoint) |
| 25 | Surge pricing (Uber, stream processing) | V.Hard | Strong stream-processing content, but overlaps #11/#20 and carries Uber-specific domain load |
| 27 | ETA service & driver/rider location sharing | V.Hard | Geospatial + live location — **redundant with the tracked Yelp/Nearby**, which teaches the indexing |
| 40 | Find a rider for Uber / Uber Eats | Hard | Matching + dispatch; same geo core as #27 and Yelp/Nearby |
| 42 | Distribute 6M free burgers in one hour | Med | The **flash-sale / thundering-herd** design, which is genuinely canonical under other names. Closest call on this list — promote it the moment a retail/commerce loop appears |
| 28 | Hotel booking system | Med | Reservation/inventory consistency. Booking-and-Airbnb territory, not MANGA generalist |
| 21 | System for sorting large data sets | Easy | External merge sort / MapReduce fundamentals. Real, but a dated round shape for L6 today |
| 53 | Distributed file transfer like BitTorrent | Hard | P2P is a narrow specialty; the sync half is already covered by the tracked Dropbox/Drive |
| 26 | Netflix: limit screens per user | Hard | Distributed leases/counting — a good *deep dive*, too thin as a whole round |
| 39 | Monitor the health of a cluster | Med | Redundant with the metrics designs (#17 tracked, #10 Tier 1) |
| 45 | Photo sharing like Flickr / Google Photos | Med | Substantially the tracked Instagram design |
| 46 | On-call escalation system | Med | A specialization of the tracked Notification Service |
| 49 | Show number of users viewing a page | Easy | Real-time counting at a low ceiling; #33 teaches the same thing harder |
| 35 | User login & authentication | Med | ⚠️ **Reclassify rather than decline** — auth is a recurring *deep-dive inside other designs*, not a round of its own. **Owed as a `components/auth.md` note**, not a design row |
| 44 | Latest stock prices worldwide | Easy | Pub/sub fan-out, low ceiling, and the live-update pattern is covered |
| 38 | Marketplace feature for Facebook | Easy | CRUD + search; no distinctive distributed-systems content |
| 43 | File downloader library (frontend→backend) | Hard | Library/client design — **wrong altitude** for an L6 distributed-systems round |

### Tier 3 — off-target (declined, not deferred)

| # | Question | Tier | Why |
|---|---|---|---|
| 31 | IoC / dependency-injection framework | V.Hard | **OOD/LLD, not distributed design.** Actively counterproductive given [[feedback_hld_altitude]] — it rehearses the learner's known failure mode |
| 32 | Credit-card processing | V.Hard | ⚠️ **Demoted from the tracker in this edit.** Fintech is a paid waypoint, not the target; keeping it in the core set was exactly the domain weighting [[project_interview_goal]] forbids. Re-promote **only** if a fintech onsite is scheduled |
| 47 | Wire transfer API | Hard | Same — fintech domain, and narrower than #32 |
| 52 | Distributed botnet | Hard | Not an interview design |
| 30 | Price alert system | Easy | Named as a skip at the Aug 6 reseed; low ceiling |
| 36 | Weather application | Easy | Named as a skip at the Aug 6 reseed |
| 54 | Parts-compatibility for eCommerce | Easy | Named as a skip at the Aug 6 reseed; domain CRUD |

### Three findings from the diff, recorded so they aren't re-derived

1. **Google Docs was never missing.** Catalog #37 reads *"…like Wikipedia, Notion **or Google Docs**"* —
   one question covering all three. The tracker row said only "Document Mgmt (Notion/Wikipedia)", which is
   what made it look absent against this ramp's canonical set. **Row renamed, not added.** ⚠️ But the row
   now has to carry the harder half: *real-time collaborative editing (OT/CRDT, presence, conflict
   resolution)* is a different design from document CRUD + versioning, and it is the part L6 asks about.
   **Do not let this one be rated on the CRUD half.**
2. **"Distributed cache" is absent from the catalog entirely.** It is in this ramp's canonical set and
   systemdesign.io has no question for it — a **source** gap, not a curation gap. It needs a different
   source or a self-directed design. Redis's technology note is not a substitute: designing a distributed
   cache (consistent hashing, eviction, replication, invalidation) is a different rep from using one.
3. **Ad-click aggregation was in the catalog the whole time** — #55 and #20, both untracked until now.

⚠️ **These tier assignments are the coach's calls, not the learner's**, and the borderline ones are named
as borderline (#42 burgers, #34 control plane, #19 RabbitMQ, #21 sorting). **Override any of them** — the
list is only useful because it is written down and arguable; it was the *absence* of a written list, not
the placement of any single item, that this section fixes.

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
  Metrics Collection · Yelp/Nearby.** Same one-row/one-session unit.
  - ⚠️ **Credit-Card Processing was removed from this list Aug 8, 2026** and sits in Tier 3 below the ROI
    line — fintech is a paid waypoint, not the target. Re-promote only against a scheduled fintech onsite.
  - **Phase C is also where the ⏳ Tier 1 advanced queue empties** (Kafka · Ads · Analytics · windowed
    Top-K · Distributed Tracing · A/B Testing · Live Comments · Data Migration · Hot-key Likes · V.Hard
    Metrics). Those are the depth reps, and **Data Migration is the one to protect** — it is rubric #7
    turned into an entire design, and #7 is what the L6 rating actually hinges on.
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

**Catalog coverage (Aug 8, 2026) — 55 systemdesign.io questions, all placed:**

| | Count | Where |
|---|---|---|
| Core canonical set | **20** | the review table in `mastery/design_progress.md` |
| ⏳ Tier 1 advanced | **10** | SD Waiting Room, `phase:B` trigger |
| 🧊 Tier 2 platform/real-world | **18** | below the line, reason each |
| 🧊 Tier 3 off-target | **7** | declined, reason each |

⚠️ **The count is not the goal and should never be reported as progress.** The gate is *a handful of
designs defended 2–3 levels deep*, so 30 above-the-line designs is a **menu**, not a target — the same
reading the DSA tracker gets ("everything still unproven", not a trophy case). At one design per Sunday,
the core 20 alone is ~5 months; the Tier-1 queue is explicitly *not* meant to be drained before the apply
trigger.
