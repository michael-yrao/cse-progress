---
name: feedback_no_code_edits
description: Never edit .py files under dsa/ — user writes all LeetCode solution code themselves
metadata:
  type: feedback
---

Never edit any `.py` files under `dsa/`. The user writes and maintains all LeetCode solution code themselves.

**Why:** User explicitly asked that LeetCode solution code be theirs only — the assistant should only read and explain.

**How to apply:** Only use Read on `.py` files under `dsa/`. Explanations, bug findings, and suggestions are fine — but do not apply fixes. Offer fixes as text the user can type themselves. Editing docs, schedules, and `review_progresion.md` is fine.
