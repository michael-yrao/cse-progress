---
name: project_curriculum_additions_pending
description: SD/AI curriculum gaps added to cse-coach on Jul 25 that must be folded into cse-progress's hand-maintained trackers when those lanes build (not auto-synced)
metadata:
  type: project
---

On **Jul 25, 2026** a curriculum spot-check added interview-tier gaps to the **cse-coach**
curriculum (source of truth). cse-progress has **no `curriculum/` dir** — SD/AI roadmaps are
hand-maintained (`design_progress.md`, SD `study_guide.md`; AI track not bootstrapped yet), so
these do **NOT** auto-sync. Fold each in when its lane builds:

**System Design** (`cse-coach/curriculum/system_design/tier1_interview_core.yml`) — fold into
`design_progress.md` / SD `study_guide.md` as those blocks/designs come up:
- **Operability** building block — observability (metrics, logging, distributed tracing, health
  checks, alerting) + deployment & rollout (blue-green, canary, feature flags, rollback).
- **2 new canonical designs** — Collaborative editing (Google Docs — OT/CRDT) and Distributed
  job scheduler / cron. (Design backlog now 16.)

**AI Engineering** (`cse-coach/curriculum/ai_engineering/tier1_core.yml`) — capture at **AI-track
bootstrap** (gated on SD Tier-1 majority retired; track not set up yet):
- **Model adaptation & decisioning** topic — RAG vs fine-tune vs prompt-eng framework, LoRA/PEFT,
  cost/latency tradeoff. **Highest-value AI-infra interview question — prioritize.**
- **Eval & guardrails** additions — prompt injection & jailbreak defense, tool-use/data-exfil safety.
- **Multimodal** topic — tagged *emerging, watch, don't front-load*.

**DSA additions from the same pass are already synced** (recognition catalog +
tree-DP/design-O(1) core-fill in `dsa_progress.md`) — see [[project_dandc_coding_gap]] neighbors.
Delete this memory once SD + AI items are all folded in.
