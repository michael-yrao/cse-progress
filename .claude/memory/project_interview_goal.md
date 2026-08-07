---
name: project_interview_goal
description: Learner is targeting Staff-level (L6) fintech interviews; SD is the binding constraint and top priority, DSA is already at bar
metadata:
  type: project
---

Set by learner Aug 7, 2026. **Target: Staff-adjacent (L6) roles at fintechs** (~10 years' experience).

- **DSA is already interview-ready** — deep, mostly-consolidated library (88 🟢, 38 retired). It drops to
  pure maintenance once Advanced Graphs closes (~Aug 16); no new intake during the SD push.
- **System design is THE binding constraint and top priority.** At L6 the emphasis is **depth over
  breadth** — 3–4 designs defended 2–3 levels deep under sustained pushback beats many shallow ones.
  Fintech domain depth (payment/ledger, idempotency, exactly-once, consistency, reconciliation) is
  non-optional.
- **The roadmap lives in [`docs/foundations/system_design/senior_ramp.md`](../../docs/foundations/system_design/senior_ramp.md)** —
  phased (A framework → B senior signals + fintech domain → C simulation), gated not dated, with a
  7-point design-scoring rubric (#5 forks, #6 failure modes, #7 evolve/operate must all pass for 🟢 at
  L6). Designs are now tracker rows in `design_progress.md` (role `Design`).

**Why:** the target level determines how SD readiness is measured and when to apply — it drives capacity
allocation (redirect a DSA active block to a 2nd design sprint/week after graphs close) and the
application trigger. **How to apply:** when planning schedules or SD work, weight SD heavily and measure
designs by depth-under-pushback, not count. The **apply trigger is a repo-evaluable SD gate** (designs at
🟢-with-forks + core techs off 🔴 + cold 45-min mock), never an offer/interview outcome — see
[[feedback_gate_on_internal_state]] and [[feedback_phase_dates_are_advisory]].
