---
name: feedback-interactive-learning
description: For conceptually heavy topics, drive learning with active-recall formats (derive-the-design, Socratic, failure-mode drills) — not explanation dumps
metadata:
  type: feedback
---

**Conceptually heavy topics get an active format, not an explanation.** The learner explicitly asked
for interactive methods (Jul 14 2026) after an explanation-only Redis thread left them more confused.

**What works (use these):**
1. **Derive-the-design** — pose the constraint, let them invent the mechanism, then name it.
   *"3 app servers, each with its own counter. User hits all 3. What breaks? Fix it."* → they invent
   shared state → **that's Redis.* Best format for "why does this exist."
2. **Failure-mode drill** — *"Redis just died. What happens to your rate limiter?"* Forces the tradeoff
   talk that interviewers actually probe. Strongest signal generator.
3. **Socratic pushback** — they explain it back; assistant plays the skeptical interviewer and asks
   the next "why" until it bottoms out. Exposes memorized-vs-understood instantly.
4. **Cold blind sprint** (the existing Recall Card) — keep. It *measures*; it doesn't teach.

**What does NOT work (stop doing):**
- Escalating explanation essays. Correct detail without a skeleton = noise. See [[feedback-spine-first]].
- Answering a follow-up with more surface area than the question had.
- Tables/mechanisms/edge cases before the learner has stated the core idea back once.

**Why:** learner owns the thinking ([[feedback-operating-principles]]). An explanation makes them a
reader; a derivation makes them the designer. Recall Cards test retention *after* learning — they were
being used as the only tool, with prose as the teaching, and prose isn't teaching.

**How to apply:** on a 🔴 Blank concept, default to **derive-the-design first**, explanation only to
patch the specific gap they hit. Confirm the spine is stated back before adding any tactic.
