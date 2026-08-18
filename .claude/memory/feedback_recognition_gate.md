---
name: feedback_recognition_gate
description: Front-gate every rep — learner states shape→technique+why (as their pre-code comment, pasted in chat) BEFORE coding; complexity gate still fires at the end
metadata:
  type: feedback
reconciled: 2026-08-17
---

Every coded rep is bookended by two gates. The learner opted into this Jul 25, 2026.

- **Front-gate (recognition):** before writing any solution code, the learner states the
  problem's **shape → technique + why** — input structure + what's asked → candidate
  technique + the one feature that picks it. They already write pre-code comments, so they
  paste that comment in chat as the recognition call. Confirm/correct it before they code.
- **Back-gate (complexity):** unchanged — still require time+space each with an itemized
  why-clause before logging the rep ([[feedback_ask_complexity]]).

**Why:** recognition is the half of interviewing that solving-in-isolation never trains —
it's what's graded in the first two minutes. The front-gate rides free on reps already
being done and mirrors the existing complexity back-gate (recognition in, complexity out).

**How to apply:** at the start of each problem, prompt for the shape→technique call (or
accept the pasted pre-code comment). Card misses in
[recognition_gotchas.md](../../docs/foundations/dsa/mastery/recognition_gotchas.md) —
trigger→technique map — same pattern as [[feedback_ask_complexity]]'s complexity ledger.
**Retries carry the method in the tracker name, so they're half-spoiled** — the *measured*
recognition reps are new problems (nothing labeled) and cold cues where the coach fires the
statement stripped of its method label. The daily habit builds the reflex regardless.
