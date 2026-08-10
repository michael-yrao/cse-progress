---
name: feedback-coverage-gap-ledger
description: End every SD teaching session by logging what the learner's questions did NOT reach, as bare open questions in the card — the accumulated list is later the mock-interview bank
metadata:
  type: feedback
---

**Set by the learner Aug 9, 2026**, one turn after they confirmed spine-then-pull as the standing format
for conceptual SD material ([[feedback_interactive_learning]]).

> *"the questions I ask might not cover everything that we want to learn about a technology or concept so
> I want you to flag what are the facts and details that are still missing or not addressed after each
> teaching and learning session and then after the appropriate learning sessions are done, we do mock
> interviews that test based on the questions we accumulated."*

**The hole it patches.** Under spine-then-pull the learner's questions set the direction, which is the
whole value — but it means coverage is bounded by what they can already see is missing. A genuine blank
spot generates no question *by definition*. Same structural argument as the `concepts/` lane
([[project_concepts_lane_port_pending]]): a missing box is visible in a design; a missing **fact** only
surfaces once you're already stuck. The pull format cannot self-audit; something outside it has to.

**The procedure (now a numbered step in CLAUDE.md's System-design-track section — not left as a paragraph
here, per the [[feedback_self_evaluation]] intervention ladder):**

1. At **end of session**, append to `## ❓ Open — not yet asked` at the bottom of the tech/concept/component
   card everything interview-relevant the session did not reach.
2. Bound it by the **L6 ROI line** ([[project_sd_roi_line]]). Every technology has infinite unasked detail;
   an unbounded list becomes noise and stops being read — the exact rot the `queued:` marker prevents in
   `technique_coverage.md`.
3. Each gap is a **bare open question, never a summary of the answer.** Writing "we never covered congestion
   control — it works by…" spoils the item and kills the mock. Written as a question, one artifact serves as
   both the coverage report and the mock bank.
4. **Ask whether to answer any of them now, or hold them for the mock — every session, both directions
   genuinely open.** The learner's explicit reason: *"depends on the availability of the user and how much
   more learning the user can still take honestly."* So this is a capacity question, and only they can
   answer it. Do not default to answering (turns every session into an appended lecture) and do not default
   to deferring (they may have room and want it closed while it's warm).
5. Items close when a later session's questions reach them. A card drained to the interview-relevant floor
   is the **repo-evaluable trigger** for a mock interview drawn from the accumulated questions — never a
   date, never an external event ([[feedback_gate_on_internal_state]]).

⚠️ **End of session only.** Surfacing a gap mid-session pre-empts the learner's next question, which is the
rep the whole format exists to produce — and requirement-gathering is itself the graded interview skill
([[feedback_interactive_learning]]).

**Why this matters beyond bookkeeping:** it makes the pull format's weakness ("it only covers what they
think to ask") measurable instead of invisible, without taking the wheel back from the learner. They still
drive; the ledger just records where they didn't go, and the mock is what converts that record into a rep.
