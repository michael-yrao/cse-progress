# System Design Study Guide — Interview Core → Architect Depth

> **📍 Overarching career goal & apply strategy → [`../career_strategy.md`](../career_strategy.md).**
> SD *execution roadmap* (phases, rubric, sourcing, tech order) → [`senior_ramp.md`](senior_ramp.md).
> This guide is the SD study *mechanics*; those two own the goal and the plan.

## 🧭 Who owns what — read this before editing any SD file

**Reconciled Aug 8, 2026.** Three files had drifted into holding three different design lists, two stale
status tables, and a claim in this file that it was *"the single source of truth"* — which it no longer is.
Each thing now has exactly one owner, and everything else **links** rather than restates:

| Thing | Owner | Everyone else |
|---|---|---|
| **State** — comfort, streak, next review, for every tech · concept · component · design | [`mastery/design_progress.md`](mastery/design_progress.md) | link to it; never restate a status in prose |
| **The plan** — L6 ROI triage of all 55 designs, phases + exit gates, the 7-point rubric, tech order, prereq-tech gate | [`senior_ramp.md`](senior_ramp.md) | link to it; never keep a second design list |
| **The mechanics** — cadence & the three lanes, session formats, the framework, fork drills, template usage | **this file** | — |

⚠️ **A status written in prose is a status that will be wrong in three weeks.** Every stale thing found in
this reconciliation was a hand-written date or ✅ duplicating something the tracker already computes
(*"Mastery ⏳ Sun Jul 19"*, *"Bootstrap ⏳ Jul 20 wk"*, *"Redis ✅"* on a row that is 🟡). **If the engine
can compute it, do not write it down here.**

## Mission & the Interview-ROI Line

**End goal:** become a genuine systems **architect** (Staff / Principal / CTO-level) — someone who can design, reason about, and defend planet-scale distributed systems from first principles. **Passing the system-design interview is a milestone on that path, not the finish line.**

As with DSA, depth has diminishing returns *for interviews specifically*, so everything is sorted around one marker:

> **The Interview-ROI Line** — the point past which added systems depth stops improving interview performance and becomes real-world architect mastery.

**Above the line — Interview Core (Tier 1). Do this first; it's the whole SD-interview surface.**

1. **Fundamentals & estimation** — latency numbers every engineer should know, back-of-envelope math (QPS, storage, bandwidth), vertical vs horizontal scaling.
2. **Building blocks** — load balancing, caching (patterns, eviction, invalidation), CDN, reverse proxy / API gateway, message queues & async processing, rate limiting, consistent hashing, bloom filters.
3. **Data layer** — SQL vs NoSQL tradeoffs, indexing, replication (leader/follower, multi-leader), sharding / partitioning, CAP & PACELC, consistency levels (strong → eventual), idempotency.
4. **The interview framework** — requirements (functional + non-functional) → core entities → API design → high-level diagram → deep dives (bottlenecks & tradeoffs); estimation inline, Data Flow only for data-processing systems. *Driving this framework fluently is 50% of the interview.* **→ Full step-by-step: [`framework.md`](framework.md).**
5. **Canonical designs** — **owned by [`senior_ramp.md`](senior_ramp.md) → *The L6 Interview-ROI Line***,
   where all 55 systemdesign.io questions are triaged (20 core · 10 ⏳ Tier-1 · 25 below the line), each
   with a written reason. *The old hand-listed "grokking set" was removed here Aug 8, 2026 — it was a
   second, unmaintained design list, and it disagreed with the triage (it named Ticketmaster,
   Uber and payment/ledger as core; the L6 triage does not).*

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
| **Fuller midweek** — swaps **both warmups** (~30 min) | **② Building blocks & probes** — write the `components/` note for whatever block the last design **hit cold**; then fire framework probe questions at a system already designed. **Pull queue empty → drill a `concepts/` card instead** (see below) | ~30 min | **the pull queue**, falling back to **concepts** (see below) |
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

### The concepts lane — lane ②'s fallback ⭐

**Added Jul 25, 2026.** The pull model catches **blocks** but structurally cannot catch **concepts.** A
block is a box on the diagram — you notice when it's missing. A *concept* (Zipf, Little's Law, quorum
math) is a fact you need mid-sentence to justify a number, so the gap only surfaces *after* you're
already stuck. `concepts/` was, accordingly, an **ambush log**: it held exactly the two things that had
already blindsided a session.

**The rule:** when lane ② has **no cold-hit block queued**, it drills a `concepts/` card instead of
idling — same blind-sprint format as lane ①. This gives concepts a lane without adding a slot.

**Reading order** (front-loaded Jul 25 — the six with no natural design trigger):

1. [Percentiles & tail latency](concepts/percentiles_and_tail_latency.md) — p99, fan-out amplification
2. [Little's Law](concepts/littles_law.md) — `L = λW`, pool sizing, bottleneck-finding
3. [Utilization & queueing](concepts/utilization_and_queueing.md) — the `1/(1−ρ)` curve, why 70%
4. [Probabilistic sketches](concepts/probabilistic_sketches.md) — HyperLogLog + Count-Min (Bloom's siblings)
5. [Retry storms & stampedes](concepts/retry_storms_and_stampedes.md) — backoff, jitter, metastable failure
6. [Quorum math](concepts/quorum_math.md) — `R + W > N`

**Deliberately *not* front-loaded** — these have a real design trigger, so let the pull queue work:
WebSocket vs SSE vs polling (→ chat), birthday paradox / base62 / Snowflake IDs (→ URL shortener),
vector clocks & clock skew (→ distributed KV), LSM vs B-tree (→ the Postgres and Cassandra cards).

Each card leads with a **"You'll want this when…"** trigger line, so it also works as a symptom-indexed
lookup when a design ambushes you — you don't have to have read it in advance for it to pay off.

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

**→ [`mastery/design_progress.md`](mastery/design_progress.md).** *The hand-maintained table that used to
sit here was deleted Aug 8, 2026: it still read "Rate limiter — Mastery ⏳ Sun Jul 19" and "Caching —
Bootstrap ⏳ Jul 20 wk", three weeks stale, while the tracker had the real state all along. The staged arc
above (Bootstrap → Transition → Mastery) is still how a block or design is worked; **the comfort rating is
how its state is recorded**, and nothing should record it twice.*

Below-the-line (Tier 2+) work is **not** a sprint activity — it's long-form reading (DDIA, papers) pursued deliberately *after* interview-core is solid, on its own track.

### Technology fluency (spaced repetition)

Designs are argued in the vocabulary of concrete **technologies** ("I'd put Redis here, Kafka there"). Those are drilled the same way as DSA — active recall, comfort rating, auto-scheduled review — tracked in [`mastery/design_progress.md`](mastery/design_progress.md), driven by the same `scripts/update_review_dates.py` and pre-commit hook.

- **The unit:** one technology, with a note + **Recall Card** in [`technologies/`](technologies/).
- **The rep (a "blind sprint"):** answer the card's prompts from memory → unfold to check → rate 🟢/🟡/🔴 → log + commit → next review auto-computes (+30/+10/+2).
- **Backlog & order** (data-store trio is highest-leverage): **Redis → PostgreSQL → Cassandra → DynamoDB ·
  Kafka → Flink · Elasticsearch · API Gateway · ZooKeeper.** Live comfort per tech is in the
  [tracker](mastery/design_progress.md) — *the "Redis ✅" that used to be written here was wrong; Redis is
  🟡 and its next slot is a **teach**, not a sprint.*
- ⚠️ **7 of the 9 have a tracker row but no note file yet** — only `redis.md` and `postgresql.md` exist. A
  row without a note **cannot be drilled**; that tech's first slot builds the note (teaching, unrated) and
  the sprint comes later. Read "9 techs queued" as *2 drillable, 7 unwritten*.
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

## Design Practice Backlog → moved

**The Sunday queue is [`mastery/design_progress.md`](mastery/design_progress.md); its ordering and ROI
triage are [`senior_ramp.md`](senior_ramp.md).** The hand-numbered 6-row table that used to sit here was
removed Aug 8, 2026 — it was the **third** competing design list in the repo, it had no state (the tracker
has comfort/streak/dates), and it predated the systemdesign.io sourcing decision of Aug 6.

**One item from it was NOT in the triage and is preserved here so it isn't lost** (schedule-integrity rule
— nothing gets dropped without a home):

- ⏳ **Design an LLM chat assistant** (Claude/ChatGPT-style) — token streaming (SSE/WebSocket),
  context-window management, request batching / GPU scheduling, rate limiting & quotas, conversation
  storage, optional RAG. **Not a systemdesign.io question**, so the catalog triage could not place it.
  **Trigger: `phase:ai_bootstrap`** — it belongs to the AI-Engineering track (not yet bootstrapped), where
  it is the natural capstone design. Until then it is genuinely parked, not forgotten.
  *(Second design with no catalog home: **distributed cache** — see `senior_ramp.md`.)*

### Building blocks — pulled in on demand

Not a queue to grind through. Each gets a `components/` note **when a design hits it**, or when it's the
obvious next gap.

⚠️ **Blocks were the last SD category with no measurement** — notes existed, none were on the review
engine, so they could not decay and nothing surfaced when one went cold. **Fixed Aug 8, 2026: a block gets
a `Component` row in the tracker the moment its note exists.** Status lives there, not here.

| Block | Note | Pulled by |
|-------|------|-----------|
| [Rate limiter](components/rate_limiter.md) | ✅ | tracked as a **design** too (`API Rate Limiter`, 🟡) — the component note carries that arc's drill targets |
| [Caching](components/caching.md) | ✅ | *done proactively* — load-bearing everywhere |
| [Load balancer](components/load_balancer.md) | ✅ | ⚠️ **2 backend failure modes still owed** (dead vs slow → health checks), from the Aug 6 close-out |
| Message queues & async | — | Chat / Messenger |
| CDN / reverse proxy / API gateway | — | News feed · YouTube *(API Gateway is also a tracked **technology** row — the block note and the tech sprint are different reps)* |
| Consistent hashing · Bloom filters | *(Bloom filter has a [concept card](concepts/bloom_filter.md))* | fold into the design that needs them |

## Where things live

**This guide owns the *mechanics*, not the plan or the state** — see *Who owns what* at the top.
Current file state:

**The three owners**
- [`mastery/design_progress.md`](mastery/design_progress.md) ✅ — **state.** Every tech · concept ·
  component · design, with comfort/streak/next-review, plus the ⏳ Tier-1 Waiting Room.
- [`senior_ramp.md`](senior_ramp.md) ✅ — **the plan.** The **L6** ramp (big tech / MANGA-adjacent, ~10 yrs
  in): the ROI triage of all 55 systemdesign.io questions, phases + exit gates, the 7-point rubric, tech
  order, the prereq-tech gate, and the 🔁 overflow block. *(Called "the L5 ramp" here until Aug 8 — stale
  since the Aug 6 re-aim.)*
- **this file** ✅ — **the mechanics.** Cadence & the three lanes, session formats, fork drills, templates.

**Material**
- [`framework.md`](framework.md) ✅ — the delivery framework, step by step. Reread before any
  Transition/Mastery sprint.
- `templates/` ✅ — the two scaffolds you fill during practice (see Cadence above).
- `technologies/` 🌱 — **2 of 9 written**: [`redis.md`](technologies/redis.md) ·
  [`postgresql.md`](technologies/postgresql.md). The other seven rows have no note yet (see *Technology
  fluency* above).
- `components/` 🌱 — **3 written**: [`rate_limiter.md`](components/rate_limiter.md) ·
  [`caching.md`](components/caching.md) · [`load_balancer.md`](components/load_balancer.md).
- `concepts/` 🌱 — **9 written, and the one lane that is fully ready to run** (9 rows, 9 files, exact
  match): networking basics · percentiles & tail latency · Little's Law · utilization & queueing ·
  probabilistic sketches · retry storms & stampedes · quorum math · Zipfian · Bloom filter.
- `case_studies/` 🌱 — [`url_shortener.md`](case_studies/url_shortener.md) (in flight).
- `archive/` — retired depth material: [`fundamentals/single_node_io_efficiency.md`](archive/fundamentals/single_node_io_efficiency.md). *Depth material, not interview-core — archived Jul 22.*

**Planned:** `databases/` — SQL vs NoSQL, replication, sharding *(may end up folded into the per-technology
notes instead; decide when Cassandra's note is built rather than creating an empty directory)*.

> ⚠️ **Counts in this section are the one place a stale number is tolerable** — they are a *map*, not a
> status, and they are cheap to re-derive with `ls`. Everything that is a **status** (comfort, stage,
> "next", ✅ done) belongs in the tracker. That distinction is what this reconciliation was about.
