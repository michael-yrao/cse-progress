# Bloom Filter

> **Role:** Probabilistic set-membership gate · **Rivals on the fork:** exact hash set (accurate, big), counting Bloom / cuckoo filter (deletable)
> **Also a DSA data structure** — cross-referenced from the SD [caching](../components/caching.md) penetration guard.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **A Bloom filter is a "definitely-no / maybe-yes" membership test that trades a little accuracy for a lot of space.**

Three facts. Everything else on this page is a consequence of one of them.

| Fact | What you get | What it costs |
|---|---|---|
| Answers are **one-sided** — "definitely not present" or "maybe present" | a cheap gate that can *reject* with certainty | it can never *confirm* — a "maybe" still needs the real store |
| Bits only flip **0→1**, never back | **never false-negative** → safe to block on "definitely no" | can't delete; false-positive rate only *grows* as you add keys |
| Stores **a few bits per key**, not the keys | fits a huge set in tiny RAM (the whole reason to use it) | you accept a tunable false-positive rate for that saving |

Everything below (k hashes, optimal k, counting variant) is **tactics for living with those three facts.**

## 🎯 In one line
A bit array + k hash functions that answers *"is this key possibly in the set?"* in `O(k)` time and a
few bits of space per key — with **no false negatives** and a **tunable false-positive rate**. It's the
space-efficient stand-in for a whitelist you can't afford to store exactly.

## 🧠 Core mechanics
**Structure:** a bit array of `m` bits (all 0) + `k` independent hash functions, each mapping a key → a
position in `[0, m)`.

- **Insert(key):** hash with all k functions → set those k bits to 1.
- **Query(key):** hash with all k functions → check those k bits.
  - any bit **0** → **definitely not in the set** (an insert would have set all k) → **reject**.
  - all bits **1** → **maybe in the set** → proceed to the real store.

**Trace** (`m=10, k=2`):
```
Insert A → bits 2,5 = 1
Insert B → bits 5,8 = 1
Array:     [0 0 1 0 0 1 0 0 1 0]
Query A  → 2,5 both 1 → "maybe" ✓ (present)
Query X  → 3,7 → bit 3 is 0 → "definitely not" ✓ (rejected)
Query Y  → 2,8 both 1 (set by A,B) → "maybe" ✗ FALSE POSITIVE (Y never inserted)
```

## 🔒 The one-sided error (the load-bearing property)
- **Never false-negative** — bits only flip 0→1, so an inserted key's k bits stay 1 forever; a real key
  *always* passes. This is why it's safe to *reject* on "definitely no": you can never wrongly reject a
  real member. (If false negatives were possible, a penetration guard would drop real products — a
  correctness bug.)
- **May false-positive** — a fake key's k bits can all coincidentally be set by *other* keys' inserts.
  The rate rises as the array fills. Harmless in a gate: the fake just falls through to the normal path.

## ⚙️ Why k hash functions? (the U-shape)
One hash = 1 bit per key = a coarse fingerprint (easy collisions). **k hashes = a k-bit *signature*;** a
false positive needs **all k** bits set → probability ≈ `p^k` (p = fraction of bits set), which shrinks
fast. But more hashes also set *more* bits per insert → the array fills → `p` climbs → past a point
false positives rise *again*. So false-positive rate is a **U-shape in k**, not "more is better."

- **Concrete** (`p = ½`): k=1 → 50% · k=3 → 12.5% · k=5 → ~3%.
- The lever that **monotonically** lowers the rate is bigger **m** (more memory). `m` sets the budget;
  **k is tuned to m**, not maximized.

**Optimal `k = (m/n)·ln 2`** (m bits, n keys) — at which point exactly **half the bits are set** (max
information per bit).

<details><summary><b>Derivation (the clean symmetry argument)</b></summary>

1. P(a given bit still 0 after n inserts) = `(1 − 1/m)^(kn) ≈ e^(−kn/m)`. Fraction set `p = 1 − e^(−kn/m)`.
2. False-positive rate `FP(k) = p^k = (1 − e^(−kn/m))^k`.
3. Minimize. Let `a = n/m`; minimize `L = ln FP = k·ln(1 − e^(−ak))`.
   `L'(k) = ln(1 − e^(−ak)) + k·a·e^(−ak)/(1 − e^(−ak))`. Set = 0.
   Substitute `x = e^(−ak)` (so `ak = −ln x`) and multiply by `(1 − x)`:
   `(1 − x)·ln(1 − x) = x·ln x`. **Symmetric under `x ↔ 1−x`** → solution `x = ½`.
   So `e^(−ak) = ½` → `ak = ln 2` → **`k = (m/n)·ln 2`**; `x = ½` = "half the bits set."
</details>

## 🚨 Gotcha & variants
- **Can't delete** from a standard Bloom filter — clearing a bit might unset one shared with another key
  → false negative. For changing sets, **rebuild periodically** or use a **counting Bloom filter** (each
  slot a small counter, increment on insert / decrement on delete).
- **Cuckoo filter** — a modern alternative that supports deletion and often better space at low FP rates.

## ⚖️ Decision rationale
- **Reach for it when:** you need cheap membership on a huge set, "no" must be trustworthy, and an
  occasional false "maybe" is harmless because a real store backs it — penetration guards, dedup, DB
  read-avoidance.
- **Prefer the alternative when:** you need exact answers (use a real set/DB), you must delete freely
  (counting Bloom / cuckoo), or the set is small enough that exact storage is cheap anyway.
- **Tradeoff accepted:** a tunable false-positive rate + no deletion, for order-of-magnitude space savings.

## 🌐 Where it recurs
Penetration guards ([caching](../components/caching.md)) · dedup ("have I seen this URL?") · DB read
avoidance (Cassandra/HBase check a per-SSTable Bloom filter before touching disk) · spell-checkers ·
any "reject the obviously-absent *cheaply*" gate in front of an expensive lookup.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. What question does a Bloom filter answer, and what are the two possible answers?</b></summary>

"Is this key *possibly* in the set?" → **"definitely not present"** (certain) or **"maybe present"** (uncertain, check the real store).
</details>

<details><summary><b>2. Why can it never give a false negative?</b></summary>

Bits only flip 0→1, never back. An inserted key's k bits stay 1 forever, so a real member always passes. That's why rejecting on "definitely no" is safe.
</details>

<details><summary><b>3. Where does the false positive come from?</b></summary>

A key that was never inserted can have all k of its bits already set to 1 by *other* keys' inserts (collisions). The rate rises as the array fills.
</details>

<details><summary><b>4. Why use k hash functions instead of 1? What breaks if k is too large?</b></summary>

k hashes make a k-bit signature → a false positive needs all k bits set (≈ p^k), far rarer than one bit. But more hashes set more bits per insert, filling the array (p→1) → false positives climb again. It's a U-shape; tune k, don't maximize it.
</details>

<details><summary><b>5. What's the optimal k, and what's true of the array at that point?</b></summary>

`k = (m/n)·ln 2` (m bits, n keys). At the optimum exactly **half the bits are set** — max information per bit. The lever that monotonically lowers FP is bigger m; k is tuned to m.
</details>

<details><summary><b>6. Can you delete from a Bloom filter? What if you need to?</b></summary>

Not from a standard one (clearing a shared bit risks a false negative). Use a **counting Bloom filter** (per-slot counters) or a **cuckoo filter**, or rebuild periodically.
</details>

<details><summary><b>7. Name three real places Bloom filters show up.</b></summary>

Cache penetration guards; dedup / "seen this before?"; DB read-avoidance (Cassandra/HBase per-SSTable). (Also spell-checkers, web-crawler URL sets.)
</details>
