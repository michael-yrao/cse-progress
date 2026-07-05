# cse-review

## Agent Memory

Persistent behavioral preferences are stored in `.claude/memory/`. At the start of each session, read `.claude/memory/MEMORY.md` for the index, then load any files relevant to the current task.

When saving new memories or updating existing ones, always write to `.claude/memory/` in this repo — not to the local `~/.claude/projects/` path. Update `.claude/memory/MEMORY.md` to index any new files. This keeps memory in sync across machines via git.

## LeetCode Review Workflow

After any problem discussion (solving, reviewing, or mentioning a problem by number or name):

1. Check the current week's schedule file (`docs/foundations/dsa/schedules/<YYYYMMDD>_schedule.md`) and mark the problem as completed in the table.
2. If the user hasn't mentioned how they felt, ask: "How did that feel — Clean, Shaky, or Blank?"
   - **Clean**: Solved from blank page, correct complexity, no hints needed. If you had to second-guess the data structure or peek at anything — that's Shaky, not Clean.
   - **Shaky**: Got the solution but needed a nudge, peeked at a hint, or weren't fully confident in the approach mid-way through.
   - **Blank**: Couldn't recall the approach, had to look it up.
3. Update `docs/foundations/dsa/mastery/dsa_progress.md` with the reported Comfort level and run the review script.

## Comfort-Based Spaced Repetition

Next review intervals (set in `docs/foundations/dsa/mastery/dsa_progress.md` and computed by `scripts/update_review_dates.py`):

| Comfort | Next Review |
|---------|-------------|
| Clean   | +30 days    |
| Shaky   | +10 days    |
| Blank   | +2 days     |

## Schedule Integrity Rule

When a problem is dropped or deferred from the schedule, a new specific slot must be assigned in the same edit. Never remove a problem without immediately adding it to another day. A deferred problem with no new date is a missed problem.

After logging any problem result, check its computed next review date and add it to the appropriate week's schedule file — whether that's next week or further out. Do not leave it only in `dsa_progress.md`. The spaced repetition dates are the source of truth; the weekly schedules must reflect them. When the target week's schedule doesn't exist yet, note the problem in the nearest existing schedule's preview section. Check for balance when inserting; spread across available slots rather than stacking on already-heavy days.

## Study Guide Files

- `docs/foundations/dsa/mastery/dsa_progress.md` — spaced repetition tracker (auto-updated by pre-commit hook)
- `docs/foundations/dsa/study_guide.md` — master plan with backlog recovery protocol
- `docs/foundations/dsa/schedules/<YYYYMMDD>_schedule.md` — current week's day-by-day schedule (e.g. `20260615_schedule.md`); archive the current week's schedule and generate the next week's schedule together at the end of the last session of the week — move the current file to `docs/foundations/dsa/schedules/archive/`
- `docs/foundations/dsa/mastery/stuck_log.md` — log for every non-Clean result: 🔴 Blank gets a full entry (where stuck, core realization, code snippet); 🟡 Shaky gets a one-liner (sticking point only)
