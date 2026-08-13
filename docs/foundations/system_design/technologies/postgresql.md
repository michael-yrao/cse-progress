# PostgreSQL

> 🧊 **Frozen reference (Aug 13, 2026).** The SD track is now mock interviews on HelloInterview's
> board; this card is no longer drilled and has no tracker row. Any "owed a sprint / next lane"
> language below is historical. Use it as lookup when a mock debrief points here.
> See [`../study_guide.md`](../study_guide.md).

**Role:** SQL DB — the default primary datastore.
**Status:** teaching session Jul 28, 2026 (unrated). First blind sprint due later — see
[`design_progress.md`](../mastery/design_progress.md).

---

## The spine (three facts everything else derives from)

**1. It answers questions about data you can't name the key for.**
Redis finds things by a key you already know. Postgres filters, joins, aggregates and sorts —
*"all URLs created by user 42 last week"* is one query here and impossible there. That capability is
what an index and a query planner buy you, and it's the whole reason a cache never replaces a database.

**2. It promises transactions: a group of writes is all-or-nothing, and once committed it survives a
crash.**
The derivation: transfer $100 from A to B is two writes — subtract from A, add to B. Lose power
between them and $100 has vanished from the world. Atomicity says both or neither ever happened;
durability says once you got the "committed" back, a crash cannot take it away.

**3. Writes go through one machine.**
This is the limit, and it's where every Postgres scaling conversation starts. Reads scale out easily;
writes do not. See *Where it breaks*, below.

---

## ACID, in one line each

| | What it promises | What breaks without it |
|---|---|---|
| **A**tomicity | all writes in a transaction, or none | half a money transfer |
| **C**onsistency | the DB moves between valid states; constraints hold | an order pointing at a customer that doesn't exist |
| **I**solation | concurrent transactions don't see each other's partial work | two people book the last seat |
| **D**urability | once committed, it survives a crash | "payment confirmed", then a reboot eats it |

**Isolation is the one interviewers actually probe**, because it has *levels* and the default is not the
strictest. Postgres defaults to **Read Committed**; you can ask for **Repeatable Read** or
**Serializable**, and each step up costs throughput. Knowing the default is Read Committed — not
Serializable — is a good senior tell.

---

## Where it breaks (the qualify half — say this before you're asked)

**Reads break first, and reads are the easy problem.** At 100k reads / 1k writes per second on one box:

1. **Cache the hot set** (Redis). URL-shortener reads are Zipfian, so a small hot set covers most
   traffic. But a cache never takes 100% — at a 95% hit rate you still land 5k reads/sec on the DB,
   plus every cold key and everything after a cache restart.
2. **Primary + read replicas** (streaming replication). Leader takes writes, followers serve reads.
   This is the read half of "horizontal scaling" — keep it distinct from sharding, which is the
   *write* half and is a different, much more painful conversation.

### The replica tradeoff — replication lag

A follower can be behind the leader, so a read can be stale.

> ⚠️ **The trap:** *"it's fine because writes are infrequent."* **Wrong reason.** The dangerous moment
> isn't when writes are frequent, it's **immediately after a write** — and that moment exists no matter
> how rare writes are. The user who just created a short link and loaded their dashboard one second
> later is exactly the request most likely to hit a stale replica. Rarity changes how *often* it
> happens, never *whether* it happens to the person who just wrote.

The two reasons it's actually acceptable here, both quantified:

- **Lag is small** — single-digit milliseconds on healthy streaming replication.
- **The consequence is mild** — a just-created link 404s briefly. Nobody loses money. Same lag on a
  payment balance would be unacceptable.

**The fix when you do need it: read-your-own-writes.** Pin that user's reads to the primary for a few
seconds after their write. Costs a little primary load, buys the one case that matters.

#### Read-your-own-writes, in detail

Two things people get wrong when describing it:

- **It's per-user, not global.** Only the user who just wrote is rerouted; everyone else stays on
  replicas. That's what makes it cheap — "users who wrote in the last few seconds" is a tiny set, so
  the primary takes a rounding error of extra load rather than all of it.
- **You can't wait for "sync to finish."** Replication is continuous and never "done." The answerable
  question is narrower: *has **this** write reached the replica yet?*

| Approach | How | Cost |
|---|---|---|
| **Time-based** *(what most systems do)* | after a write, flag the user (cookie / session / Redis key with TTL); route their reads to the primary for N seconds, N > observed p99 replication lag | wrong if lag spikes past N |
| **Position-based** *(precise)* | commit returns the write's **LSN** (write-ahead log position); store it in the session; only read from a replica whose applied LSN ≥ that value, else primary | replication internals leak into the app layer |

**Vocabulary worth having:** read-your-own-writes is one of a family of **session guarantees**. The
sibling is **monotonic reads** — you never see time run backwards — which breaks when consecutive reads
land on replicas with different lag. An interviewer going deep on staleness is usually fishing for
these two names.

### The fusion sentence (practice saying this cold)

> *"Reads go to replicas because we're 100:1 read-heavy. That trades strong consistency for read
> throughput, and it holds because replication lag is single-digit ms and a briefly-stale redirect is
> harmless. It breaks for read-your-own-writes right after creation — there I'd pin that user's reads
> to the primary for a few seconds."*

Four parts: **choice · quantified pressure · what it trades + the condition it holds under · where it
breaks + the alternative.** That shape works for every design decision, not just this one.

---

## Why Postgres and not another RDBMS?

**1. The interviewer is grading "relational vs not," almost never "Postgres vs MySQL."**
The decision carrying signal is *do you need transactions, joins, and a rigid schema?* Defending
Postgres over MySQL answers a question nobody asked. Pick one, justify in a sentence, move on.

**2. It absorbs adjacent needs, which lets you defer a second datastore.**

| Need | Postgres feature | System you don't have to add yet |
|---|---|---|
| semi-structured docs | **JSONB** | MongoDB |
| text search | built-in full-text search | Elasticsearch |
| geospatial | **PostGIS** (the standard) | a specialized geo store |
| lists / ranges in a column | array & range types | a join table |

This plays well in a design interview: *"metadata as JSONB in Postgres for now, pulled out into a
document store if the access pattern justifies it"* beats reaching for a second system on slide one.

**3. Where it genuinely loses.**
- **Sharding maturity** — MySQL has **Vitess** (sharded MySQL running YouTube and Slack). There is no
  Postgres equivalent of the same maturity.
- **Process-per-connection** — you need a pooler (**PgBouncer**) far earlier than you'd expect.
- **Vacuum / bloat** — a real operational burden at scale, falling out of its MVCC design.

> **The one-liner:** *Postgres by default because it's correct, does more out of the box, and defers
> other systems. MySQL if the org already runs it, or if you know sharding is coming.*

---

## Writes — the real ceiling *(not yet covered; owed to the Aug 3 week)*

Writes go through one machine. Vertical scaling, then partitioning, then sharding — each a step
change in operational pain. This is where "just use Postgres" eventually stops being the answer.

**Also owed here: the MVCC thread.** It's the mechanism behind both nice-Postgres (readers never block
writers) and annoying-Postgres (vacuum, bloat). Deliberately held for this session rather than the read
half, because bloat is a write-path problem and belongs next to sharding.

---

## Recall Card

*(to be written once the note is complete — the blind-sprint rep is answering these cold)*
