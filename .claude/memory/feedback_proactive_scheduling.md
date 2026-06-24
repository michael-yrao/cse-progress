---
name: feedback_proactive_scheduling
description: After logging any result, scan the tracker for problems due within the next 7 days and slot them proactively
metadata:
  type: feedback
---

After logging a problem result, scan `review_progresion.md` for any problems whose Next Review Date falls within the next 7 days and slot them into the schedule in the same edit. Do not wait for the user to notice they were missed.

At the end of each practice day (when the user signals they are done or asks to push), present a brief due-date summary: list every problem due within the next 7 days, grouped by day, so the user can see what's coming.

**Why:** User had to point out that 33 Search in Rotated and 994 Rotting Oranges were due Thu/Fri but weren't in the schedule. User also explicitly requested a daily refresh of upcoming due dates.

**How to apply:**
- After every problem log: check tracker for upcoming due dates (today through +7 days) and proactively add any unscheduled problems to the appropriate warmup slot. Spread across morning/evening to avoid stacking.
- At end of day: show a "Due this week" summary grouped by date before or after pushing. Keep it short — one line per day with problem names and comfort icons.
