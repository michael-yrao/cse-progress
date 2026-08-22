---
name: project-upstream-candidates
description: Findings from cse-progress that belong in canonical cse-coach, split into shipped-behaviour defects (send now) and new instruments (soak first)
metadata:
  type: project
reconciled: 2026-08-21
---

**Started Aug 9, 2026.** Upstream flow is a **deliberate human PR**, never automatic — one learner's
idiosyncrasy must not become everyone's rule (cse-coach §11). This file is the staging list, not a
commitment.

**The organising split:** a **defect** in shipped behaviour needs no soak time — it is wrong for every
adopter today. A **new instrument** does, because "it seemed good on the day we invented it" is not
evidence.

---


## 📤 Triage — Aug 17, 2026 (20 candidates)

**Shipped this session (defects — no soak, per the bar at the top of this file):**

| Item | Why it is a DEFECT, not an instrument |
|---|---|
| `scripts/check_single_source.py` | canonical has the **same duplication it detects** — SKILL.md restates the intervals in 4 places, plus two `DEFAULT_CONFIG`s. On first run there it found **12** restatements. De-personalised on the way up: `RETIRED_TERMS` ships **empty** (retired vocabulary is a repo's own history), `PROSE_GLOBS` gains `.claude/skills/**` since that is where canonical states rules, the graduated interval maps to canonical's `intervals.clean.retired` spelling, and CONFIG falls back to `cse.config.example.yml` so it runs in the template |
| `coach_sync.ENGINE_PATHS` += `decisions.yml` | the new decision log was matched by **no** pattern, so it was invisible to *both* sync directions. A new engine artifact does not become syncable on its own and neither direction complains about a file it was never told to look at |
| canonical `.githooks/pre-commit` | runs the checker, warn-only, same trigger set |

**Soaking (instruments — ~4 weeks per the standing bar):**

- `scripts/reconcile.py` + `decisions.yml` — the temporal reconciliation mechanism. **One day old.** It is the right idea and it works here, but "rules are reconciled against dated decisions" is a *new workflow* for an adopter, not a fix to something already broken. Soak until ~Sep 14, 2026, then re-assess with real usage data (how often does the backlog actually get worked?).

**Still untriaged — 11 memory files + 6 fundamentals cards.** Each needs the per-file check the bar demands (*"before declining on the skill-already-covers-it basis, actually grep the skill for it"*), and none is urgent. `feedback_answer_length` and `feedback_midweek_reprice` are the two strongest: both are general coaching rules with no learner-specific content, and both are one day old, so they soak with the instruments.

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

### 8. `problem_link_reminder.py` — a Stop hook that enforces the link rule

cse-coach ships `scaffold_links_reminder.py` (fires after a scaffold) but **nothing that checks the
coach's own prose**. That gap is measurable here: the rule *"every problem mention carries
`[file] · [LC/NC]`"* has lapsed **16+ times**, seven of them on Aug 15–16, 2026 alone — including
once in the very reply explaining why it kept happening.

**The failure mode is specific and worth shipping with the hook:** the coach reliably links problems
inside **tables and hand-off lists**, where the format prompts it, and misses them in **prose** —
overwhelmingly a trailing scheduling sentence (*"853 is now unrated"*). Every one of the seven was a
bare number in a sentence, never one in a table. A written rule does not fix this, because the lapse
is reflexive rather than considered; that is precisely the CLAUDE.md thesis that a rule which must
fire unprompted has to be **a step in an executable list, not a paragraph**.

**Two design details this repo learned the hard way, both of which should travel with it:**
- **Scope it to TODAY'S BOARD only.** An off-board problem must *not* be linked — a link is an
  invitation, and linking a problem that is not due advertises a rep the learner should not start.
  The hook resolves the day's board from the tracker's due dates plus the current schedule file.
- **Ask for the links alone, never a re-send.** The original remedy text said *"re-send the turn"*,
  which duplicates the entire message to fix one missing link — worst on the longest and most
  valuable turns. On Aug 15 a full algorithm teach was emitted twice for a single bare number.
  Changed Aug 16 to request only the missing pairs.

⚠️ **One open question before this can ship:** the hook needs the SELECTION-MENU exception, where an
unscaffolded retry's *file* link is itself a spoiler and only LC/NC may be given. That is implemented
here but has never been exercised against a second learner's layout, so it is the part most likely to
be over-fitted to this repo's paths.

**Classification: a defect, not an instrument.** Nothing about it is idiosyncratic — any adopter whose
coach names problems in prose has the same hole, and the cost (a manual file hunt, every time) is
identical for all of them.

---

---

## 🧊 Deliberately NOT upstreaming — the bar cuts both ways

| | Why it stays local |
|---|---|
| **Spine-then-pull as the standing format** | Explicitly this learner's stated preference. The skill already ships derive-the-design as default *with a documented floor*, which is the right general shape |
| **DSA-first day ordering** | Preference. The general half — *the item with no natural stopping point goes last* — is already implied by existing lane rules |
| ~~**`sd_lane_units: 3.0`**~~ **MOOT — retired Aug 16, 2026** | Was declined as "a calibration, not a rule". The key no longer exists: SD went off-board and the ceiling was lowered instead, so the SD evening is charged once on every day rather than per SD slot. Nothing to promote |
| **"Unseen problem on every non-SD day"** | The *principle* is general (a problem seen 3+ times measures retention of that problem's solution, not the technique). The *formulation* is welded to this learner's SD cadence. If it goes up, it goes as the principle |
| **No-autocomplete typo weighting** | Depends entirely on how a given learner practises |
| **"attempts" → "reps"** | Cosmetic. Defensible as a default, not worth a PR on its own |

---

## ✅ SHIPPED Aug 21, 2026 (`cse-coach@e67d201`) — every hook script was silently dead on Windows

**Found when a pre-commit run printed a traceback where the report belonged.** Promoted the same
night, no soak: canonical had the identical defect — **11 of its 13 scripts print non-ASCII and its
hook invokes Python 12 times**, with nothing setting the encoding anywhere. Ported `_console.py`, the
`force_utf8()` call in all 13 scripts, and the `PYTHONIOENCODING` export.

⭐ **Worth keeping as the model of what "defect, no soak" means in practice:** the finding was
reproduced *in canonical* before porting (a survey script crashed on the very bug it was measuring),
and the port was verified there — every script `--help`s, all 4 test modules import, the 20
fixture-free tests pass, and the three emoji-printing scripts run with `PYTHONIOENCODING` unset.
**pytest is not installed on that machine, so 12 fixture-taking tests did not run** — recorded rather
than glossed as a green suite.

Git runs `.githooks/pre-commit` with a console in the system ANSI codepage (cp1252 on Windows).
Python inherits it, so the **first emoji any script prints** — `✅`, `⚠️`, a comfort glyph inside a
problem title — raises `UnicodeEncodeError` and kills that script mid-report. **9 of the 10 scripts in
`scripts/` contain non-ASCII output**, so this is not an edge case; it is the default path.

⚠️ **The crash is not the problem. The silence is.** Every block in the hook is report-only and ends
in `|| true`, so the traceback scrolls past, the commit succeeds, and the check **appears to have
run**. `reconcile.py` fired exactly as designed — at the one moment a decision is recorded, which is
when its backlog is cheapest to act on — and printed a stack trace instead of the report. Nobody
would have noticed except by reading the commit output closely.

**Fix shipped here, two layers on purpose:**

| Layer | Change | Covers |
|---|---|---|
| Hook | `export PYTHONIOENCODING=utf-8` at the top of `.githooks/pre-commit` | every script the hook invokes, **including ones added later that forget the import** |
| Scripts | new `scripts/_console.py`; each CLI script calls `_console.force_utf8()` after its imports | every **other** context — Git Bash, a piped run, CI, an editor task — where nothing sets that variable |

Neither layer alone is sufficient and the overlap costs nothing. `errors="replace"` rather than
`"strict"`: a report rendering one glyph as `?` is still a report.

**Generality:** canonical ships the same hook shape and the same emoji-rich output, so any adopter on
Windows has a hook that looks installed and does nothing. Not learner-specific in any way.

---

## DEFECT (ships without soak) — a probe that EARNS a row becomes unreachable by both retry scripts

**Added Aug 21, 2026, found when 202's retry was scaffolded.**

The probe root exists outside `solutions.roots` so a disposable rep is never discovered — correct, and
candidate #5 above is the argument for it. **What nothing states is the exit condition.** A probe that
comes back 🟡/🔴 earns a tracker row and becomes an ordinary review problem, but its *file* stays in the
probe root, where:

- `new_problem.py` resolves a retry to `<root>/<pattern>/<n>_*.py` and checks for twins with
  `<root>/*/<n>_*.py` — neither reaches outside `solutions.roots`, so it **mints a second file** and
  forks the attempt history. That is exactly what the twin check exists to prevent, defeated by a path
  the check cannot see.
- `restore_history.py` keys a stash back with the same glob, so the extracted prior attempts are
  **orphaned** — extracted at scaffold time, never restored, and the file ships blank.

Both failures are silent and appear only at the *second* rep, potentially weeks later.

**Fix:** state the exit condition wherever the probe root is documented — *when a probe earns a tracker
row, move its file into the tracked tree in the same edit.* Rung 1 would be `new_problem.py` widening
its twin search to the probe root and offering the move, which turns a remembered step into a prompted
one.

**Generality:** not learner-specific. Any adopter with a probe/disposable root has the same hole the
moment a probe comes back non-🟢, which is the case the mechanism is *designed* to produce.

---

## DEFECT (ships without soak) — `effort_budget.py --day` cannot audit a day in progress

**Added Aug 18, 2026, the day it cost a real scheduling decision.**

`--day` takes a list of problem numbers and prices them. Two properties make it wrong the
moment a day is underway, and they compound because both understate:

1. **It prices exactly what it is handed.** Mid-session the natural list to pass is the
   *remaining* items — and that total then reads as the *day's* total, silently dropping
   everything already done.
2. **It re-reads CURRENT comfort.** Units are billed on the comfort a row carried **going in**;
   the tracker holds the comfort it **earned**. After a rep is logged the same number prices
   cheaper, so re-running the flag understates the day it was supposed to audit.

**Observed cost:** a day sitting at exactly the ceiling was reported as having 5.0 units spare,
and a discretionary consolidation rep was seated on capacity that did not exist. Caught by the
learner, not the tooling.

**Fix shipped here (all three rungs of the ladder, deliberately):**

| Rung | Change |
|---|---|
| **1 source** | new `--schedule-day [DATE]` — parses the week's schedule file and prices each row from the **`Start` column** (written at the build, never mutated), split into **built / done / remaining**. The tool defines the day, so there is nothing to mis-hand it |
| **1 source** | `--day` now warns, naming any number whose tracker row already carries a rep dated today |
| **3 step** | a CLAUDE.md rule under the effort-budget section: `--day` is a *live pricer, not a ledger* |

**Two design points worth carrying upstream, not just the flag:**

- **A total that omits rows is the same bug again.** `--schedule-day` reports its total as a
  **FLOOR** whenever a row could not be priced (a primer or probe with no problem number, or an
  untracked new problem guessed at Blank Medium when a new *Hard* costs 1.5x that). Hiding the
  gap would reproduce exactly the failure the flag exists to prevent.
- **The header check must know when to stay quiet.** `--schedule-day` also verifies each day
  header's stated units against the rows beneath it — nothing had ever checked that, so a
  *build-time* arithmetic slip was undetectable. It asserts a mismatch **only** when every row
  priced exactly; otherwise it reports the difference and says it cannot verify. A check that
  cries wrong on rows it admits it cannot see stops being read.

**Depends on:** the weekly schedule's daily table having a `Start` column and a
`> **<Day> <Mon> <D>** - N units` header. Both are conventions in this repo; canonical would need
them declared, or the parser made tolerant of their absence (it already degrades to pricing from
the tracker, with a warning, when a `Start` glyph is missing).
