---
name: feedback_infer_comfort
description: Infer the Clean/Shaky/Blank rating from the session and propose it for confirmation — don't ask the user cold
metadata:
  type: feedback
---

After a problem, **infer** the comfort rating yourself from what actually happened in the conversation, then state it as a proposal for the user to confirm or override. Do not ask an open "How did that feel — Clean, Shaky, or Blank?" when the transcript already answers it.

**Why:** the rubric is written down (CLAUDE.md) and I watched the whole attempt — I know how many hints I gave, whether they self-caught their bugs, and whether they could derive the approach. Making the user supply what I can already read is offloading work they shouldn't have to do.

**How to apply:**

Read the signal against the rubric:

| Signal in the conversation | Rating |
|---|---|
| Solved from blank page; no hints; I flagged no bugs (or only cosmetic ones they'd caught) | 🟢 Clean |
| Had the core approach but needed a nudge on a sub-part, OR I flagged a real bug they didn't self-catch | 🟡 Shaky |
| Couldn't derive the approach; needed it explained; the substantive fixes were all mine | 🔴 Blank |

Then **propose, don't interrogate**: "That reads as 🟡 Shaky — you had the sliding window but I flagged the inverted shrink condition. Confirm?" The user can override; their call is final (comfort is self-reported).

**Still confirm every time** — propose, wait for the yes/override, then log. Never log a rating silently.

**Rate the hint volume, not the excuse for it.** If I explained the algorithm — the data structure, the invariant, the "why this and not that" — then the approach was *supplied*, and that is 🔴 Blank by definition, no matter how reasonable it was that they didn't have it. A **first exposure to a new technique is still 🔴**: "there was nothing to recall yet" explains *why* it's Blank, it doesn't upgrade it. Deriving the problem-specific wrapper around a handed-over algorithm (e.g. on 743: "answer = max of the shortest distances", "`len(settled) == n` is the reachability test") is **not** deriving the approach — it's the easy half, and it doesn't lift 🔴 to 🟡.

The tell that I'm rationalizing: I list the substantive things I taught, and *then* argue for the higher rating anyway. If the list is non-empty, the rating follows the list. On 743 (Jul 13) I did exactly this — proposed 🟡 right after writing "I taught you Dijkstra" — and the user overruled to 🔴. That correction should never have been theirs to make.

Under-rating a fresh 🔴 as 🟡 isn't a harmless rounding: it sets the next review at +10 days instead of +2, so a technique that hasn't stuck at all gets two weeks to evaporate. The interval **is** the consequence of the rating.

Honesty matters more than agreeableness here: if they claim 🟢 but I supplied a real fix they missed, say so plainly (see the 355 and 36 exchanges) — then defer to their call. Related: [[feedback_no_spoilers]], [[feedback_phase_gated_blanks]] (which is the *one* case where a 🔴 doesn't get the +2 loop — an un-taught technique, not a just-taught one).
