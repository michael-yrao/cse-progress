---
name: feedback_no_spoilers
description: Zero hints/approaches unless explicitly asked or user says stuck; never recap the approach when a problem (especially a retry) begins
metadata:
  type: feedback
---

Give **no** hints, approaches, pattern names, or algorithm reminders unless the user **explicitly asks** for help or says they're stuck.

**Critical for retries:** When the user announces they'll (re)do a problem — *even a 🔴 Blank retry that has a full stuck_log entry* — do NOT recap, "remind," or pre-load the approach, the data structure, the pattern, or what's in the stuck_log (e.g. "you've got the dict/two-pass idea in the tank"). A retry is **retrieval practice from a blank page**; surfacing the solution direction defeats the entire point and robs the learning.

**Allowed vs not:**
- ✅ Answer clarifying questions about the *problem statement*.
- ✅ Diagnose a bug in code they've already written and shared.
- ❌ Volunteer the solution direction, the data structure, or the "trick" up front.
- ❌ Echo the stuck_log's approach when they start a problem.
- Discuss approach only *after* they finish, or when they explicitly ask / say they're stuck.

**Why:** Even a light "you have the dict/two-pass idea from stuck_log" recap when the user started 138 spoiled the retrieval practice — they noted that if they *hadn't* already remembered, that recap would have handed them the answer.

**How to apply:** When the user says "will do X now," just acknowledge and go fully hands-off — no approach, no reminder, no stuck-log echo. Wait for their result or an explicit ask. Instance of [[feedback_operating_principles]] P2 (the user owns the thinking).
