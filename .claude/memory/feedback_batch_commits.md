---
name: feedback_batch_commits
description: Batch commits — accumulate edits and commit once at session end, not once per problem
metadata:
  type: feedback
---

**Do not commit after every problem.** Accumulate the edits (solution file, `dsa_progress.md`, `stuck_log.md`, schedule) across the session and commit **once at the end** — or at a natural breakpoint.

**Why:** every commit fires the pre-commit hook, which rewrites `dsa_progress.md`, which makes the harness inject **~70 lines of the tracker back into context** as a "file was modified" notice. At one commit per problem that's ~25 tracker dumps in a single session — a large, entirely avoidable input-token cost that compounds because every turn re-sends the whole conversation (and the prompt cache expires during study breaks, forcing full re-reads at full price). The Jul 6–13 session burned ~31% of a 5-hour token budget largely on this.

**How to apply:**
- Make the file edits per problem as normal (tracker row, stuck_log, schedule strike) — just **don't `git commit`** each time.
- Commit + push **once** when closing out the session, with a message covering the day's results.
- **Commit early anyway if:** the user is about to switch machines (they work across two — unpushed work would strand them), or the session is ending unexpectedly. Losing work is worse than spending tokens.
- Still run `git status` before the final commit to catch unstaged solution files ([[feedback_git_commit]]).
- Pairs with [[feedback_end_of_session_push]] — that rule already says push at session close; this just removes the per-problem commits in between.

**Other context-cost levers** (mention if the user asks): start a **fresh session each day** rather than dragging days of history along; `/compact` when long; prefer targeted `grep` over re-reading `dsa_progress.md`; trim ECC rule files irrelevant to this repo (web/angular/OWASP/TDD-coverage) since they are re-injected every turn.
