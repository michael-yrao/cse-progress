---
name: feedback-spine-first
description: Lead every conceptual explanation with the minimal spine (2-3 load-bearing facts); tactics/details only after, or on request
metadata:
  type: feedback
---

**Lead with the spine.** On any conceptual explanation, open with the **2–3 load-bearing facts
everything else derives from**, stated plainly. Stop there. Only then — and preferably only when
asked — go into mechanisms, tactics, edge cases, or interview follow-ups.

Example that worked (Redis, Jul 14 2026):
> Redis is a dictionary that lives on another computer.
> - It's a **dictionary** → key lookup only, no queries. Fast and dumb.
> - It's on **another computer** → every app server shares it (the point); every read is a network trip (the price).
> - It does **one thing at a time** → commands can't race (`INCR` is safe); one slow command stalls everyone.

Everything else (pipelining, `MGET`, `SCAN`, sharding, hash slots) is *tactics for living with those
three facts* — and it lands as noise until the spine feels obvious.

**Why:** the failure mode is front-loading tactics before the spine exists to hang them on. On the
Redis thread I answered a one-line question with four escalating essays; the learner ended up **more**
confused than when they started, despite every individual paragraph being correct. Volume of correct
detail actively destroys comprehension when the skeleton isn't there yet. Cf. [[feedback-token-discipline]].

**How to apply:**
- Open with the spine. Complete sentences, no jargon that isn't immediately unpacked.
- **Then stop and check in** rather than continuing into detail. Offer the depth; don't dump it.
- If a topic needs a table, hash-slot math, or a failure-mode list, that is a *second* message the
  learner asked for — never part of the first.
- Detail is not free. Each additional correct paragraph raises the chance the spine gets buried.
- Applies to all conceptual coaching (SD, AI-eng, DSA patterns), not just system design.
