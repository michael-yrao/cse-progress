---
name: project_sd_roi_line
description: All 55 systemdesign.io questions are triaged against an L6 big-tech ROI line in senior_ramp.md; read it before adding or declining any SD design
metadata:
  type: project
---

**Aug 8, 2026** — SD designs now have the same structure DSA has had all along: a numbered tier stack with
**one explicit Interview-ROI Line**, calibrated to **L6 at big tech** (not fintech, not generalist senior).
Lives in [`docs/foundations/system_design/senior_ramp.md`](../../docs/foundations/system_design/senior_ramp.md)
→ *The L6 Interview-ROI Line*. All 55 systemdesign.io questions are placed:

| | Count | Where |
|---|---|---|
| Core canonical set | 20 | the 7-column review table in `mastery/design_progress.md` |
| ⏳ Tier 1 advanced | 10 | SD Waiting Room (plain table, no review load), trigger `phase:B` + extended design off 🔴 |
| 🧊 Tier 2 platform/real-world/domain | 20 | below the line, one reason each — **all triggerable** |
| 🧊 Tier 3 off-target | 5 | declined — **no trigger exists and none can**; that IS the tier's definition |

⚠️ **Tier 2 vs Tier 3 is about whether a trigger can exist, not about quality.** Corrected the same day it
was written: the two **fintech** designs (Credit-Card #32, Wire Transfer #47) were filed in Tier 3 beside
IoC/DI and Botnet, and the learner challenged it. They are *the right thing aimed at the wrong employer* —
a state with a real trigger (`waypoint_loop:fintech`) — while off-altitude declines can never fire. Merging
them is the anti-void failure the two-bin rule exists to stop. **If you want to write a trigger on a Tier-3
item, it is misfiled.**

**🔁 There is also an SD overflow block** (end of the ROI-line section): the three low-ceiling Easy designs
plus four Tier-2 easies, pullable when a Sunday finishes early. **Below the line means "never worth
displacing a Sunday for", not "never do this"** — say that plainly whenever the learner asks why they can't
just do the easy ones. ⚠️ An overflow design earns a tracker row **only at 🟡/🔴** (disposable rep,
[[project_library_carrying_capacity]]), which is what keeps it free.

**The argument that settles "why not do the easy ones anyway", worth reusing verbatim:** the instinct is
right (Phase A orders designs easiest-framework-rep first on purpose), but (1) **8 easy framework reps are
already above the line**, (2) **one design = one session ≈ one Sunday**, so an easy design is a *displaced*
canonical one rather than extra practice, and (3) **the Phase A gate is not a count** — it is *skeleton
clean on 3+ designs*, standing at 0 of 3, and the fastest route there is canonical designs that must be
done anyway. *"It's still good to know"* is true and is not the test: **the line rations Sundays, not
knowledge.**

**The bar, verbatim:** *would a strong L6 candidate at Meta/Apple/Netflix/Google/Amazon be expected to
handle this in a 45-minute round?* Three consequences do most of the sorting: **depth over breadth**
(redundancy is the most common decline, not difficulty) · **distributed-systems altitude only** (an LLD
question rehearses [[feedback_hld_altitude]], the learner's known failure) · **no domain weighting**
(fintech is a waypoint per [[project_interview_goal]], so payments designs sit below the line even when
hard and famous).

**Why:** the Aug 6 reseed picked 21 of 55 and recorded nothing about the other 34, which breaks
[[feedback_roi_promotes_to_curriculum]] — *"say what you did NOT promote and why; the bar only means
something applied in both directions."* Applied one-way, "curated by ROI" is indistinguishable from
"picked some and stopped," and a wrong decline stays invisible until you need the depth material. SD also
had no equivalent of DSA's two deferral bins, so a declined design and an unread one looked identical.

**How to apply:**
- **Before adding any SD design, read the triage** — it may already be placed, with a reason. Do not
  re-derive the catalog.
- **Before declining one, write the reason in the same edit** and put it in a tier. A dateless, reasonless
  decline is the failure this fixed.
- **Evaluate the Tier-1 triggers at every weekly build** — fired means slotted that week or re-deferred
  *in writing* ([[feedback_gate_on_internal_state]]: the trigger is repo-evaluable, never an interview outcome).
- **Never report the count as progress.** 30 above-the-line designs is a menu; the gate is a handful
  defended 2–3 levels deep including rubric #7.
- **Coach's calls, learner-overridable.** Borderline items are flagged as borderline in the doc
  (#42 burgers, #34 control plane, #19 RabbitMQ, #21 sorting).

## Aug 8 follow-up — the three SD files now have ONE owner each

The triage exposed that `study_guide.md`, `senior_ramp.md` and `design_progress.md` held **three competing
design lists** and two stale status tables, while `study_guide.md` still claimed to be *"the single source
of truth."* Reconciled the same session; the ownership table is now at the **top of `study_guide.md`**:

| Thing | Owner |
|---|---|
| **State** (comfort/streak/next review — techs, concepts, components, designs) | `mastery/design_progress.md` |
| **The plan** (ROI triage, phases, exit gates, 7-pt rubric, tech order, prereq gate, overflow block) | `senior_ramp.md` |
| **The mechanics** (cadence & 3 lanes, session formats, fork drills, templates) | `study_guide.md` |

**The rule that prevents the regression — apply it beyond SD:** ⚠️ **if the engine can compute it, do not
write it down in prose.** Every stale item found was a hand-written date or ✅ duplicating tracker state
(*"Mastery ⏳ Sun Jul 19"*, *"Bootstrap ⏳ Jul 20 wk"*, *"Redis ✅"* on a row that is 🟡, `senior_ramp`
described as *"the L5 ramp"* after the Aug 6 re-aim to L6). Deleting the duplicates beats remembering to
update them — [[feedback_self_evaluation]]'s intervention ladder: **source fix over reminder.**

**Also fixed Aug 8 — components are now measured.** Building blocks were the last SD category with notes
but **no review rows**, so they could not decay. `Component` is now a role in the tracker (Caching, Load
Balancer). ⚠️ **Rate limiter deliberately gets no Component row** — it is already tracked as
`Design (Hard) API Rate Limiter` and the component note carries that arc's drill targets. One rep, one row.

**Two designs have no catalog home and are parked with triggers, not dates:** *LLM chat assistant*
(`phase:ai_bootstrap`, capstone for the AI track) and *distributed cache* (absent from systemdesign.io
entirely — needs another source).

**Two structural gaps recorded there, worth not rediscovering:**
1. **"Distributed cache" is not in the systemdesign.io catalog at all** — a *source* gap. Needs another
   source or a self-directed session; Redis's tech note is not a substitute (using ≠ designing).
2. **Google Docs was never missing** — catalog #37 bundles Wikipedia/Notion/Google Docs into one question,
   and the tracker row's title had dropped "Google Docs". Renamed. ⚠️ The row must be rated on the
   **collaborative-editing** half (OT/CRDT, presence, conflict resolution), not document CRUD.
