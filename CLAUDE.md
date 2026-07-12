# cse-review

## Repo Setup (one-time per machine/clone)

The pre-commit hook that auto-updates the spaced-repetition tracker is **version-controlled** in `.githooks/`. To activate it on a machine, run once:

```sh
git config core.hooksPath .githooks
```

This replaces the old per-machine `.git/hooks/pre-commit` (which was never synced). After this, the hook stays in sync via git across all machines.

## Token Compression (caveman)

This repo defaults to [caveman](https://github.com/juliusbrussee/caveman) at the **`lite`** level to trim routine verbosity. At session start, run **`/caveman lite`**.

**Why `lite`, and never `full` / `ultra` / `wenyan` here:** coaching and studying live in the *explanation* — the "why" behind a comfort rating, concept walk-throughs when stuck, the mentor voice, stuck-log reasoning. Aggressive levels strip exactly that context. `lite` cuts filler without gutting the teaching.

**Keep FULL even under caveman (do not compress):**
- the comfort-rating rationale (propose + why) and any Clean/Shaky/Blank reasoning
- concept explanations when the learner is stuck or explicitly asks (respecting no-spoilers)
- the "why" behind a coaching/scheduling decision
- `stuck_log.md` entries

**Fine to compress:** mechanical output — schedule edits, git steps, status summaries, confirmations.

Install once per machine (Node ≥ 18): `curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash` — Windows PowerShell: `irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex`.

## Agent Memory

Persistent behavioral preferences are stored in `.claude/memory/`. At the start of each session, read `.claude/memory/MEMORY.md` for the index, then load any files relevant to the current task.

When saving new memories or updating existing ones, always write to `.claude/memory/` in this repo — not to the local `~/.claude/projects/` path. Update `.claude/memory/MEMORY.md` to index any new files. This keeps memory in sync across machines via git.

## Scaffolding a Problem (before the learner codes)

Set the file up **before** they start — never make them create it or paste the statement.

```sh
python scripts/new_problem.py --number 124 --title "Binary Tree Maximum Path Sum" \
    --pattern trees [--method maxPathSum] [--url ...] [--premium]
```

- **New problem** → creates `dsa/leetcode/<pattern>/<number>_<snake>.py` from
  [`docs/foundations/dsa/templates/solution_template.py`](docs/foundations/dsa/templates/solution_template.py) with an `Attempt 1 · <date>` banner.
- **Retry** (file exists) → appends an `Attempt N · <date>` banner + stub to the *same* file. Never a second file.
- `--premium` links the free NeetCode mirror instead of the paywalled LC page.

**Fill the problem statement for them** — the learner never pastes it. Fetch it from the problem
source and write it into the `{statement}` slot. In low-token / caveman mode, write a compressed
*caveman version* instead of the full text.

The script writes **no solution logic and no data-structure classes** — only the scaffold. The learner
writes everything themselves, including any `ListNode`/`TreeNode` defs (whiteboard fidelity: no shared
data-model imports).

> Note: legacy solution files predate the `Attempt N` banners, so the first append to one of them will
> read `Attempt 1` regardless of real history. `dsa_progress.md` is the source of truth for attempt counts.

## LeetCode Review Workflow

After any problem discussion (solving, reviewing, or mentioning a problem by number or name):

1. Check the current week's schedule file (`docs/foundations/dsa/schedules/<YYYYMMDD>_schedule.md`) and mark the problem as completed in the table.
2. **Infer the Comfort rating from the session, then propose it for confirmation** — don't ask an open "how did that feel?" when the transcript already answers it. You watched the attempt: how many hints you gave, whether they self-caught their bugs, whether they could derive the approach. Propose it plainly ("That reads as 🟡 Shaky — you had the sliding window but I flagged the inverted shrink condition. Confirm?"), then log on their yes/override — never log silently. Comfort is self-reported, so their call is final, but honesty over agreeableness: if they claim 🟢 but you supplied a real fix they missed (or it was a no-code rep), say so, then defer to their call.
   - **Clean**: coded from a blank page, correct complexity, no hints. Second-guessing the data structure or peeking → Shaky. A no-code blueprint caps at Shaky (coding required); the sole exception is a flawless spot check confirming an already-🏆 Retired problem.
   - **Shaky**: got there but needed a nudge, peeked, or wasn't fully confident mid-approach.
   - **Blank**: couldn't recall the approach; had to look it up.
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
- `docs/foundations/dsa/templates/solution_template.py` — solution-file scaffold, filled by `scripts/new_problem.py`

## Token discipline (efficiency by default)

Be lean: answer the thing, skip preamble, and don't restate what I can already see. Under the **caveman** skill or any low-token / low-credit setup, tighten further — telegraphic replies, caveman-compressed problem statements, no recaps. The workflow and guardrails above never change; only verbosity does. For running this repo from another agent (Copilot, caveman), see [`AGENTS.md`](AGENTS.md).
