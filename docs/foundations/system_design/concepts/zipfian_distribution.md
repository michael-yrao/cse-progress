# Zipfian Distribution (power-law access skew)

> **Role:** Math/probability foundation — *why* real-world access is skewed · **Filed under:** SD concepts (it underpins caching, sharding, load).
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Rank things by popularity and frequency falls off like 1/rank — so a tiny head carries most of the volume.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it means |
|---|---|---|
| Frequency ∝ **1/rank^s** (a power law) | popularity **collapses** toward the head, doesn't taper gently | #1 dwarfs #100 dwarfs #10,000 |
| A **small prefix of ranks** holds most of the total volume | a small hot set serves most requests → caching/CDN/replicas work | "80/20", often steeper (90/10, 95/5) |
| It arises from **preferential attachment** ("rich get richer") | it's the *default* shape, not an exception | shows up in reads, words, cities, links, wealth |

## 🎯 In one line
Empirically, item request frequency is inversely proportional to popularity rank (`freq ∝ 1/rank`), so
the most popular handful of items absorbs the overwhelming majority of traffic — the statistical law that
makes a **small cache** catch a **large fraction** of reads.

## 📉 The shape
| Rank | Relative request rate (∝ 1/rank) |
|------|-------------|
| 1 | 1.0 |
| 2 | 0.50 |
| 3 | 0.33 |
| 10 | 0.10 |
| 100 | 0.01 |
| 100,000 | 0.00001 |

The #1 item pulls ~100,000× the traffic of the #100,000 item. Summing the rates, a **small prefix of
ranks holds most of the total volume** while the millions of tail items contribute almost nothing even
in aggregate.

- **Tiny check:** 10 items, rate ∝ 1/rank → rates `1, .5, .33, …` sum ≈ 2.9. Top **2** items (1 + .5)
  already carry **~51%** of all traffic — 20% of items, half the requests.
- **The `s` exponent sets the steepness.** `s=1` is classic Zipf; `s>1` concentrates harder (a bigger
  head), `s<1` flattens toward uniform. Real catalogs vary; often `s≈0.7–1.2`.

## ⚠️ Honest caveats (state these when you invoke it)
- The exact "top 1% = 90%" figure depends on the **exponent** and on **time** — trending/seasonal spikes
  concentrate access further; a cold catalog is flatter. So "**95% hit ratio**" is a **modeling
  assumption to state and defend**, not a law.
- **Adversarial or batch access breaks it.** A scraper walking the whole catalog, or a report scanning
  every row, is *uniform* access — the skew (and the cache's value) evaporates.

## 🌱 Why 1/rank happens (generative story)
**Preferential attachment / "rich get richer":** popular items get seen, shared, linked, and recommended
more, which makes them *more* popular — a positive feedback loop on attention. Such loops produce
power-law (heavy-tailed) distributions across wildly different domains: word frequencies (Zipf's
original), city populations, web in-links, wealth, GitHub stars.

## 🌐 Design consequences (why an engineer cares)
- **Caching / CDN / read-replicas** all *bet on this skew* — a small hot set fits in fast storage and
  serves most reads. **No skew → they buy nothing.** (See [caching §Pillar 1](../components/caching.md).)
- **Hot-key / hot-shard problem** — the flip side: the head is *so* hot it can overwhelm the single
  shard/replica that owns it. Zipf is *why* naive hash-sharding still gets hot shards; mitigations =
  replicate the hot key, split it, or add a small per-node cache in front.
- **Load testing must model it** — uniform-random load *understates* tail latency and hot-key contention
  vs. real Zipfian traffic. Test with a realistic popularity distribution.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. State the Zipfian relationship in one line.</b></summary>

Rank items by popularity; request frequency ∝ 1/rank (a power law) — the head dwarfs the tail.
</details>

<details><summary><b>2. Why does this make a small cache effective?</b></summary>

Because a small prefix of ranks carries most of the *total request volume*. A cache holding just the hot set (a sliver of the catalog) still serves a large fraction of reads — hit ratio tracks access skew, not cache/catalog size.
</details>

<details><summary><b>3. What is NOT true if access is uniform?</b></summary>

Then there's no hot set — a small cache catches almost nothing, and caching/CDN/replicas buy you nothing. Skew is the load-bearing assumption.
</details>

<details><summary><b>4. Why is "95% hit ratio" an assumption, not a fact?</b></summary>

The concentration depends on the Zipf exponent (steepness) and on time (trending spikes). Adversarial/batch access (a scraper) flattens it to uniform. State it and defend it; don't assert it as a law.
</details>

<details><summary><b>5. Where does the 1/rank shape come from?</b></summary>

Preferential attachment — "rich get richer": popular things get more exposure, which makes them more popular. Feedback loops on attention produce power laws (words, cities, links, wealth).
</details>

<details><summary><b>6. Name the flip-side problem Zipf causes in a sharded system.</b></summary>

The **hot-key / hot-shard** problem — the head is so hot it can overload the single shard/replica owning it. Mitigate by replicating/splitting the hot key or caching it per-node.
</details>
