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

## ⚠️ The floor: derive-the-design needs an existing model. At TRUE ZERO it fails. (Aug 8, 2026)

The ranking above is by *how much the learner produces*, and it is right **once a foundation exists.**
Below that it inverts: deriving asks the learner to **invent** a mechanism, which requires something to
reason from. At genuine zero there is nothing, and the format degrades into guessing.

**What happened:** networking, learner self-described as *"a complete novice."* Derive-the-design opened
with *"what problems would you have to solve?"* → *"I have no idea."* Retried with a concrete
postal-service analogy → *"I don't like this direction or method, let's start over."* Two failed attempts
before the format was abandoned.

**What worked instead — offer the choice, don't pick for them.** Four concrete approaches were put up
(spine-then-pull · bootstrap with an external explainer first · learn it inside a design · rewrite the
card). The learner chose **spine first, then I pull**, and it produced the best SD session in weeks:
IP → packets → headers → private/public → NAT → ports → the 4-tuple → DNS → how `443` is derived, every
step driven by their own next question, with several sharp catches of my own errors.

**So the rule is a ladder with a floor:**

| Learner's state on the topic | Opening format |
|---|---|
| Has a model, it's rusty or partial | **derive-the-design** (unchanged — still the default) |
| **True zero — no foundation at all** | **spine first (2–3 facts, ~5 lines), then let them pull.** Derivation becomes available *after* the spine lands |

**The tell you are below the floor:** the answer to your derivation prompt is *"I have no idea"* rather
than a wrong guess. **A wrong guess means there is a model to correct; a blank means there is nothing to
derive from** — switch to spine-then-pull immediately rather than reaching for a better analogy.

⚠️ **And check Bootstrap before assuming a topic has been taught at all.** *"A note exists"* is not
*"the learner has been taught"* — writing the card is the coach producing, not the learner learning. See
the Aug 8 entry in [[self_eval_log]] and [[feedback_spine_first]].

## ⚠️⚠️ Correction, same day (Aug 8, 2026, session 3): spine-then-pull is the learner's STANDING FORMAT, not a zero-state fallback

The floor rule above was written too narrowly and **immediately licensed the exact mistake it was meant
to prevent.** Having taught the TCP spine earlier in the day, I reasoned *"a model now exists, so the
ladder says derive-the-design is available again"* and opened the next segment with a derivation prompt.
The learner stopped it:

> *"I'm not a fan of teaching like this, let's go back to how we were doing this before. You give me
> small bits and I learn by asking questions about exactly how the small bits work, this should expand
> both the breadth and depth."*

**So the trigger is not the learner's knowledge level — it is the learner's preference, and it is
standing.** The ranking at the top of this file is a general default; **for this learner, on conceptual
SD/networking material, spine-then-pull is the format**, whether they are at zero or holding a partial
model. Do not "graduate" them back to derive-the-design because the prerequisite now exists.

**The format, precisely as they described it:**

1. **Give one small bit** — one mechanism, a few lines, complete in itself. Not a lecture, not a table,
   not the next three consequences pre-empted.
2. **Stop.** Do not ask them a quiz question and do not chain into the next bit.
3. **They ask about that bit.** Their question sets the direction — depth (*how does that actually
   work*) or breadth (*what about X*). Answer exactly what was asked, at the size it was asked.
4. Repeat.

**Why it works, in their words:** *"this should expand both the breadth and depth."* The pull direction
is theirs, so the session tracks what they can't yet see rather than what I predicted they'd need —
which is why it beat two attempts at derivation and produced the best SD session in weeks.

**The distinction that matters:** a Socratic question asks them to *produce the answer*; this format asks
them to *produce the question*. They are still doing the cognitive work — they own the direction, the
gap-finding, and the depth — but they are never asked to invent a mechanism they have no basis to invent.
Do not read "no derivation" as "back to explanation dumps": [[feedback_spine_first]] and
[[feedback_turn_economy]] still bind. **One bit per turn, then stop.**

**Where derive-the-design still belongs:** DSA reps and *design* sessions (lane ③), where the learner is
building the thing rather than learning what the thing is. This carve-out is about conceptual/plumbing
material.
