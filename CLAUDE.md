# cse-progress

## Repo Setup (one-time per machine/clone)

**Four one-time steps on a fresh clone — see [`docs/SETUP.md`](docs/SETUP.md):** the git hooks path,
the scaffold-links agent hook, the problem-link Stop hook, and the session-start memory hook. The last
three need a manual paste into `.claude/settings.json`, which is **gitignored** and therefore does not
sync between machines.

*(Moved out of this file Aug 3, 2026 — it is read once per machine, ever, but was loading into every
session. The rule below stayed, because it is not setup.)*

**The structural principle behind all three hooks, worth stating once:** CLAUDE.md is *always* injected;
`.claude/memory/*.md` are *opt-in reads*. A rule that must fire **unprompted** cannot live only in memory —
memory is for rules the agent will deliberately go look up. If a standing rule keeps lapsing, the question
is not "is it written down clearly enough" but **"is it a step in an executable list, or merely a
paragraph?"** All five lapses of the links rule, and the Aug 2 complexity-gate miss, were paragraphs.

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

### Scaffold scope follows what the learner named — batching needs an actual kickoff

**A message naming specific problems scaffolds exactly those problems.** "I'll do 235", "let's do
417 and 543", "235 next" → scaffold 235 (or 417+543), and nothing else. The batch rule above fires
on a **kickoff**: an explicit "start today" / "what's up today" / `/start-day`, or a first message
that asks for the day rather than for a problem. **A named problem is a request, not a kickoff** —
do not infer one from "it's the first message I've seen today," and do not treat batching as the
safe default because it's cheap. If it's genuinely ambiguous, scaffold what they named and *ask*
before batching the rest.

**Why this is a correctness rule, not a preference.** A scaffolded-but-unattempted file is not
inert:

- **Discovery plants phantom rows.** `update_review_dates.py` auto-adds any problem file it finds
  with no tracker row as **🔴 Blank / streak 0 / attempt date = today / next review = the Blank
  interval** (`discover_source_problems`). Commit a scaffold for a problem that was never attempted
  and the tracker gains a Blank that never happened, plus a near-term rep to service it — the Blank
  interval is the shortest in the ladder, so it lands almost immediately. This collides head-on
  with the end-of-session `git status` sweep, whose whole job is to catch unstaged solution files.
- **Retry scaffolds move history out of the file.** Scaffolding a retry the learner didn't ask for
  stashes their prior attempts to `.history/`. `restore_history.py` correctly declines to restore
  an unattempted stub, so the file stays blank and the stash gets committed — recoverable, but it
  ships a solution file emptied for a rep that never ran.
- ~~**The date stamp is wall-clock.**~~ **✅ FIXED AT SOURCE (Aug 2, 2026).** `new_problem.py`,
  `restore_history.py` and `update_review_dates.py` now all resolve the **session** date via
  [`scripts/session_date.py`](scripts/session_date.py) instead of `datetime.now()`, and each takes
  `--date` as an explicit override. Past midnight, a **dirty working tree** means a session is in
  progress — so the session started yesterday, and that is the date used. The scripts announce the
  override when it fires.
  - **Why the tree and not `git log`:** in a past-midnight session the last commit is usually *also*
    past midnight and carries the rolled-over date, so the git signal is polluted by the very bug
    being fixed; and because commits are batched to session end, mid-session the newest commit is
    often the *previous* session's, 24h+ back. The tree being dirty needs no timestamp at all.
    (Recent-commit is kept as a weaker secondary signal.)
  - This was a 4+ occurrence bug that recurred **three times after** being promoted to a memory
    file — the case study for why a source fix outranks a written rule. See [[feedback_session_dating]]
    and the Aug 2 meta-review in `.claude/memory/self_eval_log.md`.

So the blast radius of an unwanted scaffold is the tracker, not just a stray file. Scaffold what
was asked for.

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
- `--premium` links the free NeetCode mirror instead of the paywalled LC page. **Usually unnecessary
  as of Aug 7, 2026** — the script asks LeetCode's GraphQL API whether the problem is paid-only and
  switches hosts on its own.

**Link verification (added Aug 7, 2026).** Before printing the `LINKS:` line the script checks the slug
against `leetcode.com/graphql`: does it exist, does its `questionFrontendId` match `--number`, and is it
premium. **Warn-only — it never blocks a scaffold and is silent when offline.** Two things worth knowing:
- **A status-code check does not work on either host** and was tried first: LeetCode returns `403` to a
  HEAD for real and fake slugs alike (bot protection), NeetCode returns `200` for both (it is an SPA).
  A 404 check would pass every broken link it exists to catch. Hence GraphQL.
- **NeetCode cannot be verified at all** — no API, and the SPA answers 200 for anything. Renamed problems
  live in the hand-curated `NEETCODE_RENAMES` map in the script (`alien-dictionary` →
  `foreign-dictionary`). **Add an entry the moment a premium link is found broken**; that is the only way
  it grows, and an unlisted premium slug says so rather than implying it was checked.
- ⚠️ A TLS-trust failure is **not** treated as "offline". A Python with no root certificates fails every
  call forever, so silence would leave the check looking installed while never running. It prints one line
  naming the fix (`Install Certificates.command` / `pip install certifi`).

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
- **Restore warns on duplicate top-level names in the merged file (added Aug 2, 2026).** The slice is
  pasted verbatim and never parsed — that opacity is the invariant — but the *result* is checked with
  `ast`, and a class or function defined twice is reported. Python binds the **last** definition, so an
  undated helper in today's attempt is silently shadowed by the same-named one from a previous attempt,
  and today's code then runs the older class. Found on 211: two `TrieNode`s (today's and Jul 21's) that
  happened to be identical, so nothing crashed — the bad case. The scaffold banner already asks for a
  dated helper (`TrieNode_20260802`); the banner is prose and was skipped, so the check reads the merge
  instead. Non-fatal by design: the paste is correct and the rename is the learner's code to change.
- **The un-attempted guard now ignores scaffold method signatures inside a dated *class* attempt
  (fixed Aug 10, 2026).** `attempt_has_body` counted any non-`pass` line as work — so a design
  problem's own `def __init__(...)` / `def add(...)`, written by `new_problem.py`, made **every
  multi-method scaffold look attempted**. Restore would then paste the prior solution back before
  the rep ran, which is precisely the spoiler the extract exists to prevent. Found on 703, whose
  stub is `class KthLargest_20260810`. Single-method (`def <name>_<stamp>`) scaffolds were never
  affected — their body really is just `pass`.
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

0. **Run the recognition gate — BEFORE they write any solution code.** Have them state
   **shape → technique → the one feature that picks it** over the nearest neighbour (*weighted* edges →
   Dijkstra not BFS; marking *edges* visited not nodes → Eulerian not Hamiltonian). If they already
   wrote a pre-code comment, that comment **is** the call — confirm or correct it before they code.
   Reference: [`recognition_gotchas.md`](docs/foundations/dsa/mastery/recognition_gotchas.md) and
   `.claude/memory/feedback_recognition_gate.md`.
   - **Then log the call either way — hit AND miss — one dated line in the miss ledger.** A ledger that
     records only misses has **no denominator**: "no entries" and "never asked" look identical, so the
     recognition axis of phase exit ends up judged on the *absence* of evidence. (Found Aug 9, 2026: two
     entries in six weeks, with no way to tell a clean streak from an unfired gate.)
   - **This is the front-gate; step 1 is the back-gate.** They were written as a pair and only one of
     them was ever promoted into this list — which is exactly the lapse the complexity gate's own note
     describes. Recognition is what the interview grades in its first two minutes, and solving a problem
     you were *told the name of* never trains it.
   - ⚠️ **A retry half-spoils this** — the tracker row names the method and the file sits in a
     pattern-named folder. The *measured* recognition reps are **new problems**, **weekly probes**
     (`.claude/memory/project_recognition_probes.md`), and **cold cues** where the statement is fired
     with its method label stripped. Fire the gate on retries anyway — the habit is worth the rep — but
     don't read a retry hit as evidence for phase exit.
1. **Run the complexity gate — FIRST, before any rating is proposed.** Ask for **time AND space, each
   with an itemized why-clause** ("O(1), one fixed 26-array" — not a bare "O(1)"), and don't move on
   until they've answered or explicitly passed. Full rules, the freebie ledger, and the trigger→cue map:
   [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md) and
   `.claude/memory/feedback_ask_complexity.md`.
   - **This step exists because its absence is a silent failure.** "Correct complexity" is a criterion
     of 🟢 in step 3, so a rating proposed without it is built on an unchecked premise, and the learner
     confirms on incomplete information. Nothing in the artifacts looks wrong afterwards — which is
     exactly why the gate has to be a *step*, not a remembered precondition (missed Aug 2, 2026 on 211;
     the learner had to ask *"you never asked the time/space complexity here"*).
   - **It fires on the rep, not on the ritual.** A session that arrives as "what's the issue with my
     code" and never had a scaffold or a kickoff is still a rep. If you are about to propose a comfort
     rating, the gate is already overdue.
2. **If the learner says they're stuck — READ THEIR SOLUTION FILE BEFORE SAYING ANYTHING.** Not before
   *asserting*; before **hinting**. It is one tool call and it is free.
   - **Why it's a step and not a nicety:** on 540 (Jul 27) the coaching started immediately — worked
     array, which indices to write down, the pair-start parity rule — and the learner already had
     `m % 2 == 0` in the file. Handing over something they'd already derived wastes the rep and is a
     spoiler by any other name. The same omission then contaminated the *rating rationale*: 🔴 was
     proposed on the premise that the invariant had been supplied, and the learner had to correct the
     person rating them. Ratings set intervals, so an unverified premise here has a cost that outlives
     the session.
   - 3+ occurrences of this root cause (Jul 25, Jul 27, Jul 29). See
     `.claude/memory/feedback_read_before_asserting.md`.
3. Check the current week's schedule file (`docs/foundations/schedules/<YYYYMMDD>_schedule.md`) and mark the problem as completed in the table.
4. **Infer the Comfort rating from the session, then propose it for confirmation** — don't ask an open "how did that feel?" when the transcript already answers it. You watched the attempt: how many hints you gave, whether they self-caught their bugs, whether they could derive the approach. Propose it plainly ("That reads as 🟡 Shaky — you had the sliding window but I flagged the inverted shrink condition. Confirm?"), then log on their yes/override — never log silently. Comfort is self-reported, so their call is final, but honesty over agreeableness: if they claim 🟢 but you supplied a real fix they missed (or it was a no-code rep), say so, then defer to their call.
   - **Clean**: coded from a blank page, correct complexity, no hints. Second-guessing the data structure or peeking → Shaky. A no-code blueprint caps at Shaky (coding required); the sole exception is a flawless spot check confirming an already-🎓 Graduated problem.
   - **Shaky**: got there but needed a nudge, peeked, or wasn't fully confident mid-approach.
   - **Blank**: couldn't recall the approach; had to look it up.
5. Update `docs/foundations/dsa/mastery/dsa_progress.md` with the reported Comfort level and run the review script.
6. **At session end, before committing:** run `python scripts/restore_history.py` to paste the
   stashed prior attempts back into the problems that actually got done (see above — un-attempted
   scaffolds keep their stash out).
   - ⚠️ It now **warns on duplicate top-level names** in the merged file. Act on the warning — an
     undated helper in today's attempt is silently shadowed by the same-named one from a prior attempt.
7. **Is this the last session of the week? Then archive + generate next week's schedule BEFORE the
   commit.** `git mv` the current file into `docs/foundations/schedules/archive/`, and write
   `<next-Monday>_schedule.md`. Both, in the same close-out — never one without the other.
   - **The check is "is today the last session of the week", not "does it feel like a milestone".**
     Missed Aug 2, 2026: the session ran long on harness work and closed out cleanly on everything
     *except* this, because the rule lived only in `feedback_end_of_week_schedule.md` — a paragraph.
   - **A week with no schedule file is not a neutral state.** The weekly build is where surplus is
     recomputed, where the per-day load row gets drawn (an aggregate is not a schedule), and where
     `technique_coverage.md` is read to pick conversion reps. Skipping it means the next week runs
     off the previous week's assumptions.
   - Minimum contents: capacity/surplus arithmetic · per-day load row · daily table · protected reps ·
     backlog/slip list (nothing dropped without a date or an explicit "no date exists") · SD lanes ·
     end-of-week targets · next-week preview · **concept primers** (below).
   - **⚠️ Does the week contain a FIRST exposure to a named algorithm? Then it carries a CONCEPT
     PRIMER, scheduled before that problem.** ~15 min, unrated, no tracker row, ~1.0 unit. It covers
     **the object being found and its name**, **the nearest neighbouring object and the one feature
     that separates them**, and **why the obvious approach is not enough** — and it stops there. The
     procedure is the first rep; the proof is later and only on request.
     - **The first attempt lands at least a day later**, exactly like a teach: a primer measured in
       the same sitting measures nothing. What measures it is whether the recognition call fires.
     - *Why this is a build step and not a coaching habit:* [[feedback_algorithm_purpose_first]] and
       the `patterns/README.md` name index both already say the right thing and are both **passive** —
       one fires while you are already explaining (i.e. after a rep went wrong), the other is a lookup
       you must know to go read. **332 cost five sessions and three `stuck_log` entries because its
       first attempt WAS the introduction to Eulerian paths.** Full rationale:
       `.claude/memory/feedback_concept_primer.md`.
     - **Trialled on Intervals + Greedy (opens Aug 24, 2026), so the primer belongs in the Aug 17
       build.** DP (Oct–Nov) is the case it has to work for.
   - **⚠️ Every day with NO SD slot carries at least one UNSEEN problem** — new intake from the active
     phase, or a recognition probe. Place these **before** any 🟢 backlog. *Why:* a problem seen 3+ times
     measures retention of that problem's solution, not the technique; unseen problems are the only test
     of recognition and transfer. Full rule + the intake-cap interaction:
     `.claude/memory/feedback_unseen_on_non_sd_days.md`.
   - **⚠️ Recompute any NUMERIC reason before renewing a deferral.** An item held because *"surplus is
     −9.6"* or *"the board is full"* **expires silently the moment the number moves** — exactly the bare-date
     failure the Waiting Room rule forbids. Re-derive it, or restate the hold as a **state** condition
     (`green:Dijkstra`, `graduates:210`). Missed Aug 9, 2026: the build carried an intake freeze while
     documenting, in the same file, that the deficit had closed.
   - **⚠️ Check every active phase has reps on the board.** Found Aug 9, 2026: `Sliding Window + Stack`
     opened Aug 3 and sat a full week with **zero** of its 8 problems in the tracker — invisible because
     the board was full of legitimate review work. Nothing else in the repo surfaces an empty active phase.
8. **Do not commit per problem — batch.** Make the edits (tracker row, `stuck_log.md`, schedule strike) and move on; commit + push **once** at session end. Every commit fires the pre-commit hook, which rewrites the tracker and causes ~70 lines of it to be re-injected into context; at one commit per problem that is a large, avoidable token cost. Commit early only if the user is about to switch machines (unpushed work would strand them) or the session ends unexpectedly.

## Single source of truth for tuned values

**Every tuned number in the engine — review intervals, the effort ceiling and floor, the comfort and
difficulty weights, `graduate_at_streak` — is stated in [`cse.config.yml`](cse.config.yml) and
NOWHERE else. Prose points at it; prose never copies it.**

⚠️ **This is a correctness rule, not tidiness.** By Aug 17, 2026 every one of those knobs existed in
three places — the config, a script's `DEFAULT_CONFIG`, and CLAUDE.md prose — with nothing checking
that they agreed. They did not:

- The effort ceiling was lowered on Aug 16. The config got it; CLAUDE.md said the old number for a
  day, and **a budget check run off the stale copy passed two days that were actually over.**
- The SD lane slot was simultaneously priced at one number in `effort_budget.md`, a different one in
  the config and CLAUDE.md, and *not priced at all* by the config's own ceiling note. **Three live
  answers, and no way to tell which was current short of reading the git log.**

**The failure is always silent, and it is always the copy nobody executes from that rots** — the
executable copy gets corrected the first time it produces a wrong answer.

### The rule, operationally

| | |
|---|---|
| **Changing a value** | edit `cse.config.yml`, and **nothing else**. If you find yourself updating a second file, that file was already a bug |
| **Writing prose** | name the key and point at the config (`the ceiling — see `effort_budget.ceiling`). Never write the number |
| **Writing code** | read the config. A `DEFAULT_CONFIG` fallback is allowed **only** where the tool must run before a config exists, and it must announce loudly when it fires |
| **Recording history** | a dated entry stating what a number *was* is correct and must not be back-dated — mark it `single-source-ok` so the checker skips it |

### It is enforced, not remembered

```sh
python scripts/check_single_source.py           # report
python scripts/check_single_source.py --check   # exit 1 on drift
```

It runs from the pre-commit hook. Two checks, because the two kinds of copy fail differently:
**script defaults vs config** is an exact comparison and is a hard finding (it changes what the engine
*computes*); **prose restating a value** is heuristic and advisory (it misleads the reader, which is
how the ceiling incident happened).

⭐ **Why a script and not this paragraph:** the intervention ladder — source fix > hook > workflow
step > written rule. A written rule against duplication is itself just another copy of a rule, and
this repo's own history says prose loses. The checker is the only version that fires unprompted.

## Comfort-Based Spaced Repetition

**The values live in [`cse.config.yml`](cse.config.yml) under `intervals:` — read them there, or run
`python scripts/update_review_dates.py`, which computes every date.** They are deliberately not
reprinted here; see [Single source of truth](#single-source-of-truth-for-tuned-values) for why.

The **ladder**, which is the part that does not change:

| Comfort | Next review |
|---------|-------------|
| Clean — **provisional** (Streak 0: first Clean directly after a 🔴 Blank) | shortest Clean interval — a lock-down check |
| Clean — Streak 1 | longer |
| Clean — Streak 2 | longer still |
| 🎓 Graduated (`graduate_at_streak`+) | longest — a recurring spot check |
| Shaky | short |
| Blank | shortest of all |

**Provisional Clean (added Jul 18, 2026):** a 🟢 that *directly follows a 🔴* is logged with **Streak 0**
(not 1), so it earns only a lock-down interval to verify the Blank→Clean stuck, before the normal
Streak-1 one. Survives (Clean again) → log Streak 1; slips → resets as usual. Only **Blank→Clean** is
provisional — a 🟢 after a 🟡 is a normal Streak-1 Clean. Rationale: one Clean right after a Blank may
be recall of fresh teaching, not durable retention (same logic as the SD teach/measure split).

## Daily load is an EFFORT BUDGET, not a problem count (adopted Aug 7, 2026)

`daily_cap` is superseded. A day is budgeted in **units**, not problems:
`units = comfort_base × difficulty` — a worse comfort and a harder problem each cost more, so a day of
five 🟢 Easies and a day of five 🔴 Hards are not the same day.

**The weights, the ceiling and the floor live in [`cse.config.yml`](cse.config.yml) under
`effort_budget:`. Don't reprint them and don't hand-compute — run the script**, which reads them:

```sh
python scripts/effort_budget.py                          # demand · floor · ceiling · overdue cost
python scripts/effort_budget.py --day 560 912 235 88 100 20    # price a specific day
```

Rationale and calibration: [`docs/foundations/effort_budget.md`](docs/foundations/effort_budget.md)
(a dated derivation — read it for the *why*, never for the *values*).

⚠️ **SD IS NOT PRICED (Aug 16, 2026) — the budget is DSA-only.** The ceiling was lowered *because* SD
moved off-board: it is now the honest DSA-only number, deliberately sized so **the leftover evening is
SD's**. Do not add an SD slot to a day's total — the lowered ceiling already accounts for it, and
charging both bills it twice. `system_design.cadence` still decides how many SD slots a week gets (the
week is built here); only the cost is gone. `sd_lane_units` / `sd_deep_dive_units` are retired, and
`effort_budget.py --sd` now adds 0 and says so.

⚠️ **`cse.config.yml` is the authority on these numbers, not this paragraph** — and stale numbers
here have already caused a bad call. The ceiling sat at 9.0 in this file for a day after the change,
and a budget check run off it passed two days that were actually over. **Read the config, or just run
the script.**

**Don't hand-compute it — run the script.** At the weekly build and before accepting any overflow pull:

```sh
python scripts/effort_budget.py                          # demand · floor · ceiling · overdue cost
python scripts/effort_budget.py --day 560 912 235 88 100 20 [--sd]   # price a specific day
```

**Why this replaced the count.** Thu Aug 6, Fri Aug 7 and Sat Aug 8 were each "7 problems" and measured
**5.5 / 8.0 / 10.5 units** — the count cannot distinguish a five-minute 🟢 Easy from a 🔴 Hard, so every
weekly note reading *"Saturday is the heaviest day by some margin"* was a human patching that in prose.

⚠️ **Never raise the ceiling to catch up on a backlog.** On a Medium row a 🟡 bills **73 units/year**
against 🟢 s2's **6.1** — a rep rushed into a 🟡 costs **12× forever**, so chasing a deficit with a higher
ceiling *increases* future demand. Demand sets the **floor**; the ceiling is a quality judgment and stays
put. (Fri Aug 7 is the worked example: the board was 7.8/9, the pull that took it to 10.8 was the single
dearest item available, and it came back 🟡 with four bugs.)

## Schedule Integrity Rule

When a problem is dropped or deferred from the schedule, a new specific slot must be assigned in the same edit. Never remove a problem without immediately adding it to another day. A deferred problem with no new date is a missed problem.

After logging any problem result, check its computed next review date and add it to the appropriate week's schedule file — whether that's next week or further out. Do not leave it only in `dsa_progress.md`. The spaced repetition dates are the source of truth; the weekly schedules must reflect them. When the target week's schedule doesn't exist yet, note the problem in the nearest existing schedule's preview section. Check for balance when inserting; spread across available slots rather than stacking on already-heavy days.

## Study Guide Files

Layout: the **DSA track** owns `docs/foundations/dsa/` — `study_guide.md`, `mastery/` (its tracker),
`templates/`, plus its own reference material. **`schedules/` is cross-track and sits beside it**, not
inside `dsa/`: one weekly file plans the DSA warmups/active block *and* the SD slots.

⚠️ **The System Design boundary is CONTENT, not the whole track (settled Aug 16, 2026).** The track
left on Aug 15 and came back the next day, minus one thing. The constraint was only ever *"I don't want
premium HelloInterview details on a public repo"* — and the material that carries those excerpts is
**the mock debriefs**, not the reference notes, not the rubric, and not a tracker of question names.
Question names and tiers are on HelloInterview's free listing; the paid part is the breakdowns.

**Here, in `docs/foundations/system_design/`:** `study_guide.md` (mock mechanics) ·
`mastery/design_progress.md` (the tracker — question names, comfort, dates). Question names and tiers
are on HelloInterview's free listing; the paid part is the breakdowns, and neither of these files
carries one.

**In private [sd-progress](https://github.com/michael-yrao/sd-progress):** `senior_ramp.md` (question
order, phase gates, the 7-point rubric) · `framework.md` · `coverage_map.md` · `mocks/` (the debriefs —
the actual risk surface) · `case_studies/` · `archive/` · `concepts/` · `components/` ·
`technologies/` · `templates/`.

⚠️ **The reference cards moved twice on Aug 16, 2026 — the second move is the live one.** An earlier
pass brought `concepts/`, `components/`, `technologies/`, `senior_ramp.md` and `coverage_map.md` back
here on the argument that generic distributed-systems theory carries no HelloInterview IP. They went
back to sd-progress the same night, and the two repos on disk are the authority: **whatever the file
tree says beats whatever this paragraph says.** Check before citing a path.

**Never paste sd-progress content into this repo — link to it.** That invariant is unchanged and is now
the *whole* of the rule, since nothing else has to be remembered.

⭐ **The existing anti-spoiler rule already enforces this for free:** the mock question is named at the
session and *never* in the weekly schedule file, so the public schedule never carries one. That rule was
written to stop the breakdown being read in advance; it happens to keep the privacy boundary clean too.

**What is scheduled here and always was:** `schedules/`, `effort_budget` and `system_design.cadence` in
`cse.config.yml` plan and price a whole **day/week across both tracks**

*(There were three tracks until Aug 13, 2026. **AI System Engineering was removed** — it was never
started, never had a session, and its guide + tracker were a plan nobody had executed. It is not
deferred and there is no trigger; if it comes back it gets rebuilt from the mock model, not restored.
The one AI-flavoured design that mattered survives as a board row: **ChatGPT**, on HelloInterview's
Hard tier.)*

**Cross-track (shared)**

- `docs/foundations/schedules/<YYYYMMDD>_schedule.md` — current week's day-by-day schedule (e.g. `20260615_schedule.md`); archived to `docs/foundations/schedules/archive/`. **The when/how is workflow step 7**, not repeated here.

**DSA track**

- `docs/foundations/dsa/mastery/dsa_progress.md` — spaced repetition tracker (auto-updated by pre-commit hook)
- `docs/foundations/dsa/study_guide.md` — master plan with backlog recovery protocol
- `docs/foundations/dsa/mastery/stuck_log.md` — log for every non-Clean result: 🔴 Blank gets a full entry (where stuck, core realization, code snippet); 🟡 Shaky gets a one-liner (sticking point only)
- `docs/foundations/dsa/templates/solution_template.py` — solution-file scaffold, filled by `scripts/new_problem.py`
- `docs/foundations/dsa/mastery/techniques.yml` — **the technique vocabulary** (hand-authored); maps canonical technique → problems → method variants
- `docs/foundations/dsa/mastery/technique_coverage.md` — **generated**, do not hand-edit; `scripts/technique_coverage.py` joins the two above

### Technique coverage (keyed by technique, not by problem)

`dsa_progress.md` is keyed by **problem** — correct for scheduling reviews, structurally unable to
answer *"do I actually know topological sort?"* A technique spans several problems and sometimes
several methods of one problem, so gaps hide in plain sight. (Found Jul 28, 2026: topological sort
had three problems and all three were Kahn's — DFS-topo had never once been written, and nothing in
the repo could surface that.)

`technique_coverage.md` is regenerated by the pre-commit hook whenever the tracker, `techniques.yml`,
or any solution file is staged. Run it by hand with `python scripts/technique_coverage.py`; use
`--check` to test staleness without writing. **Read it at three moments:**

| When | What it answers |
|---|---|
| **Weekly build** (§9a) | which technique to pull — `thin` names the ones under 3–4 problems |
| **Phase exit** | the per-algorithm bar — `no-green` is the blocker list, directly |
| **Method-variant promotion** | which variants were never exercised, minus those already queued |

Three gap checks: **no-green** (execution unproven — blocks phase exit), **thin** (fewer than
`min_problems`), **variant** (a declared method with zero problems). A variant already sitting in the
Waiting Room or Expansion Queue is marked `queued:` in the YAML and reported separately — a known gap
must never re-surface as a new finding, or the report becomes noise and stops being read.

**The anti-drift guard is the `Vocabulary maintenance` section.** Every tracker row not assigned to a
technique is listed as **unmapped**, so a newly solved problem nags until it is mapped. That is what
keeps this from rotting the way the method parentheticals did (44 of 108 rows tagged, with
`(Dijkstra)` vs `(Dijkstra / Min-Heap)` already forked). **After logging a new problem, add it to
`techniques.yml` in the same edit** — same rule as re-slotting a deferred problem.

**System design track — the learner studies, you interview (rebuilt Aug 13, 2026)**

**The split:** the learner learns system design on their own via
[HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction). **Your
entire job is running cold mock interviews on HelloInterview's questions and scoring them.** Nothing on
the schedule is "read about X"; no lanes, no note-building reps, no blind sprints, no Bootstrap →
Transition → Mastery arc. Teaching happens **on request only**, off-schedule and unrated.

**Which file is where is stated once, above** — see the System Design boundary under *Study Guide
Files*. It is not repeated here: this section carried its own copy of the file list until Aug 16, 2026,
the boundary moved, only the copy upstairs was updated, and the two then contradicted each other for a
day. One list, one place.

**Before running a mock, read `sd-progress/CLAUDE.md` and `senior_ramp.md` (both over there)** — they
carry the seven numbered steps, the question order and phase gates, the 7-point rubric, the
premium-content rule, and the comfort engine. Deliberately **not duplicated here**: two copies of a
protocol drift, and the one that drifts is always the copy nobody executes from. The mock *mechanics*
live here in `docs/foundations/system_design/study_guide.md`.

**What this repo owns for SD:** the *slot*, and the *board*. The weekly schedule file plans it,
**`effort_budget` does NOT price it** (unpriced since Aug 16 — the 8.0 DSA-only ceiling leaves the
evening for it), and `system_design.cadence` decides how many a week
gets. The tracker `docs/foundations/system_design/mastery/design_progress.md` lives here too and is
rewritten by the pre-commit hook (its own block, `--tracker` rather than source discovery — there are
no SD source files). When a mock is run, **the debrief lands in sd-progress and the computed
next-review date comes back to a schedule file here** — that is the schedule-integrity rule, and the
repo split does not exempt it.

## Token discipline (efficiency by default)

Be lean: answer the thing, skip preamble, and don't restate what I can already see. Under the **caveman** skill or any low-token / low-credit setup, tighten further — telegraphic replies, caveman-compressed problem statements, no recaps. The workflow and guardrails above never change; only verbosity does. For running this repo from another agent (Copilot, caveman), see [`AGENTS.md`](AGENTS.md).

### ⚠️ A HARD CAP: an answer to a question is ONE SMALL PARAGRAPH (adopted Aug 17, 2026)

**Answering a question — not doing work, not reporting a rep — is capped at a small paragraph.
Everything else is offered, not delivered:** end with a question asking which part they want expanded,
and expand only what they pick. No preamble, no findings tables, no "two things worth knowing", no
pre-empting the next three follow-ups.

**Why it is a cap and not a preference.** The rule above already said "be lean" and the one below
already said "one job per turn", and answers kept arriving as multi-section reports with tables and
bolded asides. A long answer is not more informative — it is **less read**, so the load-bearing
sentence gets skimmed past and the work has to be re-explained anyway. Volume was doing the opposite
of its job.

**What is NOT capped**, because these are the substance and were never the problem:
- **Comfort-rating rationale** — propose + why, in full (§3 step 4).
- **Concept explanations** when stuck or asked, respecting no-spoilers.
- **`stuck_log.md` / debrief / memory-file writing** — depth belongs in the written artifact.
- **Reporting what an action actually did** when something could be wrong, or a finding that changes
  what the learner does next. State it, then stop.

⭐ **Push depth into the file, not the chat** — the same move the multi-turn rule below prescribes.
If the detail is worth keeping it belongs in a note that gets reread, not in scrollback.

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
