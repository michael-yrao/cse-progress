# 🏢 Case Study: URL Shortener (TinyURL)

> **Session log:** steps 1–2 banked **Jul 20, 2026** (bonus, alongside the `framework.md` build).
> **Sun Aug 2, 2026 — lane ③: scale-arithmetic gate cleared, step 3 (API) derived, click-event entity found.**
>
> 🔜 **NEXT SESSION STARTS HERE — two things, in this order:**
> 1. **⚠️ Reconcile the scale numbers (below).** Jul 20 banked 1k/100k QPS; Aug 2 re-derived 100/10k.
>    Same 100:1 ratio, **one order of magnitude apart.** Pick one and make it the note's number — 100k
>    read QPS and 10k read QPS argue for visibly different infrastructure, so every downstream claim
>    inherits this choice.
> 2. **Short-code generation — the signature question of this problem, and completely untouched.**
>    You know you need ~15B codes; you have not worked out how long a code must be to have that many,
>    nor **how to generate one that's unique without two concurrent writers colliding.** Counter+base62
>    vs. hash-and-truncate vs. a pre-generated key pool is the fork. Do this before step 4 — the HLD
>    grows a box (or doesn't) depending on the answer.
>
> Remaining: step 4 (HLD) and step 5 (deep dives) are untouched — realistically two more sessions.
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
* **Scale:** ~**1k write QPS**, ~**100k read QPS** — read-heavy, ~100:1.
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

⚠️ **These are the Aug 2 numbers and they are 10× below the Jul 20 line above — reconcile before reusing.**

Working shortcuts worth keeping: **a day ≈ 100k seconds** (86,400, rounded for mental math) and
**a year ≈ 31.5M seconds**. Round early; order of magnitude is the deliverable.

* **Writes/day → QPS:** 100 writes/sec × 100k sec = **10M new URLs/day**
* **Reads/day → QPS:** 10,000 reads/sec × 100k sec = **1B reads/day** *(10⁴ × 10⁵ = 10⁹ — an exponent slip
  here cost a factor of 1000 on the first pass; add the exponents rather than the zeros)*
* **Storage over 5 years:** 10M/day × ~1,800 days ≈ **15B rows** × 256 B/row ≈ **~4 TB**
  → *five years of the entire product fits on one commodity disk. Sharding for **capacity** is not why.*
* **Click-event storage:** 1B/day × ~100 B ≈ **100 GB/day** ≈ **~180 TB over 5 years**
* **Short-code length:** ⬅ **STILL BLANK.** alphabet ^ length ≥ 15B. Do this next session.
* **Read bandwidth / cache working set:** ⬅ **STILL BLANK.**

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
