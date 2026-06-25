---
name: feedback_git_commit
description: Always run git status before committing to catch unstaged solution files
metadata:
  type: feedback
---

Always run `git status` before staging and committing to catch any modified or untracked `.py` files that the user wrote during the session.

**Why:** Solution files were left out of a commit because only doc/schedule files were explicitly staged — the user's new .py files were missed.

**How to apply:** Before every commit, run `git status` and include any modified or untracked files under `dsa/leetcode/` in the same commit alongside the tracker/schedule updates. Don't commit docs without also committing the corresponding solution files. Also run `python3 scripts/update_review_dates.py` before the final commit of each session to keep the tracker sorted by latest attempt date.
