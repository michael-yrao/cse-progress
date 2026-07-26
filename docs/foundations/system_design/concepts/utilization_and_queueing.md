# Utilization & Queueing (why you never run at 95%)

> **Role:** Capacity math — *why latency explodes before you run out of capacity* · **Filed under:** SD concepts (underpins autoscaling thresholds, headroom, load shedding).
> **You'll want this when:** someone asks **"why not just run fewer servers, you're only at 60% CPU?"** — or your latency spiked while utilization only moved a little.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Wait time scales as `1/(1−ρ)`. That's a hyperbola, not a line — so the last 10% of capacity costs more latency than the first 80% combined.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it means |
|---|---|---|
| Response time multiplier ≈ **1/(1−ρ)** | latency is **nonlinear** in utilization | 90% busy ≠ "slightly slower than 80% busy" — it's 2× worse |
| **Variability** (bursty arrivals, uneven work) multiplies the wait | the curve bends earlier and harder in reality | smooth traffic tolerates higher ρ than spiky traffic |
| **Pooling** N servers behind **one** queue beats N private queues | same hardware, much lower wait | the single supermarket line, not one line per till |

## 🎯 In one line
As utilization `ρ` (arrival rate ÷ service capacity) approaches 1, queueing delay grows without bound —
so a server is *latency*-saturated long before it is *throughput*-saturated, and the useful operating
point sits near **70–80%**, not 95%.

## 📈 The curve (memorize this table, not the formula)
For a simple single queue, average response time ≈ `S / (1 − ρ)` where `S` = service time:

| Utilization ρ | Response time (× service time) |
|---|---|
| 50% | 2× |
| 70% | 3.3× |
| **80%** | **5×** |
| 90% | 10× |
| 95% | 20× |
| 99% | **100×** |

**The knee is around 70–80%.** Read the danger in the *deltas*: going 50%→70% costs 1.3×; going 90%→95%
costs another 10×. Same 20-point move, wildly different price.

**Why headroom is the real argument:** at ρ=0.7 you're at 3.3×. A modest **20% traffic spike** pushes you
to ρ=0.84 → **6.25×**. That's a near-doubling of latency from a spike you'd call routine. At ρ=0.9 the
same spike takes you past 1.0 — which is not "slow," it's **unbounded queue growth**, i.e. an outage.

## 🌪️ Variability makes it worse
The clean `1/(1−ρ)` assumes memoryless arrivals. Real traffic is **burstier** and real work is **uneven**
(one request scans 10 rows, another scans 10 million). Kingman's approximation says the wait scales with
`ρ/(1−ρ)` **times a variability factor** — so higher variance in either arrivals *or* service time shifts
the whole curve left. Practical reading: **the more variable your workload, the lower your safe ρ.**

## 🏊 Pooling: the free win
N servers each with their own queue is strictly worse than N servers sharing one queue, at identical
utilization — because a private queue can be backed up while a peer sits **idle**. One shared queue can
never leave a server idle with work waiting.

**Design consequence:** prefer a load balancer with **least-outstanding-requests** (or a shared work queue)
over round-robin/random. Round-robin ignores that one backend is already stuck behind a slow request —
it's the "one line per till" failure, and it's a direct cause of tail latency.

## ⚠️ Gotchas
- **CPU% is a bad proxy for ρ.** The relevant queue may be a connection pool, a disk, a lock, or a
  downstream service. 40% CPU with a saturated connection pool is a saturated system.
- **ρ > 1 is not "slower," it's unstable.** The queue grows without limit until something dies (OOM,
  timeout cascade). The correct response is **load shedding**, not more queue.
- **Bigger buffers don't fix saturation** — they convert a fast failure into a slow one and inflate
  latency. This is bufferbloat; a short queue that rejects is kinder than a long one that times out.

## 🌐 Design consequences
- **Autoscale on ~70%**, and scale on the *queue* metric that actually saturates first.
- **Shed load** at the edge before ρ→1 (this is the honest job of a [rate limiter](../components/rate_limiter.md)).
- **Reduce variability** to buy headroom: separate slow endpoints from fast ones into their own pools
  (bulkheads) so one heavy query can't inflate everyone's `W`.
- Pairs with [Little's Law](littles_law.md) (which gives you `L` and `W`) and
  [percentiles & tail latency](percentiles_and_tail_latency.md) (the tail is where this shows up first).

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. How does response time scale with utilization, and why does that shape matter?</b></summary>

As `1/(1−ρ)` — a hyperbola. It matters because the cost is nonlinear: 50%→70% is nearly free, 90%→95% doubles latency again. There's a knee around 70–80% past which small load increases cause large latency increases.
</details>

<details><summary><b>2. Give the multiplier at 80%, 90%, and 99% utilization.</b></summary>

5×, 10×, and 100× the service time, respectively.
</details>

<details><summary><b>3. Why run at 70% when the box "has 30% left"?</b></summary>

Headroom for spikes. At ρ=0.7 a routine 20% traffic spike lands at ρ=0.84 (≈6.25×, survivable). Starting from ρ=0.9 the same spike pushes ρ past 1 — unbounded queue growth, i.e. an outage, not a slowdown.
</details>

<details><summary><b>4. What happens to the curve when workload variability increases?</b></summary>

It shifts left/steepens — the wait scales with `ρ/(1−ρ)` times a variability factor (Kingman). Burstier arrivals or more uneven service times mean you must run at a *lower* utilization for the same latency.
</details>

<details><summary><b>5. Why is one shared queue over N servers better than N private queues?</b></summary>

A private queue can be backlogged while another server is idle; a shared queue never leaves a server idle with work waiting. Practical form: prefer least-outstanding-requests load balancing over round-robin.
</details>

<details><summary><b>6. What's the right response to ρ > 1, and what's the wrong one?</b></summary>

Right: **shed load** (reject early, rate limit, degrade). Wrong: add buffer/queue depth — that converts a fast rejection into a slow timeout, inflating latency without adding capacity (bufferbloat).
</details>

<details><summary><b>7. Why is CPU utilization a misleading measure of ρ?</b></summary>

The saturated resource may not be CPU — connection pools, disk, locks, or a downstream dependency queue first. A box at 40% CPU with an exhausted connection pool is fully saturated in the sense that matters.
</details>
