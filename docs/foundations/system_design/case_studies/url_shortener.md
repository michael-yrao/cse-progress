# 🏢 Case Study: URL Shortener (TinyURL)

> **Session log:** steps 1–2 banked **Jul 20, 2026** (bonus, alongside the `framework.md` build).
> **Sun Aug 2, 2026 — lane ③: scale-arithmetic gate cleared, step 3 (API) derived, click-event entity found.**
>
> **Sun Aug 9, 2026 — lane ③: BOTH GATES CLEARED.** ✅ Scale reconciled (100/10k, now *derived* from a
> stated premise rather than asserted) · ✅ short-code generation settled end to end — 6 characters,
> global counter + block allocation, bijective scramble. See the two sections below.
>
> 🔜 **NEXT SESSION STARTS HERE — step 4, the HLD.**
>
> ⚠️ **Step 4 was opened Aug 9 and deliberately stopped.** The learner hit the floor on the *diagramming
> notation itself* — *"I don't know how to draw this at all"*, then *"I do not recall anymore"* — and the
> coach started supplying boxes. Called as a teaching session and halted rather than pushed into a bad rep.
> **So this is a named gap, not an assumption. Open the next session with the notation, before asking for
> any design output:**
> - **a box** = something that runs and can fail independently (app server, database, counter service, client)
> - **an arrow** = a request, pointing caller → callee, labelled with what's asked
> - **draw one path at a time**, left to right: client on the left, wherever the data lives on the right
> - the naive read path is three boxes — `Client → App Server → Database` — and that is a *complete,
>   correct* HLD. Boxes get added only when a **number** forces one.
>
> Tooling: **Excalidraw** for the whiteboard motion (it's what many companies actually use); **Mermaid**
> in this file for the durable copy.
>
> ⚠️ **This will be the design's THIRD sitting, which is one too many.** A resumed design cannot be rated
> as a cold rep. **Land step 4, rate the row on HLD reasoning, and push step 5 deep dives to a separate
> row** — do not carry the same rep into a fourth session.
>
> **Two HTTP clusters are still owed and should be pulled in when step 4 hits them:** `304`/`ETag`/
> `Cache-Control` at the caching layer, and `429`-vs-`503`-vs-`500` if a rate limiter appears.
> *(`GET` vs `POST` semantics and method idempotency were pulled in Aug 9 — closes **N21** in the
> networking card's open list.)*
>
> ⚠️ **Do not open [`templates/case_study_template.md`](../templates/case_study_template.md) today.**
> Its worked example *is* a URL shortener — storage choice, KGS, cache tier and the full diagram are
> all pre-filled. This file carries the template's *structure* with the example content stripped.

---

## 1. Requirements — *what must it do, and how well?* ✅ *(banked Jul 20)*

### Functional
* [ ] Given a long URL, return a short alias.
* [ ] Given a short alias, redirect to the original long URL.

### Non-functional
* **Scale:** ~**100 write QPS**, ~**10k read QPS** — read-heavy, **100:1**. ✅ *(reconciled Aug 9 — the
  Jul 20 line said 1k/100k; see the derivation below. **The ratio is the requirement; the rates are
  derived from a premise.**)*
  > **The premise, stated so it can be attacked:** ~**100M DAU**, of whom **~1 in 10 creates a link on a
  > given day**, one link each → **10M writes/day** → `10⁷ / 10⁵ s` = **100 write QPS**; ×100 = **1B
  > reads/day** = **10k read QPS**.
  > **Where it breaks:** a shortener's population is overwhelmingly *clickers*, not creators — if the
  > creator fraction is really 1% rather than 10%, writes drop another 10× and the whole storage story
  > shrinks with it. 10% is the generous end and is deliberately chosen as the *upper* bound.
* **Data is immutable** once written → cache-first, replicas behind.
* **Availability / consistency:** _(state it, with the condition — see Quantify & Qualify)_

---

## 2. Core Entities — *the nouns* ✅ *(banked Jul 20; **`ClickEvent` added Aug 2**)*

* **`URL`** — `{ shortCode, longUrl, createdAt, ownerId, expiresAt }`
* **`ClickEvent`** — `{ shortCode, ip, accessedAt, userAgent }` ⬅ **derived Aug 2, and it changes the design**

**Why the second entity matters more than it looks.** It was found by asking what the *read* path needs to
record, and the answer doesn't fit on the `URL` row: a URL has **one** creation and **many** accesses. The two
datasets then turn out to have almost nothing in common —

| | `URL` mappings | `ClickEvent` log |
|---|---|---|
| Shape | key → value | append-only event stream |
| Write rate | 100/sec | **10,000/sec** (every read makes one) |
| Ever updated? | rarely | never |
| 5-year size | ~4 TB | **~180 TB** |

**The analytics data is ~40× the product data.** That's the fork the whole design hangs on, and it is
*created by a decision*, not given: 302 (below) is what makes every read generate a durable write.

---

## 🔢 Scale arithmetic — ⚠️ **GATE: speak this aloud before step 3** ✅ *(cleared Aug 2)*

*(The Jul 26 rate-limiter mock skipped this step entirely. Numbers, not adjectives.)*

✅ **RECONCILED Aug 9, 2026 — these Aug 2 numbers stand, and now have a premise behind them.** The Jul 20
line (1k/100k) was retired. Nothing below needed recomputing.

> **How it was settled, because the method matters more than the number.** Three quantities were asserted
> independently — read rate, write rate, and the ratio — and **only two of those are free**: fix any two
> and the third is determined. The ratio (100:1) was the actual *requirement*, so it was held; then one
> rate was **derived from a stated premise** (100M DAU × ~10% creating a link/day) instead of picked.
> **An asserted number is what gets probed in an interview; a derived one comes with its own defence.**

Working shortcuts worth keeping: **a day ≈ 100k seconds** (86,400, rounded for mental math) and
**a year ≈ 31.5M seconds**. Round early; order of magnitude is the deliverable.

* **Writes/day → QPS:** 100 writes/sec × 100k sec = **10M new URLs/day**
* **Reads/day → QPS:** 10,000 reads/sec × 100k sec = **1B reads/day** *(10⁴ × 10⁵ = 10⁹ — an exponent slip
  here cost a factor of 1000 on the first pass; add the exponents rather than the zeros)*
* **Storage over 5 years:** 10M/day × ~1,800 days ≈ **15B rows** × 256 B/row ≈ **~4 TB**
  → *five years of the entire product fits on one commodity disk. Sharding for **capacity** is not why.*
* **Click-event storage:** 1B/day × ~100 B ≈ **100 GB/day** ≈ **~180 TB over 5 years**
* **Short-code length:** ✅ **6 characters** *(derived Aug 9)*. Alphabet = 62 (`a-z A-Z 0-9`), so supply is
  `62ⁿ`. Ladder it, rounding 62→60 for mental math: `3.8k · 230k · 14M · 900M · **57B**` → **n = 6**.
  **56.8B supply against 18B demand ≈ 3× headroom.** *(Real services ship **7** — that buys horizon for
  growth or a longer TTL, not sufficiency.)*
* **Read bandwidth / cache working set:** ⬅ **STILL BLANK.**

---

## 🔑 Short-code generation — ✅ *(gate cleared Aug 9, 2026)*

**The reduction that makes this easy:** a 6-char code is just a number in base 62, and base-62 conversion
is one-to-one. So *"give every write a unique code"* becomes **"give every write a unique number below
56.8B."** Every technique below is a different answer to that one question.

### The four standard techniques

| | How | Uniqueness | Main cost |
|---|---|---|---|
| **1. Counter + base62** ⬅ **chosen** | encode `counter++` | by construction | needs a coordination point |
| **2. Hash + truncate + check** | `md5(longUrl)` → first ~36–43 bits → encode; collision ⟹ salt & retry | probabilistic, must check | **a DB read before every write**; dedups identical URLs for free |
| **3. Key Generation Service (KGS)** | pre-generate all keys offline into an "unused" table; servers claim batches | by construction | a whole extra service + key table to run and keep HA |
| **4. Snowflake ID + base62** | timestamp + machine ID + sequence | by construction, **zero coordination** | **~11 characters** |

### Why #1, and the two follow-ups that always come

**Snowflake was derived first in this session and then rejected on length** — and that rejection is the
real insight, worth saying out loud in an interview:

> **Snowflake buys coordination-freedom with length; a counter buys shortness with a coordination point.**

A 63-bit Snowflake ID (41 timestamp + 10 machine + 12 sequence) is `2⁶³ ≈ 9.2×10¹⁸`, which needs
`63 / log₂62 ≈ 11` characters. Those bits go to machine identity and clock precision — the price of
never talking to anyone. With a 6-character budget you cannot afford them, so you pay coordination instead.

**Follow-up 1 — "a central counter is a SPOF and a bottleneck."** Answer both halves honestly:
- **Bottleneck: weak at this scale, and say so.** 100 writes/sec against a Redis doing 100k+ ops/sec is
  0.1% of one instance. Claiming a throughput problem here invites *"what's the number?"* The real cost is
  **coupling** — a network round trip on every write, and every app server depending on one component.
- **SPOF: strong.** Counter dies ⟹ **100% of writes stop**, while reads are untouched (a redirect never
  consults it). And naive failover is *worse than the outage*: a lagging replica promoted to primary
  **reissues values already handed out** ⟹ duplicate codes silently overwriting each other's URLs. Avoiding
  that needs synchronous replication, which puts the latency back on every write.

**→ Block allocation.** A server buys values in bulk instead of one at a time:

1. Server needs codes → asks the counter service once: *"give me a block."*
2. Service atomically does `counter += 10000`, returns the previous value → server owns `5,000,000–5,009,999`.
3. Server issues from that range **out of local memory** — zero network calls per write.
4. Block exhausted → ask for the next one.

⚠️ **There is still exactly ONE counter.** Servers get **disjoint ranges from it**, not counters of their
own — independent counters would collide immediately. The service's entire API is *"atomically add the
block size and return the previous value"*, so its whole state is **a single integer that only ever goes
up**. One number, one operation, no logic: cheap to persist and easy to reason about.

**What it actually buys** — the failure-mode downgrade is the headline, not the throughput:

| | Per-write counter | Block allocation |
|---|---|---|
| Coordination | every write | once per 10,000 writes |
| Counter service down | **all writes stop** | writes continue from held blocks |
| Server crashes mid-block | — | values never issued = **a gap** |
| Worst case | **duplicate codes (corruption)** | **wasted codes (harmless)** |

Gaps cost nothing — there are 56.8B codes and 3× headroom. Duplicates corrupt data. **Trading a
correctness failure for a harmless one is the move.**

**Follow-up 2 — "sequential codes are enumerable."** `aaaaab`, `aaaaac`… and someone scrapes every URL in
the system. Fix: a **bijective scramble** before encoding — multiply by a large odd constant mod the code
space (odd ⟹ coprime with 2ᵏ ⟹ invertible), or a small Feistel network. Note *where* this belongs: it does
**not** create uniqueness, it **hides the ordering** of uniqueness you already have.

---

## 3. API / Interface — *the contract* ✅ *(derived Aug 2)*

| Method | Path | Request | Response | Notes |
|---|---|---|---|---|
| `POST` | `/urls` | `{ longUrl }` | `201` + `{ shortCode }` | error → an HTTP status, **not** a `None` return — this is a wire protocol, not a function call |
| `GET` | `/{shortCode}` | — | **`302`** + `Location: <longUrl>` | the browser follows it automatically; that's why a short link works pasted into any address bar |

**The response is a redirect, not a body.** You don't hand the long URL back as JSON for the client to
parse. The status code *is* the answer, and picking it is a design decision — see the 301/302 fork below.

---

### 🔑 301 vs 302 — the decision that creates the 180 TB

The only mechanical difference: **does the client remember the answer?**

```
Alice clicks short.ly/abc a second time…

  sent 301 (Permanent):  browser → cnn.com          ← your server never hears about it
  sent 302 (Found):      browser → your server → cnn.com   ← you see every click
```

**Chosen: 302.** Two reasons, and the second is the one people forget:

1. **Analytics.** Click data *is* the product for a shortener; 301 makes repeat clicks invisible.
2. **Control — you can't take a 301 back.** Once a browser has cached `abc → cnn.com` permanently, you
   cannot expire the link, repoint it, or kill it if it turns out to be malware. For that user, on that
   browser, it is baked in.

**What it costs:** 301 would have let you serve a small fraction of 10k rps. 302 means you serve all of it
**and** generate the 10k writes/sec click firehose. The "read-heavy 100:1 system" is therefore *also* a
10k-writes/sec system — self-inflicted, deliberately.

> **The general form, and it recurs all over this design:** *every layer that answers on your behalf saves
> you load and costs you control.* Browser caches, CDNs, read replicas — same trade each time.

**⏭️ Parked for the deep dive:** the user is *waiting* on their redirect. Should they wait on your analytics
write? That's where queues enter this design — open it cold next session.

---

## 4. High-Level Design — *boxes and arrows that satisfy the API* ⏳ **START HERE NEXT SESSION**

*(HLD altitude: boxes + arrows + request flow. If you're describing what's **inside** a box —
schema fields, data structures, persistence config — that's step 5. Park it.)*

⚠️ **Do the short-code generation fork first** (see the header) — the write path grows a box, or doesn't,
depending on whether codes come from a counter, a hash, or a pre-generated pool.

**Write path:**

**Read path:**

---

## 5. Deep Dives — *defend it, break it, scale it*

---

## ⚖️ Key Design Decisions & Tradeoffs (defend every fork)

*trigger → what you chose → one-line why → where it breaks at 10×*

| Fork | Chosen | Why (the deciding question) | Where it breaks at scale |
|------|--------|-----------------------------|--------------------------|
| Redirect status code | **302 Found** | *"do we need to see the click?"* — analytics is the product, and a 301 can never be repointed or expired | Serves 100% of 10k rps **and** generates 10k writes/sec of click events (~180 TB / 5 yr). A 301 would erase most of both |
| One store or two | **Two** | *"does a URL have one of these, or many?"* — one creation vs. many accesses; 100/sec KV vs. 10k/sec append-only, 40× the volume | Forcing them together makes the small, hot, cacheable lookup share infrastructure with a firehose |

---

## ❓ Anticipated Follow-up Questions (rehearse the defense)

* **Failure:** What happens when [component] dies? →
* **10× scale:** Which piece saturates first, and the fix? →
* **Race:** Two writers hit [resource] at once? → (idempotency / locking)
* **Why this, not the alternative?** →

---

## 🗺️ Macro System Visual Map

```mermaid
graph TD
```
