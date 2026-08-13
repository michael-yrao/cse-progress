# SD Coverage Map — what the syllabus is, and what the board tests

> **Created Aug 11, 2026; rewritten Aug 13, 2026** for the mock-interview model.
>
> **The syllabus is no longer this repo's problem.** [HelloInterview's *System Design in a
> Hurry*](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) is the syllabus and
> the learner studies it directly. This file now answers the one question a syllabus cannot:
> **does the sequence of mocks actually exercise it?**
>
> **"HelloInterview" is written out in full everywhere below, deliberately** — the first draft abbreviated
> it to *"HI"*, an abbreviation invented here and expanded nowhere, in a file meant to be reread cold
> weeks later. See [[feedback_expand_acronyms]].

## The four pillars, and who owns each now

| Pillar | Owner | Where |
|---|---|---|
| **Delivery** — the six steps and their time budgets | shared: learner studies it, coach times the mock against it | [`framework.md`](framework.md) *is* HelloInterview's Delivery, step for step |
| **Key Technologies** — 10 deep dives | **learner** | [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies). Local cards for [Redis](technologies/redis.md) and [PostgreSQL](technologies/postgresql.md) stay as reference |
| **Core Concepts** — 9 | **learner** | [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts) |
| **Patterns** — 8 | **learner** | [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns) |
| **Whether any of it survives contact** | **coach**, via mocks | [`mastery/design_progress.md`](mastery/design_progress.md) |

**This is the change that mattered.** Under the old model the repo owed itself 8 pattern cards, 7 core
concepts and 7 technology notes — roughly 22 documents, none of which would be graded, all competing for
the same slots as the mock. HelloInterview has already written all 22.

## What the repo still owns, and why

**The nine `concepts/` cards.** They are *quantitative* foundations — [Little's Law](concepts/littles_law.md) ·
[percentiles & tail latency](concepts/percentiles_and_tail_latency.md) ·
[utilization & queueing](concepts/utilization_and_queueing.md) ·
[probabilistic sketches](concepts/probabilistic_sketches.md) ·
[retry storms & stampedes](concepts/retry_storms_and_stampedes.md) ·
[quorum math](concepts/quorum_math.md) · [Zipfian distribution](concepts/zipfian_distribution.md) ·
[Bloom filter](concepts/bloom_filter.md) · [networking basics](concepts/networking_basics.md).

**Seven of the nine map to nothing in HelloInterview**, whose Core Concepts are *structural* (sharding,
CAP, consistent hashing, indexing) rather than numeric. These are the facts needed **mid-sentence to
defend a number** when the interviewer pushes on "read-heavy" or "p99 is fine" — which is exactly what
rubric #5 grades. Each opens with a "You'll want this when…" trigger line, so they work as a
symptom-indexed lookup during a debrief without having been read in advance.

**The three `components/` cards** ([caching](components/caching.md) ·
[load balancer](components/load_balancer.md) · [rate limiter](components/rate_limiter.md)) stay as
remediation reference. Nothing new gets written on a schedule.

## Does the board cover the patterns? — the check to run at each weekly build

**The eight HelloInterview patterns, mapped onto the questions that force them.** This is the only
coverage question the tracker cannot answer: the tracker knows which *questions* are unproven, not which
*moves* have never been rehearsed.

| Pattern | Questions on the board that force it |
|---|---|
| **Pushing realtime updates** | WhatsApp · FB Live Comments · Google Docs · Online Chess · Game Leaderboard |
| **Dealing with contention** | **Ticketmaster** · Online Auction · Payment System · Robinhood |
| **Managing long-running tasks** | Job Scheduler · Web Crawler · YouTube (transcode) · GitHub Actions |
| **Scaling reads** | FB News Feed · Instagram · Bitly · Distributed Cache |
| **Scaling writes** | Ad Click Aggregator · Metrics Monitoring · YouTube Top K |
| **Handling large blobs** | **Dropbox** · YouTube · Instagram |
| **Multi-step processes** | Payment System · Local Delivery · Donations Website · Ticketmaster |
| **Proximity-based services** | **Yelp** · Uber · Tinder · Local Delivery · Strava |

### What that map says about the current sequence

**Phase A (Bitly · Dropbox · Local Delivery · Yelp) exercises three patterns: scaling reads, large blobs,
proximity.** It cannot test contention, scaling writes, realtime, or long-running tasks — no Easy
question does. That is the correct trade for Phase A, whose gate is framework fluency, and it is the
reason Phase B's order front-loads WhatsApp (realtime), Ticketmaster (contention) and Job Scheduler
(long-running).

**Contention is the thinnest pattern on the board.** Four questions force it and three of them are Hard
or trigger-gated, so **Ticketmaster is effectively the only accessible contention rep** — which is why
it is marked protected in [`senior_ramp.md`](senior_ramp.md).

## Maintenance

- **Re-read this at each weekly build**, alongside the tracker: this file answers *"which moves have
  never been rehearsed"*, the tracker answers *"which questions are unproven."*
- **This file holds no status.** No comfort, no ✅, no dates — those are computed. What lives here is
  taxonomy → owner, and pattern → question, both of which are stable.
- **When a mock debrief shows a pattern was needed and missing**, that is a study assignment on
  HelloInterview's page for it, recorded in the debrief. It is not a slot and it is not a card owed here.
