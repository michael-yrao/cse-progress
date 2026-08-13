# Retry Storms, Thundering Herds & Cache Stampedes

> 🧊 **Frozen reference (Aug 13, 2026).** The SD track is now mock interviews on HelloInterview's
> board; this card is no longer drilled and has no tracker row. Any "owed a sprint / next lane"
> language below is historical. Use it as lookup when a mock debrief points here.
> See [`../study_guide.md`](../study_guide.md).

> **Role:** Failure dynamics — *how a small blip becomes an outage, and the fixes* · **Filed under:** SD concepts (underpins every failure-mode drill).
> **You'll want this when:** the interviewer says **"the cache/database just went down — now what?"**, or you're asked why a system didn't recover after the original problem was fixed.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Load is not independent of failure. A blip makes clients retry, retries add load, added load extends the blip — the feedback loop is the outage.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it means |
|---|---|---|
| Retries **multiply** load exactly when capacity is lowest | a 1-second blip becomes a 1-hour outage | the retry policy *is* a capacity decision |
| Independent clients **synchronize** on shared events (a TTL, a deploy, a recovery) | thousands of simultaneous identical requests | timers and TTLs are a coordination mechanism you didn't intend |
| The loop can be **self-sustaining** — a *metastable* failure | removing the original trigger doesn't fix it | recovery may require shedding load, not restoring capacity |

## 🎯 In one line
Three named instances of one feedback loop: a **thundering herd** (many clients wake at once), a **cache
stampede** (a hot key expires and every concurrent reader misses together), and a **retry storm**
(failures generate retries that generate more failures) — all fixed by *desynchronizing* clients and
*capping* amplification.

## 🐘 Cache stampede (dogpile)
A hot key's TTL expires. Between expiry and the first refill, **every** concurrent request for that key
misses and goes to the database at once.

**Why it's worse than it sounds:** by [Zipfian skew](zipfian_distribution.md), the hottest key is exactly
the one with the most concurrent readers — so the stampede hits hardest on the key whose absence hurts
most. A key served at 50k QPS from cache becomes 50k QPS at the database for the refill window.

**Fixes, in order of preference:**
- **Single-flight / request coalescing** — one request per key acquires a lock and recomputes; the rest
  wait for its result. Best fix: caps DB load at exactly 1 per key.
- **Stale-while-revalidate** — serve the *expired* value while one background task refreshes. No request
  ever waits; costs slight staleness.
- **Probabilistic early expiry (XFetch)** — each reader independently rolls a dice that gets likelier as
  the TTL nears, so *one* reader refreshes early and the herd never forms.
- **Jittered TTLs** — never set the same TTL for a batch of keys written together (a bulk warm-up creates
  a synchronized mass expiry later). Use `TTL ± random%`.

## ⛈️ Retry storms & amplification
Every layer that retries **multiplies** the load of the layer below.

```
client 3 attempts × gateway 3 × service 3 = 27× load on the database
```
The database was already struggling; now it receives 27× traffic. This is how a partial degradation
becomes a total one.

**Fixes:**
- **Retry at exactly one layer.** Usually the outermost one that can still act meaningfully. Deep layers
  should fail fast and propagate. This single rule kills the multiplication.
- **Exponential backoff + jitter.** Backoff alone is *not enough* — synchronized clients backing off the
  same amount retry in a synchronized wave. Jitter is the load-bearing part.
  ```
  # "full jitter" — the standard
  sleep = random_between(0, min(cap, base * 2**attempt))
  ```
- **Retry budgets** — allow retries only while they're under ~10% of total requests. When a dependency is
  broadly down, retries stop automatically instead of piling on.
- **Circuit breaker** — after N consecutive failures, *stop calling* and fail fast for a cooldown, then
  let a trickle through to test recovery. Protects the *downstream* from you.
- **Retry only what's safe.** Retrying a non-idempotent write duplicates it — pair every retry policy
  with **idempotency keys**.

## 🔁 Metastable failure (the deep version)
A system that is still failing **after the trigger is gone**. The retry load alone is now enough to keep
it saturated: it can't serve fast enough to clear the queue, and every timeout produces another retry.

**The tell:** you restored the database, added capacity, and it's *still* down.
**The fix is counterintuitive** — you must **shed load** (drop traffic, disable retries, flush the queue)
to let the system escape, then ramp back up. Adding capacity often doesn't help because the amplification
scales with it.

**Cold-cache restarts are the classic trigger:** restart a service with an empty cache → hit ratio
collapses → every request goes to the DB → everything is slow → clients time out and retry → the cache
never gets a chance to warm. Mitigate by warming the cache before taking traffic, and ramping traffic in.

## 🌐 Design consequences
- **Every retry mention needs "with exponential backoff and jitter"** attached — saying "we retry" alone
  is a red flag in an interview.
- **Health checks must not stampede** either — synchronized health checks across a fleet are a herd.
- Pairs with [utilization & queueing](utilization_and_queueing.md): amplification is what pushes ρ past 1,
  and **load shedding** is the escape hatch both concepts point to.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. What is a cache stampede, and why does Zipf make it worse?</b></summary>

A hot key expires and every concurrent reader misses simultaneously, all hitting the database at once. Zipf means the hottest key has the most concurrent readers — so the stampede is largest exactly where the cache mattered most.
</details>

<details><summary><b>2. Give the best fix for a stampede and say why it's best.</b></summary>

**Single-flight / request coalescing**: one request per key recomputes under a lock while others wait for its result. It caps database load at exactly one request per key, regardless of concurrency. (Alternatives: stale-while-revalidate, probabilistic early expiry, jittered TTLs.)
</details>

<details><summary><b>3. Three layers each retry 3×. What load does the bottom layer see, and what's the rule that prevents it?</b></summary>

27× (3×3×3). Rule: **retry at exactly one layer** — inner layers fail fast and propagate. Add retry budgets to cap retries as a fraction of total traffic.
</details>

<details><summary><b>4. Why is exponential backoff insufficient without jitter?</b></summary>

Clients that failed together back off by the same amount and therefore retry **together** — the herd is preserved, just delayed. Jitter randomizes the wake-up times and is what actually breaks the synchronization.
</details>

<details><summary><b>5. Write the full-jitter formula.</b></summary>

`sleep = random(0, min(cap, base × 2^attempt))` — the delay is drawn uniformly from zero up to the exponentially growing bound, not set equal to it.
</details>

<details><summary><b>6. What is a metastable failure, and why is adding capacity often the wrong response?</b></summary>

The system stays down after the original trigger is gone, sustained by its own retry load. Amplification scales with the added capacity, so more capacity often gets consumed by retries. Escape requires **shedding load** (disable retries, drop traffic, drain queues), then ramping back up.
</details>

<details><summary><b>7. Why must a retry policy be paired with idempotency?</b></summary>

A retried non-idempotent write is a duplicated write. The client can't tell "request lost" from "response lost," so retries need idempotency keys to make repeat delivery safe.
</details>
