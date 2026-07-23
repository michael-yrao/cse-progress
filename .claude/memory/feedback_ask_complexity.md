---
name: feedback_ask_complexity
description: after a problem is coded, ASK the learner for time & space complexity before rating — don't state it for them
metadata:
  type: feedback
---

After a problem is done, **ask the learner to state the time and space complexity themselves**
before you confirm the rating. Don't announce the complexity for them.

**Why:** stating complexity is part of the thinking the learner owns ([[feedback_operating_principles]],
§0.2) — and in a real interview *they* have to volunteer it, unprompted. Reciting it for them
removes a rep and hides whether they actually know it.

**How to apply:** on any completed problem, before proposing 🟢/🟡/🔴, ask "time and space?" and let
them answer. Then confirm or correct — state the right complexity yourself only after they've
committed (or explicitly pass). Ties into [[feedback_infer_comfort]].

**⚠ PINNED (2026-07-22): does a Big-O miss lower the comfort rating?** On 242 the learner nailed the
code but analyzed space as O(n) when the fixed 26-array makes it O(1); I proposed 🟡 on that basis and
they overrode to 🟢 — *"I don't know if it's worth saying we're shaky just for big-O analysis yet. Put
a pin on that."* So: **ASK for complexity every time (settled).** Whether a wrong analysis on
otherwise-clean code counts against 🟢 is **undecided** — do NOT auto-drop to 🟡 for a Big-O miss
alone; note the correction, propose the rating without weighting the miss heavily, and defer to the
learner. Revisit once there's more signal on whether their Big-O is a recurring gap.
