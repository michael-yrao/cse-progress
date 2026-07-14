# System Design Study Guide — Interview Core → Architect Depth

## Mission & the Interview-ROI Line

**End goal:** become a genuine systems **architect** (Staff / Principal / CTO-level) — someone who can design, reason about, and defend planet-scale distributed systems from first principles. **Passing the system-design interview is a milestone on that path, not the finish line.**

As with DSA, depth has diminishing returns *for interviews specifically*, so everything is sorted around one marker:

> **The Interview-ROI Line** — the point past which added systems depth stops improving interview performance and becomes real-world architect mastery.

**Above the line — Interview Core (Tier 1). Do this first; it's the whole SD-interview surface.**

1. **Fundamentals & estimation** — latency numbers every engineer should know, back-of-envelope math (QPS, storage, bandwidth), vertical vs horizontal scaling.
2. **Building blocks** — load balancing, caching (patterns, eviction, invalidation), CDN, reverse proxy / API gateway, message queues & async processing, rate limiting, consistent hashing, bloom filters.
3. **Data layer** — SQL vs NoSQL tradeoffs, indexing, replication (leader/follower, multi-leader), sharding / partitioning, CAP & PACELC, consistency levels (strong → eventual), idempotency.
4. **The interview framework** — requirements (functional + non-functional) → estimation → API design → data model → high-level diagram → deep dives → bottlenecks & tradeoffs. *Driving this framework fluently is 50% of the interview.*
5. **Canonical designs** (the "grokking" set): URL shortener, rate limiter, chat/messenger, news feed, notification service, typeahead/autocomplete, web crawler, video streaming (YouTube/Netflix), ride-share (Uber), file storage (Dropbox/Drive), Ticketmaster, distributed KV store / cache, payment/ledger, top-K / trending.

Being fluent across (1)–(5) is the ceiling of *interview* ROI. Everything below sharpens you as an engineer but won't move an interview score much.

**=== INTERVIEW-ROI LINE ===**

**Below the line — Architect Depth (Tier 2). High real-world ROI, low interview ROI. Pursue for mastery, not interview prep.**

6. **Designing Data-Intensive Applications (Kleppmann)** — read cover to cover. The single best bridge from "interview competent" to "actually understands distributed systems." This is the on-ramp for everything below.
7. **Consensus internals** — Raft (start here), Paxos / Multi-Paxos, ZAB. Understand *why* consensus is hard, not just that ZooKeeper exists.
8. **Distributed transactions** — 2PC / 3PC, Sagas, Percolator, Calvin. When and why each fails.
9. **Consistency theory** — linearizability vs sequential vs causal vs eventual; session guarantees; CRDTs.
10. **Storage engines** — LSM-tree vs B-tree, write-ahead log, compaction, MVCC. What's actually happening inside Postgres / Cassandra / RocksDB.
11. **Stream processing** — exactly-once semantics, watermarks, backpressure (Kafka, Flink).
12. **Foundational papers** — GFS, MapReduce, Bigtable, Dynamo, Spanner, Chubby, ZooKeeper (ZAB), Kafka, Cassandra, Raft, F1. Read the primary sources.

**Tier 3 — research / specialization horizon (only for deep distributed-systems ambition; near-zero interview ROI):** formal methods (TLA+ / model checking), academic distributed systems (MIT 6.824), consensus variants (EPaxos, Flexible Paxos, Fast Paxos), advanced consistency (Bayou, COPS, highly-available transactions), chaos engineering & fault injection at scale, hardware-aware design (NUMA, RDMA, kernel-bypass), planet-scale coordination (TrueTime, hybrid logical clocks).

**How to use the line:** ask *"which side is this on, and am I optimizing for the interview or for real mastery right now?"* Finish Tier 1 before crossing. Don't mistake DDIA-depth for interview readiness (framework fluency matters more there), and don't mistake interview readiness for real systems mastery.

---

## Cadence — the three-lane rule

System design runs **three times a week** (raised from twice on **Jul 14, 2026**). Three lanes, three
slots, **each lane owns one.** This is the arbiter — never let two lanes bid for the same slot.

| Slot | Lane | Shape | Driven by |
|------|------|-------|-----------|
| **Light midweek** — swaps **one 15-min warmup** | **① Technology fluency** — one blind sprint vs a Recall Card (`technologies/*.md`) | short, ~15 min | **due dates** (spaced rep). Nothing due → build the next tech's note. Order: Redis ✅ → **PostgreSQL** → Cassandra → DynamoDB → Kafka … |
| **Fuller midweek** — swaps **both warmups** (~30 min) | **② Building blocks & probes** — write the `components/` note for whatever block the last design **hit cold**; then fire framework probe questions at a system already designed | ~30 min | **the pull queue** (see below) |
| **Sunday** — the deep sprint | **③ Designs** — one staged session on a canonical system, full framework | 45–60 min | **sequence** |

**Neither midweek slot cuts a 45-min DSA active block.** Both come out of **warmup** capacity: −4 DSA
warmup reps/week, absorbed by the **🟢 Clean backlog**. New-problem intake stays at 5/week.
*(Accepted Jul 14: the 🟢 pile is 2–5 months stale and its interval math is already meaningless — it's
the right place for the cost to land. It still owes a policy decision.)*

**Why three, not two.** Lane ② was **homeless** under the two-lane rule. "Designs pull the blocks"
says: hit a block cold mid-design → log it → *build its note in the next slot* — but with only two
slots that note had to eat the tech-fluency rep, so **the pull model starved itself.** The third
session isn't padding; it's what makes the model run.

### The Sunday lane: designs pull the blocks ⭐

**Decided Jul 14, 2026.** Do **not** grind every Tier-1 building block before attempting an
end-to-end design. At one Sunday per stage, the 7 remaining blocks are a **~5-month** wall — and only
*then* would you touch a canonical design, which is where the interview score actually lives
(*"driving this framework fluently is 50% of the interview"* — see Tier 1 item 4).

**Instead: start canonical designs now, and learn each block when a design demands it.**

> **The design is the skeleton; the blocks hang off it.** A block learned in isolation is a fact.
> A block learned because your chat design just hit a fan-out wall is a **tool.**

```
Sun: Rate Limiter — Mastery       ← close the open arc
Sun: Caching — Bootstrap          ← the one block you're actually missing
Sun: DESIGN — URL shortener       ← full framework, end-to-end
Sun: DESIGN — Chat / messenger
       ↳ hits message queues cold → next midweek builds the MQ note
Sun: DESIGN — News feed
       ↳ hits fan-out (push/pull), CDN → notes follow
...
```

The accepted cost: **you will hit blocks cold, mid-design.** That is the point — the gap is the
teaching signal, and it names its own drill target. Log the cold-hit block, then build its note in the
**next fuller-midweek slot (lane ②)** — that slot exists precisely to catch these. Don't stop the
design to go study.

**Corollary — a 🔴 on a *concept* means teach it, don't re-sprint it.** A blind sprint *measures*; it
doesn't teach. When a rep comes back 🔴 because the thing was never encoded (vs. decayed), the next
session is a **derive-the-design** (see below), **unrated**, and the rated sprint moves out far enough
to be a real test. Rating a sprint run right after teaching measures the conversation, not retention.

### Session formats

**Staged arc** (per building block / design) — one stage per Sunday:

- **Bootstrap** — first exposure: watch a good explainer, recall from memory, check gaps. No cold whiteboarding yet.
- **Transition** — sketch the design cold from memory, then **diff against the reference note**. The misses become the named drill targets for Mastery.
- **Mastery** — full mock-interview timing (~45 min), self-scored against the framework, drilling the Transition misses.

**Interactive formats** (for concepts that aren't landing — ranked by how much *the learner* produces):

1. **Derive-the-design** ⭐ — coach gives the *constraint*, learner **invents the mechanism**, coach then names it. (*"3 app servers, each with its own counter. User hits all 3. What breaks? Fix it."* → learner invents shared state → **that's Redis.**) Best format for "why does this exist." Use it on any 🔴 concept.
2. **Failure-mode drill** — *"Redis just died. Now what?"* Forces the tradeoff talk interviewers actually grade.
3. **Socratic pushback** — learner explains it back; coach plays skeptical interviewer, asking "why" until it bottoms out. Exposes memorized-vs-understood instantly.
4. **Blind sprint** (Recall Card) — **measures** retention; does not teach. Keep, but don't mistake it for instruction.

**What does not work:** escalating explanation dumps. Correct detail without a skeleton is noise and
actively *displaces* the core idea. **Lead with the spine** — the 2–3 load-bearing facts everything
else derives from — then stop and check in. Depth on request only.

### Stage status

| Topic | Bootstrap | Transition | Mastery |
|-------|-----------|------------|---------|
| [Rate limiter](components/rate_limiter.md) | ✅ Jul 5 | ✅ Jul 12 | ⏳ **Sun Jul 19** |
| Caching | ⏳ Jul 20 wk | — | — |

Below-the-line (Tier 2+) work is **not** a sprint activity — it's long-form reading (DDIA, papers) pursued deliberately *after* interview-core is solid, on its own track.

### Technology fluency (spaced repetition)

Designs are argued in the vocabulary of concrete **technologies** ("I'd put Redis here, Kafka there"). Those are drilled the same way as DSA — active recall, comfort rating, auto-scheduled review — tracked in [`mastery/design_progress.md`](mastery/design_progress.md), driven by the same `scripts/update_review_dates.py` and pre-commit hook.

- **The unit:** one technology, with a note + **Recall Card** in [`technologies/`](technologies/).
- **The rep (a "blind sprint"):** answer the card's prompts from memory → unfold to check → rate 🟢/🟡/🔴 → log + commit → next review auto-computes (+30/+10/+2).
- **Backlog & order** (data-store trio is highest-leverage): Redis ✅ · **PostgreSQL** (next) → Cassandra → DynamoDB · Kafka → Flink · Elasticsearch · API Gateway · ZooKeeper.
- **This is lane ①** — the *light* midweek slot. One rep; nothing due → build the next tech's note.

**Drive every practice session through the templates** in [`templates/`](templates/):
- Designing a whole system (Transition/Mastery on a Design Practice Backlog item) → copy [`case_study_template.md`](templates/case_study_template.md) and fill it end-to-end (requirements → estimation → data model → high-level → diagram).
- Learning one building block (a Bootstrap topic like caching or rate limiting) → copy [`component_template.md`](templates/component_template.md) (metaphor → DSA connection → strategies → failure modes → diagram).

Filling a template *is* the rep — don't just read about a system, fill the scaffold for it.

## Arriving at design decisions (the drill)

The interview isn't scored on *drawing* a system — it's scored on **defending the
choices**. A diagram anyone can memorize; the signal is *why* you picked this over
that, and knowing where it breaks. Every design is a chain of forks; for each fork,
practice naming the **trigger** (the requirement that forces the choice), the
**options**, and the **deciding question** that picks one.

**The recurring forks (memorize the deciding question, not the answer):**

| Fork | Deciding question | Picks A ⟶ / ⟵ Picks B |
|------|-------------------|------------------------|
| SQL ⟷ NoSQL | Do I need multi-row transactions / joins, or scale-out + flexible schema? | ACID & relations ⟶ SQL / massive scale, simple access ⟶ NoSQL |
| Strong ⟷ eventual consistency | Is a stale read *incorrect*, or just slightly old? | money/inventory ⟶ strong / feeds, counts ⟶ eventual |
| Sync ⟷ async (queue) | Must the caller wait for the result, or can work be deferred? | needs the answer now ⟶ sync / fire-and-forget, spikes ⟶ async |
| Cache-aside ⟷ write-through | Is read latency or write freshness the priority? | read-heavy ⟶ aside / can't serve stale ⟶ write-through |
| Replication ⟷ sharding | Am I read-bound (scale reads) or write/storage-bound (scale capacity)? | too many reads ⟶ replicas / too much data/writes ⟶ shards |
| Push ⟷ pull (fan-out) | Few writers→many readers, or many writers→few readers? | celebrity read fan-out ⟶ pull / normal ⟶ push-on-write |

**Practice the decision, not just the design.** On every backlog item below, force a
short **decision log**: for the 3–4 biggest forks, write *trigger → option chosen →
one-line why → where it breaks at 10× scale*. That last clause is the differentiator —
naming your own design's failure mode before they ask is the senior signal.

**Questions they'll ask (rehearse the probe, out loud):**
- "What happens when this component dies / the DB falls over?" (single points of failure)
- "How does this behave at 10×? 100×?" (which piece saturates first, and your fix)
- "Two users do X at the same instant — what happens?" (race conditions, idempotency)
- "Why *this* database / queue / cache and not the alternative?" (defend the fork)
- "Where's the bottleneck, and how would you shard/cache/replicate around it?"
- "How do you keep these two copies in sync? What if they diverge?" (consistency)
- "How would you roll this out / migrate with zero downtime?" (real-world ops)

Treat each as a rep: pick a system you've designed, have the coach fire these, and
defend cold. A shaky answer points at a fork you memorized instead of understood.

## Design Practice Backlog

Specific systems to design end-to-end (drive the full framework on each). **This is the Sunday queue** — designs pull the blocks in behind them (see Cadence). Ordered easiest-framework-rep first, so the *framework* is what's being drilled early, not the exotica.

| # | System | Tier | Blocks it will pull in |
|---|--------|------|------------------------|
| 1 | **URL shortener** | 1 | hashing/encoding, KV store, cache-aside, read-heavy scaling. *The canonical first design — small enough that the **framework** is the thing you're practicing.* |
| 2 | **Chat / messenger** | 1 | WebSockets, **message queues**, fan-out, presence, delivery/read receipts |
| 3 | **News feed** | 1 | **push vs pull fan-out** (the celebrity problem), CDN, ranking |
| 4 | **Typeahead / autocomplete** | 1 | tries (← DSA 208!), **caching**, top-K |
| 5 | **Design YouTube** | 1 | upload/transcoding pipeline, **CDN**, metadata + view counts, recommendations |
| 6 | **Design an LLM chat assistant** (Claude/ChatGPT-style) | 1–2 | token streaming (SSE/WebSocket), context-window mgmt, request batching / GPU scheduling, **rate limiting** & quotas, conversation storage, optional RAG. Ties into the planned AI-Engineering phase. |

Remaining canonical set to slot in later: notification service, web crawler, ride-share (Uber), file storage (Dropbox), Ticketmaster, distributed KV store, payment/ledger, top-K/trending.

### Building blocks — pulled in on demand

Not a queue to grind through. Each gets a `components/` note **when a design hits it**, or when it's the obvious next gap.

| Block | Status |
|-------|--------|
| [Rate limiter](components/rate_limiter.md) | Mastery ⏳ Sun Jul 19 |
| Caching (patterns, eviction, invalidation) | Bootstrap ⏳ Jul 20 wk — *the one block to do proactively; it's load-bearing everywhere* |
| Message queues & async | pulled by **Chat** (#2) |
| CDN / reverse proxy / API gateway | pulled by **News feed** (#3) / **YouTube** (#5) |
| Load balancing | pulled by whichever design saturates first |
| Consistent hashing · Bloom filters | small; fold into the design that needs them |

## Where things live

This guide is the single source of truth (map + ROI line). Current file state — **built** vs **planned**:

**Built:**
- `fundamentals/` ✅ — [`single_node_io_efficiency.md`](fundamentals/single_node_io_efficiency.md) (the 4096-byte buffer / sectors / pages / syscalls). *Depth material, not interview-core.*
- `templates/` ✅ — the two scaffolds you fill during practice (see Cadence above).

- `components/` 🌱 — per-block deep-dives, started: [`rate_limiter.md`](components/rate_limiter.md) (Transition ✅ — carries the named drill targets for Mastery). Grows as you cover each block.

**Planned (not yet created — build as you reach each phase, no number prefixes):**
- `databases/` — SQL vs NoSQL, replication, sharding
- `case_studies/` — worked canonical designs (start from the templates)
