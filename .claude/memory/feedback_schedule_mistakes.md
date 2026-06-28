---
name: feedback_schedule_mistakes
description: When user does a problem out of scheduled order, proactively detect and fix the swap without waiting for user to catch it
metadata:
  type: feedback
---

When logging a problem result, check whether it was scheduled for today or a different day. If the user did a problem early (or from the wrong day), proactively detect the displaced problem and reschedule it — don't wait for the user to notice.

**Why:** User accidentally did 355 Design Twitter (Thu's active block) on Wednesday instead of 621 Task Scheduler (Wed's active block). They had to point out the mistake after the fact.

**How to apply:** After logging any result, cross-check the problem against today's schedule. If it belongs to a different day, identify what was displaced and find it a new slot in the same edit. Common cases:
- User does tomorrow's active block today → move today's active block to tomorrow
- User does a problem from next week → note the original slot is still open
- Always fix both sides of the swap (mark the right day done, reschedule the displaced problem)
- **User does a future-scheduled problem early**: move the entry to today's block in the schedule (don't leave it marked done in the future day's slot). The attempt date in the tracker is the source of truth, but the schedule should also reflect the actual day it was done.
