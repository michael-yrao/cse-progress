---
name: project_curriculum_additions_pending
description: SD/AI curriculum gaps added to cse-coach on Jul 25 that must be folded into cse-progress's hand-maintained trackers when those lanes build (not auto-synced)
metadata:
  type: project
reconciled: 2026-08-17
---

On **Jul 25, 2026** a curriculum spot-check added interview-tier gaps to the **cse-coach**
curriculum (source of truth). cse-progress has **no `curriculum/` dir** — SD/AI roadmaps are
hand-maintained (`design_progress.md`, SD `study_guide.md`; AI track not bootstrapped yet), so
these do **NOT** auto-sync. Fold each in when its lane builds:

**System Design** (`cse-coach/curriculum/system_design/tier1_interview_core.yml`) — fold into
`design_progress.md` / SD `study_guide.md` as those blocks/designs come up:
- **Operability** building block — observability (metrics, logging, distributed tracing, health
  checks, alerting) + deployment & rollout (blue-green, canary, feature flags, rollback).
  - ✅ **Partly folded Aug 8, 2026:** *Distributed Tracing* is now a ⏳ Tier-1 design in the SD Waiting
    Room, and *Metrics Collection* (Hard) + *Distributed Metrics Logging & Aggregation* (V.Hard) are both
    placed. **Still owed as building-block notes:** health checks/alerting, and the whole deployment &
    rollout half (blue-green, canary, feature flags, rollback) — no `components/` note exists for either.
- **2 new canonical designs** — Collaborative editing (Google Docs — OT/CRDT) and Distributed
  job scheduler / cron. (Design backlog now 16.)
  - ✅ **Both folded Aug 8, 2026.** Job Scheduler was already a core row. Google Docs turned out **not to
    be missing** — systemdesign.io #37 bundles *"Wikipedia, Notion **or Google Docs**"* into one question
    and the tracker row title had dropped the Google Docs half; renamed rather than added. ⚠️ **The
    OT/CRDT content is the point** — that row must be rated on real-time collaborative editing (presence,
    conflict resolution), not on document CRUD + versioning, or the fold is cosmetic. See
    [[project_sd_roi_line]].

⚠️ **The SD half changed shape Aug 13, 2026** ([[project_sd_mock_model]]): building-block notes are no
longer written on a schedule, so *"still owed as building-block notes"* above no longer means a slot. It
means **the learner's own HelloInterview study**, and the mock is where a missing one shows up. The
Distributed Tracing and Data Migration designs are parked with trigger `board:hard-tier-open` in
`design_progress.md`, since HelloInterview's board does not carry them.

~~**AI Engineering**~~ — **VOID Aug 13, 2026.** The AI System Engineering track was removed from
cse-progress (never started, no sessions, no restore trigger), so the RAG-vs-fine-tune, prompt-injection
and multimodal additions have nowhere to fold into. They remain in **cse-coach's** curriculum, which is
correct — cse-coach ships a curriculum for any learner, and one learner declining a track is not a reason
to delete it upstream. **Do not re-add them here.** The one interview-relevant piece survives as the
**ChatGPT** row on the SD board.

**DSA additions from the same pass are already synced** (recognition catalog +
tree-DP/design-O(1) core-fill in `dsa_progress.md`) — see [[project_dandc_coding_gap]] neighbors.
Delete this memory once SD + AI items are all folded in.
