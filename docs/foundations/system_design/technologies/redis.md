# Redis

> **Role:** Cache / shared in-memory state · **Rival on the fork:** Memcached
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check. Rate 🟢/🟡/🔴 and log in [`../mastery/design_progress.md`](../mastery/design_progress.md).

## 🎯 In one line
Redis (**RE**mote **DI**ctionary **S**erver) is a **shared, in-RAM dictionary** running as its own server that every app instance talks to over the network. Single-threaded execution makes its operations **atomic**; every key can carry a **TTL**. That's exactly why it's the counter store for a [rate limiter](../components/rate_limiter.md).

## 🎯 Recall log — blind sprints

**Jul 13, 2026 — first blind sprint → 🔴 Blank** (3 of 8 prompts attempted).

**Came back cold (the hard part — solid):** the *why-shared-state* argument — horizontally-scaled middleware each has its own memory, so a per-instance counter is bypassed; Redis holds the **global** count.

**Drill targets — these did NOT come back.** Restudy focuses here:

| # | Gap | The thing to be able to say |
|---|-----|------------------------------|
| 1 | **Atomicity** ⚠️ *biggest* | Never mentioned. Redis is **single-threaded** → `INCR` is one atomic read-modify-write, so two concurrent requests can't both read the same count and both pass. This is *the* follow-up the instant you say "Redis." |
| 2 | **TTL vs token bucket** *(crossed wires)* | Asked how the window resets, reached for the *token-bucket refill*. Two different layers: **token bucket = the middleware's algorithm; `EXPIRE`/TTL = the Redis mechanism** that self-destructs the key so the next `INCR` starts fresh. Don't fuse them. |
| 3 | **Failure modes** | Blank. Redis on the request path is a **single point of failure** → mitigate with **replication** (follower failover) + a **fail-open vs fail-closed** policy when it's unreachable. |

**Precision fix (Q1):** "shared cache" undersells it — say **in-RAM dictionary on its own server**, and the name is **RE**mote **DI**ctionary **S**erver.

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

## ⏳ TTL / expiry
Any key can auto-delete: `EXPIRE key 60` or `SET key val EX 60`. For a fixed-window limiter this *is* the window — `INCR` the key, `EXPIRE` it 60s; it self-destructs and the next request starts fresh. No cleanup job.

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
