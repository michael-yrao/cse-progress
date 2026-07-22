# Redis

> **Role:** Cache / shared in-memory state · **Rival on the fork:** Memcached
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check. Rate 🟢/🟡/🔴 and log in [`../mastery/design_progress.md`](../mastery/design_progress.md).

## 🦴 The spine — everything else derives from this
> **Redis is a dictionary that lives on another computer.**

Three facts. Every other thing on this page is a consequence of one of them.

| Fact | What you get | What it costs |
|---|---|---|
| It's a **dictionary** | O(1) lookup, dead simple | key lookup *only* — no queries, no search. **You index at write time.** |
| It's on **another computer** | every app instance shares it ← *the whole reason it exists* | every op is a **network round trip** |
| It does **one thing at a time** | commands can't race → `INCR` is atomic, no locks | one slow command **stalls every client** |

Everything below (TTL, pipelining, `MGET`, `SCAN`, sharding) is just **tactics for living with those three facts.** If a mechanism doesn't obviously trace back to one of them, you haven't understood it yet.

## 🎯 In one line
Redis (**RE**mote **DI**ctionary **S**erver) is a **shared, in-RAM dictionary** running as its own server that every app instance talks to over the network. Single-threaded execution makes its operations **atomic**; every key can carry a **TTL**. That's exactly why it's the counter store for a [rate limiter](../components/rate_limiter.md).

## 🎯 Recall log — blind sprints

**Jul 21, 2026 — rated blind sprint → 🟡 Shaky** (~6 of 11 clean + card 7 essentially there; +10 → Jul 31). Big jump from Jul 19's 🔴. **Clean cold:** 1, 2, 3, 5, 6 (more detailed than the note — AOF replay-cost vs RDB), and **4 with ZERO token-bucket fusion** — the 3×-fused key finally clean. **The two never-recalled targets (5, 6) came back.** **Three real gaps remain:**
- **Card 9 — scaling inverted.** Said "can't scale horizontally nor vertically." Wrong half: single-threaded ⇒ can't scale **up** (vertical), but you **do** scale **out** (horizontal — sharding / Redis Cluster + read replicas). Scaling out *is* the escape hatch. Got the other two costs (slow-command-blocks-all; network-bound-not-CPU-bound).
- **Card 8 — type right, "how" missing.** ZSet correct, but the mechanism is the **score**: leaderboard = points; sliding window = request **timestamp**, drop entries older than the window. Recalled "ordering + uniqueness" (the *what*), not the *how*.
- **Card 11 — footgun missed.** Had "not alternatives / both run at once." Missed the `volatile-*`-only-evicts-keyed-with-TTL footgun (immortal untTL'd key → Redis refuses writes while full of junk). Also had to be told what "footgun" means.
- **Card 7 — concept solid, name it.** Whole answer was about handling Redis down + correct fail-open/closed split + leader/follower failover — but never said the words **single point of failure (SPOF)**. Name the risk before the mitigations. (Contrast Jul 19, where the *parse* of "request path" was itself the blocker — that's fully resolved.)
- **Next drill targets (Jul 31):** 9 (scale out ≠ up), 8 (the score-is-the-mechanism "how"), 11 (the volatile-* footgun).

**Jul 19, 2026 — rated blind sprint → 🔴 Blank** (~4 of 11 cold; +2 → Jul 21). Stronger 🔴 than Jul 13. **Solid, cold:** card 2 (why shared/global count), card 3 **atomicity** (the #1 Jul-13 gap — now reflexive), card 1 & 10 (name + remote-vs-in-RAM). **Missed:** cards 5 (right/wrong tool), 8 (ZSet leaderboard/sliding-window), 9 (three costs of single-threaded), 4 & 11 partial.
- **Root unlock for the failure-modes gap (card 7):** it wasn't the *content* — the learner couldn't parse the phrase **"on the request path."** Once defined (a mandatory synchronous stop for every request → its failure is total/immediate → SPOF), the SPOF→replication+fail-open/closed chain followed. If card 7 blanks again, check phrase-parsing first, not the mitigation list.
- **TTL vs token-bucket fused a 3rd time (card 4).** Fix that stuck this session: **"window" is a fixed-window word → TTL/`EXPIRE` deletes the key; "refill / smooth / burst" → token bucket.** Sawtooth vs continuous trickle.
- **fail-open/closed nuance corrected:** brute-force/login = clean fail-**closed**; **DDoS is NOT** — failing closed completes the attacker's denial-of-service, and DDoS is usually absorbed at the edge (CDN/WAF), not app-Redis. Dividing line: fail-closed when leaking is worse than denying (login, payments); fail-open when the limiter causing an outage is the bigger harm.
- **Terminology:** use **leader/follower** (or primary/replica), not master/slave.
- **Next drill targets (Jul 21):** cards 5, 8, 9 (never recalled) + the two stubborn ones (4 TTL-mechanism, 11 volatile-* footgun).

**Jul 15, 2026 — derive-the-design session (unrated, teaching).** Derived the full chain cold from constraints: N-server undercount → shared remote store → naive `GET`/`SET` race → atomic `INCR` → single-threaded → TTL reset → fail-open/closed policy. Big step from Jul 13. **Still sticky, drill before the Jul 19 rated sprint:** (1) **atomicity is fragile under full narration** — solid when isolated, dropped out when chaining the whole story, recovered only on a targeted re-ask; (2) **TTL vs token bucket re-fused ×2 in one session** — kept reaching for token-bucket to explain the window reset; the reset is *TTL/`EXPIRE`*, token bucket is a different algorithm with no role in this design. Also clarified: RDBMS (ACID, transaction+rollback) atomicity vs Redis single-command atomicity (really isolation, free from single-threading), and that "database" = *persistence*, not atomicity.

**Jul 13, 2026 — first blind sprint → 🔴 Blank** (3 of 8 prompts attempted).

**Came back cold (the hard part — solid):** the *why-shared-state* argument — horizontally-scaled middleware each has its own memory, so a per-instance counter is bypassed; Redis holds the **global** count.

**Drill targets — these did NOT come back.** Restudy focuses here:

| # | Gap | The thing to be able to say |
|---|-----|------------------------------|
| 1 | **Atomicity** ⚠️ *biggest* | Never mentioned. Redis is **single-threaded** → `INCR` is one atomic read-modify-write, so two concurrent requests can't both read the same count and both pass. This is *the* follow-up the instant you say "Redis." |
| 2 | **TTL vs token bucket** *(crossed wires)* | Asked how the window resets, reached for the *token-bucket refill*. Two different layers: **token bucket = the middleware's algorithm; `EXPIRE`/TTL = the Redis mechanism** that self-destructs the key so the next `INCR` starts fresh. Don't fuse them. |
| 3 | **Failure modes** | Blank. Redis on the request path is a **single point of failure** → mitigate with **replication** (follower failover) + a **fail-open vs fail-closed** policy when it's unreachable. |

**Precision fix (Q1):** "shared cache" undersells it — say **in-RAM dictionary on its own server**, and the name is **RE**mote **DI**ctionary **S**erver.

**Naming trap (asked Jul 13):** *"remote"* is not the opposite of *in-RAM* — it's the opposite of **in-process**. Two orthogonal axes: **in-memory** = what medium holds the bytes (RAM, not disk); **remote** = whose address space and how you reach it (a socket, not a pointer). A Python dict is in-memory *and local*. Redis is in-memory *and remote* — **someone else's RAM, over the wire**. That's the whole point: state all instances can see cannot live inside any one of them. Corollary: **every op is a network call**, which is why pipelining / `MGET` / Lua exist (amortize the round trip) and why a 1,000-`GET` loop costs 1,000 hops, not 1,000 ns.

## 🧠 The core idea
It's `{key: value}` — but instead of living inside one process (like a Python dict), it lives in a **separate server** every machine can reach.

```
Your Python dict:              Redis:
lives in ONE process           lives in its OWN server
dies on restart                can persist to disk
only THAT process sees it      EVERY app instance sees it   ← the whole point
```

That last line is why Redis exists in a rate limiter: horizontally-scaled middleware each has its *own* memory, so a per-instance counter gets bypassed (3 instances → 3× the limit). Redis is the **one shared dictionary** all instances read/write, so the count is **global**.

## ⚡ Why "in-memory" is the headline
All data lives in **RAM**, not disk — the defining trade:

| | RAM (Redis) | Disk (Postgres) |
|---|---|---|
| Speed | ~microseconds | ~milliseconds (1000×) |
| Capacity | GBs | TBs |
| Survives power loss | no (by default) | yes |

**Reusable instinct:** reach for Redis whenever you need *shared, mutable state that's touched very frequently and doesn't need perfect durability* — counters, sessions, caches, leaderboards, rate limits.

## 🔒 Atomicity — the key mechanism
Redis is **single-threaded**: one thread runs commands to completion, one at a time. No two commands interleave. So `INCR` (read-modify-write in one step) can't race:

```
BROKEN (read + write as 2 steps):        CORRECT (INCR atomic):
A: read 4 ┐ both see 4                    A: INCR → 5   (all one step)
B: read 4 ┘ both pass                     B: INCR → 6   (can't start till A done
A: write 5                                              → sees 5 → over limit → reject)
B: write 5   → 2 admitted, +1 only
```

`INCR` returns the *new* value; the middleware checks that against the limit. **"Consume a token AND check" = `INCR`.** This is the standard follow-up the instant you say "Redis."

### What single-threaded *costs* (the other half — say both)
Atomicity is what you buy; here's the bill. Volunteering it is the senior signal.

- **Why it isn't the bottleneck you'd expect:** Redis is **not CPU-bound** — a RAM hash lookup is nanoseconds. It's bound by **network I/O**. The one thread is mostly idle on sockets, and multiplexes thousands of connections with epoll (no thread-per-connection). ~100k ops/sec on one core.
- **One slow command blocks *everyone*.** `KEYS *` on a million keys, or `ZRANGE huge 0 -1`, stalls every other client behind it. This is *the* classic Redis prod incident — hence "never run `KEYS` in prod."
- **Scale out, not up.** More cores don't help one instance. You add **instances** (sharding / Redis Cluster) or **replicas** for reads.
- **Footnote for accuracy:** modern Redis uses extra threads for socket I/O and lazy-freeing big objects. **Command execution is still one thread** — the invariant that buys atomicity is intact.

## ⏳ TTL / expiry — and how it differs from eviction
Any key can auto-delete: `EXPIRE key 60` or `SET key val EX 60`. For a fixed-window limiter this *is* the window — `INCR` the key, `EXPIRE` it 60s; it self-destructs and the next request starts fresh. No cleanup job.

### TTL vs LRU eviction — two different questions (asked Jul 14)
They are **not alternatives**; both run at once.

| | **TTL (expiry)** | **LRU (eviction)** |
|---|---|---|
| Question it answers | *"When should this key die **on purpose**?"* | *"I'm **out of RAM** — who dies **against their will**?"* |
| Scope | one key, chosen by **you** at write time | whichever key **Redis** picks, under memory pressure |
| How you set it | `EXPIRE` / `SET ... EX` per key | config: `maxmemory 2gb` + `maxmemory-policy allkeys-lru` |

**LRU is not something you implement for Redis** — it's a config knob, built in. (Contrast **LC 146 LRU Cache**, where *you* build it from a hashmap + doubly-linked list. Redis already did that internally; same idea, opposite side of the API.)

**Where they touch — and the footgun.** Policies split into `allkeys-*` and `volatile-*`. The **`volatile-*` policies only evict keys that have a TTL set.** So under `volatile-lru`, a key with **no** TTL is *immortal* no matter how cold it gets → Redis fills up and starts **refusing writes** while full of junk it isn't allowed to touch. Classic prod incident.

Policies worth naming: `noeviction` (default — writes error out when full), `allkeys-lru`, `allkeys-lfu` (frequency, not recency — better for skewed access), `volatile-ttl` (evict nearest-expiry first).

**Precision note:** Redis's LRU is **approximate** — it samples a few keys (default 5) and evicts the oldest *of the sample*. True LRU would need a pointer per key; the memory overhead isn't worth it. Same for LFU. Knowing it's sampled, not exact, is a nice "why."

## 🧰 Data types (why it's more than a dict)
Values can be whole structures, each with atomic ops:

| Type | What | Classic use |
|---|---|---|
| String / int | value or counter | rate-limit counters (`INCR`), cached JSON |
| Hash | dict inside a key | store an object's fields |
| List | push/pop both ends | simple queues |
| Set | unique members | dedup, "seen?" checks |
| **Sorted Set (ZSet)** | members ordered by score | **leaderboards**, **sliding-window** rate limiting (timestamps as scores) |

## 🚨 Failure modes interviewers probe
- **"You said RAM — what on restart?"** Redis *can* persist: **RDB** (periodic snapshots) + **AOF** (append-only write log). For a rate limiter you often skip it on purpose (losing counters just resets windows).
- **"What if Redis dies?"** It's now a **single point of failure** on the request path. Answers: **replication** (a follower takes over) and a **fail-open vs fail-closed** policy (Redis down → let requests through, or block them?). Volunteering this tradeoff is a senior signal.

## ⚖️ Decision rationale
- **Choose Redis when:** shared, hot, mutable state at microsecond latency (counters/sessions/cache).
- **Prefer the alternative when:** you need durable, queryable, relational data → a real DB. Pure/simple caching with multithreaded throughput → Memcached.
- **Tradeoff accepted:** durability & capacity, for speed & atomicity.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. What is Redis in one sentence, and what does the name stand for?</b></summary>

A shared, in-RAM dictionary running as its own networked server. **RE**mote **DI**ctionary **S**erver.
</details>

<details><summary><b>2. Why can't a rate limiter just use the middleware's own memory?</b></summary>

Middleware is horizontally scaled; each instance has its own RAM. A user hitting different instances bypasses a per-instance counter (N instances → N× the limit). Redis centralizes the count so it's **global**.
</details>

<details><summary><b>3. A user's 2 requests hit Redis at the same instant. Why don't both slip through the limit?</b></summary>

Redis is **single-threaded** — commands run one at a time, no interleaving. `INCR` is an atomic read-modify-write, so the second request sees the first's result. It returns the new count, which the middleware checks against the limit.
</details>

<details><summary><b>4. How does the time window reset without a cleanup job?</b></summary>

Per-key **TTL**: `EXPIRE key 60` / `SET ... EX 60`. The key self-destructs; the next `INCR` starts fresh at 1.
</details>

<details><summary><b>5. When is Redis the right tool — and when is it the wrong one?</b></summary>

Right: shared, hot, mutable state, touched constantly, durability optional (counters, sessions, cache, leaderboards). Wrong: durable/relational/queryable data → a real DB.
</details>

<details><summary><b>6. You said data lives in RAM. What happens on restart, and can you prevent loss?</b></summary>

By default data is volatile. Redis *can* persist via **RDB** (snapshots) and **AOF** (append-only write log). For a rate limiter you often skip persistence deliberately.
</details>

<details><summary><b>7. Redis is now on your request path. What's the risk and two mitigations?</b></summary>

It's a **single point of failure**. Mitigate with **replication** (follower failover) and a **fail-open vs fail-closed** policy when Redis is unreachable.
</details>

<details><summary><b>8. Which Redis data type powers a leaderboard or a sliding-window rate limiter, and how?</b></summary>

**Sorted Set (ZSet)** — members ordered by a score. Leaderboard: score = points. Sliding window: score = request timestamp; drop entries older than the window.
</details>

<details><summary><b>9. Single-threaded buys you atomicity. What does it <i>cost</i>? (Name three.)</b></summary>

1. **One slow command blocks every client** — `KEYS *`, `ZRANGE huge 0 -1`. The classic prod incident.
2. **Can't scale up** — extra cores do nothing for one instance. Scale *out*: shard (Redis Cluster) or add read replicas.
3. **It's fine anyway** because Redis is **network-bound, not CPU-bound** — RAM lookups are nanoseconds, so the thread idles on sockets and multiplexes them with epoll. ~100k ops/sec/core.
</details>

<details><summary><b>10. Why "<i>Remote</i>" Dictionary Server — isn't it in RAM?</b></summary>

Orthogonal axes. **In-memory** = the medium (RAM, not disk). **Remote** = the address space (a socket, not a pointer). A Python dict is in-memory *and local*; Redis is in-memory *and remote* — **someone else's RAM, over the network**. Remote is the *feature*: shared state can't live inside any one instance. Cost: **every op is a network round trip** → pipelining, `MGET`, Lua exist to amortize it.
</details>

<details><summary><b>11. TTL vs LRU eviction — are they alternatives? What's the footgun?</b></summary>

**No — different questions, both run at once.** TTL = *"when should this key die on purpose?"* (you set it, per key, at write time). LRU = *"I'm out of RAM, who dies against their will?"* (Redis picks, under memory pressure, via `maxmemory-policy`). LRU is **config, not something you implement** — unlike LC 146.

**Footgun:** `volatile-*` policies **only evict keys that have a TTL**. A key with no TTL is immortal under `volatile-lru` → Redis fills up and **refuses writes** while stuffed with junk it can't touch.

*(Bonus: Redis's LRU is **approximate** — samples ~5 keys, evicts the oldest of the sample. True LRU would cost a pointer per key.)*
</details>
