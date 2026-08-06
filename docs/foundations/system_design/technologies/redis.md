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

**Aug 5, 2026 — rated blind sprint → 🟡 Shaky** (7 of 12 clean; +10 → Aug 15). **Flat against Jul 21, and the shape is the finding, not the count.** **Clean cold:** 1, 2, 3, 5 (still zero token-bucket fusion — that fix has held 2 sprints), 6, and **7 stronger than the note** (RDB-vs-AOF framed as a restore-speed / data-loss trade, replication unprompted). **First-time win: card 3b/4 — `EVAL` + Lua recalled correctly**, having been a cold miss when added Jul 26; gap is that the *fix* came without the *principle* (atomicity is **per command, not across commands**).
- ⚠️ **All three Jul-21 drill targets missed again — third sprint running.** Card 8 (the score *is* the mechanism; sliding window not reached at all) · card 9 (scale-out still absent; **new error: claimed RAM can't scale vertically either** — single-threading caps cores, not memory) · card 11 (footgun still inverted — described LRU evicting a long-TTL key, which is normal `allkeys-lru` behaviour, not the `volatile-*`-immortal-key trap).
- ⚠️ **Card 7 REGRESSED to blank** ("still hangs here, hard to answer on the fly"). Jul 21 had the entire mitigation chain correct and only missed the *word* SPOF; this time nothing came back. Second-order note: on Jul 19 the root cause was phrase-parsing ("on the request path"), which was fixed — so this is retention, not comprehension.
- **Card 9's third cost was a category error, worth its own line:** offered "lives in RAM so volatile." True of Redis, **not a cost of single-threading** — different axis. The card's third is that it's *fine anyway* (network-bound, not CPU-bound).
- **🛑 TEACH TRIGGER — do not sprint this card a fourth time.** Cards 7, 8, 9, 11 have now missed three consecutive sprints. Per the repo's 540/19 rule, three misses on one clause is a teaching signal, not a repetition signal. Next Redis slot is a **teach**, unrated, measured later.
- **⚠️ Instrument critique raised by the learner mid-sprint, and it is upheld** — see [Card design](#-card-design-why-the-questions-look-the-way-they-do) below. **Two distinct defects, raised separately and both upheld:** (1) the stems **named the answer's category**, making it recognition rather than recall; (2) the twelve questions had **no connectivity** — a quiz, not a line of inquiry, so nothing the learner said ever had a consequence. Rebuilt the same session as **one twelve-node thread** where each node is caused by the last. The irony worth remembering: the fix was already in this file — the 🦴 spine and the Jul 15 derivation are both chains; only the card wasn't. *(Separately, the scope is still rate-limiter-shaped — see Coverage gaps.)*

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

### ⚠️ Per COMMAND, not across commands — the limit of what atomicity buys (added Jul 26, 2026)

**This is the trap, found cold in the Rate Limiter Mastery mock.** `INCR` is safe because the read
*and* the modify happen **inside one command**. The guarantee does **not** extend across two
commands with your own logic in between:

```
BROKEN AGAIN (logic between round trips):
A: HGETALL → (tokens=1, ts=T) ┐ both read 1 token
B: HGETALL → (tokens=1, ts=T) ┘ both compute "a token is available"
A: HSET tokens=0                both allow → limit bypassed
B: HSET tokens=0
```

Anything needing **read → compute → conditionally write** (a token bucket: `min(capacity,
tokens + elapsed × rate)`, then decrement) is a multi-step read-modify-write, and single-threadedness
does nothing for it. *"Redis is single-threaded so I'm safe"* is only true per command.

### 🌙 `EVAL` — Lua scripting, the fix for multi-step atomicity

Send Redis a **Lua script**; it runs the whole script on the single thread as **one command**. Nothing
interleaves. Read + math + clamp + conditional write become one indivisible operation, one round trip.

```
EVAL "<lua>" <numkeys> <key1> ... <arg1> ...
EVAL "return redis.call('HGET', KEYS[1], 'tokens')" 1 bucket:abc123
```

- `numkeys` splits **`KEYS[]`** from **`ARGV[]`**. Not cosmetic: **Redis Cluster shards by key**, so it
  must know which keys a script touches to route it. Passing a key via `ARGV` works on one instance and
  **breaks the day you cluster** — a common bug.
- **`EVALSHA <sha1>`** invokes a cached script by hash instead of resending the source. ⚠️ **The cache
  is not durable** — restart, failover, or `SCRIPT FLUSH` empties it and you get `NOSCRIPT`. Standard
  pattern: *try `EVALSHA` → on `NOSCRIPT`, fall back to `EVAL`* (which re-caches). At high rps this
  surfaces as an error burst right after a failover. Redis 7's `FUNCTION LOAD` registers persistently
  and removes the dance.
- **Cost:** the script occupies the one thread and blocks every other client — same bill as `KEYS *`.
  Keep scripts **tiny and loop-free**.
- **Determinism:** scripts were historically replicated as scripts, so they must not read the clock or
  use unseeded randomness. **Pass `now` in as an `ARGV`** rather than calling a time function inside.

**Why Lua and not Python:** ~200KB interpreter *designed* to be embedded in C · microsecond startup
(it's blocking the server) · small enough surface to sandbox (no file I/O, no `os`) · deterministic.
Same reasons nginx embeds it.

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

## 🧭 Card design (why the questions look the way they do)

**Redesigned Aug 5, 2026, on the learner's challenge — mid-sprint, and it was upheld.**

The old card asked twelve questions that **named the answer's category in the stem**: *"Which Redis **data
type** powers a leaderboard"* tells you it's a data type (pick 1 of ~5); *"**TTL vs LRU** — are they
alternatives?"* hands you both terms and the axis; *"…what does it **cost**? Name three"* hands you the
premise, the axis, and the count. That is **recognition with a cue**, not retrieval — and it is not how the
knowledge gets used. Nobody in an interview or an incident says "name the data type." They describe a
**symptom** or a **requirement**, and supplying the category is the whole job.

Suggestive evidence from the record: the card whose stem supplied the least (the request-path/SPOF one) is
the one that had **never once come back clean** across four sprints.

### Rule 1 — the stem states a situation, never the kind of answer

Concretely, a probe must not contain: the name of a Redis feature, command, or data type · the word "type",
"policy", "mechanism", or "trade-off" as a pointer to the answer's shape · a count ("name three") · a
this-vs-that framing that supplies both sides. If deleting a phrase from the stem makes the question harder,
that phrase was scaffolding — delete it.

### Rule 2 — the card is one thread, not a list

**Added the same session, on the learner's second and sharper challenge:** *"from question 1 to question 2
there is no connectivity at all except that we're looking at Redis."* Correct, and it is a **separate defect
from rule 1** — twelve perfectly-framed stems still make a quiz if nothing you say ever has a consequence.
Real probing is *"given what you just said, what breaks now?"*

So the card is **one scenario that grows**, and **every node is caused by the one before it**: sessions move
in (⑥) which is *why* volatility starts to matter (⑦); ZSets buy precision (⑨) which is *why* they get big
enough to block the single thread (⑩) and *why* they later fill memory the policy can't evict (⑫).

**This is not a new idea here — it is the note's own shape.** The 🦴 spine derives everything from three
facts, and the **Jul 15, 2026 derive-the-design session remains the best Redis rep on record**, logged
precisely as a chain (*N-server undercount → shared store → race → `INCR` → single-threaded → TTL → fail-open/
closed*). The flat card was the one artifact that had thrown that away.

⚠️ **Accepted cost: a chain leaks forward.** Node ③ hands you node ②'s answer as its premise. That is
deliberate — it's what a real interviewer does, and it stops one blank cascading into twelve — but it means
**a node can never be scored on the answer to the node before it.** Grade per node.

### Rule 3 — grading: a noun without its mechanism is not clean

Partial credit is *not* "said the right noun." A node is clean only when the **mechanism** is there — the
score *is* the sliding window; the TTL *is* the window reset. A noun without its mechanism is the failure
mode this card exists to catch, and it is exactly what the old cards 8/9/11 kept scoring on.

⚠️ **The scope problem is separate and NOT yet fixed** — see [Coverage gaps](#-coverage-gaps--the-teach-agenda)
below. This card is Redis-as-seen-from-the-rate-limiter, because that is the design it was born in.
Reframing the stems does not widen the surface.

---

## 🃏 Recall Card (the rep)

**One thread, twelve nodes. Each node is a consequence of the last.**

Answer from memory before unfolding, and work **in order** — the sequence is the point, not decoration.
**A noun without its mechanism is not clean.**

> ### 🎬 The premise
> You're putting a rate limiter in front of an API. **100 requests per minute per user.** It runs as
> middleware, in front of a horizontally-scaled service. That's all you get; everything below follows from
> here.

<details><summary><b>① It passes every test in dev. In prod, users get roughly 10× the limit. Nothing errored, no exception was thrown, the code is identical. What is happening?</b></summary>

The middleware is **horizontally scaled** and each instance has its **own RAM**. A per-instance counter is
bypassed the moment the load balancer spreads one user's requests — 10 instances each admitting the full
limit ⇒ ~10×. Nothing errors because every instance *is* behaving correctly by its own count.

⇒ The count has to be **global** — one store every instance can reach.
</details>

<details><summary><b>② So the count must live somewhere all of them can see. Name what you're adding to the architecture — one sentence — and expand the acronym.</b></summary>

A **shared, in-RAM dictionary running as its own networked server**. **RE**mote **DI**ctionary **S**erver.

*"A cache" undersells it — caching is one use. The defining properties are shared, in-RAM, remote, and
single-threaded, and the next four nodes are all consequences of those.*
</details>

<details><summary><b>③ The count is in Redis now. Under load test, the 100/min limit still admits 103–107 — but only sometimes, and only at high concurrency. Why, and what's the one-command fix?</b></summary>

`GET` then `SET` is **two** operations with a gap. Two concurrent requests both read 99, both conclude
they're under, both write 100 — a lost update. It only appears at high concurrency because the gap has to be
straddled.

**`INCR`** — one atomic read-modify-write. Redis is **single-threaded**: commands run to completion, one at
a time, and cannot interleave. `INCR` returns the **new** value, which the middleware compares to the limit.
</details>

<details><summary><b>④ <code>INCR</code> fixed it, and you now believe Redis makes you safe. Product asks for smooth refill instead of a hard window — read tokens and a timestamp, refill by <code>elapsed × rate</code>, clamp, decrement. Over-admission is back, and <code>INCR</code> is nowhere in the code. What did you over-conclude in ③?</b></summary>

That single-threadedness makes *you* safe. It doesn't — Redis guarantees atomicity **per command, not
across commands**. `INCR` was safe because the read *and* the modify sat inside **one** command. Read →
compute → conditional-write is **two** round trips with your logic in the gap; two instances both read
`tokens=1`, both compute "available", both allow.

**Fix: `EVAL`** — ship a Lua script, which Redis runs on its single thread as one indivisible command, in
one round trip.
- `numkeys` splits **`KEYS[]`** from **`ARGV[]`** — not cosmetic: **Cluster shards by key**, so passing a key
  through `ARGV` works on one instance and **breaks the day you cluster**.
- **`EVALSHA <sha1>`** runs a cached script by hash; the cache is **not durable**, so handle `NOSCRIPT` by
  falling back to `EVAL`.
- Keep scripts tiny — they block every other client (which is node ⑩) — and pass `now` as an `ARGV` for
  determinism.
</details>

<details><summary><b>⑤ It's correct now. You go looking for the cleanup job that resets each user's window and discover there isn't one — no cron, nothing issues a delete, and the keys aren't accumulating. How?</b></summary>

Per-key **TTL** — `EXPIRE key 60`, or `SET … EX 60` at write time. The key **self-destructs**; the next
`INCR` finds nothing and starts fresh at 1. The reset is a **deletion**, not a decrement.

*⚠️ The classic wrong answer is token-bucket refill. Different layer: token bucket is the middleware's
algorithm; TTL is the Redis mechanism. Tell: "window" is a fixed-window word ⇒ TTL. "Refill / smooth /
burst" ⇒ token bucket.*
</details>

<details><summary><b>⑥ It works, it's fast, and the team has noticed. They propose moving three more things in: logged-in session tokens, "all orders over $50 last quarter", and the canonical record of account balances. Sort them, and say what decides it.</b></summary>

**Redis:** session tokens — shared, hot, mutable, touched constantly, and losing them costs a re-login.
**A real database:** the order query, because it *is* a **query** (predicates, ranges, joins) and Redis is
key-lookup only — you index at write time or not at all. Balances, because they need **durability and
transactional correctness**, and money cannot be reconstructed.

**The deciding question:** *what does losing this cost me, and am I looking it up by key or asking a question
of it?*
</details>

<details><summary><b>⑦ Sessions move in. That raises the stakes on a word you used in ②: <i>in-RAM</i>. The box reboots. What did you lose, what could you have turned on, and which option gets you serving traffic soonest?</b></summary>

By default, **everything** — it's RAM.
- **RDB (snapshots)** — periodic point-in-time dump. Loses everything since the last snapshot. **Fastest
  restore**: load one compact file.
- **AOF (append-only file)** — logs every write command. Loses far less (sub-second with `everysec`), but
  restore **replays the log**, so it's slower and the file grows (hence rewrite/compaction).

Choose by what the data is worth. For the *counters* you'd often skip persistence deliberately — a lost
counter costs one over-generous minute. For the *sessions* you just moved in, it logs everyone out.
</details>

<details><summary><b>⑧ Reboots are survivable. Now Redis is simply unreachable for 90 seconds. Walk me through what users experience, and what you should have built beforehand. <i>(Name the risk before you list fixes.)</i></b></summary>

**Name it: Redis is on the request path, so it is a single point of failure (SPOF).** Every request makes a
mandatory synchronous stop there — its failure is total and immediate, not degraded.

Two mitigations:
1. **Replication** — leader/follower with failover, so a dead node isn't a dead dependency.
2. **A declared fail-open vs fail-closed policy** for when it's unreachable anyway.

**The policy is a judgement, not a default.** Fail **closed** when leaking is worse than denying (login
brute-force, payments). Fail **open** when the limiter causing an outage is the bigger harm. **DDoS is not a
fail-closed case** — failing closed *completes* the attacker's denial of service; that traffic is absorbed at
the edge (CDN/WAF), not at app-Redis.

*Terminology: leader/follower (or primary/replica), not master/slave.*
</details>

<details><summary><b>⑨ It's resilient now, so product gets ambitious: kill the sawtooth at the minute boundary, and add a live top-10 leaderboard. Neither is a counter. What do you store for each — and what does the first one cost you as traffic grows?</b></summary>

**Sorted Set (ZSet)** for both — members kept in order by a **score**. The type is the easy half; **the score
is the mechanism.**

- **Sliding window:** score = the request **timestamp**. `ZADD` per request, `ZREMRANGEBYSCORE key 0
  (now - window)` to drop what aged out, `ZCARD` for the count. No sawtooth, because the window edge moves
  continuously.
- **Leaderboard:** score = **points**. `ZADD` to update, `ZREVRANGE key 0 9` for the top 10.

**The cost:** the sliding window stores **one entry per request**, not one integer per user — memory scales
with *traffic*, where a fixed window scales with *users*. That is what you're buying the precision with, and
it sets up ⑩ and ⑫.
</details>

<details><summary><b>⑩ Those ZSets got big. Ops reports the whole service froze for four seconds; Redis was pegged on one core while fifteen sat idle. Explain everything that tells you, and what you do about it.</b></summary>

Three things, and the third is the surprise:

1. **One slow command blocks every client.** Single-threaded means no preemption — a `KEYS *` or an
   unbounded `ZRANGE huge 0 -1` holds the thread and everyone waits. This is the classic prod incident and
   it's what happened here. Fix: `SCAN` not `KEYS`, bound your ranges, keep Lua scripts (④) tiny.
2. **You cannot scale *up* out of it.** Extra **cores** do nothing for one instance. You scale **out** —
   shard (Redis Cluster) or add **read replicas**. ⚠️ The cap is on **cores, not RAM**: more memory scales a
   Redis instance perfectly well, so "can't scale vertically" is only true of CPU.
3. **It's fine anyway, normally** — Redis is **network-bound, not CPU-bound**. RAM lookups are nanoseconds,
   so the thread mostly idles on sockets and multiplexes them with epoll (~100k ops/sec/core). A pegged core
   is therefore *a signal that some command is pathological*, not evidence you've outgrown the box.

*⚠️ "The data is volatile" is **not** on this list — that comes from living in RAM, a different axis entirely
from single-threadedness.*
</details>

<details><summary><b>⑪ "Network-bound" catches a teammate's eye and they push back: "Redis is in-memory, so it's basically a local dict — why is our p99 300µs instead of 300ns?" Answer them.</b></summary>

They've collapsed two **orthogonal** axes:
- **In-memory** = the **medium** holding the bytes (RAM, not disk).
- **Remote** = the **address space** and how you reach it (a socket, not a pointer).

*Remote* is the opposite of **in-process**, not of in-RAM. A Python dict is in-memory *and local*; Redis is
in-memory *and remote* — **someone else's RAM, over the wire**. The 300µs is the **network round trip**; the
lookup itself really is nanoseconds.

And remote is the **feature**, not a tax — it's the entire answer to ①: state every instance can see cannot
live inside any one of them. The cost is that a 1,000-`GET` loop is 1,000 round trips, which is exactly why
**pipelining, `MGET`, and Lua** exist.
</details>

<details><summary><b>⑫ Final state: counters, sessions, sliding windows, leaderboards. You set <code>maxmemory</code> with policy <code>volatile-lru</code>. Redis is now at 100% and refusing writes — but most of the keyspace is stale junk nobody reads. What did you get wrong?</b></summary>

**`volatile-*` policies only evict keys that have a TTL.** The stale junk was written **without** one — the
leaderboard entries from ⑨ never got an `EXPIRE`, unlike the counters from ⑤ — which makes it **immortal**
under this policy. Redis would rather refuse writes than touch it. Fix: set TTLs at write time, or use an
`allkeys-*` policy.

The framing behind it: TTL and LRU are **not alternatives**. They answer different questions and both run at
once.
- **TTL** = *"when should this key die on purpose?"* — you set it, per key, at write time.
- **LRU** = *"I'm out of RAM; who dies against their will?"* — Redis picks, under memory pressure, via
  `maxmemory-policy`. It is **configuration, not something you implement** (unlike LC 146).

*⚠️ LRU evicting a key that still had TTL left is **not** the footgun — under `allkeys-lru` that's the
intended behaviour. The footgun is the key it **cannot** evict.*

*(Bonus: Redis's LRU is **approximate** — it samples ~5 keys and evicts the oldest of the sample. True LRU
would cost a pointer per key.)*
</details>

### 🔗 The thread, in one line

**can't count across instances → shared remote dict → races → `INCR` → atomicity is per-command → `EVAL` →
windows expire themselves → what else belongs here → RAM is volatile → and unreachable → ZSets for
precision → which get big and block the one thread → which is network cost, not CPU → and fills memory it
can't evict.**

If you can say that chain end to end, the twelve nodes are recoverable from it. **That is the actual target
— the chain, not the cards.** It is also, verbatim, the shape of the Jul 15, 2026 derive-the-design session,
which remains the best Redis rep on record.

## 🕳️ Coverage gaps — the teach agenda

**Raised Aug 5, 2026 and deliberately NOT closed in the same edit.** These have no teaching content in this
note, so writing probes for them would produce questions with no checkable answer — and would measure
material that was never taught, which the teach/measure split forbids.

Everything above is **Redis-as-seen-from-the-rate-limiter**, because that is the design it was born in. What
a cold *"tell me about Redis"* would reach that this note currently cannot:

| Gap | Why it matters |
|---|---|
| **Data types beyond ZSet** — hash, list, set, bitmap, stream | "Which structure" is a routine follow-up; only ZSet is covered |
| **Cache-aside vs write-through vs write-behind** | the actual *caching* patterns — the headline use case, and it's absent |
| **Cache stampede / thundering herd** | the classic cache failure mode; the mitigation set (jittered TTL, lock-on-miss, early recompute) is a real interview beat |
| **Invalidation** | "the second hard problem"; not mentioned anywhere here |
| **Redis Cluster mechanics** — hash slots, resharding, why multi-key ops break | q10 says "scale out" and then stops precisely where the follow-up starts |
| **Distributed locks / Redlock** | commonly asked, and *contested* — knowing why it's disputed is the answer |
| **Pub/Sub and Streams** | fire-and-forget vs durable consumer groups; the Kafka comparison |
| **Session storage** | named in q6 as a fit, never developed |

**Sequencing, so this doesn't become a course:** the four stuck cards (8, 9, 10, 12) are the **teach trigger
already fired** and come first. The gap list above is a *second* teach, and it should be split across at
least two slots. Neither is rated on the day it's taught.
