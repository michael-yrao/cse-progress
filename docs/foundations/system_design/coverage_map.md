# SD Coverage Map — the syllabus, and what of it exists

> **Created Aug 11, 2026**, after the learner asked how to fold
> [HelloInterview's *System Design in a Hurry*](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts)
> structure into this repo. Answer: **three of its four pillars are already here under different names.**
> The fourth is entirely absent. This file is that mapping.

## 🧭 What this file owns (read before editing)

Per the ownership table in [`study_guide.md`](study_guide.md), every SD thing has exactly one owner.
This file adds a fourth:

| Thing | Owner |
|---|---|
| **State** — comfort, streak, next review | [`mastery/design_progress.md`](mastery/design_progress.md) |
| **The plan** — design triage, phases, exit gates, rubric, tech order | [`senior_ramp.md`](senior_ramp.md) |
| **The mechanics** — cadence, lanes, session formats, templates | [`study_guide.md`](study_guide.md) |
| **The syllabus** — what topics exist, and where each one lives | **this file** |

**This is the SD analogue of [`techniques.yml`](../dsa/mastery/techniques.yml).** DSA has a vocabulary
layer keyed by *technique*, joined against the tracker to answer *"do I actually know topological sort?"*
— a question the problem-keyed tracker structurally cannot answer. **SD had no vocabulary layer at all.**
The tracker lists 54 rows; nothing said whether those 54 rows *cover the subject*.

⚠️ **This file holds NO status.** Not comfort, not ✅, not "done." Status is computed by the tracker and a
status written in prose is wrong within three weeks — that is the whole lesson of the Aug 8 reconciliation.
What lives here is **taxonomy → intended home**, which is stable. "Does a file exist" is `ls`-derivable and
appears here only as *none yet* (a routing fact, not a progress claim).

---

## Pillar 1 — Delivery ✅ already adopted

**HelloInterview's *Delivery* is [`framework.md`](framework.md).** Not "similar to" — the same six steps,
the same time allocations, and it already carries HI's distinctive estimation stance (don't front-load a
wall of math; do the arithmetic at the box where a number changes a decision).

| HI step | budget | `framework.md` |
|---|---|---|
| Requirements (functional · non-functional · capacity) | ~5 min | §1 |
| Core Entities | ~2 min | §2 |
| API / System Interface | ~5 min | §3 |
| *[optional]* Data Flow | ~5 min | §3, marked skip-by-default |
| High Level Design | ~10–15 min | §4 |
| Deep Dives | ~10 min | §5 |

**Nothing to import.** What this pillar needs is *reps*, and reps are lane ③ — which is running (URL
shortener, Sun Aug 16). **No action.**

---

## Pillar 2 — Key Technologies ✅ structurally present, ⚠️ mostly unbuilt, and mislabelled

All ten HI technologies have a home. **Only one is drilled.**

| HI technology | This repo | File |
|---|---|---|
| Relational Database | `PostgreSQL` row | [`technologies/postgresql.md`](technologies/postgresql.md) |
| NoSQL Database | `Cassandra` + `DynamoDB` rows | none yet |
| Blob Storage | ❌ **no row, no file** | — |
| Search Optimized Database | `Elasticsearch` row | none yet |
| API Gateway | `API Gateway` row | none yet |
| Load Balancer | `Load balancer` row | [`components/load_balancer.md`](components/load_balancer.md) |
| Queue | ⚠️ **no row for the role** — `Kafka` is filed as *streaming log* | — |
| Streams / Event Sourcing | `Kafka` + `Flink` rows | none yet |
| Distributed Lock | `ZooKeeper` row (adjacent, not the same) | none yet |
| Distributed Cache | `Redis` row | [`technologies/redis.md`](technologies/redis.md) |

### Two real findings, not bookkeeping

**1. Blob storage is missing outright**, and it is load-bearing for Dropbox, YouTube, Instagram — three
designs already on the board. Any design that moves a file larger than a row hits it immediately.

**2. ⭐ HI names technologies by ROLE; this repo names them by PRODUCT — and HI's framing is the better
interview instrument.** *Queue · Distributed Lock · Distributed Cache · Search Optimized Database* are
**jobs**; *Kafka · ZooKeeper · Redis · Elasticsearch* are **answers**. In an interview you reach for the
job first (*"I need to decouple this write path"*) and name the product second, and the product is
substitutable — SQS, RabbitMQ and Kafka all fill the queue slot with different tradeoffs.

A product-keyed list quietly teaches the retrieval path backwards, and it hides substitution: **a
`Kafka` row cannot show that the *queue* role has never been drilled, because Kafka is only one way to
fill it.** Same failure mode as DSA's free-text method parentheticals, and the same fix — key on the
role, name products underneath.

**Proposal:** re-label the tech rows as `Role — Product` (`Queue — Kafka`, `Distributed Lock — ZooKeeper`,
`Distributed Cache — Redis`). Cheap, non-destructive, and it makes a missing *role* visible. **Decide at
the Aug 17 build.**

---

## Pillar 3 — Core Concepts ⚠️ 2 of 9

| HI core concept | This repo | Status of the mapping |
|---|---|---|
| Networking Essentials | [`concepts/networking_basics.md`](concepts/networking_basics.md) | ✅ mapped (re-teach scheduled Thu Aug 13) |
| Caching | [`components/caching.md`](components/caching.md) | ✅ mapped, and deeper than HI's version |
| **API Design** | — | ❌ **gap** |
| **Data Modeling** | — | ❌ **gap** |
| **Database Indexing** | — | ❌ **gap** (checked: `postgresql.md` covers ACID, replication, replica lag — *not* indexing) |
| **Sharding** | — | ❌ **gap** (a `databases/` folder is "planned" in `study_guide.md` and does not exist) |
| **Consistent Hashing** | — | ❌ **gap** |
| **CAP Theorem** | — | ❌ **gap** ([`quorum_math.md`](concepts/quorum_math.md) is adjacent — R+W>N is a *consequence* of the CAP position, not a statement of it) |
| **Numbers to Know** | — | ❌ **gap** (percentiles and Little's Law are adjacent; neither is the latency/throughput cheat sheet) |

### ⚠️ Do NOT collapse `concepts/` into HI's Core Concepts — they are different axes

Seven of the nine files in `concepts/` map to **nothing** in HI: Little's Law · percentiles & tail latency ·
utilization & queueing · probabilistic sketches · retry storms & stampedes · Zipfian · Bloom filter.

That is not redundancy to prune — it is the **quantitative-foundations lane**, added deliberately because
*the pull model structurally cannot catch concepts.* A missing building block is a visible hole in a
diagram; a missing *fact* only surfaces once you are already stuck mid-sentence trying to justify a number.
Deleting or merging that lane would re-open the exact hole it was built to close.

**So `concepts/` grows in two directions and both are legitimate:**

| | |
|---|---|
| **Quantitative foundations** (existing 9) | facts needed mid-sentence to defend a number. No natural design trigger ⟹ must be front-loaded |
| **HI Core Concepts** (the 7 gaps) | structural techniques every design touches. **These *do* have natural triggers** ⟹ let designs and patterns pull them |

---

## Pillar 4 — Patterns ❌ 0 of 8 — the actual hole

| HI pattern | This repo |
|---|---|
| Pushing Realtime Updates | ❌ |
| Managing Long-Running Tasks | ❌ |
| Dealing with Contention | ❌ |
| Scaling Reads | ❌ |
| Scaling Writes | ❌ |
| Handling Large Blobs | ❌ |
| Multi-Step Processes | ❌ |
| Proximity-Based Services | ❌ |

**Why this is the one to attack, stated as an argument rather than a preference.**

The other three pillars are *inventory* and *process*. Technologies are things you can name; concepts are
facts you can state; delivery is the order you walk. **Patterns are the reusable moves** — what you reach
for when the interviewer says *"now make it realtime"* or *"now it's write-heavy."* With zero of them
written, every design re-derives each move live, under time pressure, from first principles.

**And they are the cheap pillar.** A pattern card is short — trigger, the two or three standard moves, the
fork between them, where each breaks. It is not a technology deep-dive.

### ⭐ Patterns pull concepts, the same way designs pull blocks

This is the structural reason to do patterns before the Core Concepts backlog, and it is the repo's own
existing model applied one level up:

- **Scaling Reads** drags in replication, caching (have it), **CAP**
- **Scaling Writes** drags in **sharding**, **consistent hashing**, **data modeling**
- **Dealing with Contention** drags in **distributed locks**, isolation levels, idempotency
- **Handling Large Blobs** drags in **blob storage** (the Pillar-2 gap), presigned URLs, CDN
- **Managing Long-Running Tasks** drags in the **queue role** (the other Pillar-2 gap), workers, retries
- **Pushing Realtime Updates** drags in WebSocket vs SSE vs polling — *already named as a pull-queue item*

**Six of the seven Core Concepts gaps and both Key Technology gaps are pulled in by patterns.** Building
patterns first means the concept backlog largely schedules itself, in dependency order, with a live reason
attached. Building the concepts list first means grinding an inventory with no skeleton to hang it on —
the §1a failure in curriculum form, which is the same mistake the *designs-pull-blocks* rule already
exists to prevent.

**Left over, needing front-loading because no pattern pulls them:** API Design · Database Indexing ·
Numbers to Know.

---

## Proposed order — and what it costs

| # | Work | Why here |
|---|---|---|
| **1** | **8 pattern cards** | 0/8, cheapest pillar, and it pulls 6 of 7 concept gaps + both tech gaps |
| **2** | **API Design · DB Indexing · Numbers to Know** | the three nothing pulls; front-load like the quantitative lane |
| **3** | **Blob Storage + the Queue *role*** | pulled by patterns 6 and 2; blocks Dropbox / YouTube / Instagram, all on the board |
| **4** | **Re-label tech rows `Role — Product`** | one edit; makes an undrilled *role* visible |
| **5** | Remaining tech notes | already sequenced in [`senior_ramp.md`](senior_ramp.md); unchanged by this map |

### ⚠️ The cost is a lane conflict, and it must be resolved, not absorbed

**Lane ② already has a fallback queue.** The rule is *each lane owns a slot; never let two lanes bid for
the same one* — and lane ② currently runs cold-hit block notes, falling back to `concepts/` cards when the
pull queue is empty. **Patterns would be a third bidder for one ~30-minute midweek slot.**

Options, to decide at the build — **not** to leave implicit:

| | Option | Effect |
|---|---|---|
| **a** | Patterns **displace** concepts as lane ②'s fallback until drained | ~8 slots ≈ 4 weeks at `three_weekly`. Quantitative lane pauses |
| **b** | Add a **fourth** SD slot | +3.0 units/week against a 63-unit ceiling. DSA yields the difference |
| **c** | Alternate patterns / concepts week by week | halves both rates; drains neither. **Weakest — this is how a queue becomes an ambush log** |

**Recommendation: (a).** Patterns are finite (8) and unblock the rest of the map; the quantitative lane has
no deadline and resumes after. **The learner picks.**

---

## Maintenance

- **When a pattern or concept card is written, add its row to the tracker in the same edit** — same rule as
  mapping a DSA problem into `techniques.yml` the moment it is logged. Without it, this map drifts behind
  the tracker exactly the way the method parentheticals rotted.
- **This file is taxonomy, not progress.** If you find yourself typing a ✅ or a date here, it belongs in
  the tracker instead.
- **Re-read at each weekly build**, alongside `technique_coverage.md`: this one answers *"is the syllabus
  covered"*, the tracker answers *"is it retained."*
