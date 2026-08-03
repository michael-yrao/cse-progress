---
name: feedback_ask_complexity
description: after a problem is coded, ASK the learner for time & space complexity before rating — don't state it for them
metadata:
  type: feedback
---

After a problem is done, **ask the learner to state the time and space complexity themselves**
before you confirm the rating. Don't announce the complexity for them.

**Why:** stating complexity is part of the thinking the learner owns ([[feedback_operating_principles]],
§0.2) — and in a real interview *they* have to volunteer it, unprompted. Reciting it for them
removes a rep and hides whether they actually know it.

**How to apply:** on any completed problem, before proposing 🟢/🟡/🔴, ask "time and space?" and let
them answer. Then confirm or correct — state the right complexity yourself only after they've
committed (or explicitly pass). Ties into [[feedback_infer_comfort]].

**✅ RESOLVED (2026-07-24) — the Big-O rating question (pinned Jul 22) is now decided.** Complexity is
enforced through the interval engine (the only real lever) via two rules:

1. **The gate (every rep, no skip):** the learner must state **time AND space, each with an itemized
   why-clause** — "O(1), one fixed 26-array" not a bare "O(1)". Naming each contributor is what
   surfaces the miss; a bare symbol hides it. Don't log any rep until they've answered (or explicitly
   passed). This supersedes the softer "ask for complexity" wording above.

2. **Per-problem freebie, then it counts:** the **first** complexity miss on a given problem →
   correct it + add it to [`complexity_gotchas.md`](../../docs/foundations/dsa/mastery/complexity_gotchas.md),
   **no rating hit**. A **repeat** complexity miss on the **same problem** (a later rep) → **caps that
   rep at 🟡**. The gotchas card doubles as the ledger: **if the problem is already on the card, its
   freebie is spent** → the next miss drops it. The gate and the correction+card entry always happen;
   the freebie only governs the *rating consequence*.

**Why per-problem (not per-category):** the problem is already the unit of spaced repetition here, so
this needs no new taxonomy — check "is this problem on the card?" and rate accordingly. It's less strict
(the same category on a different problem gets a fresh freebie), but the card still teaches the transfer
and the simplicity fits the data model. Learner chose this dial Jul 24 over per-category / separate-track.

**Diagnosis that drove it:** the misses are almost all **space**, in a small set of categories —
fixed-alphabet-array = O(1) (242, 567), recursion stack = O(depth) (206), 2D structure = O(n²) (778),
output-counting. Not general Big-O weakness; 4 specific leaks. Time is consistently correct.

**Use the card to GUIDE, not just to catch (added 2026-07-24).** The gotchas card is also a live prompt:
at complexity time, scan the code's *shape* and fire the matching checklist question — the cue, never
the answer. Trigger → cue: **recursion** → "count the stack, how deep?"; **`[0]*k` fixed array** →
"bounded by input or by the alphabet?"; **grid `visited`/heap of cells** → "frontier: a line or an
area?"; **returns a built structure** → "counting the output or extra-only?".

**First run vs review — opposite postures:**
- **New problem (first-ever attempt):** complexity is a **guided teaching moment**. Cue the checklist
  **proactively, before they answer**, name the category, card it. **Double freebie** — *two* free
  misses before repeats cap at 🟡 — because first exposure means learning the algorithm *and* its
  analysis at once. (Reviews get one freebie.)
- **Review:** ask **cold** — they own the analysis. Cue the *why* only if they give a bare symbol or
  miss. One freebie (ledger state in the card).

The card thus **teaches forward on new problems and tests on reviews**; the trigger→cue map lives in
[`complexity_gotchas.md`](../../docs/foundations/dsa/mastery/complexity_gotchas.md).

## ⚠️ WHEN it fires (added 2026-08-02, after the gate was skipped entirely on 211)

The gate is **step 1 of CLAUDE.md's LeetCode Review Workflow** — ahead of the schedule mark and ahead of
the rating. It was moved there because keeping it *only* here, as a precondition to a workflow that didn't
list it, meant the workflow could reach the rating step without it — and did. Step 3's 🟢 definition
requires *"correct complexity"*, so the list was consuming an input it never gathered.

- **It fires on the rep, not on the ritual.** 211 arrived as *"whats the issue with my code here"* — no
  `new_problem.py` call, no kickoff, no front-gate. None of the usual cues fired, and the gate went with
  them. **The trigger is: am I about to propose a comfort rating?** If yes, the gate is already overdue.
- **The failure is silent, which is why it needs to be a step.** A skipped gate leaves every artifact
  looking correct — no wrong date, no unstaged file, nothing that surfaces later. Only the learner can
  catch it, in the moment, and on 211 that is exactly what happened.
- **Late is better than never, but say so.** Running it after the rating means their confirmation was
  given on incomplete information — re-check whether the miss changes the rating and tell them either way.
