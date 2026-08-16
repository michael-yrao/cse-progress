# Little's Law (L = λW)

> 🧊 **Frozen reference (Aug 13, 2026).** The SD track is now mock interviews on HelloInterview's
> board; this card is no longer drilled and has no tracker row. Any "owed a sprint / next lane"
> language below is historical. Use it as lookup when a mock debrief points here.
> See [`../study_guide.md`](../study_guide.md).

> **Role:** Capacity math — *turns two numbers you already estimated into a third you need* · **Filed under:** SD concepts (underpins pool sizing, bottleneck-finding, back-of-envelope).
> **You'll want this when:** you're asked **"how many servers / threads / connections?"** and you only have QPS and latency — or you need to prove *where* the bottleneck is.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Concurrency = arrival rate × time spent. Know any two, you get the third — with no assumptions about anything.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it means |
|---|---|---|
| `L = λ × W` for **any** stable system | pool/thread/server counts from QPS + latency | the single most reusable formula in SD estimation |
| It assumes **nothing** about arrival or service distributions | it's an identity, not a model — always true in steady state | you never have to defend a distribution assumption |
| It composes — apply it to **any boundary** you can draw | whole system, one service, one queue, one connection pool | rearranged, it *names the bottleneck* |

## 🎯 In one line
For any system in steady state, the average number of items **inside** it (`L`) equals the average
**arrival rate** (`λ`) times the average **time each item spends inside** (`W`) — so concurrency,
throughput, and latency are three views of one relationship, and fixing two pins the third.

## 🧠 Why it's true (the intuition, not the proof)
Requests arrive at 10/sec and each stays 0.2s. In any snapshot, the ones "inside" are exactly those that
arrived within the last 0.2s → `10 × 0.2 = 2` in flight. That's it. It's an accounting identity about
area under a curve — which is why it needs **no** distributional assumptions, only that the system is
**stable** (what goes in comes out; the queue isn't growing without bound over your measurement window).

## 🔧 The three ways you'll actually use it

**1. Size a pool (solve for L)** — *"1,000 QPS, each request holds a DB connection for 50ms."*
```
L = 1000 × 0.05 = 50 concurrent connections
```
→ a 50-connection pool is the *floor*; provision above it for variance. A 20-connection pool **cannot**
serve this load no matter how many app servers you add — requests will queue for a connection.

**2. Find the ceiling (solve for λ)** — *"200-thread pool, 100ms average request."*
```
λ = L / W = 200 / 0.1 = 2,000 QPS max
```
→ this is a **hard throughput ceiling**. Beyond it, latency rises but throughput doesn't. Any claim of
3,000 QPS from this box is wrong unless W drops.

**3. Prove the bottleneck (solve for W)** — measure L and λ at each tier; the tier whose `W` dominates is
where the time goes. A queue with growing `L` at flat `λ` is a tier that has already saturated.

## ⚠️ Gotchas
- **Steady state is required.** During a spike or an outage, arrivals ≠ departures and the law doesn't
  describe the transient — it describes the average once things settle.
- **Averages only.** `L = λW` relates *means*. It says nothing about p99 — pair it with
  [percentiles & tail latency](percentiles_and_tail_latency.md) and
  [utilization & queueing](utilization_and_queueing.md) for the tail story.
- **W is *residence* time, not service time** — it includes time spent **waiting in the queue**, not just
  being worked on. Using service time understates L badly at high utilization.
- **Match the units.** Latency in ms with rate in QPS is the classic slip: 1,000 QPS × 50**ms** = 50, not
  50,000. Convert to seconds first.

## 🌐 Design consequences
- **Thread / connection / worker pool sizing** — the standard answer to "how big?" is `λ × W` plus headroom.
- **Async justification** — if `W` is dominated by *waiting* on I/O, async/non-blocking lets one thread
  hold many in-flight requests, decoupling `L` (concurrency) from thread count. That's the whole argument
  for event-loop servers in one line.
- **Autoscaling targets** — desired instance count ≈ `(λ × W) / concurrency-per-instance`.
- **Queue depth alarms** — a queue whose `L` grows while `λ` is flat is the definition of a saturated
  downstream.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. State Little's Law and define every term.</b></summary>

`L = λW`. **L** = average number of items in the system (concurrency), **λ** = average arrival rate (throughput), **W** = average time an item spends in the system (residence time, *including* queue wait).
</details>

<details><summary><b>2. What does it assume?</b></summary>

Only **steady state** (stable system: arrivals ≈ departures over the window). It assumes *nothing* about arrival or service-time distributions — it's an accounting identity, not a queueing model.
</details>

<details><summary><b>3. 2,000 QPS, each request holds a DB connection for 25ms. How big must the pool be?</b></summary>

`L = 2000 × 0.025 = 50` connections, minimum — plus headroom for variance. A smaller pool caps throughput regardless of how many app servers you run.
</details>

<details><summary><b>4. You have a 100-thread pool and 200ms average latency. What's your max throughput?</b></summary>

`λ = L/W = 100/0.2 = 500 QPS`. Past that, latency climbs but throughput is pinned — the pool is the bottleneck.
</details>

<details><summary><b>5. Why is using *service* time instead of *residence* time a bug?</b></summary>

W must include queue wait. At high utilization, waiting dominates service time, so using service time massively understates L — you'd size a pool far too small exactly when load is highest.
</details>

<details><summary><b>6. How does Little's Law justify async I/O in one sentence?</b></summary>

If W is mostly *waiting* rather than *working*, concurrency (L) can be held by cheap in-flight state instead of one OS thread each — so an event loop achieves the same `λ = L/W` with a fraction of the threads.
</details>
