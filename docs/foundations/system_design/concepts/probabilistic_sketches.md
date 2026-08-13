# Probabilistic Sketches — HyperLogLog & Count-Min

> 🧊 **Frozen reference (Aug 13, 2026).** The SD track is now mock interviews on HelloInterview's
> board; this card is no longer drilled and has no tracker row. Any "owed a sprint / next lane"
> language below is historical. Use it as lookup when a mock debrief points here.
> See [`../study_guide.md`](../study_guide.md).

> **Role:** Approximate counting in tiny, fixed memory · **Family sibling:** [Bloom filter](bloom_filter.md) (membership) — same trade, different question.
> **You'll want this when:** the design needs **"how many unique X"** or **"which X are trending"** at a scale where an exact map obviously won't fit in RAM.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **Three questions about a stream, three sketches, one trade: give up exactness, get fixed sublinear memory and mergeability.**

| Question | Exact cost | Sketch | Error shape |
|---|---|---|---|
| "Have I seen X?" (membership) | hash set of all keys | **[Bloom filter](bloom_filter.md)** | never false-negative; may false-**positive** |
| "How many *distinct* X?" (cardinality) | set of all keys | **HyperLogLog** | ~±1–2% relative, two-sided |
| "How often did X occur?" (frequency) | counter per key | **Count-Min Sketch** | never under-counts; may **over**-count |

Three facts that make the family worth learning as a family:

| Fact | What you get | What it costs |
|---|---|---|
| Memory is **fixed and tiny**, independent of stream size | count billions in kilobytes | answers are estimates, with a tunable error bound |
| Errors are **one-sided** (Bloom, CMS) or **bounded relative** (HLL) | you know which way you're wrong, so you can design around it | you must never use them where exactness is contractual |
| Sketches **merge** — combine two sketches into one for the union | per-shard sketches roll up into a global answer with no reshuffle | merging must be the *right* operation (max, sum) per sketch |

**Mergeability is the underrated one.** It's what makes these work in a distributed system: every shard
keeps a local sketch, and the union is a cheap combine — no data movement, no coordination.

## 🔢 HyperLogLog — count distinct
**The core trick:** hash each item to a uniform random bit string. In a uniform stream, a hash starting
with `k` leading zeros appears about once every `2^k` distinct items. So **track the maximum run of
leading zeros you've ever seen** — if it's 10, you've probably seen ~`2^10` distinct items.

That single estimator is wildly noisy (one lucky hash ruins it), so HLL splits the hash: the first `p`
bits pick one of `m = 2^p` **registers**, and the rest supplies the leading-zero count for *that*
register. Each register holds its own max. Combine all `m` estimates with a **harmonic mean** (which
suppresses outliers) and apply a bias correction.

- **Accuracy:** standard error ≈ `1.04/√m`. Redis uses `m = 16384` → **0.81% error in ~12 KB**, for
  cardinalities up to 2^64. That number is worth memorizing: *billions of uniques, 12 kilobytes.*
- **Duplicates are free** — re-adding an item can't raise a max it already set, so the estimate is
  idempotent. This is why it works on a firehose with no dedup step.
- **Merge = element-wise max** of the register arrays. Perfectly associative → per-shard, per-hour HLLs
  roll up into any time range or any fleet-wide total.
- **API you'll cite:** Redis `PFADD` / `PFCOUNT` / `PFMERGE`.

**Uses:** unique visitors / DAU-MAU, distinct search terms, unique IPs hitting an endpoint, distinct
users per feature — anywhere the *identity* of the uniques doesn't matter, only the count.

## 📊 Count-Min Sketch — estimate frequency
**Structure:** a `d × w` grid of counters, with `d` hash functions (one per row).
- **Increment(x):** for each row `i`, `grid[i][h_i(x)] += 1`.
- **Query(x):** return `min` over rows of `grid[i][h_i(x)]`.

**Why `min`:** collisions only ever *add* other keys' counts into your cell, so every row is an
**overestimate**. The smallest row is the least-polluted one — taking the min is taking the tightest
upper bound. Hence: **never undercounts**, may overcount. (Same one-sided-error logic as the Bloom filter,
which is why they're worth learning together.)

- **Sizing:** `w = e/ε`, `d = ln(1/δ)` for error `≤ ε·N` with probability `1−δ`. Practical reading: wider
  = tighter estimate, deeper = higher confidence.
- **Merge = element-wise sum** of the grids.
- **Heavy hitters / top-K:** CMS alone can't *enumerate* the top keys (it only answers about a key you
  name). Pair it with a small **min-heap of candidates** — update the sketch, then check whether the
  estimate beats the heap's minimum. That pairing is the standard "top-K trending" answer.

**Uses:** trending topics, per-key rate limiting at scale, hot-key detection (the flip side of
[Zipfian skew](zipfian_distribution.md)), network flow monitoring.

## ⚠️ Gotchas
- **Skew hurts CMS.** Under [Zipfian](zipfian_distribution.md) traffic, rare keys collide with the
  monster head key and get badly inflated — the estimate is good for heavy hitters, poor for the tail.
  (Count-Min with *conservative update* helps.)
- **HLL is bad at small cardinalities** without correction — real implementations switch to a sparse/exact
  representation under a threshold and only convert to dense registers later.
- **Never use these where exactness is contractual** — billing, financial ledgers, "you have 3 items in
  your cart," legal/compliance counts. The interviewer is checking that you know the boundary.
- **"Approximate" must be stated as a tradeoff you chose**, with the error number attached — "0.81% error
  for 12 KB instead of gigabytes" is a design decision; "roughly" is hand-waving.

## 🌐 Where this shows up in a design
Top-K / trending · analytics dashboards (unique visitors) · web crawler seen-URL set (Bloom) · cache
penetration guard (Bloom) · hot-key detection ahead of resharding · rate limiting billions of keys.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. Name the three sketches, the question each answers, and the direction of each one's error.</b></summary>

**Bloom filter** — membership ("seen X?"); never false-negative, may false-positive. **HyperLogLog** — cardinality ("how many distinct?"); bounded relative error (~1%), two-sided. **Count-Min Sketch** — frequency ("how often is X?"); never undercounts, may overcount.
</details>

<details><summary><b>2. What is HyperLogLog's core trick?</b></summary>

Hash items uniformly; a hash with `k` leading zeros shows up roughly once per `2^k` distinct items, so the **max leading-zero run** estimates cardinality. Split the hash across `m` registers and combine with a **harmonic mean** to kill the variance of a single noisy estimator.
</details>

<details><summary><b>3. Roughly how much memory for billions of uniques, at what error?</b></summary>

~**12 KB** for ~**0.81%** standard error (Redis: 16384 registers; error ≈ `1.04/√m`). Memory is fixed regardless of stream size.
</details>

<details><summary><b>4. Why does Count-Min take the MIN across rows?</b></summary>

Collisions can only add other keys' counts into a cell, so every row overestimates. The minimum row is the least-contaminated, i.e. the tightest upper bound — which makes the error strictly one-sided (never undercounts).
</details>

<details><summary><b>5. Why is mergeability the property that matters in a distributed system?</b></summary>

Each shard keeps a local sketch and the union is a cheap element-wise combine (HLL = **max**, CMS = **sum**, Bloom = **OR**) — so you get a global answer with no data movement, no coordination, and roll-ups across any time range or fleet subset.
</details>

<details><summary><b>6. Count-Min gives frequency for a key you name. How do you get the top-K list?</b></summary>

Pair it with a small **min-heap of candidate keys**: on each update, query the sketch and, if the estimate beats the heap minimum, insert/replace. Sketch supplies counts; heap supplies the ranking.
</details>

<details><summary><b>7. Where must you refuse to use these?</b></summary>

Anywhere exactness is contractual — billing, financial ledgers, compliance counts, small user-visible counts. Also note CMS degrades for *tail* keys under Zipfian skew (heavy hitters stay accurate).
</details>
