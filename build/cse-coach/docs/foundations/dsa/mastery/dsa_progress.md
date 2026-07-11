# DSA Progress

<!--
Notes for the coach / future agents:
- Columns: Difficulty, Problem, Comfort, Streak, Next Review Date, Latest Attempt Date, Attempt Dates.
- `Streak` = consecutive Clean results. Increments on Clean; resets to 0 on Shaky or Blank.
- `Next Review Date` is COMPUTED from Comfort + Streak by scripts/update_review_dates.py
  (intervals come from cse.config.yml; defaults: Clean s1 +30, s2 +60, Retired +180,
  Shaky +10, Blank +2). Do not hand-edit it — edit Comfort/Streak and re-run the script.
- At Streak == retire_at_streak (default 3), change Comfort to 🏆 to retire the problem.
  Retired problems return for a spot check every 180 days.
- The script also auto-discovers solution files under the configured roots
  (cse.config.yml → solutions.roots/globs) and adds missing rows.
- Titles should include the method when relevant, e.g. `(BFS)` / `(DFS)`; a same-number
  problem solved by a different method gets a NEW row, not an overwrite.
- The pre-commit hook runs the script when this file or a solution file is staged.
  Manual run: `python scripts/update_review_dates.py`.
- Replace the example row below with your own once you log your first problem.
-->

> **0** problems &nbsp;·&nbsp; **0** solutions &nbsp;·&nbsp; **0** attempts

| | 🏆 Retired | 🟢 Clean | 🟡 Shaky | 🔴 Blank |
|:---|:---:|:---:|:---:|:---:|
| **Solutions** | 0 | 0 | 0 | 0 |

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🔴 | 0 |  |  |  |

## Knowledge Expansion Queue

Problems for algorithmic depth — not part of the spaced-repetition stats. These enter the schedule when the relevant topic arrives. (Populated as you cross into the expansion tiers; see `../study_guide.md` and `../../../curriculum/`.)
