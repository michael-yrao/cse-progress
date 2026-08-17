---
name: feedback-answer-length
description: An answer to a question is capped at one small paragraph; offer expansions as a question rather than delivering them
metadata:
  type: feedback
---

**Learner, Aug 17, 2026:** *"When answering a user question, it cannot be bigger than a small
paragraph. Any additional info and followups can be provided to the users in the form of a question on
whether they want certain portions expanded. This makes answers actually readable."*

**Why:** a long answer is not more informative, it is **less read**. When a reply arrives as a
multi-section report with tables and bolded asides, the one load-bearing sentence gets skimmed past and
has to be re-explained anyway — so volume actively defeats its own purpose. This was said after a run
of answers that each opened with a findings table and closed with "two things worth knowing".

⚠️ **It is a CAP, not a nudge.** [[feedback_turn_economy]] already said "one job per turn" and the
CLAUDE.md token-discipline rule already said "be lean", and answers stayed long. Both were phrased as
dispositions; this one is a hard limit with a fixed escape hatch, which is the difference between a
rule that fires and a paragraph.

**How to apply:**
- **Answering a question** → one small paragraph. Then **ask** which part to expand, and expand only
  that. Never pre-empt the next three follow-ups.
- **NOT capped**, because these were never the problem: the comfort-rating rationale (propose + why),
  concept explanations when stuck or asked, `stuck_log`/debrief/memory writing, and reporting that an
  action may have gone wrong or a finding that changes what to do next — state it, then stop.
- **Depth goes in a file, not the chat.** Same move as [[feedback_turn_economy]]: if it is worth
  keeping, it belongs in a note that gets reread, not in scrollback.

Full rule: the *Token discipline* section of `CLAUDE.md`. Related: [[feedback_spine_first]],
[[feedback_interactive_learning]].
