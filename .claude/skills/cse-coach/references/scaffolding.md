<!-- reconciled: 2026-09-11 -->
# Scaffolding a problem

**Open this** before you create or set up any problem file for the learner.
**Not for** retries' prior-attempt handling — that's `retry-and-restore.md`. **Not for**
writing any solution logic: the script writes the scaffold only; the learner writes
everything, including any `ListNode`/`TreeNode` defs (whiteboard fidelity — no shared
data-model imports).

Set the file up **before** they start — never make them create it or paste the statement.

## Scaffold scope follows what the learner named — batch only on a kickoff

- **A message naming specific problems scaffolds exactly those.** "I'll do 235", "let's
  do 417 and 543", "235 next" → scaffold those, and nothing else.
- **Batch the whole day only on a real kickoff:** an explicit "start today" / "what's up
  today" / `/start-day`, or a first message that asks for *the day* rather than for a
  problem. On a kickoff, scaffold **every** problem on the day's schedule — active block
  *and* both warmup slots, 🔴/🟡/🟢 alike — in one batch. (This repo overrides the
  cse-coach default of files-only-for-coding-reps.)
- **A named problem is a request, not a kickoff.** Do not infer a kickoff from "first
  message I've seen today," and don't batch because it's cheap. If genuinely ambiguous,
  scaffold what they named and *ask* before batching the rest.

### Why scope is a correctness rule, not a preference

A scaffolded-but-unattempted file is not inert — its blast radius is the tracker:

- **Discovery plants phantom rows.** `update_review_dates.py` auto-adds any problem file
  with no tracker row as **🔴 Blank / streak 0 / attempt date = today / next review = the
  Blank interval** (`discover_source_problems`). Commit a scaffold never attempted and the
  tracker gains a Blank that never happened, plus a near-term rep to service it (the Blank
  interval is the shortest). This collides with the end-of-session `git status` sweep.
  - ⚠️ **DELETING THE SCAFFOLD DOES NOT DELETE THE ROW — undo BOTH, in the same edit.**
    Once discovery has run, the row is independent of the file; removing the `.py` leaves
    the row and the script has nothing to reconcile it against. Delete the file AND the
    tracker row, then re-run the script to confirm the row does not return. (Found Aug 31,
    2026 on 84 — file deleted, row survived uncommitted for a rep that never happened.)
  - **Grep for a phantom:** `| Unknown | [<n>. …] | 🔴 | 0 | | | |` — **`Unknown`
    difficulty and blank dates**. Blank dates are why it hides (no scheduled demand, never
    in a due list); only reading the tracker's tail surfaces it.
- **Retry scaffolds move history out of the file.** Scaffolding a retry they didn't ask for
  stashes prior attempts to `.history/`; restore correctly declines an unattempted stub, so
  the file stays blank and the stash ships — a solution file emptied for a rep that never ran.
- **Dates are session-dated, not wall-clock (fixed at source Aug 2, 2026).**
  `new_problem.py`, `restore_history.py`, `update_review_dates.py` resolve the session date
  via [`scripts/session_date.py`](scripts/session_date.py) (a dirty tree past midnight means
  the session started yesterday); each takes `--date` to override, and announces it.

So: scaffold what was asked for.

**Consequence, stated plainly:** coding is the only path to 🟢, so scaffolding a 🟡/🟢 warmup
**raises** its ceiling from the no-code cap (🟡) to a real 🟢. Warmups are still 15-min slots
— if they'd rather blueprint one verbally, the file just goes unused; nothing is lost.

## The call

```sh
python scripts/new_problem.py --number 743 --title "Network Delay Time" --pattern graphs \
    --signature "times: List[List[int]], n: int, k: int -> int" \
    [--method networkDelayTime] [--url ...] [--premium]
```

- **New problem** → creates `dsa/leetcode/<pattern>/<number>_<snake>.py` from
  [`docs/foundations/dsa/templates/solution_template.py`](docs/foundations/dsa/templates/solution_template.py).
- **Retry** (file exists) → inserts a dated stub `def <method>_<YYYYMMDD>(self)`; never a
  second file. (Full retry handling: `retry-and-restore.md`.)
- **Always pass `--signature` on a new problem.** `self` is implied, return annotation
  optional. Without it the stub is a bare `(self)` and the learner retypes the signature
  every attempt — transcription, not recall. Repeat once per `--method`, in order, for a
  multi-method problem. On a retry it's only a fallback — the signature already in the file
  wins (it can't drift from disk).
- **Attempts are keyed by date, not a counter** (`checkInclusion_20260712`) — matches the
  file convention and keys straight to the tracker's attempt dates.
- `--premium` links the free NeetCode mirror instead of the paywalled LC page. **Usually
  unnecessary since Aug 7, 2026** — the script asks LeetCode's GraphQL API whether the
  problem is paid-only and switches hosts on its own.

**Fill the problem statement for them** — the learner never pastes it. Fetch it from the
source and write it into the `{statement}` slot. In low-token / caveman mode, write a
compressed *caveman version* instead of the full text.

### Worked example — scaffolding a new problem

```sh
$ python scripts/new_problem.py --number 743 --title "Network Delay Time" \
    --pattern graphs --signature "times: List[List[int]], n: int, k: int -> int"
Created dsa/leetcode/graphs/743_network_delay_time.py
LINKS: https://leetcode.com/problems/network-delay-time/
```

The created file holds the statement + a bare stub — no logic:

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        pass
```

## Link verification (added Aug 7, 2026)

Before printing `LINKS:` the script checks the slug against `leetcode.com/graphql`: does it
exist, does `questionFrontendId` match `--number`, is it premium. **Warn-only — it never
blocks a scaffold and is silent when offline.**

- **A status-code check does not work on either host** (tried first): LeetCode returns `403`
  to a HEAD for real and fake slugs alike (bot protection); NeetCode returns `200` for both
  (SPA). A 404 check would pass every broken link. Hence GraphQL.
- **NeetCode cannot be verified at all** — no API, SPA answers 200 for anything. Renamed
  problems live in the hand-curated `NEETCODE_RENAMES` map (`alien-dictionary` →
  `foreign-dictionary`). **Add an entry the moment a premium link is found broken** — that's
  the only way it grows; an unlisted premium slug says so rather than implying it was checked.
- ⚠️ A TLS-trust failure is **not** "offline." A Python with no root certificates fails every
  call forever, so silence would leave the check looking installed while never running. It
  prints one line naming the fix (`Install Certificates.command` / `pip install certifi`).

## Presenting the kickoff / lineup board — name + links, NOTHING else

A presented lineup — the kickoff board, a mid-session restate, a "what's next" hand-over —
carries **only the problem, as its links**: `[<n> <title>](repo-relative .py path) · [LC]`
(or `[NC]` if premium), the pair inside the problem cell. **No Note/Focus/technique/comfort/
units/difficulty column, and no technique parenthetical in the title.**

⚠️ **Any column beyond the name spoils the recognition front-gate** — the one thing the gate
exists to measure. `Course Schedule IV (Floyd-Warshall)`, a "Focus" cell reading "post-order
hinge", a Note cell with the exact miss to watch — each hands the learner the call before they
recall it. Comfort/units belong in the *schedule file* for planning; they never ride the lineup
shown to the learner. (Learner, twice: *"The tables should just be the name of the problems and
links, nothing else."*)

⭐ **Build the lineup from `scripts/links.py <n> ...`, VERBATIM — never hand-copy schedule rows.**
The script reads the title from each file's header, so it emits a clean pair with no technique
parenthetical and no Note column; hand-copying a row drags along its `(technique)` title and its
rep-directive Note cell, which is exactly how the spoiler leaks. Run it, paste the lines, add
nothing:

```sh
$ python scripts/links.py 743 332
[743 Network Delay Time](dsa/leetcode/graphs/743_network_delay_time.py) · [LC](https://leetcode.com/problems/network-delay-time/)
[332 Reconstruct Itinerary](dsa/leetcode/graphs/332_reconstruct_itinerary.py) · [LC](https://leetcode.com/problems/reconstruct-itinerary/)
```

⭐ **Recommend by number, steer by description.** When you suggest what to do next, link **only the pick**
(name + `[file]·[LC]`); refer to problems you're steering *away from* by **description, not number** — a
link is an invitation, so linking a steer-away advertises the rep you're declining. full rule:
[`feedback_recommend_by_number_steer_by_description`](.claude/memory/feedback_recommend_by_number_steer_by_description.md).

full rule: [`feedback_lineup_links_only.md`](.claude/memory/feedback_lineup_links_only.md); the links
pair itself is the links rule (both links, inside the problem cell, `NC` when premium).

## The recognition probe variant

A **recognition probe** gets a file — but at a neutral path that does **not** name the
technique (so the page can't leak the call). See `dsa/probes/README.md`. (The old "blind
sprint" exception — a page left blank *was* the rep — is gone: SD blind sprints and the AI
track were both retired Aug 13, 2026.)
