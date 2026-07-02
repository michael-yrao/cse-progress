---
name: feedback_git_commit
description: Always run git status before committing to catch unstaged solution files
metadata:
  type: feedback
---

Always run `git status` before staging and committing to catch any modified or untracked `.py` files that the user wrote during the session.

**Why:** Solution files were left out of a commit because only doc/schedule files were explicitly staged — the user's new .py files were missed.

**How to apply:** Before every commit, run `git status` and include any modified or untracked files under `dsa/leetcode/` in the same commit alongside the tracker/schedule updates. Don't commit docs without also committing the corresponding solution files. Also run `python3 scripts/update_review_dates.py` before the final commit of each session to keep the tracker sorted by latest attempt date.

**Post-logging edits (important):** A problem being already logged/committed does NOT mean its file is clean. When the user later refactors or optimizes a solution we already committed (e.g. discussing a follow-up O(N) improvement after the Shaky/Blank was recorded), that edit lands *after* the original commit and gets stranded unstaged. So don't scope `git add` to only the current problem's files — check `git status` for ANY dirty `dsa/leetcode/*.py` and sweep it into the next commit. A dedicated `perf:`/`refactor:` commit for the optimization is fine. This actually happened: 621's O(N) optimization sat unstaged for two later commits because staging was scoped to just the new problem's files.
