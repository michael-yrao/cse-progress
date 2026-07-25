---
name: feedback_session_dating
description: Date logs by the study SESSION, not the wall clock — a session crossing midnight keeps its start date; verify the date against the schedule day being marked
metadata:
  type: feedback
---

Attempt dates and comfort logs follow the **study session**, not the wall-clock date.

- A single continuous session that runs **past midnight keeps the date it started on.** Do not roll logged dates to the next day, and do not treat the session as "over," just because the clock passed midnight. All problems done in one sitting share one date.
- Only advance to a new date when the user begins a **genuinely new session** (they signed off and came back, or explicitly say it's a new day).
- If a "current date" signal is ambiguous or changes mid-session, **cross-check against the weekly schedule row you're actively marking** before dating anything — the schedule day is the source of truth for which session this is.

**Why (promoted from the self-eval log — 2 occurrences of date-handling errors):**
1. Logged a day's problems as Jun 16 when it was Jun 29 (trusted a stale date signal; entries sorted wrong, review dates off).
2. A continuous Thu Jul 2 session crossed midnight and 703 got dated Jul 3 while 98/323 from the same session were Jul 2 — inconsistent. Corrected 703 back to Jul 2.

**How to apply:** Determine the session's date once at the start — **confirm it explicitly with the user rather than inferring it from a problem's due date** (inferring caused a whole session to be mis-anchored to the wrong day). Then use that date for logs in the session. **Caveat when correcting a date:** a session can legitimately span two dates (e.g. the user does a few problems after midnight and considers those the next day) — do NOT assume one session maps to a single date. When the user corrects a date, confirm the per-problem split instead of blanket-re-dating everything. This is an instance of [[feedback_operating_principles]] P1 (accurate, consistent propagation). See [[self_eval_log]].

**⚠ Tooling that defaults to the wall clock (added 2026-07-24).** The session date isn't just for logs — **scripts default to `now()` and will silently do the wrong thing past midnight.** `restore_history.py`'s default `--date` is `now()`; on a session that started Jul 24 and crossed into Jul 25, it looked for `_20260725` attempt methods (found none — the scaffolds/solutions are `_20260724`), declared every problem "still empty," and kept **all** stashes out. Committing then ships the solved files *without their restored history*. **On any midnight-crossing close-out, pass the session date explicitly: `python scripts/restore_history.py --date <session-YYYYMMDD>`**, and read the output (all-"Kept" is the tell it used the wrong date). Same vigilance for any other now()-defaulting tooling at close-out.
