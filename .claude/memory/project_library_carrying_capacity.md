---
name: project-library-carrying-capacity
description: A tracked problem bills ~0.039 slots/week forever, capping the library at ~500-600 — two valves added Jul 26 2026, graduation (🎓 above 🏆) and disposable reps (no row for a 🟢 pull/consolidation rep)
metadata:
  type: project
---

**Decided Jul 26, 2026**, from the learner's question about running out of problems as intervals
lengthen. See `docs/foundations/dsa/study_guide.md` → "Library carrying capacity".

**The constraint:** even fully retired at +180, a tracked problem bills **0.039 slots/week forever.**
At ~28 slots/week the library caps out around **500–600 problems**, and sustainable new intake decays
with size: ~3/week at 190 rows, ~2 at 350, ~1 at 500, **zero at ~700**. Unbounded "keep adding
problems" self-strangles in roughly three years.

**Valve 1 — 🎓 Graduation, the tier above 🏆.** A 🏆 problem passing **two consecutive 180-day spot
checks** leaves the tracker entirely for a plain-list `## 🎓 Graduated` section: no interval, no cost.
Re-enters at 🟡 if it ever resurfaces and fails.

**Valve 1b — the over-learned fast-track** (added Jul 26, 2026). A 🟢 problem that's been cleaned
before may skip straight to **🏆 (Streak 3, +180)** on its next clean rep, if the learner declares it
over-learned **and** the technique appears in ≥1 *harder* tracked problem still on the normal ladder.
**That coverage gate is the whole rule** — you stop testing the technique at its *easiest instance*
while harder ones keep doing the work; if no harder representative exists, the easy problem *is* the
coverage and the fast-track is refused. Cuts a row's load ~6× (0.033 → 0.006 slots/day). First
applied to 704 Binary Search, Jul 26 2026 (binary search carried by 74/875/540/33/153/2300/1011, two
of them 🟡 at the time). Aims squarely at the stale-🟢 pile, which is almost entirely Easy problems.
*Open: whether a fast-tracked 🏆 graduates after one spot check rather than two.*

**Valve 2 — disposable reps.** A [[feedback-consolidation-reps]] rep or an application pull is a
**probe testing whether a *technique* transfers**, not an asset to maintain. Solve it → log to the
technique's ledger (`recognition_gotchas.md` / `complexity_gotchas.md`) → **create no review row if it
came back 🟢.** Only 🟡/🔴 earns a row. This makes new problems nearly free: maintenance tracks ~30
*techniques*, not 700 *problems*, so 3–5 fresh pulls a week can run indefinitely. **This is the answer
whenever the learner raises staleness.**

**⚠️ The mechanical trap that breaks both — discovery resurrection.**
`update_review_dates.py` scans `dsa/leetcode/**` and **auto-adds a row for any problem it finds without
one.** So deleting a row is not enough for either valve; the next commit silently brings it back.
- **Graduating** requires *both* moving the row **and** adding the number to `discovery_skip` in
  `cse.config.yml`.
- **Probes** need either a root outside `solutions.roots` (e.g. `dsa/probes/` — preferred, but needs a
  `--probe` flag on `new_problem.py`, **not yet built**) or a `discovery_skip` entry (works today,
  grows unbounded).
- The Graduated list must stay a **plain bullet list**, never the 7-column table, or the parser eats it.

**What the tracker now means:** *"everything still unproven"* — a work queue, not a trophy case. A
**shrinking** row count is healthy. Don't report row count as progress; the accomplishment record is
the 🎓 list plus the technique ledgers. Related: [[feedback-surplus-triggered-intake]] (the capacity
math this derives from), [[feedback-phase-exit-per-algorithm]] (why techniques, not problems, are the
unit of mastery).

**Status:** documented, not yet exercised. Zero rows have reached 🏆 as of Jul 26, 2026 (max streak 2),
so the first graduation can't occur before ~2028. Disposable reps become live as soon as consolidation
reps/pulls start being scheduled.
