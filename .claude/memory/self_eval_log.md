# Self-Evaluation Log

Append-only log of corrections. Governed by [[feedback_self_evaluation]]. Newest at top. Meta-review promotes recurring root causes into rules; entries are never deleted, only re-statused.

- 2026-07-01 — 271 Encode/Decode labeled "Linked List catch-up" when it's an arrays/strings problem → relabeled to "Arrays/Strings catch-up". Root: the phase name ("Heap + Linked List catch-up") was copy-pasted as the per-problem label. [P1] (status: open)
- 2026-07-01 — 621's O(N) optimization sat unstaged across two later commits → committed separately + strengthened the rule. Root: `git add` was scoped to only the current problem's files, assuming an already-logged problem's file was clean. [P1] (status: consolidated→[[feedback_git_commit]])
- 2026-07-01 — Logged the day's 5 problems with the wrong date (Jun 16 instead of Jun 29), so they sorted below existing rows and had wrong next-review dates → corrected all dates and recomputed. Root: trusted an ambiguous/stale "current date" signal instead of cross-checking against the schedule row I was actively marking. [P1] (status: open)
