---
name: project-sd-three-lane-structure
description: System design = 3 slots/wk (from Jul 20 2026) — light midweek = tech fluency, fuller midweek = blocks & probes, Sunday = designs; designs PULL blocks in, don't grind blocks first
metadata:
  type: project
---

**Decided Jul 14, 2026.** System design runs **3×/week** (raised from 2× the same day), starting the
**Jul 20** week. Three lanes, **each owns one slot** — never let two bid for the same one:

| Lane | Slot | Job | Driven by |
|------|------|-----|-----------|
| **①** | *light* midweek — swaps **one 15-min warmup** | **Tech fluency** — one blind sprint vs a Recall Card (`technologies/*.md`) | **due dates** (spaced rep). Nothing due → build next tech's note. Order: Redis ✅ → **PostgreSQL** → Cassandra → DynamoDB → Kafka … |
| **②** | *fuller* midweek — swaps **both warmups** (~30 min) | **Blocks & probes** — write the `components/` note for whatever block the last design **hit cold**; then fire framework probe questions at an already-designed system | **the pull queue** |
| **③** | **Sunday**, 45–60 min | **Designs** — one staged session on a canonical system, full framework | **sequence** |

**Why three, not two:** lane ② was **homeless** under the original two-lane rule. "Designs pull the
blocks" says *build the cold-hit block's note in the next slot* — but with two slots that note had to
eat the tech-fluency rep, so **the pull model starved itself.**

**Time cost (accepted):** both midweek slots come out of **warmup** capacity, never the 45-min DSA
active block. −4 warmup reps/week, absorbed by the **🟢 Clean backlog** (already 2–5 months stale, its
interval math already meaningless — the right place for the cost to land). **New-problem intake stays
at 5/week.** The 🟢 pile still owes a policy decision (batch-check / burn-down week / re-baseline).

**Sunday rule — designs PULL the blocks. ⭐**
Do *not* grind all Tier-1 building blocks before the first end-to-end design (that's ~5 months at one
Sunday per stage, with zero framework reps in it — and framework fluency is ~50% of the interview
score). Instead: **start canonical designs now; learn each block when a design demands it.**

> The design is the skeleton; blocks hang off it. A block learned in isolation is a *fact*.
> A block learned because your chat design just hit a fan-out wall is a *tool*.

Sunday queue: Rate Limiter Mastery → Caching Bootstrap (only block done proactively — load-bearing
everywhere) → **DESIGN: URL shortener** → Chat → News feed → Typeahead → YouTube → LLM assistant.

**Accepted cost:** you *will* hit blocks cold mid-design. That's the point — the gap is the teaching
signal and names its own drill target. Log it, build the note in the next slot, **don't stop the
design to go study.**

**Corollary:** finish a half-done component arc before opening a new one. (Caching Bootstrap was
pushed off Jul 19 because Rate Limiter sat at Mastery ⏳ — deferred only because its gaps were Redis
facts, which Wed's session fixes.)

**Also:** a 🔴 from *never encoded* (not decayed) → next session is **derive-the-design, unrated**;
the rated sprint moves out far enough to be a real test. See [[feedback-interactive-learning]] and
[[feedback-spine-first]].
