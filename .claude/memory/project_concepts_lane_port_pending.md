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

⚠️ **Lane ② no longer exists (Aug 13, 2026)** — the three-lane study model was replaced by mock
interviews ([[project_sd_mock_model]]) and the `Concept` rows came off the review engine. **The finding
above is why the nine cards were kept anyway**: seven of them map to nothing in HelloInterview, whose
core concepts are structural (sharding, CAP, consistent hashing) rather than numeric. They are the
quantitative lane, and a mock is exactly where a missing number ambushes you mid-sentence.

**How to apply:** the cards stay repo-side and stay **frozen reference** — nothing schedules them. When a
mock debrief shows a number could not be defended, point at the card. When writing a new one, lead with
the **"You'll want this when…" trigger line** naming the symptom; these get reached for mid-panic far
more than read in advance. Related: [[project_sd_mock_model]], [[project_curriculum_additions_pending]].
