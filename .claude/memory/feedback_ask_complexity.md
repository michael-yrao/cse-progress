---
name: feedback_ask_complexity
description: after a problem is coded, ASK the learner for time & space complexity before rating — don't state it for them
metadata:
  type: feedback
reconciled: 2026-08-23
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

⚠️ **READ THE LEDGER BEFORE PROPOSING THE RATING — not after (promoted 2026-08-23, 2 occurrences).**
The freebie rule above only works if its input is read *first*. Twice the rating was proposed and *then*
the ledger checked, once in each direction: **2026-08-22** on 15 — proposed 🟡 (miss caps) when the
freebie was **unspent** → should have been 🟢; **2026-08-23** on 567 — proposed 🟢 s2 when the freebie was
**spent** (a REPEAT) → the rule says 🟡. Same defect, both signs: a rating that hinges on a complexity
miss was announced to the learner before its deciding input existed. **So the sequence is fixed:**
1. learner states time + space with why-clauses (the gate);
2. if any bound is a miss, **open `complexity_gotchas.md` and read that problem's row** — is the freebie
   spent (problem already carded with a dated miss) or not?
3. *only then* propose the rating, and say the freebie state out loud ("first miss on this problem →
   freebie, no hit" / "already spent Jul 24 → repeat, caps at 🟡").
The tell you skipped it: you named a rating consequence of a complexity miss without having cited the
ledger. If you can't point to the ledger row, you haven't earned the rating yet. (Comfort override still
belongs to the learner afterward — 567 was overridden 🟡→🟢 s2 on defensible pre-constraint grounds — but
the *proposal* must be right first.)

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

## ⚠️ Known false positive in `rating_gate.py` — a RESULTS TABLE reads as a proposal (found Aug 28, 2026)

The hook blocked a turn that proposed **no rating at all**: a factual answer about the probe tally,
rendering the six past probe results as a table of 🟢/🟡 glyphs. The hook saw the glyphs, found no
complexity statement in the learner's recent messages, and blocked.

**The failure shape is not "too sensitive" — it is that a RECORD of a past result and a PROPOSAL about a
current one are lexically identical.** Same class as the link hook's orphan-number problem, which was
fixed by letting the turn carry the fixed tag `(links owed, order unchanged)` to mark a debt rather than
a pick. Candidate fixes, cheapest first:

1. **Let a turn declare itself historical** with a fixed tag the hook recognises (mirrors the link fix).
2. **Require a proposal cue**, not a bare glyph — the rating turns all say *"proposed rating"* /
   *"reads as"* / *"confirm?"*. A glyph inside a markdown table row is almost never a proposal.

⚠️ **Do not fix it by weakening the gate itself.** The gate caught two real backwards-run ratings (15 on
Aug 22, 127 on Aug 23) and that is worth occasional noise. The bug is the *trigger*, not the *rule*.
Raise at the Aug 30 reconcile pass.
