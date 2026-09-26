# Interview Formats — what the loops look like in 2025–26, and what this repo does about it

<!-- reconciled: 2026-09-26 -->

> **Scope.** Cross-track, like [`career_strategy.md`](career_strategy.md): it describes the *round shapes*
> the route's companies run today, which pillar in this repo already trains each shape, and where the
> gaps are. It does not restate the goal (that is `career_strategy.md`) or how DSA / SD are studied
> (`dsa/study_guide.md`, `system_design/study_guide.md`). **Problem demand by company** is a separate,
> generated artifact: [`dsa/mastery/company_demand.md`](dsa/mastery/company_demand.md).
>
> **Researched Sep 26, 2026** from public guides and candidate reports (sources at the bottom). Company
> processes change quarterly and much of the secondary literature is prep-vendor content — treat every
> row as *"what candidates were reporting in 2026,"* verify with the recruiter before a loop, and
> re-research when a tier's applications open. **Ask the AI rules up front, every loop.**

## 1. What changed, 2025–26 — six shifts

| # | Shift | What it means in the room | Evidence |
|---|---|---|---|
| 1 | **AI-assisted coding rounds** | An assistant is *in* the editor and you are scored on how you direct, verify and own its output. | Meta piloted Oct 2025: 60-min **multi-file project** in CoderPad with a built-in assistant (choice of GPT / Claude / Gemini / Llama models), **replaces one of the two onsite coding rounds**, expected to roll out broadly (back-end / ops-focused SWE roles first) through 2026; the rubric is the classic four pillars — the AI is "furniture". Google's 2026 pilot is Gemini-only, a **code-comprehension round** (read unfamiliar code → find/fix bugs → implement a feature → optimise), junior/mid US teams first; **AI fluency is on the rubric** (prompt quality, output validation, debugging the AI's suggestions). Microsoft: no company-wide format; CoreAI-adjacent teams run AI-assisted rounds, and Microsoft has added an *AI-awareness* discussion to many loops. |
| 2 | **Practical / codebase rounds** | You are dropped into an unfamiliar repo with tests, and graded on method, not speed. | Stripe: **Bug Squash** (45–60 min, unfamiliar repo + failing pytest suite → reproduce, isolate, production-quality fix), **Integration** (parse API responses, wire a feature into an existing system), plus a **writing exercise**; look-ups allowed, AI not. Datadog: 60-min systems-flavoured coding (a metrics aggregator, a log parser). Snowflake / Databricks / Confluent / MongoDB: a **concurrency / systems-programming** coding round next to the DSA one, an infra-shaped SD round, and (Snowflake, mid/senior) a **project presentation**. Bloomberg: multiple live coding rounds and sometimes a practical round (code review, debugging, production judgement). Uber: a "machine coding" round and a **technical retrospective** for seniors. |
| 3 | **In-person and AI-off modes return** | Virtual rounds get harder to game; expect "why this variable name / what if the input is null" probes. | Google banned AI in virtual interviews and is bringing some loops back in person (town hall Feb 2025); Cisco, McKinsey, Deloitte likewise (Computerworld, Aug 2025). Fabric flagged ~38% of 19k technical interviews for AI use, Jul 2025–Jan 2026; a 2025 Blind survey had 20% admitting it. CoderPad / HackerRank / CodeSignal ship AI-off modes. **Amazon, Goldman Sachs, Anthropic prohibit AI live** — Amazon's stated consequence is disqualification (though Amazon's *online assessment* now includes an AI-assisted task, and every 2026 Amazon loop carries a behavioural question about *how you use AI*). |
| 4 | **GenAI system design inside general loops** | "Design a system that serves an LLM" is no longer a specialist question. | RAG path (chunk → embed → retrieve → rank → assemble), model routing and caching for cost, eval methodology, guardrails / prompt-injection, latency budgets in tokens, observability. Dedicated rounds at OpenAI / Anthropic / DeepMind / AI-first startups; shows up in Google / Apple / Meta general loops. *"Evaluation methodology is the new system design."* |
| 5 | **Level-calibrated scoring** | The same answer that passes at L5 fails at L6 for being tactical. | Google: a hiring committee votes the *level*; one weak dimension caps it rather than averaging. L6 = trusted to set direction for other teams with minimal oversight. Netflix moved from one "Senior Engineer" rung to an explicit ladder and scores against the target band. |
| 6 | **Senior behavioural depth** | A real round, not a formality: ownership, ambiguity, cross-team influence, feedback. | Google G&L (now folding in technical-design discussion of past work); Amazon LP rounds; Netflix runs 1–2 director interviews per loop; Apple weighs leadership and mentorship for seniors; MongoDB's hiring-manager round is a gate before onsite. |

What did **not** change: **the phone screen is still unaided DSA everywhere**, and the onsite still carries at
least one unaided coding round at every company on the route. The DSA engine in this repo is not made
redundant by any of the above — it is the prerequisite for all of it.

## 2. Loop shapes by company (the career-strategy tiers)

| Company | Tier | Onsite rounds (typical, 2026 reports) | AI in live coding | Practical round? | SD flavour |
|---|---|---|---|---|---|
| **Google** | big tech | 4–6 × 45 min: 2 coding · 1 SD · 1 G&L (+ RRK for L6); hiring committee sets level | banned in virtual; AI-assisted *code-comprehension* pilot (Gemini) for junior/mid | pilot only | product-scale; L6 = direction-setting |
| **Meta** | big tech | 2 coding (one now the **AI-assisted 60-min multi-file** round) · SD · behavioural | yes, in the AI round only | yes (the AI round is project-shaped) | product-scale, depth by level |
| **Amazon** | big tech | OA (incl. one AI-assisted task) → loop: coding ×2 + SD (SDE II+, incl. a 20-min "design sketch") + LP-heavy behavioural throughout | **prohibited → disqualification** | no | service-oriented; LP framing |
| **Microsoft** | big tech | 4–5: coding, design, behavioural; AI-awareness discussion common | team-dependent; never assume | some teams: repo work in a local IDE | product / platform |
| **Apple** | big tech | ~6 (4–8), team-driven: coding (no IDE autocomplete), SD, behavioural | no | no | privacy-first, on-device, offline-first |
| **Netflix** | big tech | 1–3 technical + 2 behavioural, 1–2 directors in loop; new level ladder | no | coding is often domain-shaped ("production-style extensions") | CDN, streaming, personalisation, low-latency APIs |
| **Snowflake** | data platform | 4–5 × 60 min: DSA coding · **systems/concurrency coding** · infra SD · values · project presentation (mid/senior) | no | yes (concurrency round) | distributed rate limiter, metadata service, query engine |
| **Databricks** | data platform | 4–5: coding (harder-than-average, graph/tree heavy) · systems/concurrency · design · behavioural (+ domain) | no | yes | at-scale data infra |
| **Datadog** | data platform | 4–5: 60-min **practical systems coding** · SD · behavioural | no | yes (metrics aggregator, log parser) | ingestion, time-series, alerting |
| **Confluent** | data platform | phone screen DSA → concurrency / LLD follow-up; 3–4 onsite: coding, SD, values | no | partly (LLD / concurrency follow-ups) | log-shaped: distributed KV, LRU at O(1) |
| **MongoDB** | data platform | Karat screen (2–3 practical DSA) → HM gate → onsite: DB internals, concurrency, system building | no | yes | storage-engine internals |
| **Stripe** | fintech | ~5: coding · **Bug Squash** · **Integration** · SD · behavioural (+ writing exercise) | no (look-ups yes) | **yes ×2** | payments-scale APIs |
| **Bloomberg** | fintech | 4–5 stages, multiple live coding rounds, sometimes a practical (code review / debugging) round | no | sometimes | terminal / market-data systems |
| **Goldman Sachs** | fintech | HackerRank or HireVue → CoderPad screen (1–2 problems) → onsite: DSA + finance-flavoured SD + culture | **prohibited** | no | finance-flavoured |
| **Citadel · Robinhood · J.P. Morgan** | fintech | not enough 2026 reporting found — verify with the recruiter | — | — | — |
| **Uber** | supplementary | 4–6: coding (60-min, pair-programming feel) · **machine coding** · SD · behavioural · technical retrospective (senior) | no | yes | dispatch, geospatial, marketplace |
| **Airbnb · DoorDash · LinkedIn** | supplementary | reports are LeetCode-style + SD + behavioural; no format novelty found | no | not reported | product-scale |

## 3. What each format tests → which pillar already covers it → the gap

| Format | The skill actually being scored | Covered by | Gap |
|---|---|---|---|
| Unaided DSA (phone screen; ≥1 onsite round everywhere) | recognition → technique → correct, explained code; complexity with a why | the whole DSA engine — spaced reps, comfort ratings, technique coverage | none structural; **demand** gaps are in `company_demand.md` |
| AI-off probing ("why this name", "what if null", explain line by line) | you own every line you wrote | the recognition gate + complexity gate + whiteboard-fidelity coding rule | none — these gates *are* that probe |
| Code comprehension / **bug squash** / integration (Stripe, Google pilot, Datadog, Bloomberg) | read unfamiliar code fast, form a hypothesis, reproduce, isolate, fix cleanly, test | **nothing** — every rep here starts from a blank file the learner wrote | **the biggest untrained shape on the route**, and the first one the fintech tier will run (Stripe) |
| **AI-assisted multi-file** (Meta now, Google/Microsoft spreading) | direct the model in bounded steps, verify its claims against the code, catch its errors, keep design ownership, narrate | nothing — and it is a *different* skill from working unaided | untrained; note the rubric (Formation): interrogate requirements *before* prompting, name two candidate designs, verify complexity claims against the code, log the AI's caught mistakes, work in reviewable steps |
| Concurrency / systems coding (Snowflake, Databricks, Confluent, MongoDB) | locks, queues, producer/consumer, an LRU at O(1), a rate limiter in code | partly — LRU (146) and design-shaped problems on the DSA side; SD concepts on the other | a **"design in code"** shape sits between the two pillars; `company_demand.md`'s Design tag is its DSA-side proxy |
| SD at L6 depth (all tiers) | scoped requirements → trade-offs defended 2–3 levels deep → failure modes → evolve/operate | the SD mock model (`senior_ramp.md`, rubric #7) — study mode today | none structural; the ramp owns it |
| GenAI SD | RAG, routing/caching for cost, evals, guardrails, token-denominated latency | the ChatGPT row on the SD board; the parked AI pillar's `10-ml-system-design` | partial — becomes real when the AI pillar activates |
| Level-calibrated scoring | scoping ambiguity alone; direction for other teams | SD ramp Phase-C gate; nothing on the coding side scores *at level* | coding reps are never scored "is this an L6 answer?" — a rubric question for the mocks, not a new track |
| Senior behavioural | ownership / ambiguity / influence stories at level | **not in the repo at all** | named here so it is not forgotten; out of scope for this pass (it is story-bank work, not spaced reps) |

## 4. Prep matrix — what to do, and when

| Format | Drill | Status |
|---|---|---|
| Unaided DSA | keep running the engine; close the *demand* gaps `company_demand.md` names at each weekly build (new families → `techniques.yml`, pulls → Waiting Room) | **running** |
| AI-off probing | nothing new — the gates already do it; keep the explain-every-line habit | **running** |
| Bug squash / integration / code comprehension | **Practical coding rep** (§5): a small unfamiliar repo + failing tests, 45–60 min, scored on method | **parked** — trigger below |
| AI-assisted multi-file | the same rep's **AI variant**: a model in the loop, scored on direction/verification/ownership (the Formation rubric) | **parked** — same trigger; run the unaided variant first |
| Concurrency / "design in code" | DSA-side: the Design family once it exists in `techniques.yml` (LRU/LFU, hit counter, time-based KV, rate limiter in code); SD-side: HelloInterview concepts already on the learner's list | **partly running**; no new slot |
| SD at level · GenAI SD | the SD mock model as designed; GenAI rows ride the AI pillar's activation | **as planned** |
| Behavioural | a story bank at L6 framing (STAR + level: scope, ambiguity, influence) — 6–8 stories | **not started, out of scope here** |
| Every loop, free | ask the AI rules in writing before the round; confirm the environment (CoderPad AI-off vs assistant); narrate; state two approaches before coding — the same discipline the recognition gate already enforces | **habit** |

## 5. Parked practice mode — the Practical Coding Rep

**One design, two variants; nothing scheduled until the trigger fires.**

- **Shape.** The coach supplies a small, unfamiliar repo (a few hundred lines, 3–6 files, a pytest
  suite with 1–3 failing tests and one deliberately vague feature request). 45–60 min. The learner
  reproduces, isolates, fixes, tests, and narrates. **Unaided variant** first (Stripe / Google-comprehension
  shape); **AI-assisted variant** second (Meta shape: a model in the loop, the learner directs and
  verifies). The first two of each variant are **unrated calibration**; after that a short methodology
  rubric (reproduce before touching · hypothesis stated · smallest fix · tests added · trade-off named ·
  for the AI variant: requirements interrogated before the first prompt, every AI claim verified,
  mistakes caught and logged) and a comfort rating, spaced like any other rep.
- **Cost.** One evening slot when it runs — off the DSA ceiling, like an SD mock. Not before DP.
- **Trigger (gate, not date — [[feedback_gate_on_internal_state]]).** Fires at a weekly build when
  **both** hold: (1) `career_strategy.md` Gate 1's **DSA half** holds (roadmap through the hard blocks,
  low 🔴/🟡), and (2) **the learner says applications are opening** — their word, exactly as SD mocks
  start on their word. Rationale: Stripe's Bug Squash is the *first* practical round on the route, so the
  drill has to exist before the fintech calibration loops run, and is pointless earlier. Until then:
  **don't nudge** (same discipline as SD study mode and the AI pillar).
- **Where it lives when it fires.** A `references/practical-coding.md` skill reference + a tracker row
  type; both are **not built until activation** (no premature scaffold — same rule as the AI pillar).

## Sources (retrieved Sep 26, 2026)

- Meta AI-assisted round: [interviewing.io — how to use AI in Meta's AI-assisted coding interview](https://interviewing.io/blog/how-to-use-ai-in-meta-s-ai-assisted-coding-interview-with-real-prompts-and-examples) · [Fahim ul Haq — Meta transformed their coding interviews with AI](https://medium.com/@fahimulhaq/meta-just-transformed-their-coding-interviews-with-ai-heres-what-developers-must-know-363b50dceda4)
- Google pilot + senior loop: [Aced — Google's AI-assisted coding interview](https://www.tryexponent.com/blog/google-ai-coding-interview) · [Grokking — Google vs Meta AI rounds](https://www.grokkingthecodinginterview.com/blog/google-ai-assisted-coding-interview) · [daily.dev — the Google senior loop in 2026 and downleveling](https://daily.dev/posts/the-google-senior-software-engineer-interview-in-2026-why-most-strong-engineers-still-get-downlevel-jpjcuz284)
- AI policy by company: [techinterview.org — are you allowed to use AI in coding interviews, 2026 rules](https://www.techinterview.org/post/3233475415/ai-coding-interviews-rules-2026/) · [Formation — what gets scored in AI-assisted coding interviews](https://formation.dev/blog/ai-assisted-coding-interviews) · [PracHub — Microsoft AI-assisted coding interview guide](https://prachub.com/resources/microsoft-ai-assisted-coding-interview-guide-2026-tools-rules-and-scoring)
- Industry data: [Karat — engineering interview trends 2026](https://karat.com/engineering-interview-trends-2026/) · [Fabric — 38.5% of 19,368 interviews flagged](https://fabrichq.ai/blogs/state-of-ai-interview-cheating-in-2026-insights-from-19-368-interviews) · [Computerworld — companies bring back in-person interviews (Aug 2025)](https://www.computerworld.com/article/4044734/to-counter-ai-cheating-companies-bring-back-in-person-job-interviews.html)
- Practical rounds: [Leon — Stripe Bug Squash & Integration (2026)](https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/) · [Coditioning — Stripe Bug Squash](https://www.coditioning.com/blog/804/stripe-swe-bug-squash-interview) · [ophyai — Datadog interview process](https://ophyai.com/blog/company-guides/datadog-interview-guide) · [ophyai — Snowflake interview process](https://ophyai.com/blog/company-guides/snowflake-interview-guide) · [claveprep — Databricks vs Snowflake](https://claveprep.com/blog/databricks-snowflake-data-engineer-interview-guide-2026) · [Interview Query — Confluent](https://www.interviewquery.com/interview-guides/confluent-software-engineer) · [TechPrep — MongoDB](https://www.techprep.app/blog/mongodb-interview-process) · [ophyai — Bloomberg](https://ophyai.com/blog/company-guides/bloomberg-interview-guide) · [TechPrep — Goldman Sachs](https://www.techprep.app/blog/goldman-sachs-interview-process) · [Aced — Uber](https://www.tryexponent.com/guides/uber-software-engineer-interview)
- Big-tech loops: [dglearning — inside the Amazon 2026 loop](https://dglearning.substack.com/p/inside-the-amazon-2026-loop-rounds) · [Aced — Amazon SDE guide](https://www.tryexponent.com/guides/amazon-software-development-engineer-interview) · [Aced — Apple SWE guide](https://www.tryexponent.com/guides/apple-software-engineer-interview) · [interviewing.io — Netflix senior guide](https://interviewing.io/guides/hiring-process/netflix) · [intervu.dev — FAANG compared 2026](https://intervu.dev/blog/cracking-faang-coding-interviews/)
- GenAI SD: [System Design Handbook — generative AI system design interview](https://www.systemdesignhandbook.com/guides/generative-ai-system-design-interview/) · [IGotAnOffer — GenAI system design](https://igotanoffer.com/en/advice/generative-ai-system-design-interview) · [Aced — ML system design guide](https://www.tryexponent.com/blog/machine-learning-system-design-interview-guide)
