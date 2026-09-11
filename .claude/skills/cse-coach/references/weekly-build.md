<!-- reconciled: 2026-09-10 -->
# End-of-week close-out & schedule build

**Open this** when today is the last session of the week. **Not for** a mid-week rep (that's
`review-workflow.md`). **Not for** pricing a single day in progress (that's `effort-budget.md`
`--schedule-day`). The check is *"is today the last session of the week"* — **not** "does it feel
like a milestone" (missed Aug 2, 2026 when a long session closed out on everything *except* this).

**Archive + generate next week — both, in the same close-out, before the commit:**

```sh
git mv docs/foundations/schedules/<this-Mon>_schedule.md docs/foundations/schedules/archive/
# then write docs/foundations/schedules/<next-Mon>_schedule.md
```

Never one without the other. A week with no schedule file is not neutral: the weekly build is
where surplus is recomputed, the per-day load row is drawn (an aggregate is not a schedule), and
`technique_coverage.md` is read to pick conversion reps. Skip it and next week runs off last
week's assumptions.

## The close-out checklist

- ⭐ **End-of-week complexity cleanup (Sep 3, 2026).** Read the cleanup-queue table in
  [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md): for each queued
  problem (clean code, missed Big-O — the step-1 waiver), have the learner **re-open that code and
  re-state time + space cold, with the why**. No re-solving; only the bound. Clean → clear the row;
  missed again → keep it queued and escalate to a proper complexity teach on that category. An
  empty queue is a clean pass, not a skip.
- ⭐ **Seed ~2 cold complexity probes into the week's warmups (Sep 6, 2026).** Distinct from the
  cleanup queue: a probe fires **cold on any mature 🟢/🎓 solved problem** to keep the miss-cluster
  categories fresh. Learner states time + space cold on the existing code. **Disposable — only a
  MISS is carded** (probe ledger in `complexity_gotchas.md`); a repeated same-category miss
  escalates to a teach. Rides free on warmups, no dedicated slot.
- **⚠️ Refresh the technique comfort audit — `python scripts/technique_comfort_audit.py`.** Comfort
  + coverage auto-roll from the tracker; the **why-lines are hand-authored and preserved** (the
  script names any technique missing one) and the **FUTURE section** (roadmap algorithms not yet
  started) is hand-authored between its markers. Run it, fill any why-line it flags, update the
  future block as phases approach.
  - **Read the "⚠️ Needs work" callout at the top FIRST — it is the pull-order source.** Priority:
    **🔴/🟡 conversions (zero-green list, weakest first) > overdue 🟢 cleans > thin-green fills +
    probes.** A zero-green technique outranks *discretionary* work and *fresh* cleans — but **not** a
    clean aged far past its interval (a retention risk that manufactures new demand). A 🔴 bills ~12×
    a 🟢 forever, so converting one removes the most demand.
- **⚠️ Does the week contain a FIRST exposure to a named algorithm? Then it carries a CONCEPT
  PRIMER, scheduled before that problem.** ~15 min, unrated, no tracker row, ~1.0 unit. It covers
  the object being found and its name, the nearest neighbouring object and the one feature that
  separates them, and why the obvious approach is not enough — and stops there. **The first attempt
  lands at least a day later** (a primer measured in the same sitting measures nothing; what
  measures it is whether the recognition call fires). 332 cost five sessions because its first
  attempt WAS the introduction to Eulerian paths.
- **⚠️ Every day with NO SD slot carries at least one UNSEEN problem** — new intake from the active
  phase, or a recognition probe. Place these **before** any 🟢 backlog: a problem seen 3+ times
  measures retention of that problem's solution, not the technique; unseen problems are the only
  test of recognition and transfer.
- **⚠️ Recompute any NUMERIC reason before renewing a deferral.** An item held because "surplus is
  −9.6" or "the board is full" expires silently the moment the number moves. Re-derive it, or
  restate the hold as a **state** condition (`green:Dijkstra`, `graduates:210`).
- **⚠️ Check every active phase has reps on the board.** (Found Aug 9, 2026: `Sliding Window +
  Stack` opened Aug 3 and sat a week with zero of its 8 problems in the tracker — invisible because
  the board was full of legitimate review work.)

**Minimum contents of the built week:** capacity/surplus arithmetic · per-day load row · daily
table · protected reps · backlog/slip list (nothing dropped without a date or an explicit "no date
exists") · SD slots (placed, never priced — see `effort-budget.md`) · end-of-week targets ·
next-week preview · concept primers.

## Pricing the build

Price hypothetical days at build time only with `python scripts/effort_budget.py --day <nums>`;
never price a day already underway that way (use `--schedule-day`). Full budget rules:
`effort-budget.md`. Coverage / which technique to pull: `technique-coverage.md`.

full rule: [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md);
`decisions.yml` `complexity-cleanup-formalized`, `complexity-probe-drill`, `technique-comfort-audit`;
[`feedback_end_of_week_schedule.md`](.claude/memory/feedback_end_of_week_schedule.md),
[`feedback_concept_primer.md`](.claude/memory/feedback_concept_primer.md),
[`feedback_unseen_on_non_sd_days.md`](.claude/memory/feedback_unseen_on_non_sd_days.md).
