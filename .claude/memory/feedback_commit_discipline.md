---
name: feedback_commit_discipline
description: Why the coach asks before every commit/push, accumulates edits into one commit, sweeps git status first, and treats a close-out signal as not-yet-permission — the 31-commit failure behind it
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the always-injected layer** — CLAUDE.md gate 8 (ask before every commit/push)
and `SKILL.md` §3 / `references/review-workflow.md` §8. This file is the *why* + the failure log. Merges
the former `batch_commits` (anchor), `git_commit`, `end_of_session_push`.

## Ask before every commit and every push — no exceptions

Set by the learner Aug 16, 2026 (*"ask me before you commit and push, always."*). Make the edits, say what
is staged, **stop**; the learner decides when it lands.

**This replaced a weaker rule that failed.** The prior wording — commit once at the end *"or at a natural
breakpoint"* — is a loophole wide enough to drive a session through: *every* finished unit reads as a
natural breakpoint. **31 commits ran in the Aug 15–16 session under it.** Judgement was the failure point,
so the rule no longer asks for judgement.

## Accumulate, don't commit per problem

Make the per-problem edits (solution file, tracker row, `stuck_log`, schedule strike) as normal, but **don't
`git commit`** each time — they land in one commit when the learner says so. *Why:* every commit fires the
pre-commit hook, which rewrites `dsa_progress.md`, which makes the harness re-inject ~70 lines of the
tracker as a "file modified" notice — ~25 tracker dumps in a session, a large avoidable input-token cost
that compounds (every turn re-sends the conversation; the prompt cache expires over study breaks).

## Sweep git status first; a close-out signal is not yet permission

- Run `git status` before the final commit to catch **unstaged solution files** — docs/schedule were once
  committed while the learner's new `.py` files were missed. Include any dirty `dsa/leetcode/*.py`
  (incl. post-logging refactors); run `update_review_dates.py` before the final commit.
- A close-out phrase (*"call it a night"*) reports that the work is done — it is **not** publish
  authorization. Surface what's unstaged and *ask* ([[feedback_verify_terminal_actions]] — confirm the
  visible state actually matches "done").

## The one exception, and how to take it

**Commit early anyway if** the learner is about to switch machines (unpushed work strands them across their
two machines) or the session is ending unexpectedly — losing work beats saving tokens. But **say so and
ask**; never decide unilaterally that this instance is the exception (that judgement is exactly what
produced the 31). See the Aug 16 entry in `self_eval_log.md`.

⭐ **Source-fix candidate (raised, not yet built):** a pre-commit warning when the session is not being
closed out would make this self-enforcing — the link rule is obeyed because a hook enforces it; this ran
unchecked all session because it is only prose.
