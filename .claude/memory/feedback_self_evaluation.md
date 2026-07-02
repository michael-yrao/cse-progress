---
name: feedback_self_evaluation
description: On any self-correction, append a note to self_eval_log.md; periodically meta-review the log to promote recurring mistakes into durable rules
metadata:
  type: feedback
---

Run a continuous self-improvement loop so mistakes convert into durable rules instead of silently recurring.

## 1. On every correction — log it

Whenever something you did gets corrected — whether **you** catch it or the **user** does — append a one-line dated entry to `self_eval_log.md` in this folder. Do this in the same flow as the fix, not later. An entry is warranted for: a wrong value logged, an artifact mislabeled, a missed propagation (unstaged file, unscheduled due problem), a spoiler slip, a bad assumption, etc. Format:

```
- YYYY-MM-DD — <what went wrong> → <the fix>. Root: <why it happened>. [P1|P2] (status: open | consolidated→[[rule]])
```

`[P1]` = broke "close the loop completely/proactively"; `[P2]` = broke "user owns thinking + code, you coach" (see [[feedback_operating_principles]]). Default status is `open`.

## 2. Periodically — meta-review the log

At the **start of each week's first session** (or whenever `open` entries reach ~8), do a self-evaluation of the self-evaluations:
- Cluster the `open` entries by root cause.
- Any root cause that appears **2+ times** gets promoted: create or update a specific rule memory (or tighten [[feedback_operating_principles]]) so the mistake is prevented structurally, not just remembered.
- Mark promoted entries `consolidated→[[rule]]`. Leave true one-offs `open` (they may still cluster later).
- Keep the log append-only; don't delete entries, just update their status.

**Why:** The user wants mistakes to feed back into the system. A one-off correction is noise; a *repeated* one is a missing rule. This loop surfaces the repeats. It's the same synthesis we did manually to produce [[feedback_operating_principles]] — now automated and ongoing.
