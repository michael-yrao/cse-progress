# cse-review

## Repo Setup (one-time per machine/clone)

The pre-commit hook that auto-updates the spaced-repetition tracker is **version-controlled** in `.githooks/`. To activate it on a machine, run once:

```sh
git config core.hooksPath .githooks
```

This replaces the old per-machine `.git/hooks/pre-commit` (which was never synced). After this, the hook stays in sync via git across all machines.

## Agent Memory

Persistent behavioral preferences are stored in `.claude/memory/`. At the start of each session, read `.claude/memory/MEMORY.md` for the index, then load any files relevant to the current task.

When saving new memories or updating existing ones, always write to `.claude/memory/` in this repo — not to the local `~/.claude/projects/` path. Update `.claude/memory/MEMORY.md` to index any new files. This keeps memory in sync across machines via git.

## Scaffolding a Problem (before the learner codes)

Set the file up **before** they start — never make them create it or paste the statement.

**Scaffold ALL of today's items at start-of-day — this is the default.** This repo overrides the
cse-coach default of writing files only for coding reps: at "start today" (or any session kickoff),
scaffold **every** problem on the day's schedule — active block *and* both warmup slots, 🔴/🟡/🟢
alike — in one batch, before the learner starts. New → new file; retry → appended dated attempt.
Don't ask which ones to set up.

Consequence, stated plainly: coding is the only path to 🟢, so scaffolding a 🟡/🟢 warmup **raises**
its ceiling from the no-code cap (🟡) to a real 🟢. Warmups are still 15-min slots — if they'd rather
blueprint one verbally, the file just goes unused that day; nothing is lost. Blind sprints (SD/AI
recall reps) remain the one exception: those get **nothing**, because leaving it blank *is* the rep.

```sh
python scripts/new_problem.py --number 743 --title "Network Delay Time" --pattern graphs \
    --signature "times: List[List[int]], n: int, k: int -> int" \
    [--method networkDelayTime] [--url ...] [--premium]
```

**Always pass `--signature` on a new problem.** `self` is implied and the return annotation is
optional. Without it the stub is a bare `(self)` and the learner retypes the signature every
attempt — transcription, not recall. Repeat the flag once per `--method`, in order, for a
multi-method problem. On a **retry** it's only a fallback: the signature is read from the method
already in the file, which always wins (it can't drift from what's on disk).

- **New problem** → creates `dsa/leetcode/<pattern>/<number>_<snake>.py` from
  [`docs/foundations/dsa/templates/solution_template.py`](docs/foundations/dsa/templates/solution_template.py).
- **Retry** (file exists) → inserts a dated stub `def <method>_<YYYYMMDD>(self)` at the end of the
  `Solution` class body. Never a second file.
- `--premium` links the free NeetCode mirror instead of the paywalled LC page.

**Attempts are keyed by date, not by a counter** (`checkInclusion_20260712`) — matching the existing
convention across the solution files. A counter can't be derived correctly on legacy files (they carry
no banners to count); a datestamp is always right and keys straight to the attempt dates in the tracker.

**Fill the problem statement for them** — the learner never pastes it. Fetch it from the problem
source and write it into the `{statement}` slot. In low-token / caveman mode, write a compressed
*caveman version* instead of the full text.

The script writes **no solution logic and no data-structure classes** — only the scaffold. The learner
writes everything themselves, including any `ListNode`/`TreeNode` defs (whiteboard fidelity: no shared
data-model imports).

### Retries must not show prior attempts

**The new stub goes at the TOP of the `Solution` class, and everything below it is wrapped in a
`# region ⚠ PRIOR ATTEMPTS — SPOILERS` … `# endregion` fold.** Reading your own previous solution
before a retry destroys the rep — the whole point is recall from a blank page. Bottom-appending made
the *old solution* the first thing on screen when the file opened, i.e. the spoiler was the default
view. Now the blank stub is.

The region **auto-collapses on open** via the [Explicit Folding](https://marketplace.visualstudio.com/items?itemName=zokugun.explicit-folding)
extension (`zokugun.explicit-folding`, recommended in [`.vscode/extensions.json`](.vscode/extensions.json),
rule in [`.vscode/settings.json`](.vscode/settings.json)). Auto-folding is set **per rule**, so only
this region collapses — ordinary folds (`def`, `if`, `for`) behave normally. Without the extension
the region still folds, just manually: `Ctrl+K Ctrl+8`.

It's a speed bump, not a lock — the code is one keystroke away, and that's accepted. What it buys is
that seeing it becomes a deliberate act instead of an accident.

**The load-bearing invariant:** the generated scaffold block *always ends with the region head*, and
the region *always closes at EOF*. Both markers are emitted by `new_problem.py` — neither is matched
against your old code. So the fold spans exactly "everything below today's stub" without the script
ever having to parse the shape of prior attempts, which vary a lot and are not ours to interpret.
Keep it that way; anchoring the fold on anything inside a prior solution is how this breaks.

Notes for whoever maintains this:
- Region markers are **comments**, so they carry no indentation meaning in Python. That's what lets
  one region open inside a class body and close at module level.
- Two scaffold layouts, one invariant. Single method → a dated `def <method>_<stamp>` at the top of
  `class Solution`. **Multi-method problem** (`--method encode,decode`) or a legacy file with no
  `class Solution` → a dated `class Solution_<stamp>` above the prior code, matching the convention
  [271](dsa/leetcode/arrays_and_hash/271_encode_and_decode_string.py) already used.
- The stub carries the problem's **real signature**, pulled from the existing method — retyping
  `(self, strs: List[str]) -> str` every attempt is transcription, not recall. A **new** problem has
  no prior method to read, which is what `--signature` is for; supply it or the stub is a bare
  `(self)`.
- `new_problem.py` strips the previous run's markers and re-wraps, so it's idempotent: on the next
  retry, today's attempt gets folded away too.
- The target path is derived from `--title`/`--pattern`, so a title that differs from what's on disk
  (LeetCode says "Encode and Decode String**s**"; the file is `..._string.py`) would fork the
  attempt history into two files and quietly break streak tracking. The **problem number is the real
  identity**, so the script now matches on that and **refuses** the write, naming the file it found.
  `--force-new` overrides, for the rare genuinely-distinct problem sharing a number.
- **The folding config lives in `../progressiveOverflow.code-workspace`, not in this repo.** This repo
  is normally opened as one folder of that multi-root workspace, which makes
  [`.vscode/settings.json`](.vscode/settings.json) *folder* settings — and Explicit Folding reads its
  config with **no resource** (`getConfiguration('explicitFolding', null)`), which never resolves
  folder settings. The repo keeps a synced copy of the rules for when it's opened as a lone folder;
  the workspace file is the one that actually runs. The `.code-workspace` lives outside every repo, so
  **this setup does not follow you to a new machine** — reproduce it there by hand.
  Symptom of getting this wrong: `[main] regex: /a^/` in the Explicit Folding output channel.
- **`editor.defaultFoldingRangeProvider` must be top-level, never inside `"[python]"`** — same reason:
  the extension reads it unscoped. Scoped, it looks correct, applies cleanly, and does nothing; the
  extension then falls into "proxy mode", registering a stub provider and the real one a second later
  while Pylance is still live. The auto-fold fires against Pylance's stale model, where the innermost
  region containing the `# region` line is `class Solution` — **so the whole class collapses instead
  of the spoiler region.** The cost of top-level is that the extension claims every language, which is
  why `explicitFolding.wildcardExclusions` (keeps native markdown/JSON/TS/Dart folding in the other
  folders) and the `"*"` indentation rule (fallback for the rest) are both load-bearing.
- **`foldLastLine` must stay `false` on the region rule.** `true` extends the fold onto the
  `# endregion` line, which sits at indent 0 — one line past where the class body's indentation block
  ends. The region would then start inside `class Solution` and end outside it, and VSCode silently
  discards crossing ranges. The visible `# endregion` line is the price.
- Naming the extension as Python's folding provider makes indentation folding **its** job, which is
  why the `indentation` / `offSide` rule is load-bearing — delete it and every `def`/`if`/`for` fold in
  the repo stops working. Note the `"*"` wildcard rule is appended *after* each language's own rules,
  so its `offSide` must match Python's or it silently overrides it.

## LeetCode Review Workflow

After any problem discussion (solving, reviewing, or mentioning a problem by number or name):

1. Check the current week's schedule file (`docs/foundations/dsa/schedules/<YYYYMMDD>_schedule.md`) and mark the problem as completed in the table.
2. **Infer the Comfort rating from the session, then propose it for confirmation** — don't ask an open "how did that feel?" when the transcript already answers it. You watched the attempt: how many hints you gave, whether they self-caught their bugs, whether they could derive the approach. Propose it plainly ("That reads as 🟡 Shaky — you had the sliding window but I flagged the inverted shrink condition. Confirm?"), then log on their yes/override — never log silently. Comfort is self-reported, so their call is final, but honesty over agreeableness: if they claim 🟢 but you supplied a real fix they missed (or it was a no-code rep), say so, then defer to their call.
   - **Clean**: coded from a blank page, correct complexity, no hints. Second-guessing the data structure or peeking → Shaky. A no-code blueprint caps at Shaky (coding required); the sole exception is a flawless spot check confirming an already-🏆 Retired problem.
   - **Shaky**: got there but needed a nudge, peeked, or wasn't fully confident mid-approach.
   - **Blank**: couldn't recall the approach; had to look it up.
3. Update `docs/foundations/dsa/mastery/dsa_progress.md` with the reported Comfort level and run the review script.
4. **Do not commit per problem — batch.** Make the edits (tracker row, `stuck_log.md`, schedule strike) and move on; commit + push **once** at session end. Every commit fires the pre-commit hook, which rewrites the tracker and causes ~70 lines of it to be re-injected into context; at one commit per problem that is a large, avoidable token cost. Commit early only if the user is about to switch machines (unpushed work would strand them) or the session ends unexpectedly.

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

**Caveman default = `lite` (installed by default).** Caveman ships at `full` (aggressive); this repo pins it to **`lite`** — run `/caveman lite` at session start — and **never `full` / `ultra` / `wenyan`**, which strip the explanation coaching depends on. Compress mechanical output (schedule edits, git steps, status, confirmations), but **keep FULL**: the comfort-rating rationale (propose + why), concept explanations when stuck/asked (respecting no-spoilers), the "why" behind a decision, and `stuck_log.md` entries. Install once per machine (Node ≥ 18): `curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash` (Windows: `irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex`).
