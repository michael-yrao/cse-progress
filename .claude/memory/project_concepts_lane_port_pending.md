---
name: project-concepts-lane-port-pending
description: SD "concepts lane" — built in cse-progress Jul 25-26 2026, ported up to cse-coach Jul 26; port is DONE, kept only for the finding behind it (the pull model cannot catch concepts)
metadata:
  type: project
---

**Status: ported, Jul 26, 2026.** All three gaps are closed in cse-coach — lane ② fallback in
`SKILL.md` + its study guide, `concept_template.md`, and a `Quantitative foundations` topic in
`tier1_interview_core.yml` with bloom filters moved out of *Building blocks*. Nothing is owed
upstream. Kept because the *finding* outlives the port.

**The finding:** the "designs pull the blocks" model catches **building blocks** but structurally
cannot catch **concepts**. A block is a box on the diagram — you notice it's missing. A concept
(Zipf, Little's Law, quorum math) is a fact needed mid-sentence to justify a number, so the gap
surfaces only *after* you're already stuck. Evidence: `concepts/` held exactly the two things that
had already ambushed a session (Zipf, Bloom filter) — an ambush log, not a plan.

**Why it's a model defect, not a preference:** any learner on the pull model hits it. The old policy
on bloom filters — *"small; fold into the design that needs them"* — is precisely what caused the
ambush, and that phrasing is the tell to watch for if it reappears for another concept.

**How to apply:** the cards themselves stay repo-side — cse-coach ships templates and guides, never
filled notes, so a new concept card written here is *not* a port owed unless it changes the model.
When writing one, lead with the **"You'll want this when…" trigger line** naming the symptom; these
get reached for mid-panic far more than read in advance. Six cards are live and unrated (🔴,
Streak 0) in `design_progress.md` under role `Concept`. Related:
[[project-sd-three-lane-structure]], [[project-curriculum-additions-pending]] (the opposite
direction: cse-coach → cse-progress, still open).
