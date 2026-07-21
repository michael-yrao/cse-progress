# The Delivery Framework — how to drive any SD interview

> *"Driving this framework fluently is 50% of the interview."* — [study_guide.md](study_guide.md) Tier 1 #4.
> This note is the reference you reread. The **skill isn't the six boxes — it's knowing, at each box,
> the one question that drives it and the fork it forces.** Memorizing the boxes is an afternoon.

## The spine (memorize this order)

```
1. Requirements        (functional + non-functional)   ~5 min
2. Core Entities       (the nouns — 2 min, don't overthink)
3. API / Interface     (one endpoint per functional req)  ~5 min
   ── Data Flow ──      (ONLY for data-processing systems — usually skip)
4. High-Level Design   (boxes + arrows that satisfy the API)  ~10-15 min
5. Deep Dives          (NFRs + interviewer probes drive these)  ~10 min
```

Estimation is **not a standalone box** — see the note under step 1. Time budget assumes a ~35–45 min interview.

---

## 1. Requirements — *what must it do, and how well?*

**Produces:** a short bulleted list, two headings. **Driving question:** *"Who uses this and what are the
top 2–3 things they do?"* — then *"how big, how fast, how consistent?"*

- **Functional (FRs)** — the verbs. *Users can shorten a URL; users can follow a short URL.* Keep it to the
  **core 2–3.** Explicitly de-scope the rest out loud ("I'll leave analytics/auth out unless you want them").
- **Non-functional (NFRs)** — the *qualities*, and the thing that actually drives the design: **scale,
  latency, availability, consistency, read/write ratio, durability.** *"100:1 read-heavy, <100ms redirect,
  HA, eventual consistency OK."*

**The #1 mistake:** rushing this or listing FRs without NFRs. **The NFRs are what force every later fork** —
a "read-heavy, eventual-consistency-OK" system and a "write-heavy, strongly-consistent" system with the same
FRs are *completely different designs.* Slow down here; it's the cheapest place to earn signal.

**On estimation (the one real divergence from Grokking):** HelloInterview's stance — **don't do a wall of
math upfront.** Do the arithmetic *inline, at the box where a number changes a decision* (e.g. compute
QPS when you're deciding whether one DB can take the write load; compute 5-yr storage when you're choosing
SQL vs NoSQL). A number that doesn't change a decision is theater. If the interviewer explicitly wants
upfront estimation, give it — otherwise defer it to where it earns its place. *(The guide's old step-2
"Estimation" box is folded into this rule.)*

## 2. Core Entities — *the nouns*

**Produces:** a 3–6 line list of the main objects and their key fields. **Driving question:** *"What are the
persistent things this system stores?"*

- These become your data model and the resources in your API. For a URL shortener: `User`, `URL` (shortCode,
  longUrl, ownerId, createdAt).
- **Spend ~2 minutes. Do not design the schema yet** — no partition keys, no indexes, no SQL-vs-NoSQL. Just
  name the nouns and their obvious fields. The DB choice is a **deep dive**, not here.

**The #1 time-sink:** designing the database in this step. Resist it. Naming entities early just gives your
API something to talk about; the storage fork comes later when the access patterns are visible.

## 3. API / Interface — *the contract*

**Produces:** one endpoint per functional requirement. **Driving question:** *"For each FR, what's the request
and the response?"*

- One-to-one with the FRs. Shorten → `POST /urls {longUrl} → {shortUrl}`. Follow → `GET /{shortCode} → 302
  Location: longUrl`.
- Prefer **REST** by default; reach for a different style only when a requirement forces it (real-time push →
  WebSocket/SSE; complex client-shaped reads → GraphQL). Say *why* if you deviate.
- **Security freebie:** never put anything the server should own in the request body. `createdBy` comes from the
  auth token, not the client payload — mentioning this is cheap senior signal.

**The #1 mistake:** designing endpoints that don't map to an FR (or missing an FR). The API is the checksum on
step 1 — if an FR has no endpoint, one of them is wrong.

## ── Data Flow (conditional — usually skip) ──

**Only insert this for data-*processing* systems** where moving/transforming data *is* the design: web crawler,
analytics/metrics pipeline, ad click aggregation, a search indexer. Write it as a numbered list of stages
(*ingest → queue → process → store → serve*).

**For request/response systems** (URL shortener, chat, feed, e-commerce) **skip it** — the high-level design
already shows the flow. Knowing *when to skip a step* is itself senior signal; don't perform a Data Flow box
just because it's on a list.

## 4. High-Level Design — *boxes and arrows that satisfy the API*

**Produces:** a component diagram — client, gateway/LB, app service(s), datastore(s), and the arrows between
them. **Driving question:** *"Walk each API call through the system — what does it touch?"*

- Build it **one API endpoint at a time.** Trace the write path, then the read path. Add a component only when
  a request needs it — don't pre-place a cache/queue/CDN "because scale." Justify each box by the call that
  needs it.
- Keep it **simple and correct first.** A clean design that plainly serves the API beats a busy one with a
  queue nobody uses. Scaling machinery is the *deep dive's* job.

**The #1 mistake:** jumping to a maximal architecture (cache + queue + CDN + shards) before the basic
request path is drawn. Draw the boring correct version, *then* let the NFRs pull in the machinery.

## 5. Deep Dives — *defend it, break it, scale it*

**Produces:** 2–4 focused deep dives, each resolving one NFR or interviewer probe. **Driving question (this is
the whole interview):** *"Where does this break, and what do I do about it?"*

Deep dives are driven by two things:
1. **Your own NFRs** — you said <100ms and 100:1 read-heavy → deep-dive the **cache** (which pattern,
   eviction, invalidation) and **read scaling** (replicas). You said HA → deep-dive **failover / single points
   of failure.**
2. **The interviewer's probes** — the questions in [study_guide.md](study_guide.md#L160):
   *"What happens when the DB dies? Behavior at 10×? Two users at the same instant? Why this DB not that one?"*

**For every deep dive, run the decision drill** ([study_guide.md](study_guide.md#L136)): name the **trigger**
(the NFR that forces it) → the **options** → the **deciding question** → **where your choice breaks at 10×.**
That last clause — naming your own design's failure mode before they ask — is the Staff signal.

**The #1 mistake:** deep-diving where it's easy instead of where it matters. The deep dive should hit the part
of *your* design that's under the most pressure from *your* NFRs, not the part you happen to know best.

---

## Quantify & Qualify — the habit that turns a claim into an answer

Two reflexes, applied at **every step**, separate a mid answer from a senior one. Neither adds a step;
both change *how you say every sentence.* This is the highest-leverage speaking habit in the interview.

**Quantify — put a number on every claim.** A number turns an assertion into reasoning the interviewer
can check. Every number you *volunteer* is a decision you've justified before being asked.

- ❌ "It's read-heavy." → ✅ "100:1 read:write — **~100k read QPS** vs **~1k write QPS**."
- ❌ "We need a cache." → ✅ "A cache at **~90% hit rate** drops DB reads from 100k to **~10k QPS** — one replica set serves that."
- ❌ "Storage gets big." → ✅ "100M/day × 500 B × 5 yr ≈ **900 GB**, **~1.8 B rows**."

**Qualify — put a condition and a boundary on every choice.** A choice without its conditions is a
guess; with them it's a defended decision. Name the **assumption** (what must be true), the **tradeoff**
(what you gave up), and the **boundary** (where it breaks and what you'd switch to).

- ❌ "Use eventual consistency." → ✅ "Eventual is fine *because* a 2-second-stale redirect is harmless — inventory or payments would force strong."
- ❌ "Shard by shortCode." → ✅ "Hash-shard on shortCode for even spread; holds while access is uniform — a viral link (hot key) breaks it, and I'd add a cache tier in front."

**The fusion — one sentence template to speak every decision:**

> **"I'll use [choice] because [quantified pressure]; it trades [X for Y] and holds while [condition] —
> it breaks at [scale/boundary], where I'd move to [alternative]."**

Say every fork this way and you hit quantify + qualify + the failure-mode signal in one breath.

**Per-step targets — what to reach for at each box:**

| Step | Quantify (the number) | Qualify (the condition) |
|------|-----------------------|-------------------------|
| Requirements | read/write QPS, storage/5 yr, payload size, read:write ratio | which NFR is the *hard* constraint vs a nice-to-have |
| Core entities | rough row size, row count | which fields are hot/queried vs cold |
| API | request rate & payload per endpoint | idempotency; what the server owns vs the client sends |
| High-level design | load each component absorbs (cache hit % → DB QPS), # servers, per-shard size | *why each box exists* — the call that needs it |
| Deep dives | replication lag, cache TTL, failover time, shard count | the assumption + boundary for **every** fork |

**The tell you're doing it:** you almost never say a bare adjective — *fast, big, scalable, heavy* — without
immediately following it with **the number that makes it true** and **the condition under which it holds.**

## The question-lenses — how to generate the interviewer's questions yourself

> ⚠️ **Provisional (synthesis, not a cited framework) — validate against Hello Interview's material
> Wed Jul 22.** This is *my* distillation, and a tidy list of 7 feels more authoritative than it is.
> If HI's rate-limiter deep-dive raises a question that fits none of these, that's a real gap → add it,
> then drop this banner. Several lenses already restate the probe list in [study_guide.md](study_guide.md#L160).

You don't invent design questions from experience — you **run a fixed checklist of lenses over every
component**, and the questions fall out. Experience makes running them fast; the checklist is the
learnable substitute for it. (Twin of Quantify & Qualify: Q&Q makes each *answer* senior; these lenses
make each *question* senior.)

| Lens | The question it generates | Example (rate limiter) |
|------|---------------------------|------------------------|
| **Placement** | Where in the request path does it live? | gateway vs per-service middleware vs sidecar |
| **Key / granularity** | It acts *per what*? | per user / IP / API key / endpoint |
| **State & storage** | Does it hold state? where, and is it shared across instances? | local counter vs shared Redis |
| **Concurrency** | Two requests at the same instant — what happens? | atomic increment at the limit boundary |
| **Failure mode** | This (or its store) dies — fail open or fail closed? | Redis down → block all vs allow all |
| **Accuracy vs cost** | Exact or approximate? | fixed window vs sliding window vs token bucket |
| **Scale / distribution** | One node or N — how do they coordinate? | shared count across many gateways |

**How to use it:** at every deep dive, walk the lenses down the component under pressure. Each lens that
applies *is* a question you raise (and then answer with Quantify & Qualify). Two questions the video
raised — "where should it live?" (Placement) and "how do we identify clients?" (Key/granularity) — are
just two lenses pointed at a rate limiter.

## The meta-rules (what actually scores)

- **NFRs drive everything.** Every fork downstream traces back to a non-functional requirement. If you can't
  name the NFR forcing a choice, you're guessing.
- **Simple-correct before scaled.** Draw the boring version, then let requirements pull in complexity. Machinery
  without a driving requirement reads as pattern-matching, not reasoning.
- **Defend, don't draw.** The diagram is memorizable; the *why* is the signal. For every box: trigger → option →
  why → failure mode.
- **Drive it — don't wait to be asked.** You own the whiteboard. Move yourself through the steps; the
  interviewer interrupts only to probe.
- **Skipping a step is a decision, not a lapse.** Estimation-inline, Data-Flow-only-when-relevant — knowing
  what *not* to do is senior signal.

## How this note gets used

- **Every Sunday design** ([case_study_template.md](templates/case_study_template.md)) walks these six steps in
  order. This note is the *why* behind that template's headings.
- **The forks table** ([study_guide.md](study_guide.md#L146)) is the deep-dive ammunition — memorize the
  *deciding question* per fork, not the answer.
- Reread this before any Transition/Mastery sprint until driving the order is automatic.
