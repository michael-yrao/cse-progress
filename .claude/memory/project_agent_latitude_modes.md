---
name: project_agent_latitude_modes
description: Latitude when thinking/teaching, stringency when executing — the three enforcement options considered Aug 21, 2026, which one shipped, and the conditions for reaching for the other two
metadata:
  type: project
reconciled: 2026-08-21
---

**Set by the learner Aug 21, 2026**, at the end of the reconcile pass:

> *"I want to make sure I don't neuter the agent's creativity, so I don't want to bottleneck the agent
> when the agent is thinking, planning and researching and teaching as a good interviewer. I want the
> agent to be stringent when implementing and pulling basic details without much thought. How do I
> enforce this? subagents? other suggestions?"*

**The normative rule lives in CLAUDE.md** ("Two registers"), per the two-layer split — this file carries
the reasoning, the options not taken, and their triggers.

## The diagnosis

**The rules in this repo were never the threat to coaching quality — their SCOPE was.** Almost all of
them constrain *packaging and bookkeeping* (link format, commit timing, session dating, scaffold scope,
single-source), not *content*. The failure is that ~67 rule files read as one undifferentiated wall, so
a rule written for a status report gets applied to an explanation.

**Aug 21 is the evidence, and it points the same way.** In one session the coaching held up — the
recognition gate fired verbally, 150's operand-order bug was found by handing over a failing case rather
than the fix, and 14's `min(strs)` premise was corrected without touching the rating. **Every stumble was
mechanical**: the link rule twice, and two banned clipped imperatives. Nothing was lost to over-caution
in the teaching; things were lost to inattention in the bookkeeping. That asymmetry is the whole argument
for treating the two as different registers.

## The three options, all logged (learner: *"we can log all 3 options"*)

| | Option | Cost | Status |
|---|---|---|---|
| **1** | **Scope the rules in CLAUDE.md** — name the two registers and which rules bind in each | one edit | ✅ **SHIPPED Aug 21, 2026** |
| **2** | **Subagents for bounded mechanical sweeps** — audits, coverage checks, weekly-build arithmetic | a cold context per sweep | 🧊 held — see trigger |
| **3** | **Hooks for anything that must fire unprompted** | one script per rule | 🧊 held — see trigger |

### Why option 1 first

It is the only one that addresses the **misapplication** directly; 2 and 3 move work around without
telling anyone which rules govern which work. It is also the cheapest to reverse.

### ⚠️ The subagent inversion, which is the counter-intuitive half

**Delegate the STRINGENT work, never the creative work.** A subagent starts cold, so the session context
that makes coaching good — what hints were already given, what the learner just self-caught, what the
pre-code comment said — is exactly what it does not have. Sending a teach or a rep to one produces
generic coaching and a rating built on nothing.

What it *is* good for: a self-contained sweep whose output is a record rather than a judgement (a
reconcile audit, a coverage check, a link sweep over a schedule file).

## Triggers — state conditions, not dates

Per [[feedback_gate_on_internal_state]] and the Waiting-Room rule (a bare date expires silently):

| Item | Fires when |
|---|---|
| **Option 2 — subagents** | a mechanical sweep takes **more than ~15 tool calls inline** and its output is a record, not a judgement. The Aug 21 reconcile pass (64 files read) is the first thing that would have qualified |
| **Option 3 — hooks** | **any mechanical rule lapses a 2nd time after option 1 ships.** Two live candidates already: the banned clipped-imperative / vocabulary list (1 occurrence, Aug 21 — see `self_eval_log.md`), and anything else the intervention ladder would rank above a memory file |
| **Revisit the split itself** | the learner reports coaching feeling either **thin** (over-constrained → loosen the deliberative column) or **sloppy** (under-constrained → the mechanical column needs a hook). Their framing: *"we can adjust based on how the relationship develops"* |

⚠️ **Do not treat the register split as a defence.** *"That was deliberative"* is not an answer to a
missed gate — the gates are mechanical steps that run **during** deliberative work. If this file is ever
cited to excuse a skipped complexity gate or an unasked commit, the split has been misread and that is
worth a `self_eval_log` entry on its own.

Related: [[feedback_self_evaluation]] (the intervention ladder, which is what ranks hook above memory
file), [[feedback_answer_length]] (the cap is on answers, never on explanation),
[[feedback_operating_principles]].
