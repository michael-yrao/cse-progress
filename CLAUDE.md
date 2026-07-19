# cse-progress

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

**On a retry the new stub goes at the TOP of the `Solution` class, and everything below it (the prior
attempts) is MOVED OUT of the file into a per-problem stash at `<root>/.history/<number>_<snake>.txt`.**
Reading your own previous solution before a retry destroys the rep — the whole point is recall from a
blank page. So the spoiler isn't hidden, it's *physically absent* while you work: the file on disk
holds only the statement and today's blank stub, plus a one-line pointer to the stash.

This needs **no editor and no extension** — it reads as a blank page in any editor, on GitHub, in a
plain `git diff`. That portability is the whole reason for the stash: the old approach folded the
prior attempts with the `zokugun.explicit-folding` extension, whose auto-collapse config had to live
in an external `.code-workspace` and be reproduced by hand on every machine. All of that is gone.

It's a speed bump, not a lock — the stash file is one click away, and that's accepted. What it buys is
that seeing your old solution becomes a deliberate act instead of an accident.

### Restore the stash once the day's reps are done

The stash is protection *before* the attempt. Once the rep is written, the prior attempts belong back
in the file as dated history — so **restore them at end of session, before the commit**:

```sh
python scripts/restore_history.py            # today's completed attempts
python scripts/restore_history.py --dry-run  # report only
```

Restore pastes the stash back *after* today's completed attempt (recent on top), deletes the stash
file, and strips the pointer — reconstructing the single file with full dated history, exactly as it
was before the extract. It also migrates **legacy folded files**: any solution still carrying an old
`# region ⚠ PRIOR ATTEMPTS` fold has the markers stripped here (same guard, no stash involved).

**It only restores a problem whose dated attempt has a real body.** A retry that was scaffolded but
never attempted still has `pass` under today's stub — pasting the prior attempts back would expose the
old solution before the rep ever happened, the exact failure the extract prevents. Those keep their
stash *out* of the file and get reported as kept. `--all` overrides the guard (for reconciling old
files, never at session end).

**Committed, but self-clearing.** `.history/` is tracked, not ignored. On a normal day, restore empties
it before the session-end commit, so nothing extra is committed. If a session is **cut short**, the
stash files are still committed — so the extracted state travels to the next machine (where restore
finishes the job). A cut-short then resumed retry re-extracts safely: an un-attempted stub is dropped
and the existing stash is left untouched (never clobbered with an empty stub).

**The load-bearing invariant (unchanged from the fold era):** today's stub goes at the top, and
*everything below it* is the prior-attempts slice — a **verbatim line slice**, moved to the stash and
later pasted back without the script ever parsing its shape (dated methods, dated sibling classes,
trailing unittest blocks all vary and are not ours to interpret). Extract cuts at EOF; restore appends
at EOF; today's attempt sits above. Keep it that way — anything that reaches *into* a prior solution to
decide the cut is how this breaks.

Notes for whoever maintains this:
- The stash is a **`.txt`**, deliberately: it never matches the `*.py` source glob, so the tracker's
  discovery (`scripts/update_review_dates.py`) ignores it and no phantom problem row appears. If you
  ever add `.txt` to `source_globs`, exclude `.history/` there.
- Two scaffold layouts, one slice. Single method → a dated `def <method>_<stamp>` at the top of
  `class Solution`; the slice is the remaining indented methods. **Multi-method problem**
  (`--method encode,decode`) or a legacy file with no `class Solution` → a dated `class Solution_<stamp>`
  at module level, matching [271](dsa/leetcode/arrays_and_hash/271_encode_and_decode_string.py); the
  slice is the prior module-level classes. Either way the slice pastes straight back.
- The stub carries the problem's **real signature**, pulled from the existing method — retyping
  `(self, strs: List[str]) -> str` every attempt is transcription, not recall. A **new** problem has
  no prior method to read, which is what `--signature` is for; supply it or the stub is a bare
  `(self)`.
- `new_problem.py` strips any leftover pointer and any legacy `# region` markers before re-extracting,
  so it's idempotent and migrates old folded files on their next retry.
- `restore_history.py` keys the stash back to its source file by **problem number** (globs
  `<root>/*/<number>_*.py`), because the stash filename drops the pattern folder. The number is the
  identity — same reason `new_problem.py` matches on it.
- The target path is derived from `--title`/`--pattern`, so a title that differs from what's on disk
  (LeetCode says "Encode and Decode String**s**"; the file is `..._string.py`) would fork the
  attempt history into two files and quietly break streak tracking. The **problem number is the real
  identity**, so the script matches on that and **refuses** the write, naming the file it found.
  `--force-new` overrides, for the rare genuinely-distinct problem sharing a number.

## LeetCode Review Workflow

After any problem discussion (solving, reviewing, or mentioning a problem by number or name):

1. Check the current week's schedule file (`docs/foundations/schedules/<YYYYMMDD>_schedule.md`) and mark the problem as completed in the table.
2. **Infer the Comfort rating from the session, then propose it for confirmation** — don't ask an open "how did that feel?" when the transcript already answers it. You watched the attempt: how many hints you gave, whether they self-caught their bugs, whether they could derive the approach. Propose it plainly ("That reads as 🟡 Shaky — you had the sliding window but I flagged the inverted shrink condition. Confirm?"), then log on their yes/override — never log silently. Comfort is self-reported, so their call is final, but honesty over agreeableness: if they claim 🟢 but you supplied a real fix they missed (or it was a no-code rep), say so, then defer to their call.
   - **Clean**: coded from a blank page, correct complexity, no hints. Second-guessing the data structure or peeking → Shaky. A no-code blueprint caps at Shaky (coding required); the sole exception is a flawless spot check confirming an already-🏆 Retired problem.
   - **Shaky**: got there but needed a nudge, peeked, or wasn't fully confident mid-approach.
   - **Blank**: couldn't recall the approach; had to look it up.
3. Update `docs/foundations/dsa/mastery/dsa_progress.md` with the reported Comfort level and run the review script.
4. **At session end, before committing:** run `python scripts/restore_history.py` to paste the
   stashed prior attempts back into the problems that actually got done (see above — un-attempted
   scaffolds keep their stash out).
5. **Do not commit per problem — batch.** Make the edits (tracker row, `stuck_log.md`, schedule strike) and move on; commit + push **once** at session end. Every commit fires the pre-commit hook, which rewrites the tracker and causes ~70 lines of it to be re-injected into context; at one commit per problem that is a large, avoidable token cost. Commit early only if the user is about to switch machines (unpushed work would strand them) or the session ends unexpectedly.

## Comfort-Based Spaced Repetition

Next review intervals (set in `docs/foundations/dsa/mastery/dsa_progress.md` and computed by `scripts/update_review_dates.py`):

| Comfort | Next Review |
|---------|-------------|
| Clean — **provisional** (Streak 0: first Clean directly after a 🔴 Blank) | **+10 days** (lock-down check) |
| Clean — Streak 1 | +30 days |
| Clean — Streak 2 | +60 days |
| Clean — Retired (Streak 3+) | +180 days (spot check) |
| Shaky   | +10 days    |
| Blank   | +2 days     |

**Provisional Clean (added Jul 18, 2026):** a 🟢 that *directly follows a 🔴* is logged with **Streak 0**
(not 1) → it earns only a **+10 lock-down** to verify the Blank→Clean stuck, before the normal +30. Survives
(Clean again) → log Streak 1 (→ +30); slips → resets as usual. Only **Blank→Clean** is provisional — a 🟢
after a 🟡 is a normal Streak-1 Clean. Rationale: one Clean right after a Blank may be recall of fresh
teaching, not durable retention (same logic as the SD teach/measure split). Interval configurable via
`clean_provisional` in `cse.config.yml`.

## Schedule Integrity Rule

When a problem is dropped or deferred from the schedule, a new specific slot must be assigned in the same edit. Never remove a problem without immediately adding it to another day. A deferred problem with no new date is a missed problem.

After logging any problem result, check its computed next review date and add it to the appropriate week's schedule file — whether that's next week or further out. Do not leave it only in `dsa_progress.md`. The spaced repetition dates are the source of truth; the weekly schedules must reflect them. When the target week's schedule doesn't exist yet, note the problem in the nearest existing schedule's preview section. Check for balance when inserting; spread across available slots rather than stacking on already-heavy days.

## Study Guide Files

Layout: each **track** owns a folder under `docs/foundations/` (`dsa/`, `system_design/`,
`ai_engineering/`) with the same shape — `study_guide.md`, `mastery/` (its tracker), `templates/`,
plus its own reference material. **`schedules/` is cross-track and sits beside them**, not inside
`dsa/`: one weekly file plans the DSA warmups/active block *and* the SD slots *and* AI builds. Its
per-track trackers stay in each track's `mastery/`.

**Cross-track (shared)**

- `docs/foundations/schedules/<YYYYMMDD>_schedule.md` — current week's day-by-day schedule (e.g. `20260615_schedule.md`); archive the current week's schedule and generate the next week's schedule together at the end of the last session of the week — move the current file to `docs/foundations/schedules/archive/`

**DSA track**

- `docs/foundations/dsa/mastery/dsa_progress.md` — spaced repetition tracker (auto-updated by pre-commit hook)
- `docs/foundations/dsa/study_guide.md` — master plan with backlog recovery protocol
- `docs/foundations/dsa/mastery/stuck_log.md` — log for every non-Clean result: 🔴 Blank gets a full entry (where stuck, core realization, code snippet); 🟡 Shaky gets a one-liner (sticking point only)
- `docs/foundations/dsa/templates/solution_template.py` — solution-file scaffold, filled by `scripts/new_problem.py`

**System design track**

- `docs/foundations/system_design/mastery/design_progress.md` — technology-fluency tracker; same 7-column table and same interval math as DSA, same script (`update_review_dates.py --tracker …`), rows added by hand
- `docs/foundations/system_design/study_guide.md` — mission, Interview-ROI line, tiers
- `docs/foundations/system_design/technologies/<tech>.md` — per-technology note + Recall Card (the blind-sprint rep)

## Token discipline (efficiency by default)

Be lean: answer the thing, skip preamble, and don't restate what I can already see. Under the **caveman** skill or any low-token / low-credit setup, tighten further — telegraphic replies, caveman-compressed problem statements, no recaps. The workflow and guardrails above never change; only verbosity does. For running this repo from another agent (Copilot, caveman), see [`AGENTS.md`](AGENTS.md).

**Interactive sessions — one job per turn (avoid walls of text).** In derive-the-design, Socratic
pushback, or failure-mode drills, keep **each turn to one job**: a one-line affirmation + at most one
correction + one question, then stop. The back-and-forth *is* the teaching — a turn must not also
sharpen, tabulate, and pre-empt the next three follow-ups. **Push depth into the written note, not the
chat:** tables, mnemonics, full derivations belong in the tech/tracker note (e.g. a `technologies/<tech>.md`),
updated live and referenced ("added to your note") so the chat stays conversational and the note is the
thing they reread. Use **progressive disclosure** — short answer first, *offer* the deeper why rather
than dumping it — and when the learner nails an answer, acknowledge in one line and move on; never
re-explain what they just demonstrated. This is the [Spine-first rule](#) applied across a whole
multi-turn session. (The depth still matters — this is about *packaging*, not cutting substance.)

**Teaching a new algorithm — procedure-first, not proof-first.** When the learner is trying to
understand or code an algorithm they don't know, lead with the **literal loop in plain operational
language** (*"each round: pick the unvisited node with the smallest number, mark it done, update its
neighbors"*) and **run it by hand on a tiny 3–4 element example as concrete numbers**. Introduce the
correctness proof, complexity, and named concepts (jargon) **only later, and only if they ask "why does
this work?"** — for an algorithm-you're-coding, the load-bearing thing is the *procedure*, not the
theorem (this is what "spine-first" means for algorithms). Separate **execute it** from **why it's
optimal** — two lessons; get execution first (greedy-correctness proofs especially are the hardest part
and are *not* needed to write the code). Answer a **mechanics question with mechanics**, never with more
concept. Strip jargon unless they ask for the name. **The tell:** when they say "this makes no sense,"
strip *down* to the concrete procedure — never add another layer of *why*. (Learned the hard way on
Prim's/1584, Jul 18 — opened with the cut-property proof + "settled" + complexity before the learner
could run a single step; their own plain code comments were clearer than the explanation.)

**Caveman default = `lite` (installed by default).** Caveman ships at `full` (aggressive); this repo pins it to **`lite`** — run `/caveman lite` at session start — and **never `full` / `ultra` / `wenyan`**, which strip the explanation coaching depends on. Compress mechanical output (schedule edits, git steps, status, confirmations), but **keep FULL**: the comfort-rating rationale (propose + why), concept explanations when stuck/asked (respecting no-spoilers), the "why" behind a decision, and `stuck_log.md` entries. Install once per machine (Node ≥ 18): `curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash` (Windows: `irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex`).
