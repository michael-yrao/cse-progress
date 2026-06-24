---
name: feedback_proactive_scheduling
description: After logging any result, scan the tracker for problems due within the next 7 days and slot them proactively
metadata:
  type: feedback
---

After logging a problem result, scan `review_progresion.md` for any problems whose Next Review Date falls within the next 7 days and slot them into the schedule in the same edit. Do not wait for the user to notice they were missed.

**Why:** User had to point out that 33 Search in Rotated and 994 Rotting Oranges were due Thu/Fri but weren't in the schedule — they shouldn't have to circle back for this.

**How to apply:** After every problem log, check the tracker for upcoming due dates (today through +7 days) and proactively add any unscheduled problems to the appropriate day's warmup slot. Spread across morning/evening to avoid stacking. Do this in the same edit as the result logging.
