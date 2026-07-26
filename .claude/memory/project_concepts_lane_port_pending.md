---
name: project-concepts-lane-port-pending
description: cse-progress built an SD "concepts lane" (Jul 25-26, 2026) that cse-coach still lacks — port owed upstream; cse-coach's tier1 curriculum has no quantitative-foundations category at all
metadata:
  type: project
---

**Jul 25–26, 2026** — cse-progress added a **concepts lane** to the SD track. cse-coach does **not**
have it. This is an upstream port owed in the *opposite* direction from
[[project-curriculum-additions-pending]] (which tracks cse-coach → cse-progress).

**The finding:** the "designs pull the blocks" model catches **building blocks** but structurally cannot
catch **concepts**. A block is a box on the diagram — you notice it's missing. A concept (Zipf, Little's
Law, quorum math) is a fact needed mid-sentence to justify a number, so the gap surfaces only *after*
you're already stuck. Evidence: `concepts/` held exactly the two things that had already ambushed a
session (Zipf, Bloom filter) — an ambush log, not a plan.

**Built in cse-progress:** six cards in `docs/foundations/system_design/concepts/` (percentiles & tail
latency, Little's Law, utilization & queueing, probabilistic sketches, retry storms & stampedes, quorum
math); a `Concept`-role row per card in `design_progress.md`; and a lane-② fallback rule ("pull queue
empty → drill a concepts card") in the SD study guide.

**What cse-coach is missing (verified by reading, not assumed):**
1. `.claude/skills/cse-coach/SKILL.md` (~line 465) and `docs/foundations/system_design/study_guide.md`
   (~line 46) define lane ② as pull-queue-only — **no fallback**, so it idles when nothing was hit cold.
2. No `concepts/` folder in the scaffolded doc tree, and no concept template (only
   `component_template.md` / `case_study_template.md`).
3. `curriculum/system_design/tier1_interview_core.yml` has **no quantitative-foundations topic at all** —
   zero mention of Zipf, percentiles/p99, Little's Law, utilization, quorum math, sketches, or
   jitter/backoff/stampede. "bloom filters" is mis-filed under *Building blocks*, and the study guide
   says of it "small; fold into the design that needs them" — **that exact policy is what caused the
   ambush.**

**Why:** this is a defect in cse-coach's model, not a cse-progress preference — any learner on the pull
model hits it. Fix = add a `Quantitative foundations` topic to tier1, move bloom filters into it, and
give lane ② the concepts fallback.

**How to apply:** when next working in cse-coach, port items 1–3. The six filled cards stay repo-side —
cse-coach ships templates and guides, not filled notes. Related: [[project-sd-three-lane-structure]].
