<!-- reconciled: 2026-09-11 -->
# LeetCode review workflow — gate detail

**Open this** for any problem discussion (solving, reviewing, or the learner mentioning a
problem by number or name). **Not for** setting the file up (`scaffolding.md`) or the weekly
close-out (`weekly-build.md`). **Not a tempo to impose** — it's the checklist for closing a
rep correctly; the learner sets when to move on (SKILL.md principle 3).

The step spine is in SKILL.md §3. This file carries the gate detail and the "why".

## Step 0 — Recognition gate (before any solution code)

Have them state **shape → technique → the one feature that picks it** over the nearest
neighbour (*weighted* edges → Dijkstra not BFS; marking *edges* visited not nodes → Eulerian
not Hamiltonian). If they already wrote a pre-code comment, **that comment IS the call** —
confirm or correct it before they code.

- ⚠️ **The learner writes the call; the coach must not lead.** When you prompt verbally, name
  only the **shape cues** and ask for the technique — **never list candidate techniques.** A
  leading multiple-choice (*"monotonic deque or a heap?"*) hands over the answer (the spoiler
  that leaked on 239, Aug 20). The scaffold no longer prints a RECOGNITION block (removed
  Aug 22, 2026) — the anti-spoiler purpose rests on the top-comment habit plus this rule.
- ⚠️ **The top-of-method comment IS the call — the block is optional (Aug 21, 2026).** Read
  the top comment as the call; never re-demand a scaffold block, never read a blank block as a
  missing gate. Being asked to use a form is what makes them route around it. Don't build a
  mechanism to police comment order — enforcement is trust-based; the ungameable measure is the
  **cold hit rate over ~15 label-stripped probes**, not per-rep policing.
- **Log the call either way — hit AND miss — one dated line in the miss ledger.** A miss-only
  ledger has no denominator: "no entries" and "never asked" look identical (found Aug 9, 2026:
  two entries in six weeks, no way to tell a clean streak from an unfired gate).
- **Front-gate vs back-gate:** this is the front-gate, the complexity gate is the back-gate.
  Recognition is what the interview grades in its first two minutes; solving a problem you were
  *told the name of* never trains it.
- ⚠️ **A retry half-spoils this** (the row names the method, the folder names the pattern). The
  *measured* recognition reps are **new problems**, **weekly probes**, and **cold cues**
  (statement fired with its label stripped). Fire the gate on retries anyway for the habit, but
  don't read a retry hit as evidence for phase exit.

full rule: [`recognition_gotchas.md`](docs/foundations/dsa/mastery/recognition_gotchas.md),
[`feedback_recognition_gate.md`](.claude/memory/feedback_recognition_gate.md),
[`project_recognition_probes.md`](.claude/memory/project_recognition_probes.md); `decisions.yml`
`recognition-block-removed-from-scaffold`, `recognition-call-is-the-top-comment`.

## Step 1 — Complexity gate (before any rating is proposed)

Ask for **time AND space, each with an itemized why-clause** ("O(1), one fixed 26-array" — not
a bare "O(1)"); don't move on until they answer or explicitly pass.

- **It exists because its absence is a silent failure.** "Correct complexity" is a 🟢 criterion
  (step 4), so a rating proposed without it rests on an unchecked premise and the learner
  confirms on incomplete information — nothing looks wrong afterwards. (Missed Aug 2, 2026 on
  211; the learner had to ask *"you never asked the time/space complexity here"*.)
- **It fires on the rep, not the ritual.** A session arriving as "what's wrong with my code"
  with no scaffold or kickoff is still a rep. If you're about to propose a rating, it's overdue.
- ⭐ **Clean code + a Big-O miss does NOT cap the rating (Sep 3, 2026).** When **recognition AND
  code were clean off a blank page** and the *only* miss was a complexity bound, rate on the
  code (a clean rep is 🟢) and **do not apply the freebie/repeat-🟡 cap** — re-repping clean code
  to re-ask its Big-O is churn. Instead **queue the missed bound in the end-of-week complexity
  cleanup**, re-asked cold at the close-out (`weekly-build.md`). Scope is exactly *clean code +
  Big-O miss*; if the code needed a real fix, the normal freebie→🟡 cap stands. Always still
  correct the miss and ledger it — the waiver moves the *rating consequence* and *re-test
  timing*, never whether the concept is tested.

full rule: [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md),
[`feedback_ask_complexity.md`](.claude/memory/feedback_ask_complexity.md); `decisions.yml`
`complexity-cleanup-formalized`.

## Step 2 — Stuck? Read their solution file before hinting

Not before *asserting* — before **hinting**. It is one tool call and it is free. On 540
(Jul 27) coaching started immediately (worked array, indices, the pair-start parity rule) and
the learner already had `m % 2 == 0` in the file — handing over something they'd derived wastes
the rep and is a spoiler. It then contaminated the *rating*: 🔴 was proposed on a false premise
and the learner had to correct the person rating them. Ratings set intervals, so an unverified
premise here outlives the session. 3+ occurrences (Jul 25/27/29).

full rule: [`feedback_read_before_asserting.md`](.claude/memory/feedback_read_before_asserting.md).

## Steps 3–5 — Mark, rate, log

3. Mark the problem completed in the current week's schedule table.
4. **Infer the comfort rating, propose it plainly for confirmation** — don't ask an open "how
   did that feel?" when the transcript answers it. Judge from what you watched: how many hints,
   whether they self-caught bugs, whether they derived the approach. Propose + log on their
   yes/override — never silently. Comfort is self-reported, so their call is final; honesty over
   agreeableness — if they claim 🟢 but you supplied a real fix they missed (or it was a no-code
   rep), say so, then defer. The **rating rationale is not length-capped**: propose + why, in
   full. Scale + ladder: `spaced-repetition.md`. full rule:
   [`feedback_infer_comfort.md`](.claude/memory/feedback_infer_comfort.md).
5. Update `docs/foundations/dsa/mastery/dsa_progress.md`; the pre-commit hook recomputes dates.
   Log non-Clean in `stuck_log.md` (🔴 full entry: where stuck, core realization, snippet;
   🟡 one-liner: sticking point only). Add the problem to `techniques.yml` in the same edit
   (see `technique-coverage.md`).

## Schedule integrity

**Any lineup or restate table you present** (mark-completed step, "what's next", hand-over) is **problem
name + links only** — build from `python scripts/links.py <n> ...`, no Note/Focus/technique/comfort column
(it spoils the recognition gate). See `scaffolding.md` → "Presenting the kickoff / lineup board".

When a problem is dropped or deferred, **a new specific slot is assigned in the same edit** —
never remove a problem without immediately adding it to another day. A deferred problem with no
new date is a missed problem. After logging any result, add its computed next-review date to the
appropriate week's schedule (this week or further out); don't leave it only in the tracker. The
spaced-repetition dates are the source of truth; the schedules must reflect them. When the
target week's file doesn't exist yet, note the problem in the nearest schedule's preview section.
Spread across available slots rather than stacking on already-heavy days.

⭐ **The near half is checked, not remembered (Aug 21, 2026):**

```sh
python scripts/check_schedule_integrity.py          # current week: done rows vs the tracker
python scripts/check_schedule_integrity.py --check  # exit 1 on a finding
```

Runs from the pre-commit hook when a tracker or schedule file is staged. Reports two things: a
**struck row missing its `End`/`Next`**, and a **rep the tracker dates inside this week whose
row is not struck**. ⚠️ It does **not** verify every future date is pre-placed — distant dates
are *pulled* by the weekly build's tracker sweep, so that reading would report ~73 of 115 healthy
rows. The paragraph above is still yours to run.

## Step 8 — Ask before every commit and every push

Make the edits, say what is staged, and **stop**. Accumulate edits across the session; they land
in one commit when the learner says so. Commit early only if the learner is about to switch
machines or the session ends unexpectedly — and then *say so and ask*, never decide unilaterally.
The normative rule lives in the always-injected CLAUDE.md (that copy wins); this is the workflow
step. full rule: [`feedback_commit_discipline.md`](.claude/memory/feedback_commit_discipline.md).
