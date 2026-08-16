# Percentiles & Tail Latency

> 🧊 **Frozen reference (Aug 13, 2026).** The SD track is now mock interviews on HelloInterview's
> board; this card is no longer drilled and has no tracker row. Any "owed a sprint / next lane"
> language below is historical. Use it as lookup when a mock debrief points here.
> See [`../study_guide.md`](../study_guide.md).

> **Role:** Measurement foundation — *how to state a latency number without lying* · **Filed under:** SD concepts (underpins SLOs, fan-out design, load testing).
> **You'll want this when:** you just said "average latency is 50ms" and the interviewer asked "and p99?" — or you're designing anything that **fans out** to many services and can't explain why it's slow.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Averages describe a system nobody experiences; the tail is what users feel, and fan-out *multiplies* the tail.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it means |
|---|---|---|
| Latency is **heavy-tailed**, not normal | the mean sits near the fast body and **hides** the slow 1% | quoting a mean tells you nothing about the worst experience |
| **p99 is a per-request property, not a per-user one** | a user making 100 requests very likely hits your p99 | your "1% edge case" is most users' *daily* experience |
| **Fan-out takes the MAX**, not the average, of its calls | one slow dependency sets the whole response time | service p99 becomes user-facing p50 fast |

## 🎯 In one line
`pN` = the latency below which N% of requests complete; you report **p50 / p99 / p999** instead of a mean
because latency distributions are heavy-tailed, and any request that **fans out to N backends and waits for
all of them** inherits the *worst* of N draws — so tail latency compounds as a system decomposes.

## 📉 Why the average lies
```
100 requests: 99 take 10ms, 1 takes 5000ms
mean  = (99×10 + 5000)/100 = 59.9ms   ← describes NO actual request
p50   = 10ms                          ← the typical experience
p99   = 10ms
p99.9 = 5000ms                        ← the thing that pages you
```
The mean is **dragged by the outlier** yet still **understates** it by 100×. Neither number is the
experience. Percentiles are the experience.

## 🔢 Tail amplification (the load-bearing math)
A request that fans out to **N** services **in parallel and waits for all** finishes when the *slowest*
returns. If each service independently meets its p99:

> P(all N under p99) = `0.99^N` → P(at least one slow) = `1 − 0.99^N`

| Fan-out N | Chance the user hits a p99+ response |
|---|---|
| 1 | 1% |
| 10 | **9.6%** |
| 100 | **63%** |

**At 100 dependencies, your service's p99 is roughly the user's p50.** This is why "each service is fast"
does not imply "the product is fast" — and it's the reason microservice fan-out is a latency *decision*,
not just an org decision. (Canonical source: Dean & Barroso, *The Tail at Scale*.)

## ⚠️ Gotchas that get you caught
- **You cannot average percentiles.** "Server A's p99 is 100ms, B's is 200ms, so the fleet p99 is 150ms" is
  **wrong** — percentiles don't compose linearly. Aggregate the **histograms** (t-digest / HDR histogram),
  then compute the percentile once.
- **The mean of percentiles over time is also wrong** — a dashboard averaging one-minute p99s understates
  the real hourly p99.
- **Percentiles hide *how* bad the tail is.** p99 = 1s tells you nothing about whether p99.9 is 1.1s or 60s.
  Quote a pair (p99 **and** p999) when the tail matters.
- **Coordinated omission** — a load generator that waits for a response before sending the next request
  *stops measuring* during a stall, silently deleting the worst samples. Use open-loop / fixed-rate load.

## 🌐 Design consequences (why an engineer cares)
- **SLOs are written in percentiles** ("p99 < 200ms"), never in means. An error budget is defined against
  that percentile.
- **Reduce fan-out or hedge it.** *Hedged requests*: after waiting p95, send a duplicate to a second replica
  and take whichever answers first — costs a few % extra load, cuts the tail hard.
- **Load-test with a realistic distribution.** Uniform-random keys understate tail latency badly; pair this
  with [Zipfian access skew](zipfian_distribution.md) — hot keys are where the tail lives.
- **Latency and utilization are linked** — the tail explodes as a server saturates. See
  [utilization & queueing](utilization_and_queueing.md).

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. Define p99, and say why it's reported instead of the mean.</b></summary>

p99 = the latency below which 99% of requests complete. Latency is heavy-tailed, so the mean is simultaneously dragged by outliers *and* hides them — it describes a request nobody actually made. Percentiles describe real experiences.
</details>

<details><summary><b>2. A request fans out to 100 services in parallel and waits for all. Each meets its p99. What fraction of users see a p99+ response?</b></summary>

`1 − 0.99^100 ≈ 63%`. The response takes the **max** of the fan-out, so the service-level p99 becomes roughly the user-level p50. Tail latency compounds with fan-out.
</details>

<details><summary><b>3. Why can't you average the p99s of ten servers to get the fleet p99?</b></summary>

Percentiles don't compose linearly — they're order statistics, not sums. You must merge the underlying **histograms** (t-digest / HDR) and compute the percentile once over the combined distribution.
</details>

<details><summary><b>4. What is coordinated omission?</b></summary>

A closed-loop load generator waits for each response before issuing the next request, so during a stall it *stops sampling* — the worst latencies are never recorded and the measured tail is fictitiously good. Fix: open-loop / fixed-rate load generation.
</details>

<details><summary><b>5. Name one concrete technique for cutting tail latency without making the backend faster.</b></summary>

**Hedged / backup requests** — after waiting ~p95, fire a duplicate to another replica and take the first response. Small extra load, large tail reduction. (Also: reduce fan-out width, or return partial results on timeout.)
</details>

<details><summary><b>6. Why does "1% of requests are slow" understate the problem?</b></summary>

p99 is per *request*, not per *user*. A user session making 100 requests has a ~63% chance of hitting at least one p99 response — so the "1% case" is something most users experience routinely.
</details>
