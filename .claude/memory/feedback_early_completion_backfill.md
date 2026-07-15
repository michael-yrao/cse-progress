---
name: feedback_early_completion_backfill
description: When a problem finished early frees a future day below the 5/day target, ASK the user before backfilling that slot
metadata:
  type: feedback
---

When the learner finishes a scheduled problem **early**, it vacates that problem's future slot. If
striking it drops that future day **below the daily target of 5**, **ask the user whether to backfill
the freed slot with another problem** — don't silently leave the day short, and don't silently fill it.

**Why:** the daily cap ([[feedback_daily_cap]]) is a ceiling *and* the day's target is a floor — an
early completion shouldn't quietly reduce a future day's throughput. But what to backfill (or whether
to bank the lighter day) is the learner's call, so surface it as a question rather than deciding for them.

**How to apply:** on logging an early completion, (1) mark it done on the day it was actually done and
strike it from its scheduled future day ([[feedback_schedule_mistakes]] out-of-order handling); (2) if
that future day is now < 5, ask whether to fill the slot; (3) on yes, pull the highest-priority due
item by review tier (🔴 > 🟡 > 🟢 > 🏆) — favor the overdue-🟢 burn-down backlog — and re-slot it in the
same edit (strike it from wherever it was previewed, no double-count). Establishes Jul 14, 2026 (167
Two Sum II done early, freeing a Thu Jul 16 slot → backfilled with 1 Two Sum from the overflow).
