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

## Cadence

System design runs **twice a week** (`cse.config.yml` `system_design.cadence:
twice_weekly`): the deep **Sunday sprint** plus **one midweek SD slot** — a
once-a-week touch is too weak to build a real sticking point. The midweek slot is a
warmup swap on a lighter DSA day and never cuts the 45-min DSA active block.
Interview-core work (Tier 1) happens in staged form:

- **Bootstrap** — first exposure to a topic: watch a good explainer, recall from memory, check gaps. No cold whiteboarding yet.
- **Transition** — sketch the design cold from memory, then **diff against the reference note**. Record what came back and what didn't; the misses become the named drill targets for Mastery.
- **Mastery** — full mock-interview timing (~45 min), self-scored against the framework, drilling the Transition misses.

One stage per session, so a full Bootstrap → Transition → Mastery arc is ~3 sessions ≈ 1.5 weeks at twice-weekly.

### Stage status

| Topic | Bootstrap | Transition | Mastery |
|-------|-----------|------------|---------|
| [Rate limiter](components/rate_limiter.md) | ✅ Jul 5 | ✅ Jul 12 | ⏳ next up |

Below-the-line (Tier 2+) work is **not** a sprint activity — it's long-form reading (DDIA, papers) pursued deliberately *after* interview-core is solid, on its own track.

### Technology fluency (spaced repetition)

Designs are argued in the vocabulary of concrete **technologies** ("I'd put Redis here, Kafka there"). Those are drilled the same way as DSA — active recall, comfort rating, auto-scheduled review — tracked in [`mastery/design_progress.md`](mastery/design_progress.md), driven by the same `scripts/update_review_dates.py` and pre-commit hook.

- **The unit:** one technology, with a note + **Recall Card** in [`technologies/`](technologies/).
- **The rep (a "blind sprint"):** answer the card's prompts from memory → unfold to check → rate 🟢/🟡/🔴 → log + commit → next review auto-computes (+30/+10/+2).
- **Backlog & order** (data-store trio is highest-leverage): Redis ✅ · PostgreSQL → Cassandra → DynamoDB · Kafka → Flink · Elasticsearch · API Gateway · ZooKeeper.

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

Specific systems to design end-to-end (drive the full framework on each). Above the ROI line unless noted.

| System | Tier | Notes |
|--------|------|-------|
| **Design YouTube** | 1 (interview core) | Video upload/transcoding pipeline, CDN delivery, metadata + view counts, recommendations. Already named in the canonical list — make it an explicit mock. |
| **Design an LLM chat assistant (Claude/ChatGPT-style)** | 1–2 | AI-serving: token streaming (SSE/WebSocket), context-window management, request batching / GPU scheduling, rate limiting & quotas, conversation storage, optional RAG. Ties into the planned AI-Engineering phase. |

## Where things live

This guide is the single source of truth (map + ROI line). Current file state — **built** vs **planned**:

**Built:**
- `fundamentals/` ✅ — [`single_node_io_efficiency.md`](fundamentals/single_node_io_efficiency.md) (the 4096-byte buffer / sectors / pages / syscalls). *Depth material, not interview-core.*
- `templates/` ✅ — the two scaffolds you fill during practice (see Cadence above).

- `components/` 🌱 — per-block deep-dives, started: [`rate_limiter.md`](components/rate_limiter.md) (Transition ✅ — carries the named drill targets for Mastery). Grows as you cover each block.

**Planned (not yet created — build as you reach each phase, no number prefixes):**
- `databases/` — SQL vs NoSQL, replication, sharding
- `case_studies/` — worked canonical designs (start from the templates)
