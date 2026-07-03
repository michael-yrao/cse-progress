# Self-Evaluation Log

Append-only log of corrections. Governed by [[feedback_self_evaluation]]. Newest at top. Meta-review promotes recurring root causes into rules; entries are never deleted, only re-statused.

- 2026-07-01 — 271 Encode/Decode labeled "Linked List catch-up" when it's an arrays/strings problem → relabeled to "Arrays/Strings catch-up". Root: the phase name ("Heap + Linked List catch-up") was copy-pasted as the per-problem label. [P1] (status: open)
- 2026-07-01 — 621's O(N) optimization sat unstaged across two later commits → committed separately + strengthened the rule. Root: `git add` was scoped to only the current problem's files, assuming an already-logged problem's file was clean. [P1] (status: consolidated→[[feedback_git_commit]])
- 2026-07-02 — In one continuous Thu Jul 2 session that crossed midnight, dated 703 as Jul 3 while 98/323 from the same session were Jul 2 → corrected 703 back to Jul 2. Root: rolled the log date on wall-clock midnight instead of holding the session's start date. [P1] (status: consolidated→[[feedback_session_dating]])
- 2026-07-01 — Logged the day's 5 problems with the wrong date (Jun 16 instead of Jun 29), so they sorted below existing rows and had wrong next-review dates → corrected all dates and recomputed. Root: trusted an ambiguous/stale "current date" signal instead of cross-checking against the schedule row I was actively marking. [P1] (status: consolidated→[[feedback_session_dating]])

<!-- META-REVIEW 2026-07-02: date-handling root cause hit 2 occurrences → promoted to [[feedback_session_dating]]. -->

