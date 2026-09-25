<!-- reconciled: 2026-09-25 -->
# End-of-week close-out & schedule build

**Open this** when today is the last session of the week. **Not for** a mid-week rep (that's
`review-workflow.md`). **Not for** pricing a single day in progress (that's `effort-budget.md`
`--schedule-day`). The check is *"is today the last session of the week"* — **not** "does it feel
like a milestone". This was missed Aug 2, 2026, when a long session closed out on everything
*except* this.

**Archive + generate next week — both, in the same close-out, before the commit:**

```sh
git mv docs/foundations/schedules/<this-Mon>_schedule.md docs/foundations/schedules/archive/
# then write docs/foundations/schedules/<next-Mon>_schedule.md
```

Never one without the other. A week with no schedule file is not neutral. The weekly build is
where surplus is recomputed, the per-day load row is drawn (an aggregate is not a schedule). It
also reads `technique_coverage.md` to pick conversion reps. Skip it and next week runs off last
week's assumptions.

## The close-out checklist

- ⭐ **End-of-week complexity cleanup.** This was set Sep 3, 2026; the queue was widened to
  every rep's misses on 2026-09-23. Read the cleanup-queue table in
  [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md). This covers any
  missed Big-O, since the rating no longer considers complexity. For each queued problem, have the
  learner **re-open that code and re-state time + space cold, with the why**. No re-solving; only the
  bound. Clean → clear the row; missed again → keep it queued and escalate to a proper complexity
  teach on that category. An empty queue is a clean pass, not a skip.
- ⭐ **Cold complexity probes fire at the Sunday close-out**, NOT scattered across weekday warmups.
  This was consolidated Sep 20, 2026 — STANDING, learner's call. ~2 probes fire **cold on any mature 🟢/🎓
  solved problem** to keep the miss-cluster categories fresh. The learner states time + space cold on
  the existing code. **Disposable — only a MISS is carded** (probe ledger in `complexity_gotchas.md`); a
  repeated same-category miss escalates to a teach. **ALL complexity checks** now live in one
  focused block on Sunday. That block covers both these probes AND the cleanup queue above. The weekday
  boards carry none, so the daily tables stay lean and the learner meets complexity work in a single sitting.
- **⚠️ Refresh the technique comfort audit — `python scripts/technique_comfort_audit.py`.** Comfort
  + coverage auto-roll from the tracker. The **why-lines are hand-authored and preserved** (the
  script names any technique missing one). The **FUTURE section** (roadmap algorithms not yet
  started) is hand-authored between its markers. Run it, fill any why-line it flags, update the
  future block as phases approach.
  - **Read the "⚠️ Needs work" callout** at the top FIRST — it is the pull-order source. Priority:
    **🔴/🟡 conversions (zero-green list, weakest first) > overdue 🟢 cleans > thin-green fills +
    probes.** A zero-green technique outranks *discretionary* work and *fresh* cleans — but **not** a
    clean aged far past its interval (a retention risk that manufactures new demand). A 🔴 bills ~12×
    a 🟢 forever, so converting one removes the most demand.
- **⚠️ Does the week contain a FIRST exposure to a named algorithm?** Then it carries a CONCEPT
  PRIMER, scheduled before that problem. ~15 min, unrated, no tracker row, ~1.0 unit. It covers
  the object being found and its name, and the nearest neighbouring object and the one feature
  that separates them. It also covers why the obvious approach is not enough, and stops there.
  **The first attempt lands at least a day later.** A primer measured in the same sitting
  measures nothing. What measures it is whether the recognition call fires. 332 cost five sessions
  because its first attempt WAS the introduction to Eulerian paths.
- **⚠️ Every day with NO SD slot carries at least one UNSEEN problem** — new intake from the active
  phase, or a recognition probe. Place these **before** any 🟢 backlog: a problem seen 3+ times
  measures retention of that problem's solution, not the technique; unseen problems are the only
  test of recognition and transfer.
- **⚠️ Recompute any NUMERIC reason before renewing a deferral.** An item held because "surplus is
  −9.6" or "the board is full" expires silently the moment the number moves. Re-derive it, or
  restate the hold as a **state** condition (`green:Dijkstra`, `graduates:210`).
- **⚠️ Check every active phase has reps on the board.** (Found Aug 9, 2026: `Sliding Window +
  Stack` opened Aug 3 and sat a week with zero of its 8 problems in the tracker. It was invisible
  because the board was full of legitimate review work.)
- **⚠️ A variant parenthetical** on the board is READ FROM the due tracker row, never hand-typed. A
  multi-variant problem has a SEPARATE tracker row per variant with its own due date. Same LC
  number, e.g. 21 Iterative vs Recursion, 130 Union-Find vs BFS. Seat the variant whose row is actually coming
  due this week, and copy its label from that row — do not free-type "(Iterative)" from habit. Found
  Sep 18, 2026: one build tagged 21/206/130 with the *other* variant in each case (already 🎓
  or due weeks later). This would have re-repped a graduated or not-yet-due variant. Its sibling in the
  method NAME is source-fixed. `new_problem.py` strips an accreted `_<date>[_variant]` from the
  stub name (self_eval 2026-09-15). The board LABEL is hand-authored, so verify it against the row.
- **⚠️ Run `python scripts/check_schedule_integrity.py` on the built week.** Beyond the result-writeback
  checks, it now flags any tracker row DUE within the week that is seated on NO day of the board. This
  is the 2026-09-14 leak. Two overdue 🔴s crossed a week boundary and slipped consecutive builds.
  Every flagged row must be seated OR have its due date pushed (a deferral gets a new date). A
  due row on no board is exactly the "nothing dropped without a date" violation.
- **⚠️ Run `python scripts/check_phantom_scaffolds.py` before the pre-commit discovery.** It flags two
  things. (a) PHANTOM ROWS: a scaffolded-but-never-attempted file discovery minted a row for (empty Rep
  Dates / `Unknown` difficulty). Record the rep, or delete the file AND the row (deleting the file alone
  leaves the row, self_eval 2026-08-31). (b) STRANDED PROBES: an earned probe still under `dsa/probes/`,
  outside `solutions.roots`, where the tooling can't maintain it (self_eval 2026-09-16). `git mv` it to
  its canonical `dsa/leetcode/<category>/` path. The upfront kickoff scaffold makes phantoms systematic,
  so this reconcile runs every close-out.
- **If the AI pillar is still PARKED, test its activation trigger** (see
  [`project_ai_pillar`](.claude/memory/project_ai_pillar.md)): DP/Backtracking phases closed AND
  `effort_budget.py` shows ≥2 days/week well under the ceiling for 2 weeks. Met → raise starting it
  with the learner; not met → say nothing. This is the firing mechanism that keeps "deferred" from
  becoming "forgotten" — don't skip it just because AI isn't on the board.

## ⚙️ How the Sunday close-out is RUN (STANDING, set Sep 20, 2026 — learner's call)

The close-out follows the repo's **plan → execute → review** split, and runs under the global execution
workflow (`~/.claude/rules/execution-workflow.md`):

| Phase | Model | What |
|---|---|---|
| **Plan** | tech lead (the session) | price capacity, read the coverage / ⚠️-Needs-work callout, decide the pulls + day placement — the whole build *design*. Get learner approval. |
| **Execute** | `engineer` agent (Sonnet) | the mechanical writeback ONLY: `git mv` the archive, write the next-week file from the approved plan, run the checker scripts, report the diff. **Never commit/push.** |
| **Review** | tech lead (the session) | review the engineer's diff, run `advisor`, then commit/push per the close-out authorization. |

The build is one engineer's worth of writeback — under the spawn rule (2:1) that means no team lead; the
tech lead supervises the engineer directly.

⭐ Never send the *planning* (judgement) or a *teach/rep* to the subagent — only the mechanical build
writeback. This is the deliberative-vs-mechanical register split (CLAUDE.md "Two registers").

Two standing passes ride every Sunday close-out:

- **⚠️ Self-eval meta-review + skill-update evaluation (Sunday, set Sep 20, 2026).** Run
  `python scripts/meta_review_digest.py` (one line per OPEN entry). For each open entry: resolved →
  consolidate it into `self_eval_archive.md`. Still live → decide whether it names a recurring miss
  that warrants a **skill / CLAUDE.md change** per the intervention ladder, and make that change
  **in this pass**. A self-eval that sits open for weeks is exactly the failure this pass exists to
  stop. Sunday is where the log gets drained and the skills get updated *because* of it, not just
  where entries pile up.
- **⚠️ Lean daily table — THE FORMAT.** This was set Sep 20, 2026, learner-approved; worked example:
  `docs/foundations/schedules/20260921_schedule.md`. The board must read **at a glance.** Columns are
  **`| Problem | S | E | Next | Technique |`**:
  - **Problem** — glyph prefix(es) + `[name](file) · [LC](url)` (a variant parenthetical stays, read from
    the tracker row per the variant rule above);
  - **S / E** — start / end comfort glyph; **Next** — next-review glyph;
  - **Technique** — exactly **ONE word** (Backtracking · Dijkstra · Kruskal · Prefix-sum · …), nothing else.

  Three homes, so nothing is lost by leaving the table. *Rep rationale* ("was 🔴 Sep 10", "template
  writable cold?") goes to the mastery ledgers (`stuck_log.md` · `complexity_gotchas.md` ·
  `recognition_gotchas.md`). *Status* (protected / backfill / new / moved / variant / probe / primer)
  goes to the **glyph** per the Tags legend, never prose. *A build caveat that truly needs a
  sentence* goes to a compact **⚙️ Build notes** list below the table, keyed by problem #. Examples:
  a move + new date, an LC-premium mirror, a scaffold note. A Note column carrying prose is a
  **build defect** — trim it. ⚠️ A cold complexity/recognition re-ask that prints its own answer in
  the board is a **spoiler bug**. This was found Sep 20: the 226 row stated "O(n): invert visits
  every node" next to a *cold* re-ask. The answer stays in the ledger; only the problem and which
  bound go on the board. full rule: `decisions.yml` `eow-close-out-process-sep20`.

**Day order:** within each day, place **all DSA first, SD last**. The SD slot gets the open-ended
tail, so SD also absorbs any overrun. Spine-then-pull has no natural stopping point; bounded DSA
reps do. Never push SD to the next day unless the learner asks (a started design that moves
becomes unratable). full rule:
[`feedback_dsa_before_sd`](.claude/memory/feedback_dsa_before_sd.md).

**Minimum contents of the built week:** capacity/surplus arithmetic · per-day load row · daily
table · protected reps · backlog/slip list (nothing dropped without a date or an explicit "no date
exists") · SD slots (placed, never priced — see `effort-budget.md`) · end-of-week targets ·
next-week preview · concept primers.

## Pricing the build

Price hypothetical days at build time only with `python scripts/effort_budget.py --day <nums>`;
never price a day already underway that way (use `--schedule-day`). Full budget rules:
`effort-budget.md`. Coverage / which technique to pull: `technique-coverage.md`.

full rule: [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md);
`decisions.yml` `complexity-cleanup-formalized`, `rating-ignores-complexity`,
`complexity-probe-drill`, `technique-comfort-audit`;
[`feedback_end_of_week_schedule.md`](.claude/memory/feedback_end_of_week_schedule.md),
[`feedback_concept_primer.md`](.claude/memory/feedback_concept_primer.md),
[`feedback_unseen_on_non_sd_days.md`](.claude/memory/feedback_unseen_on_non_sd_days.md).
