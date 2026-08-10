---
name: project-upstream-candidates
description: Findings from cse-progress that belong in canonical cse-coach, split into shipped-behaviour defects (send now) and new instruments (soak first)
metadata:
  type: project
---

**Started Aug 9, 2026.** Upstream flow is a **deliberate human PR**, never automatic — one learner's
idiosyncrasy must not become everyone's rule (cse-coach §11). This file is the staging list, not a
commitment.

**The organising split:** a **defect** in shipped behaviour needs no soak time — it is wrong for every
adopter today. A **new instrument** does, because "it seemed good on the day we invented it" is not
evidence.

---

## 🐞 Defects in shipped cse-coach behaviour — send without soak

### 1. The recognition ledger has no denominator ⭐ *(strongest)*
§3.3 says card recognition **misses** to `recognition_gotchas.md`. §5 makes recognition one of the two
phase-exit axes. **Nothing records hits** — so "a clean streak" and "the gate was never fired" produce an
identical file, and the phase-exit axis ends up judged on *absent* evidence.
**Found here:** two entries in six weeks, with no way to tell which situation that was.
**Fix:** log every fired gate, hit or miss. One line. Costs nothing and makes the axis measurable.

### 2. The complexity freebie is keyed to the wrong unit ⭐
The per-problem freebie caps a rep at 🟡 on a **repeat miss on the same problem**. But the dominant miss
class recurs **across** problems — fixed-alphabet has missed 5× on 5 different problems here, spending
five fresh freebies, and the cap fired exactly once. **A gap that recurs on one problem is decay; a gap
that recurs across five is a missing transfer** — which is worse, and is precisely what the "Recurring
categories" table exists to fix. **The enforcement mechanism is blind to the failure it most needs to catch.**
**Fix options (a menu, not a decree — it changes rating semantics):** category freebie alongside the
per-problem one · proactive cue whenever constraints name a bounded alphabet · leave as-is and rely on the
cue table.

### 3. The weekly build cannot see an active phase with zero reps ⭐
§9a is entirely **demand**-driven: due reviews, overdue counts, surplus. All of those can be healthy while
a phase that opened two weeks ago has **not one problem** in the tracker — and a full board hides it.
**Found here:** `Sliding Window + Stack` opened Aug 3, was found empty on Aug 9, and only because the
learner asked why there were no new problems.
**Fix:** a `phase status` line in `technique_coverage.py` — for each phase whose window contains today,
how many of its problems have tracker rows. Rung-1; it turns a remembered check into a computed one.
**This is the same shape as the Jul 28 technique-coverage finding:** a tracker keyed by *problem* cannot
answer *"is this phase started?"* any more than it could answer *"do I know topological sort?"*

### 4. A deferral justified by a NUMBER expires silently
§5 rightly forbids a bare **date** as a Waiting Room trigger, because a date expires with nothing
watching it. **A numeric reason has the identical property and is not covered** — an item held because
*"surplus is −9.6"* keeps not being scheduled long after the surplus turns positive, and the schedule
looks complete the whole time.
**Fix:** extend the trigger-vocabulary rule — *any deferral justified by a number must have that number
recomputed before the deferral is renewed*, and prefer restating the hold as the **state that must exist
before the item is useful** (`green:Dijkstra`) over the capacity that was missing when it was parked.

### 5. The scaffold path is a spoiler for any recognition-focused rep
`new_problem.py` writes to `<root>/<pattern>/<number>_<name>.py`. **The folder name is the technique.**
Harmless for ordinary reps; fatal for anything measuring recognition.
**Fix:** document a neutral probe root outside `solutions.roots` (it also dodges discovery-resurrection,
which the disposable-rep guidance currently handles with a `discovery_skip` stopgap).

---

## 🧪 New instruments — soak here first, revisit after ~4 weeks

### 6. Recognition probes
One unseen problem/week, label stripped, disposable (no tracker row on 🟢). **The general trigger is
already worked out and it is not learner-specific:** recognition reps **ride free on new intake**, and
intake **decays by design** in the carrying-capacity model (~3/wk at 190 rows, ~1 at 500, zero at ~700).
So recognition measurement decays with it, silently, for *every* adopter. **The probe is the successor to
new intake — it starts when intake falls below ~1 new problem/week and holds cold-recognition reps at
1–2/week indefinitely.**
**Evidence needed before upstreaming:** does the row-creation rate actually work as the
"has the pool stopped teaching" diagnostic? First probe runs Aug 11.

### 7. Coverage-gap ledger on concept cards
End every teaching session by writing what the learner's questions did **not** reach into the card, as
**bare open questions** — so one artifact is both the coverage report and an unspoiled mock-interview bank.
**The general half:** any learner-driven format (Socratic, pull-based, derive-the-design) is bounded by
what the learner can already see is missing, and cannot self-audit. That is not one learner's quirk.
**The specific half is:** it was built around this learner's spine-then-pull preference.
**Evidence needed:** does the bank get used, or does it rot like an untended backlog?

---

## 🧊 Deliberately NOT upstreaming — the bar cuts both ways

| | Why it stays local |
|---|---|
| **Spine-then-pull as the standing format** | Explicitly this learner's stated preference. The skill already ships derive-the-design as default *with a documented floor*, which is the right general shape |
| **DSA-first day ordering** | Preference. The general half — *the item with no natural stopping point goes last* — is already implied by existing lane rules |
| **`sd_lane_units: 3.0`** | A calibration, not a rule. The skill ships a value and says calibrate from your own data; that is working as intended |
| **"Unseen problem on every non-SD day"** | The *principle* is general (a problem seen 3+ times measures retention of that problem's solution, not the technique). The *formulation* is welded to this learner's SD cadence. If it goes up, it goes as the principle |
| **No-autocomplete typo weighting** | Depends entirely on how a given learner practises |
| **"attempts" → "reps"** | Cosmetic. Defensible as a default, not worth a PR on its own |
