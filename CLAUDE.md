# cse-review

## LeetCode Review Workflow

After any problem discussion (solving, reviewing, or mentioning a problem by number or name):

1. Check the current week's schedule file (`docs/practice/schedules/week_of_*.md`) and mark the problem as completed in the table.
2. If the user hasn't mentioned how they felt, ask: "How did that feel — Clean, Shaky, or Blank?"
   - **Clean**: Solved from blank page, correct complexity, no hints needed. If you had to second-guess the data structure or peek at anything — that's Shaky, not Clean.
   - **Shaky**: Got the solution but needed a nudge, peeked at a hint, or weren't fully confident in the approach mid-way through.
   - **Blank**: Couldn't recall the approach, had to look it up.
3. Update `docs/practice/review_progresion.md` with the reported Comfort level and run the review script.

## Comfort-Based Spaced Repetition

Next review intervals (set in `docs/review_progresion.md` and computed by `scripts/update_review_dates.py`):

| Comfort | Next Review |
|---------|-------------|
| Clean   | +30 days    |
| Shaky   | +10 days    |
| Blank   | +2 days     |

## Study Guide Files

- `docs/practice/review_progresion.md` — spaced repetition tracker (auto-updated by pre-commit hook)
- `docs/practice/study_guide.md` — master plan with backlog recovery protocol
- `docs/practice/schedules/week_of_<mon><day>_<year>.md` — current week's day-by-day schedule (e.g. `week_of_jun15_2026.md`)
- `docs/practice/stuck_log.md` — log for problems attempted 3+ times without mastery
