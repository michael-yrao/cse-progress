---
name: feedback_batch_commits
description: NEVER commit or push without asking first — the learner decides when; batching alone was not enough, 31 commits ran in one session through the “natural breakpoint” loophole
metadata:
  type: feedback
reconciled: 2026-08-21
---

⚠️ **ASK BEFORE EVERY COMMIT AND EVERY PUSH. No exceptions.** Set by the learner Aug 16, 2026: *"ask me before you commit and push, always."* Make the edits, say what is staged, and **stop**. The learner decides when it lands.

**This replaced a weaker rule that failed.** The previous wording said commit once at the end “**or at a natural breakpoint**” — and that clause is a loophole wide enough to drive a session through, because *every* finished unit reads as a natural breakpoint: a hook fix, a doc, a rating, a refactor. **31 commits ran in the Aug 15–16 session under it.** Judgement was the failure point, so the rule no longer asks for judgement.

**Do not commit after every problem.** Accumulate the edits (solution file, `dsa_progress.md`, `stuck_log.md`, schedule) across the session; they land in one commit when the learner says so.

**Why:** every commit fires the pre-commit hook, which rewrites `dsa_progress.md`, which makes the harness inject **~70 lines of the tracker back into context** as a "file was modified" notice. At one commit per problem that's ~25 tracker dumps in a single session — a large, entirely avoidable input-token cost that compounds because every turn re-sends the whole conversation (and the prompt cache expires during study breaks, forcing full re-reads at full price). The Jul 6–13 session burned ~31% of a 5-hour token budget largely on this.

**How to apply:**
- Make the file edits per problem as normal (tracker row, stuck_log, schedule strike) — just **don't `git commit`** each time.
- Commit + push **once** when closing out the session, with a message covering the day's results.
- **Commit early anyway if:** the user is about to switch machines (they work across two — unpushed work would strand them), or the session is ending unexpectedly. Losing work is worse than spending tokens.
- Still run `git status` before the final commit to catch unstaged solution files ([[feedback_git_commit]]).
- Pairs with [[feedback_end_of_session_push]] — that rule already says push at session close; this just removes the per-problem commits in between.

**Other context-cost levers** (mention if the user asks): start a **fresh session each day** rather than dragging days of history along; `/compact` when long; prefer targeted `grep` over re-reading `dsa_progress.md`; trim ECC rule files irrelevant to this repo (web/angular/OWASP/TDD-coverage) since they are re-injected every turn.

⚠️ **Committing is not the only way to be safe.** If holding the work feels risky — a lot accumulated, a machine switch coming — **say so and ask**. Do not decide unilaterally that this instance is the exception; that judgement is exactly what produced the 31. See the Aug 16 entry in `self_eval_log.md`.

⭐ **Worth fixing at the source.** The link rule is obeyed because `problem_link_reminder.py` enforces it within one turn; this rule ran unchecked all session because it is only prose. A pre-commit warning when the session is not being closed out would make it self-enforcing — raised as a build item.
