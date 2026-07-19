---
name: feedback-provisional-clean
description: A 🟢 Clean that directly follows a 🔴 Blank is logged with Streak 0 (provisional) → +10 lock-down, not the normal +30; only Blank→Clean is provisional
metadata:
  type: feedback
---

**When logging a 🟢 Clean that directly follows a 🔴 Blank, set Streak 0, not 1.** `update_review_dates.py`
treats a 🟢 with Streak 0 as a **provisional Clean** and computes **+10 days** (a lock-down check), not the
normal +30. Rationale: one Clean right after a Blank may be recall of fresh teaching, not durable retention
(same logic as the SD teach/measure split). It has to survive the +10 check before earning the real ladder.

**How it flows:**
- 🔴 → 🟢 : log the 🟢 with **Streak 0** → +10.
- Survives (🟢 again at the +10 check): log **Streak 1** → +30, rejoins the normal ladder (streak 1/2/retired = 30/60/180).
- Slips (🟡/🔴): resets as usual.
- **🟡 → 🟢 is NOT provisional** — log Streak 1 as normal. Only **Blank→Clean** gets the lock-down (a 🟡 got
  there with a nudge; a 🔴 blanked — less trustworthy).

**Do not "fix" a 🟢 / Streak-0 row to Streak 1** — that silently deletes the lock-down and the row jumps to +30.

**Why (added Jul 18, 2026):** learner wanted 787 Bellman-Ford (🔴 Jul 14 → 🟢 Jul 16) reviewed at +10 to
confirm it stuck, not +30. Generalized into this policy instead of a one-off manual date (the pre-commit hook
recomputes and reverts manual date edits — see the Redis date incident). Config: `clean_provisional` in
`cse.config.yml` (default 10). Documented in `dsa_progress.md` header + CLAUDE.md interval table.
Related: [[feedback-infer-comfort]] (this fires at log time, keyed to the *prior* attempt's comfort).
