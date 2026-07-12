# Memory Index

- [Operating principles (READ FIRST)](feedback_operating_principles.md) — north star: (1) close the loop completely & proactively, never make the user catch a gap; (2) user owns thinking + code, you coach. All other feedbacks are instances of these.
- [Self-evaluation loop](feedback_self_evaluation.md) — on any correction, append to self_eval_log.md; meta-review weekly to promote recurring mistakes into rules
- [Self-eval log](self_eval_log.md) — append-only running log of corrections (data for the meta-review)
- [Session dating](feedback_session_dating.md) — date logs by study session not wall clock; a session crossing midnight keeps its start date; verify against the schedule day
- [No code edits in cse-review](feedback_no_code_edits.md) — never edit source files; user writes all code, assistant reads/explains only
- [No spoilers](feedback_no_spoilers.md) — zero hints/approaches unless explicitly asked or stuck; NEVER recap the approach (or stuck_log content) when a problem/retry begins
- [Infer comfort rating](feedback_infer_comfort.md) — read Clean/Shaky/Blank from the conversation against the rubric and propose it for confirmation; don't ask the user cold
- [Git commit checklist](feedback_git_commit.md) — always run git status before committing to catch unstaged solution files
- [Proactive scheduling](feedback_proactive_scheduling.md) — after logging any result, scan tracker for problems due within 7 days and slot them immediately
- [Schedule mistake handling](feedback_schedule_mistakes.md) — when user does a problem out of order, detect the swap and fix both sides without waiting for user to catch it
- [Daily problem cap](feedback_daily_cap.md) — max 5 problems per day; push extras (lowest priority first) to next available slot and note in preview
- [End of session push](feedback_end_of_session_push.md) — commit unstaged solutions and push all commits when closing out the day
- [End of week schedule](feedback_end_of_week_schedule.md) — generate next week's schedule file before closing out the last session of the week
- [Expansion pull scheduling](feedback_expansion_pull_scheduling.md) — post-NC150, weekly generation fills application slots via pull_interview.py gated by learned patterns + comfort; pulled problems get identical Clean/Shaky/Blank treatment
- [Pull-map expansion TODO](project_pull_map_expansion_todo.md) — extend pull_interview.py's pattern map to expansion techniques (segment tree, KMP, …) once the learner starts retiring them
- [New vs retry problems](feedback_new_vs_retry.md) — only list a problem as "new" if it's from the study_guide roadmap phase AND has no existing tracker row
- [Method-variant promotion](feedback_method_variant_promotion.md) — pull an alternate-method variant (e.g. 42 Two-Pointer) into rotation only when the base method retires (🏆), not while it's still churning 🟡/🟢
- [Schedule markdown escaping](feedback_schedule_markdown.md) — escape the period on bullets starting with a bare problem number (`- 143\.`) to avoid roman-numeral list markers
