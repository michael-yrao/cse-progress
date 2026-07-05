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

System design runs on the **Sunday sprint** (see the weekly schedule). Interview-core work (Tier 1) happens there in staged form:

- **Bootstrap** — first exposure to a topic: watch a good explainer, recall from memory, check gaps. No cold whiteboarding yet.
- **Transition** — sketch the design cold on paper, then compare against reference.
- **Mastery** — full mock-interview timing (~45 min), self-scored against the framework.

Below-the-line (Tier 2+) work is **not** a Sunday-sprint activity — it's long-form reading (DDIA, papers) pursued deliberately *after* interview-core is solid, on its own track.

## Design Practice Backlog

Specific systems to design end-to-end (drive the full framework on each). Above the ROI line unless noted.

| System | Tier | Notes |
|--------|------|-------|
| **Design YouTube** | 1 (interview core) | Video upload/transcoding pipeline, CDN delivery, metadata + view counts, recommendations. Already named in the canonical list — make it an explicit mock. |
| **Design an LLM chat assistant (Claude/ChatGPT-style)** | 1–2 | AI-serving: token streaming (SSE/WebSocket), context-window management, request batching / GPU scheduling, rate limiting & quotas, conversation storage, optional RAG. Ties into the planned AI-Engineering phase. |

## Where things live

- `01_fundamentals/`, `02_components/`, `03_databases/` — Tier 1 concept notes
- `04_case_studies/` — worked canonical designs
- `05_architectural_templates/` — blank templates to drive the framework during practice
- This guide — the map and the ROI line
