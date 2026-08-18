---
name: feedback_end_of_session_push
description: "At the end of each study session, surface unstaged solution files and ASK to commit + push — never do it unprompted (see feedback_batch_commits)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 52e81ee3-fbd0-48e9-a646-216c288288cf
reconciled: 2026-08-17
---

⚠️ **AMENDED Aug 16, 2026 — this rule now ENDS IN A QUESTION, not an action.** [[feedback_batch_commits]] supersedes the acting half: *"ask me before you commit and push, always."*

At the end of each day's study session, check for unstaged solution files, **report what is unstaged and what would be committed, and ask.** Do not commit or push on your own.

⭐ **This file caused a real failure on Aug 17, 2026.** Its trigger list — *"that's it for today", "closing out", "done for the day"* — reads as authorization, so *"call it a night"* was taken as a go-ahead and ~12 commits and two pushes ran unasked across the session. A close-out signal means **the work is done**, not **the work may be published**. Those are different permissions and only the learner grants the second.

**Why:** User noticed commits weren't pushed after a full session. Closing out the day should always end with a push.

**How to apply:** When the learner signals the session is done ("that's it for today", "closing out", "done for the day", "call it a night"), run `git status`, then **report**: which solution files are unstaged, what the commit would cover, and whether anything is unpushed. **Then stop and ask.** Do not stage, commit, or push until they say so — a close-out signal is not the answer to a question you have not asked.