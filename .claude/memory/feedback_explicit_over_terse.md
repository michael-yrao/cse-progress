---
name: feedback_explicit_over_terse
description: don't suggest terser Python idioms (chained comparisons, comprehensions, walrus) in solution files — the learner writes explicitly on purpose, for readability under interview pressure
metadata:
  type: feedback
reconciled: 2026-08-30
---

**Do not propose "more Pythonic" rewrites of working solution code.** The learner writes bounds
checks and conditions out longhand deliberately — `nr >= 0 and nr < rows` over `0 <= nr < rows` —
and told me so directly (Aug 3, 2026, on 994): *"i like being explicit with my code for easier
readability."*

**Why:** this is a preference about *their* code, not a defect, and it is a reasonable one for the
context. These files are interview-rep artifacts read cold weeks later and written under time
pressure; an explicit conjunction is unambiguous at a glance and has no idiom to misremember at a
whiteboard. Suggesting the terse form costs a line of their attention and returns nothing — the
rating already ignores it, because style was never a 🟢 criterion.

**How to apply:** in a code review, flag **correctness, complexity, and naming that misleads**
(e.g. `minSize` for a threshold, which they took). Do **not** flag chained comparisons,
comprehension-vs-loop, `enumerate`/`zip` substitutions, walrus, ternaries, or any other
compression whose only argument is brevity. If a terse form is genuinely load-bearing — it fixes a
bug, or changes complexity — that is a correctness note and it stands on that, not on style.

Scope: the learner's `dsa/leetcode/**` solution files. Repo tooling under `scripts/` is ordinary
code and follows the normal style rules. Related: [[feedback_no_code_edits]] (never edit their
solutions at all), [[feedback_infer_comfort]] (style is not a rating input).
