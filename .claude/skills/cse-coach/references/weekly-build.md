<!-- reconciled: 2026-09-20 -->
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
- ⭐ **Cold complexity probes — fire them at the Sunday close-out, NOT scattered across weekday warmups
  (consolidated Sep 20, 2026 — STANDING, learner's call).** ~2 probes fire **cold on any mature 🟢/🎓
  solved problem** to keep the miss-cluster categories fresh; the learner states time + space cold on
  the existing code. **Disposable — only a MISS is carded** (probe ledger in `complexity_gotchas.md`); a
  repeated same-category miss escalates to a teach. **ALL complexity checks — these probes AND the
  cleanup queue above — now live in one focused block on Sunday.** The weekday boards carry none, so the
  daily tables stay lean and the learner meets complexity work in a single sitting.
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
- **⚠️ A variant parenthetical on the board is READ FROM the due tracker row, never hand-typed.** A
  multi-variant problem (same LC number, e.g. 21 Iterative vs Recursion, 130 Union-Find vs BFS) has a
  SEPARATE tracker row per variant with its own due date. Seat the variant whose row is actually coming
  due this week, and copy its label from that row — do not free-type "(Iterative)" from habit. Found
  Sep 18, 2026: one build tagged 21/206/130 with the *other* variant in each case (already 🎓 or due
  weeks later), which would have re-repped a graduated or not-yet-due variant. Its sibling in the method
  NAME is source-fixed (`new_problem.py` strips an accreted `_<date>[_variant]` from the stub name,
  self_eval 2026-09-15); this is the board LABEL, which is hand-authored — so verify it against the row.
- **⚠️ Run `python scripts/check_schedule_integrity.py` on the built week.** Beyond the result-writeback
  checks, it now flags any tracker row DUE within the week that is seated on NO day of the board — the
  2026-09-14 leak (two overdue 🔴s crossed a week boundary and slipped consecutive builds). Every flagged
  row must be seated OR have its due date pushed (a deferral gets a new date); a due row on no board is
  exactly the "nothing dropped without a date" violation.
- **⚠️ Run `python scripts/check_phantom_scaffolds.py` before the pre-commit discovery.** It flags (a)
  PHANTOM ROWS — a scaffolded-but-never-attempted file discovery minted a row for (empty Rep Dates /
  `Unknown` difficulty): record the rep, or delete the file AND the row (deleting the file alone leaves
  the row, self_eval 2026-08-31); and (b) STRANDED PROBES — an earned probe still under `dsa/probes/`,
  outside `solutions.roots`, where the tooling can't maintain it (self_eval 2026-09-16): `git mv` it to
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
| **Review** | tech lead (the session) | review the engineer's diff yourself, then commit/push per the close-out authorization. |

The build is one engineer's worth of writeback — under the spawn rule (2:1) that means no team lead; the
tech lead supervises the engineer directly.

⭐ Never send the *planning* (judgement) or a *teach/rep* to the subagent — only the mechanical build
writeback. This is the deliberative-vs-mechanical register split (CLAUDE.md "Two registers").

Two standing passes ride every Sunday close-out:

- **⚠️ Self-eval meta-review + skill-update evaluation (Sunday, set Sep 20, 2026).** Run
  `python scripts/meta_review_digest.py` (one line per OPEN entry). For each open entry: resolved →
  consolidate it into `self_eval_archive.md`; still live → decide whether it names a recurring miss that
  warrants a **skill / CLAUDE.md change** per the intervention ladder, and make that change **in this
  pass**. A self-eval that sits open for weeks is exactly the failure this pass exists to stop — Sunday
  is where the log gets drained and the skills get updated *because* of it, not just where entries pile up.
- **⚠️ Lean daily table — THE FORMAT (set Sep 20, 2026, learner-approved; worked example:
  `docs/foundations/schedules/20260921_schedule.md`).** The board must read **at a glance.** Columns are
  **`| Problem | S | E | Next | Technique |`**:
  - **Problem** — glyph prefix(es) + `[name](file) · [LC](url)` (a variant parenthetical stays, read from
    the tracker row per the variant rule above);
  - **S / E** — start / end comfort glyph; **Next** — next-review glyph;
  - **Technique** — exactly **ONE word** (Backtracking · Dijkstra · Kruskal · Prefix-sum · …), nothing else.

  Three homes, so nothing is lost by leaving the table: *rep rationale* ("was 🔴 Sep 10", "template writable
  cold?") → the mastery ledgers (`stuck_log.md` · `complexity_gotchas.md` · `recognition_gotchas.md`);
  *status* (protected / backfill / new / moved / variant / probe / primer) → the **glyph** per the Tags
  legend, never prose; *a build caveat that truly needs a sentence* (a move + new date, an LC-premium
  mirror, a scaffold note) → a compact **⚙️ Build notes** list below the table, keyed by problem #. A Note
  column carrying prose is a **build defect** — trim it. ⚠️ A cold complexity/recognition re-ask that prints
  its own answer in the board is a **spoiler bug** (found Sep 20 — the 226 row stated "O(n): invert visits
  every node" next to a *cold* re-ask); the answer stays in the ledger, only the problem + which bound on
  the board. full rule: `decisions.yml` `eow-close-out-process-sep20`.

**Day order:** within each day, place **all DSA first, SD last** — the SD slot gets the open-ended tail
(spine-then-pull has no natural stopping point; bounded DSA reps do), so SD also absorbs any overrun. Never
push SD to the next day unless the learner asks (a started design that moves becomes unratable). full rule:
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
`decisions.yml` `complexity-cleanup-formalized`, `complexity-probe-drill`, `technique-comfort-audit`;
[`feedback_end_of_week_schedule.md`](.claude/memory/feedback_end_of_week_schedule.md),
[`feedback_concept_primer.md`](.claude/memory/feedback_concept_primer.md),
[`feedback_unseen_on_non_sd_days.md`](.claude/memory/feedback_unseen_on_non_sd_days.md).
