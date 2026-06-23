---
name: feedback_no_code_edits
description: Never edit code files in the cse-review repo — user makes all code changes themselves
metadata:
  type: feedback
---

Never edit code files in the cse-review repo. The user writes and maintains all code themselves.

**Why:** User explicitly asked that code changes be done by them only — the assistant should only read and explain.

**How to apply:** In cse-review, only use Read to look at code. Never use Edit or Write on .py files (or any source files). Explanations, bug findings, and suggestions are fine — but do not apply the fix. Offer the fix as text the user can type themselves.
