---
name: feedback_no_spoilers
description: Zero hints/approaches unless asked or stuck — the anti-spoiler anchor across three surfaces: session start/retry recap, the .history prior-attempt slice, and shared pattern docs
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `SKILL.md` invariant (never hand over the approach) +
`references/review-workflow.md` §2 (read-before-hinting; diagnose with a failing case) +
`references/retry-and-restore.md` (the prior-attempt slice is opaque by design). This file is the *why*,
and the anchor for three surfaces. Absorbs the former `no_prior_attempt_comparison` and
`check_schedule_before_docs`.

## The rule

Give **no** hints, approaches, pattern names, or algorithm reminders unless the learner **explicitly asks**
or says they're stuck.
- ✅ Answer clarifying questions about the *problem statement*; diagnose a bug in code they've already
  written (with a **failing case** — "on `[1,2,3]` this returns 5, not 6" — and let them find the fix).
- ❌ Volunteer the solution direction / data structure / "trick"; echo the stuck_log's approach when they
  start; discuss approach before they finish.

Instance of [[feedback_operating_principles]] P2 (the learner owns the thinking).

## Surface 1 — session start / retry recap

When the learner announces they'll (re)do a problem — **even a 🔴 retry with a full stuck_log entry** — do
NOT recap, "remind," or pre-load the approach, data structure, pattern, or stuck_log contents. A retry is
**retrieval from a blank page**; surfacing the direction defeats the point. *Why:* even a light *"you have
the dict/two-pass idea from stuck_log"* on 138 spoiled it — the learner noted that if they *hadn't* already
recalled it, that recap would have handed them the answer.

## Surface 2 — the `.history/` prior-attempt slice

When they ask "what's the issue with my implementation?", point at the bug **in today's code** and stop.
Do **not** open, read, or cite the prior attempts (moved to `<root>/.history/<number>_<snake>.txt` on a
retry; older files may show a `# region ⚠ PRIOR ATTEMPTS` fold) — not to compare approaches, not to say
"your last attempt had this right," not as rating evidence. *Why:* the prior attempts are extracted by
design; narrating the old solution drags the spoiler back and turns feedback into a diff against an answer
they were deliberately not looking at (*"feedback is a hint aimed forward, not a comparison aimed
backward"*). The comfort rating is inferred from today's session, never from resemblance to a previous one.

## Surface 3 — shared pattern/technique docs

Before adding a worked example, diagram, walkthrough, or "the one trap is…" note to a shared doc
(`patterns/**`, `components/**`, `concepts/**`), **check the week's schedule for problems it would reveal —
including *method variants***, since a doc can spoil one method while a different method is scheduled. If a
problem is queued today/this week, **defer** the edit, or write it and **say so before the rep** ("don't
open X until after the rep"). *Why (promoted Jul 26 after two same-session occurrences):* solution files
get elaborate protection (the stash), but pattern docs had no guard, and that's exactly where a technique
writeup and a scheduled problem collide. Both times (Dutch-flag diagrams in `two_pointer.md` with 75 on the
warmup list; three-reversals in `array_string.md` with 189 queued) were caught by *noticing*, not process —
the failure is silent, and a corrupted rating is a corrupted interval.
