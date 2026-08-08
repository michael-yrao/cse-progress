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
| 🧊 Tier 2 platform/real-world | 18 | below the line, one reason each |
| 🧊 Tier 3 off-target | 7 | declined outright, one reason each |

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

**Two structural gaps recorded there, worth not rediscovering:**
1. **"Distributed cache" is not in the systemdesign.io catalog at all** — a *source* gap. Needs another
   source or a self-directed session; Redis's tech note is not a substitute (using ≠ designing).
2. **Google Docs was never missing** — catalog #37 bundles Wikipedia/Notion/Google Docs into one question,
   and the tracker row's title had dropped "Google Docs". Renamed. ⚠️ The row must be rated on the
   **collaborative-editing** half (OT/CRDT, presence, conflict resolution), not document CRUD.
