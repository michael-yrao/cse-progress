# System Design — Senior/Staff (L6) Interview Ramp

> **Created Aug 6, 2026. Rebuilt Aug 13, 2026 for the mock-interview model** — the learner studies system
> design independently on [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction);
> the coach runs cold mocks on HelloInterview's questions and scores them. Mechanics:
> [`study_guide.md`](study_guide.md). State: [`mastery/design_progress.md`](mastery/design_progress.md).
>
> **Target: big tech / MANGA-adjacent** (Meta, Apple, Netflix, Google, Amazon + the tier around them),
> **senior/staff (L6)** given ~10 years' experience. **Fintech and other domain roles are paid waypoints,
> not the target.**
>
> This is a **sequence with exit gates, not a calendar of deadlines** ([[feedback_phase_dates_are_advisory]]).
> Week bands are advisory — you advance a phase when its **gate** is met. A phase that runs long carries
> forward; that is a normal outcome.

## Target & emphasis — depth over breadth

~10 years in ⟹ the bar is **Staff-adjacent (L6)**. At L6 the interviewer assumes you can produce a
competent design and spends the round trying to **break** it — requirements ambiguity, cross-cutting
concerns (multi-region, migration, zero-downtime rollout, cost, failure domains), and relentless
"why not X / what happens at 100× / how do you evolve this."

- **The gate is depth, not count:** *a handful of designs defended 2–3 levels deep under sustained
  pushback plus a live curveball requirement change* — never "N designs banked."
- **35 rows is a menu, not a target.** At one mock a week the board is eight months long and is not meant
  to be drained. Draining it is not the apply trigger and never becomes one.
- **No domain weighting.** Payment System and Robinhood sit off the rotation behind
  `waypoint_loop:fintech` even though HelloInterview rates them Hard and they are well-known designs.

## The rubric — how a mock is scored

**The unit is a timed ~45-min cold mock, scored right after it against these seven checkpoints, logged as
a comfort rating.** Each is pass/fail, and the evidence for each is named out loud in the debrief.

| # | Checkpoint | Pass test |
|---|---|---|
| 1 | Requirements | functional + non-functional + scale numbers, pinned unprompted |
| 2 | Estimation | QPS / storage / bandwidth, correct order of magnitude, done where a number changes a decision |
| 3 | API + data model | core entities, API surface, schema |
| 4 | High-level architecture | components + data flow, coherent, drawn |
| 5 | **Forks defended** | 3–4 biggest forks: trigger → choice → one-line why → **breaks at 10×** |
| 6 | **Failure modes** | named SPOF (single point of failure) / bottleneck / race **before** being asked |
| 7 | **Evolve & operate** | migration / multi-region / zero-downtime rollout / cost & failure domains, unprompted — **and how the design bent under the curveball** |

**Rating:** 🟢 = #1–4 solid **and** #5, #6, #7 all pass · 🟡 = skeleton solid, senior half thin (also the
ceiling for a non-cold mock) · 🔴 = couldn't drive the framework cold.

**The senior gate is inside the rating.** #1–4 are *assumed* at L6, so the score lives in tradeoff
defense, naming your own failure modes, and evolve/operate — not in drawing boxes. A mock that walks the
framework cleanly and stops is a 🟡, by design.

**The curveball is graded under #7 and is mandatory.** Around minute 30 the interviewer changes a
non-functional requirement in a way that invalidates part of the design. What is graded is not whether
the first design survives — it usually shouldn't — but whether the learner can name what breaks, what
they'd keep, and what the new tradeoff costs.

## The board and the order

**35 rows, HelloInterview's own tiers** — see [`mastery/design_progress.md`](mastery/design_progress.md)
for state. Order within a phase is *what it teaches*, not alphabetical.

### Phase 0 — study mode (current, from Aug 13, 2026)

**No SD slot is scheduled.** The learner is working through HelloInterview's Core Concepts and Key
Technologies at **junior/senior depth**, and **Phase A begins on their signal** — see
[`study_guide.md`](study_guide.md). The next SD session is a **restructure session** that scopes those
two pillars to a workable depth; they call it.

⚠️ **"Scoped" means a senior *bar*, not a low ceiling** — the mocks probe as deep as the design allows,
and a probe that runs past the bar costs nothing on the rating. **A staff-level tier follows the core**
and raises the ceiling rather than the bar. Both rules, and the caveat about ratings not being comparable
across a bar change, are in [`study_guide.md`](study_guide.md) → *Depth*.

**Nothing else waits on it.** DSA runs at full capacity, and every day without an SD slot carries an
unseen problem.

### Phase A — framework fluency (advisory: ~Aug → Sep)

**Goal:** make #1–4 automatic, so later mocks spend their 45 minutes on the senior half instead of
remembering the steps. The Easy tier is where the framework itself is the thing being drilled.

| # | Question | Why here |
|---|---|---|
| 1 | **Bitly** | closes the in-flight URL-shortener arc; the cleanest possible framework rep |
| 2 | **Dropbox** | large blobs, presigned URLs, chunked upload — the one topic the old repo never had a note for |
| 3 | **Local Delivery (GoPuff)** | inventory + proximity at an Easy slope |
| 4 | **Yelp** | geospatial indexing proper |
| — | **Rate Limiter** *(re-mock, currently 🟡, overdue since Aug 5)* | already banked once; scored **specifically on #5–7**, not on walking the framework again |

**Exit gate:** #1–4 pass on **3+ different questions**, and at least one mock reaches #5 with a fork
defended to its breaking point.

### Phase B — senior signals (advisory: ~Sep → Oct)

**Goal:** where L6 is won — forks, failure modes, evolve/operate. This is also where the **midweek
deep-dive round** starts running, because there is finally something banked to push on.

**Order:** WhatsApp → FB News Feed → YouTube → **Ticketmaster** → Job Scheduler → Notification System →
Instagram → Distributed Cache → Tinder → LeetCode → Strava → Online Auction → FB Live Comments →
News Aggregator → Price Tracking.

- **Ticketmaster is the one to protect** — it is the contention design (holds, reservations, oversell),
  and contention is the pattern with no cheap substitute anywhere else on the board.
- **Distributed Cache** covers what the old board could not source at all: designing a cache rather than
  using one (consistent hashing, eviction, replication, invalidation).
- **Re-mock Phase-A designs here at +10/+30**, scored only on #5–7.

**Exit gate:** **~4 designs defended 2–3 levels deep under sustained pushback**, including #7, across
varied domains — measured by the deep-dive rounds, not by the first mock.

### Phase C — simulation & calibration (advisory: ~Oct+, overlaps the DP phase)

**Goal:** convert bank into reflexes and calibrate against real loops.

**Order:** Web Crawler → Ad Click Aggregator → YouTube Top K → FB Post Search → Metrics Monitoring →
Google Docs → Uber → ChatGPT.

**Then the four no-write-up questions** — Food Review App · Game Leaderboard · Donations Website ·
GitHub Actions. **Hold them until here.** They are the only rows that cannot become prepared mocks (no
worked answer exists to read), which makes them the honest test of whether the framework transfers to a
question that was never studied. Spending them in Phase A wastes the one thing they measure.

**Also here:** the parked non-HelloInterview designs, `board:hard-tier-open` (typeahead, key-value store,
Google Calendar, distributed tracing, A/B testing, **data migration**, stream-processing). **Protect data
migration** — it is rubric #7 turned into an entire design, and #7 is what the L6 rating hinges on.

**Trigger-gated, not in any phase:** Payment System · Robinhood (`waypoint_loop:fintech`) · Online Chess
(lowest ceiling on the board; pull only as overflow).

**SD exit gate** — the mechanics live here; the apply *decision* is
[`../career_strategy.md`](../career_strategy.md) §4 Gate 3, which also requires DSA in maintenance:

- a handful of designs defended deep under pushback, including #7,
- a clean cold 45-min mock end-to-end without prompting,
- **at least one 🟢 on a no-write-up question** — the transfer test.

**The trigger is the gate, not the calendar.**

## The scoreboard at a glance

| Metric | Now (Aug 13) | Phase A gate | Phase B gate | Apply trigger |
|---|---|---|---|---|
| Designs with #1–4 passing | 0 | 3 | — | — |
| Designs defended deep (incl. #7) | 0 | — | ~4 | handful |
| Cold 45-min mock, unprompted | no | — | — | **yes** |
| 🟢 on a no-write-up question | no | — | — | **yes** |

⚠️ **Never report row count as progress.** Every row on the board is "still unproven"; that is what the
tracker means.

---

## Historical — the systemdesign.io triage (Aug 6–11, 2026)

**The board was [systemdesign.io](https://systemdesign.io/)'s 55 questions until Aug 13, 2026**, triaged
against the L6 bar on Aug 8 with a written reason for every placement. Reseeding to HelloInterview
replaced the source. That triage is kept in compressed form because its **declines** are the part with
ongoing value — if one of these is ever proposed again, the reason already exists.

**Most of the old core set maps onto the new board** (URL shortener → Bitly · Messenger → WhatsApp ·
Doc Mgmt → Google Docs · Top-K → YouTube Top K · Metrics → Metrics Monitoring · Nearby → Yelp · Ads →
Ad Click Aggregator · Instagram, Web Crawler, News Feed, YouTube, Job Scheduler, Notification, Dropbox
all present by name). What did **not** map is parked with a trigger in
[`mastery/design_progress.md`](mastery/design_progress.md).

**Declined then, still declined — one line each:**

| Question | Why below the line |
|---|---|
| Distributed queue (RabbitMQ) | Kafka covers queueing at higher L6 frequency |
| Control plane for a distributed DB | data-platform round, not generalist |
| Surge pricing · ETA service · Uber matching | geo/stream content redundant with Uber + Yelp |
| 6M free burgers (flash sale) | closest call on the list; promote if a retail loop appears |
| Hotel booking | reservation consistency — Ticketmaster teaches it harder |
| Large-data sorting | dated round shape |
| BitTorrent file transfer | P2P specialty; sync half covered by Dropbox |
| Netflix screen limits · page-viewer counts · FB like counts | good deep dives, too thin as whole rounds |
| Cluster health monitor · on-call escalation · photo sharing | redundant with Metrics / Notification / Instagram |
| User login & auth | a deep dive *inside* other designs, not a round |
| Stock prices · marketplace · weather · parts-compatibility · price alerts | low ceiling, no distinctive distributed content |
| File-downloader library · IoC framework · botnet | wrong altitude (LLD) or not an interview design |

⚠️ **The reasons are the coach's calls and remain arguable.** The list is useful because it is written
down, not because any single placement is beyond challenge.
