# AI System Engineering Study Guide — Practitioner Core → Infra Depth

## Mission & the Interview-ROI Line

**End goal:** be able to design and reason about **production AI/LLM systems** —
retrieval pipelines, model serving, agentic orchestration, and the evaluation and
guardrails that keep them safe and cheap. **Passing an AI-infra interview is a
milestone on that path, not the finish line.**

As with DSA and System Design, this pillar is built on the **same engine**: the
Comfort scale (🟢/🟡/🔴), spaced repetition, and template-driven reps reviewed by
a **blind rebuild** (design/rebuild the capability cold from memory, then compare).
It is organized around one marker:

> **The Interview-ROI Line** — past which added AI-infra depth stops improving
> interview performance and becomes real production-systems mastery.

**Prerequisite:** AI System Engineering is **System Design specialized for ML/LLM
serving.** Do not start it until System Design Tier 1 (building blocks, data layer,
the interview framework) is largely retired — vector DBs, token/context management,
GPU batching, and RAG all assume you already reason fluently about caching, queues,
sharding, and API design.

**Above the line — Practitioner Core (Tier 1). Do this first; it's the whole AI-infra interview surface.**

1. **Retrieval & vector search** — text chunking strategies, embedding pipelines,
   index methods (HNSW / IVF / IVF-PQ), similarity metrics, hybrid (BM25 + vector)
   retrieval, reranking. RAG end to end.
2. **Context-window & token management** — context ranking / selection, prompt
   compression, semantic caching, token budgeting and cost control, streaming
   (SSE / WebSocket) of tokens to the client.
3. **Agentic orchestration & tool use** — deterministic function/tool calling,
   structured (JSON-schema) outputs, state tracking across turns, multi-step
   planning, retries and idempotency, human-in-the-loop checkpoints.
4. **Serving fundamentals** — request batching, KV-cache, GPU scheduling and
   utilization, autoscaling for spiky load, quotas & rate limiting per tenant,
   latency vs throughput tradeoffs.
5. **Evaluation & guardrails** — programmatic eval harnesses (offline + online),
   golden sets, LLM-as-judge and its pitfalls, hallucination / grounding checks,
   safety proxies filtering unsafe input/output, canary + rollback for prompt and
   model changes.

Being fluent across (1)–(5) is the ceiling of *interview* ROI. Everything below
sharpens you as an infra engineer but won't move an interview score much.

**=== INTERVIEW-ROI LINE ===**

**Below the line — Infra Depth (Tier 2). High real-world ROI, low interview ROI.**

6. **Serving internals** — continuous / in-flight batching (vLLM, TGI), paged
   attention, speculative decoding, tensor / pipeline parallelism, quantization
   (GPTQ / AWQ / FP8) tradeoffs.
7. **Retrieval quality at scale** — chunking/embedding ablations, evaluation of
   retrievers (recall@k, nDCG), query rewriting, multi-vector / late-interaction
   (ColBERT), freshness and incremental indexing.
8. **Distributed training & fine-tuning** — data/model/pipeline parallelism, LoRA
   / QLoRA, RLHF / DPO pipelines, checkpoint & data management.
9. **Cost & reliability engineering** — multi-model routing, caching layers,
   fallback/degradation, observability for non-deterministic systems, drift and
   regression detection.

**Tier 3 — research / specialization horizon (near-zero interview ROI):** novel
attention/architecture work, training-infra research (MoE routing, long-context
methods), inference-kernel engineering, agent-planning research, formal safety /
alignment evaluation. Pursue only for deep specialization.

**How to use the line:** ask *"which side is this on, and am I optimizing for the
interview or for real mastery right now?"* Finish Tier 1 before crossing.

---

## Cadence

AI System Engineering runs on the same weekly rhythm as System Design — a
**mode-switch subject**, not a separate calendar. When it's your active pillar,
the 45-minute block is an AI-infra rep; DSA stays warm via the 15-minute
maintenance flashcard.

Staged the same way:

- **Bootstrap** — first exposure to a topic: watch/read a good explainer, recall
  from memory, check gaps. No cold whiteboarding yet.
- **Transition** — sketch the design cold on paper (e.g. a RAG pipeline, a serving
  stack), then compare against reference.
- **Mastery** — full mock-interview timing (~45 min), self-scored against the
  framework; reviewed later by a **blind rebuild**.

**Drive every practice session through a template** in [`templates/`](templates/):
filling the scaffold *is* the rep — don't just read about token batching, design
the batching path for a concrete system.

## Design Practice Backlog

Systems to design end to end (drive the full framework on each). Above the ROI
line unless noted.

| System | Tier | Notes |
|--------|------|-------|
| **RAG chat over a private corpus** | 1 | Chunking → embeddings → vector index → retrieval + rerank → prompt assembly → streamed answer with citations. The canonical Tier-1 build. |
| **LLM chat assistant (Claude/ChatGPT-style)** | 1–2 | Token streaming, context-window management, request batching / GPU scheduling, per-tenant quotas, conversation storage. Shared with the System Design backlog. |
| **Agent with tools** | 1 | Deterministic tool calling, structured outputs, state across turns, retries/idempotency, a human checkpoint. |
| **Eval + guardrail harness** | 1 | Offline golden set + online eval, LLM-as-judge, hallucination/grounding checks, canary + rollback for prompt/model changes. |
| **High-throughput inference service** | 2 | Continuous batching, KV-cache, autoscaling for spiky load, latency vs throughput. |

## Where things live

This guide is the single source of truth (map + ROI line). Current file state:

**Built:**
- `study_guide.md` ✅ — this file.
- `templates/` ✅ — the scaffold you fill during practice (see Cadence).

**Planned (build as you reach each phase, no number prefixes):**
- `components/` — per-topic deep-dives (chunking, HNSW, batching, guardrails), started as you cover each.
- `case_studies/` — worked canonical builds (start from the template).

## Reference materials

- **Practical frameworks / courses:** short courses on DeepLearning.AI (LangChain,
  Vector Databases, Evaluating LLM Applications).
- **Production case studies:** the Pinecone engineering blog (vector search / RAG),
  serving-engine docs (vLLM, TGI).
- **Orchestration internals:** LlamaIndex / framework architecture guides for how
  ingestion and retrieval pipelines work under the hood.
- Use these to look up the specific gap you hit — not front-to-back reads.
