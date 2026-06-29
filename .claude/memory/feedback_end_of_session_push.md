---
name: feedback_end_of_session_push
description: "At the end of each study session, commit any unstaged solution files and push all commits to remote"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 52e81ee3-fbd0-48e9-a646-216c288288cf
---

At the end of each day's study session, check for unstaged solution files, commit them, and push everything to remote before closing out.

**Why:** User noticed commits weren't pushed after a full session. Closing out the day should always end with a push.

**How to apply:** When the user signals the session is done ("that's it for today", "closing out", "done for the day"), check `git status` for unstaged solution files, commit them if present, then push. Don't wait to be asked.
