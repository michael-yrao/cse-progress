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

Honesty matters more than agreeableness here: if they claim 🟢 but I supplied a real fix they missed, say so plainly (see the 355 and 36 exchanges) — then defer to their call. Related: [[feedback_no_spoilers]].
