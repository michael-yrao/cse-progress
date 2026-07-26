---
name: feedback-check-schedule-before-docs
description: Before writing solution content into shared pattern/technique docs, check today's and this week's schedule — a worked example is a spoiler for whoever has that problem queued
metadata:
  type: feedback
---

**Promoted Jul 26, 2026** after two occurrences in a single session.

**The rule:** before adding a worked example, diagram, walkthrough, or "the one trap is…" note to a
shared doc (`patterns/**`, `components/**`, `concepts/**`), **check the current schedule file for the
problems it would reveal**. If any is queued today or this week, either defer the edit until after the
rep, or write it and **say so explicitly before the rep starts** so the learner can avoid the file.

**Why:** solution files get elaborate protection — a retry stashes prior attempts out of the file
entirely so it reads blank in any editor ([[feedback_no_prior_attempt_comparison]]). Pattern docs had
no equivalent guard, yet they're exactly where a technique writeup and a scheduled problem collide.
Documentation work and rep scheduling feel like independent workstreams; they aren't. The failure is
silent — nothing errors, the learner just opens a reference mid-rep and gets handed the answer, and
the rating is quietly corrupted ("the interval is the consequence of the rating").

**What it looked like both times (Jul 26):** wired Dutch-flag diagrams + a Sort Colors walkthrough into
`two_pointer.md` with **75 on that day's warmup list**; wrote the three-reversals rotation section into
`array_string.md` with **189 on the same list**, three-reversals being the learner's own method. Both
were caught before the rep, but by noticing rather than by process — and the first was partly defused
by an unrelated decision of the learner's.

**How to apply:**

1. **Check before writing, not after.** Read the week's `schedules/<YYYYMMDD>_schedule.md` for problem
   numbers the edit would spoil — including *method variants*, since a doc can spoil one method of a
   problem while a different method is what's scheduled.
2. **Disclose plainly if it's already written.** "Don't open X until after the rep" — one line, before
   they start, never after.
3. **Prefer deferring** when the problem is queued the same day. The doc improvement keeps; the rep
   doesn't.
4. Applies to *any* solution-revealing content, not just full solutions — a named trap ("don't advance
   `mid` after a high swap") is often the whole rep.
