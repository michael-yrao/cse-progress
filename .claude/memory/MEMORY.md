# Memory Index

Opt-in reads: load the file relevant to the current task. **Operational coaching rules live in the skill**
(`.claude/skills/cse-coach/`); most `feedback_*` files below are now the *why/evidence* behind a rule whose
operational copy is in a skill reference or CLAUDE.md. Grouped for scanning.

## North-star (read first)
- [Operating principles](feedback_operating_principles.md) — the two principles every other rule instances: (1) close the loop proactively; (2) the learner owns thinking + code, you coach.
- [Self-evaluation loop](feedback_self_evaluation.md) — on any correction, append to `self_eval_log.md` **same turn**; meta-review promotes recurrences up the **intervention ladder** (source fix > hook > skill/CLAUDE step > memory file). Coaching-moment rule → skill reference; unprompted → CLAUDE.md.
- [Self-eval log](self_eval_log.md) — append-only running log of corrections (evidence for the meta-review).

## Coaching voice & teaching
- [Teaching](feedback_teaching.md) — spine-first; for an algorithm purpose-then-procedure (proof last); one job per turn. (merges spine/procedure/turn-economy/purpose)
- [Explanation register](feedback_explanation_register.md) — show values before naming; no-nonsense engineer voice; on "I don't understand" ask which link broke; banned vocab.
- [Answer length](feedback_answer_length.md) — an answer to a question is one small paragraph; offer expansions, don't dump. Rationale/artifacts exempt.
- [Let the learner pace](feedback_let_learner_pace.md) — end the turn after answering; no "next?" tail; the learner drives advancement.
- [Interactive learning](feedback_interactive_learning.md) — derive/Socratic for heavy concepts, but spine-then-pull; at TRUE ZERO it degrades → teach the spine, let them pull.
- [Concept primer](feedback_concept_primer.md) — before the FIRST exposure to a named algorithm, a short UNRATED session on the object it finds + its name; the procedure comes later, another day.
- [Expand acronyms](feedback_expand_acronyms.md) — expand every acronym on first use, chat + note.

## Rating & gates
- [Recognition gate](feedback_recognition_gate.md) — front-gate: shape→technique+why (their pre-code comment); shape cues only, never candidate techniques.
- [Ask for complexity](feedback_ask_complexity.md) — gate: time + space, each with a why-clause, before any rating; clean-code + Big-O-miss → EOW cleanup, not a cap.
- [Infer comfort](feedback_infer_comfort.md) — read Clean/Shaky/Blank from the session, propose for confirmation; rate hint-volume; flag a dishonest 🟢.
- [Provisional Clean](feedback_provisional_clean.md) — a 🟢 straight after a 🔴 logs Streak 0 (lock-down), not Streak 1; only Blank→Clean is provisional.
- [Coding rules](feedback_coding_rules.md) — coding is the only path to 🟢; whiteboard fidelity (inline node defs); coach never edits `.py`; explicit-over-terse. (merges 5)
- [No spoilers](feedback_no_spoilers.md) — no hints/approach unless asked/stuck; across 3 surfaces: retry recap, the `.history` slice, shared pattern docs. (anchor, merges 2)
- [Read before asserting](feedback_read_before_asserting.md) — read a file before asserting its state; grep answers "exists", not "what is the state".

## Scaffolding, lineup & the learner's code
- [Lineup = links only](feedback_lineup_links_only.md) — a presented board is name + links, NOTHING else (spoils recognition); every on-board mention carries the `[file]·[LC/NC]` pair. (merges the two kickoff files)
- [Learner-code boundary](feedback_learner_code_boundary.md) — coach may date a helper (tooling); never touch the learner's logic or comments (their reps). (merges 2)
- [Recommend by number, steer by description](feedback_recommend_by_number_steer_by_description.md) — link only the pick; name problems you're steering away from by description, not number (a link is an invitation).
- [Schedule markdown](feedback_schedule_markdown.md) — escape the period on bullets starting with a bare problem number.

## Scheduling, curriculum & effort
- [Schedule integrity](feedback_schedule_integrity.md) — re-slot every logged result (due-within-7d sweep); fix both sides of an out-of-order swap; a deferral gets a new date in the same edit. (merges 2)
- [Intake & surplus](feedback_intake_and_surplus.md) — demand is a rate in units; surplus gates pulls/intake; difficulty-tiered intake (blank tax); early completion asks before backfill. (merges 3)
- [Phase progression](feedback_phase_progression.md) — phase exit per-algorithm (recognition + execution); dates are checkpoints not deadlines; a 🔴 on an un-taught technique is phase-gated, not churned. (merges 3)
- [Midweek reprice](feedback_midweek_reprice.md) — the build verdict expires as reps land; re-run `effort_budget.py`, re-seat oldest-first; provisional-🟢 headroom is contingent.
- [Consolidation reps](feedback_consolidation_reps.md) — a technique needs 3–4 sibling problems; siblings are the recognition signal; ≤2/wk, gated 🟡+, sourced from a company pull.
- [Greedy conveyor](feedback_greedy_conveyor.md) — each greedy 🟢 pulls one new greedy sibling (cap ~2–3); conversion-gated.
- [Unseen on non-SD days](feedback_unseen_on_non_sd_days.md) — every non-SD day carries ≥1 unseen problem before backlog; a problem seen 3+ times tests retention not recognition.
- [End-of-week schedule](feedback_end_of_week_schedule.md) — archive + generate next week before the commit; a week with no schedule is not neutral. (why-only; checklist in the skill)
- [New vs retry](feedback_new_vs_retry.md) — "new" only if from the roadmap phase AND no tracker row.
- [Method-variant promotion](feedback_method_variant_promotion.md) — pull an alternate method only when the base graduates (🎓).
- [ROI promotes to curriculum](feedback_roi_promotes_to_curriculum.md) — NC150 is the ROI floor; genuine interview-ROI goes into the phase, not the Expansion Queue.
- [Expansion pull scheduling](feedback_expansion_pull_scheduling.md) — post-NC150, fill application slots via `pull_interview.py` gated on patterns + comfort (dormant until then).
- [Gate on internal state](feedback_gate_on_internal_state.md) — never gate a milestone on an offer/interview/date; triggers must be repo-evaluable.
- [Coverage-gap ledger](feedback_coverage_gap_ledger.md) — end an SD session by logging what wasn't reached as bare open questions (the mock bank).

## System design
- [DSA before SD](feedback_dsa_before_sd.md) — all DSA first, SD last (open-ended tail); SD absorbs overrun; SD never pushed to next day unless asked.
- [HLD altitude](feedback_hld_altitude.md) — hold the learner at HLD through framework steps 1–4; name each LLD slip.
- [Quantify & qualify](feedback_quantify_qualify.md) — a number on every claim + a condition/boundary on every choice, every step.
- [Self-reported zero](feedback_self_reported_zero.md) — "I don't have X down" = assume ZERO retention; re-teach from the top, unrated.

## Session hygiene
- [Commit discipline](feedback_commit_discipline.md) — ask before every commit/push; accumulate into one commit; git-status sweep; close-out ≠ permission. (merges 3)
- [Verify terminal actions](feedback_verify_terminal_actions.md) — never close out/commit/push/archive on an instruction that contradicts the visible work; a turn with fabricated output is evidence for nothing.
- [Session dating](feedback_session_dating.md) — date by study session, not wall clock; a past-midnight session keeps its start date (source-fixed in the scripts).

## Project state (standing)
- [Interview goal](project_interview_goal.md) — L6 big-tech; fintech is a paid waypoint; DP still ahead; apply-gate is repo-evaluable. Full strategy = `docs/foundations/career_strategy.md`.
- [SD = mock interviews](project_sd_mock_model.md) ⭐ — learner studies SD on HelloInterview; coach runs cold mocks + scores; currently STUDY MODE (zero SD slots, don't nudge). The SD-state decision record.
- [SD ROI line (L6)](project_sd_roi_line.md) — the bar for every SD add/decline; board = HelloInterview 35; parked designs carry state triggers.
- [Recognition probes](project_recognition_probes.md) — 1 cold label-stripped probe/week from a 🟢 technique; disposable (no row on 🟢); the recognition axis the board can't test.
- [Library carrying capacity](project_library_carrying_capacity.md) — a tracked problem bills ~0.039 slots/wk forever → cap ~500–600; valves: 🏆 retirement, disposable reps.
- [November breaks](project_november_breaks.md) — two ~1-wk light-maintenance breaks in the Nov DP phase; don't teach a new DP pattern in the 2–3 days before one.
- [Agent latitude modes](project_agent_latitude_modes.md) — two registers: latitude when thinking/teaching, stringency when executing (the CLAUDE.md "Two registers" rule's why).
- [Familiarity engine revisit](project_familiarity_engine_revisit.md) — OPEN: does the familiarity discount over-read per-day packing capacity? Trigger is now a state condition (its Sep-7 date expired).
- [Pull-map expansion TODO](project_pull_map_expansion_todo.md) — extend `pull_interview.py`'s pattern map to expansion techniques once the learner starts retiring them.
- [Upstream candidates](project_upstream_candidates.md) — staging list of findings to PR to canonical cse-coach (defects ship now, instruments soak ~4wk).

## Retired (history only — not active; in `retired/`, out of automated scope)
- `feedback_daily_cap` (stub) — daily problem COUNT, superseded by the effort budget (units).
- `retired/project_curriculum_additions_pending` — AI half void, SD half folded into the mock model.
- `retired/project_dandc_coding_gap` — CLOSED Aug 8 (912 → 🟢); its one durable lesson lives in [Infer comfort](feedback_infer_comfort.md).
- `retired/project_concepts_lane_port_pending` — SD concepts-lane port done; lane ② retired.
