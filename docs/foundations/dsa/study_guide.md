# DSA Study Guide — Interview Foundation → Competitive Depth

## Mission & the Interview-ROI Line

**End goal:** become a *competent competitive programmer* — not merely pass technical interviews. Interview readiness is a **milestone on that path, not the finish line.**

But depth has diminishing returns *for interviews specifically*. So everything in this repo is sorted relative to one marker:

> **The Interview-ROI Line** — the point past which added technique depth stops paying interview dividends and becomes purely competitive-programming growth.

**Above the line (serves BOTH goals — do this first, in order):**
1. **NC150 core** — the scheduled roadmap. Non-negotiable interview foundation.
2. **Framework lenses** — knapsack / interval / LIS / space-compression (folded into the DP blocks), taught as unifying patterns.
3. **Pattern docs** (`docs/foundations/dsa/patterns/`) — cross-cutting techniques (sliding window, monotonic stack/deque, prefix sum, fast/slow, union-find, topo sort, binary-search boundaries, backtracking, …).
4. **Tier 1 advanced** (Knowledge Expansion Queue) — segment tree, Fenwick, KMP, XOR trie, Manacher's, matrix expo, Tarjan's, meet-in-the-middle, reservoir sampling, difference array, number theory. Advanced, but still shows up in *hard* interviews. This is the top of the ROI curve.

**=== INTERVIEW-ROI LINE ===**

**Below the line (competitive-programming growth; NOT for interview ROI):**
5. **Tier 2 "further horizon"** (Knowledge Expansion Queue) — sweep line, max-flow, LCA, Mo's algorithm, SOS DP, suffix automaton, Aho-Corasick, persistent structures, etc. Pursue **only** after interview-readiness is solid, and **only** for competitive-programming ambition — near-zero interview payoff.
6. **Tier 3 "competitive / research horizon"** (Knowledge Expansion Queue) — the deepest layer: HLD, centroid decomposition, link-cut trees, suffix automaton/Eertree, FFT/NTT, MCMF & min-cut modeling, D&C DP / Aliens trick, segment tree beats, 2-SAT, advanced geometry, Sprague–Grundy. ICPC/Codeforces territory — pursued deliberately over months for true competitive-programmer depth. See the Tier 3 section in `mastery/dsa_progress.md`.

**How to use the line:** when deciding whether to learn something, ask *"which side of the line is it, and am I currently optimizing for interviews or competitive depth?"* Don't spend interview-prep time below the line; don't mistake below-the-line mastery for interview readiness. Finish NC150 + Tier 1 before crossing.

---

## Weekly Review Priority

Every Sunday, open `docs/foundations/dsa/mastery/dsa_progress.md` and sweep for all problems whose `Next Review Date ≤ end of the coming week`. Slot them into the upcoming schedule before filling active blocks or new content. Use this priority order for warmup slots:

1. **Priority 1 (High Risk)**: 🔴 Blank — oldest Latest Attempt Date first.
2. **Priority 2 (Medium Risk)**: 🟡 Shaky — oldest Latest Attempt Date first.
3. **Priority 3 (Maintenance)**: 🟢 Clean — due this week. No-code review is allowed, but it **caps at 🟡 Shaky** — to hold or advance 🟢 Clean toward retirement you must code it. Coding your way to 🏆 Retired is what buys cheap no-code maintenance later.
4. **Priority 4 (Spot Check)**: 🏆 Retired — due every 180 days; a flawless no-code blueprint *confirms* retention (stays 🏆). This is the one place a blueprint holds a status.

Daily cap is **5 problems**. The active block is never cut — trim from warmup slots first (max 4 warmup problems across morning + evening combined). When a problem is bumped, slot it to a specific future day in the same edit.

---

## Backlog Recovery

**Trigger**: Any time the Next Review Date is 7+ days overdue with no new attempt logged.

### Emergency Double Session Rule

When triggered, both morning and evening warmup slots are filled with overdue problems until the list is cleared. Do not start any new active block problems until the overdue count drops below 5.

### Permanent Backlog Rule

If the overdue count ever exceeds **5 problems**, suspend new problem intake entirely. Run double warmup sessions daily until it drops below 5, then resume at half pace (1–2 new per week) until fully cleared.

## ⏱️ The 15-Minute "No-Code" Warmup Execution
Because 15 minutes passes incredibly fast, **never write code during a backlog warmup**. Code writing is reserved for your 45-minute active block. Optimize your 15 minutes like this:
* **00:00–00:05 | The Read**: Open the LeetCode prompt. Analyze the sample inputs and outputs.
* **00:05–00:12 | The Conceptual Blueprint**: Out loud, state the optimal Time/Space complexity and the core structural trick. (e.g., *"This is Top K Frequent. I count frequencies with a Hash Map, then use Bucket Sort where array indices represent frequencies to guarantee O(n) runtime."*)
* **00:12–00:15 | The Verification**: Open your past successful code or your "Why I Got Stuck" log entry to verify if your mental blueprint was 100% accurate.

### 📋 Post-Warmup Updates:
Log the result in `docs/foundations/dsa/mastery/dsa_progress.md` using the comfort system.

> **Coding is required for 🟢 Clean.** A no-code blueprint **cannot** log Clean — the best a no-code rep earns is 🟡 Shaky, no matter how flawless. To *reach* or *advance* Clean (increment the streak toward retirement), you must **code it** — in the 45-min active block, or as an Easy problem coded in-warmup. "Mostly remembered it out loud" is not mastery. The one carve-out is below (🏆 Retired spot checks).

* **Blueprint flawless but not coded** → 🟡 Shaky. Keeps the problem warm (+10 days); code it to restore/advance 🟢.
* **Needed a nudge or wasn't fully confident** → 🟡 Shaky. Streak resets to 0; next review in +10 days.
* **Completely forgot the approach** → 🔴 Blank. Streak resets to 0; next review in +2 days.
* **🏆 Retired spot check (the carve-out)** → a flawless no-code blueprint on an already-Retired problem *confirms* it (stays 🏆, +180 days). Retirement — earned by repeated **coded** Cleans — is the one status a blueprint can hold; everything below it needs code to reach or keep 🟢.

### ⚡ Easy Problem Exception

For problems marked **Easy**, the no-code rule is lifted:

* **During warmup**: Code the solution directly. Target **2 easy problems per 15-minute slot** (~7 min each). If you finish the first and still have time, pull the next Easy from the backlog immediately — do not stop at one.
* **During the active block**: Target **2 easy problems per session** instead of 1. Use the time saved to run the Speed Demon Protocol (edge cases + alternative solutions) on at least one of them.
* **Comfort bar is the same**: Easy does not lower the standard. Both problems must be completable from a blank page with correct complexity to log 🟢 Clean.

---

## 🗂️ The Weekly Macro-Schedule

*   **Monday – Saturday | The Split Focus Routine**:
    *   *Morning warmup (15 min)*: 1–2 problems due today/tomorrow — no-code blueprint format.
    *   *Evening warmup (15 min)*: 1–2 problems due today/tomorrow — no-code blueprint format.
    *   *Active block (45 min)*: New or current roadmap problem. Never cut this slot.
    *   **Daily cap: 5 problems total.** Trim from warmup slots first if over cap.
*   **Saturday | Blind Code Sprint**:
    *   Pick one problem from the past week's logs. Clear your screen, open a blank file, write the solution from memory.
*   **Sunday | System Design Sprint (30 min soft target)**:
    *   Pick one system from the Phase 2 design list below. Problems are still allowed after — but attempt the sprint first.
    *   **Which format to use depends on where you are in the progression:**

    | Stage | When | Format |
    |-------|------|--------|
    | **Bootstrap** | First 4–6 systems | Watch ByteByteGo 10 min → close tab → sketch from memory 15 min → compare 5 min |
    | **Transition** | Systems 5–8 | Attempt cold sketch 10 min (even if incomplete) → watch + compare 20 min |
    | **Full sprint** | Once vocabulary is built | Sketch cold 20 min → compare to reference 10 min |

    *   **Watch actively, not passively** — pause when a new component appears and ask "why this, not something simpler?" Same energy as watching NeetCode after struggling with a problem.
    *   **Don't have enough context to sketch at all?** Use the user journey: trace what happens when a user takes one action (e.g. "clicks Pay"). That trace is your sketch. The reference fills in how to make each step reliable at scale.
    *   Alex Xu and ByteByteGo are references for *that specific system* — not front-to-back reads.

---

## Daily Structure: DSA Phase (Blocks 1–4)
*Use this structure for the first 16 weeks of your study journey.*
*   **00:00–00:15 | Recall Warm-up**: Open a problem solved 2–3 days ago. Do not rewrite code; trace its variable state changes on paper or in comments.
*   **00:15–00:30 | Whiteboard & Ideate**: Read a new problem. Sketch the approach, constraints, and edge cases in plain English. No code!
*   **00:30–00:45 | Look up / Validate**: If completely stuck or your logic loops, stop. Watch the NeetCode video explanation immediately.
*   **00:45–01:00 | Python Implementation**: Type out the clean code, trace logic line-by-line, and add comments explaining the "why".

## Early Finish: Depth Extension

If you finish an active block problem in under 15 minutes, don't move on to a new problem. Use the remaining time for depth:
*   **Min 15–30 | Edge case trace**: Run your solution manually against size-0, size-1, and size-2 inputs. Confirm no index errors or infinite loops.
*   **Min 30–45 | Alternative approaches**: Check the LeetCode solutions tab for a cleaner or more memory-efficient implementation. Note what trade-offs the author made.
*   **Min 45–60 | Real-world connection**: Ask how this pattern applies at scale. (e.g., if this linked list represented browser history, how would a backend safely delete the last N entries for millions of users without locking the database?)

---

## Daily Structure: Design & AI Phase (Blocks 5–8)
*Use this structure from Week 17 onward to protect your DSA knowledge.*
*   **00:00–00:15 | DSA Maintenance Flashcard**: Look at a random past LeetCode prompt. Explain the data structure pattern and optimal Time/Space complexity out loud.
*   **00:15–01:00 | Architecture Deep Dive**: Spend 45 minutes on system design practice using the weekly loop below.

> **Phase 2 is not additional work.** It is a mode switch. The same 1-hour daily slot continues — only the content of the 45-minute block changes. DSA is kept warm through the 15-minute maintenance slot and the spaced repetition system in `docs/dsa_progress.md`.

### 🗂️ Phase 2 Weekly Macro-Schedule

*   **Monday – Friday | The Split Focus Routine**:
    *   *00:00–00:15*: DSA Maintenance Flashcard — spaced repetition from `dsa_progress.md`, no code, narrate the approach out loud
    *   *00:15–01:00*: System Design Active Block — see weekly loop below
*   **Saturday | Split Sprint (60 min)**:
    *   *First 30 min — Randomized DSA*: Pull a problem from the live sources below (no category label). Identify the pattern first, then solve it. This trains the recognition skill that NeetCode 150 alone doesn't build.
    *   *Last 30 min — Blind Design Sprint*: Pick a system design question from 2 weeks ago. Without notes, whiteboard the full design from scratch under a 20-minute timer. Spend the remaining 10 minutes comparing to your notes and naming what you missed.
*   **Sunday | System Design Sprint (30 min)**:
    *   By Phase 2 you should be at the **Full sprint** stage: sketch cold 20 min → compare 10 min.
    *   The comparison at this stage is for tradeoffs and bottleneck reasoning, not basic structure — you should already know the components.
    *   Alex Xu and *Designing Data-Intensive Applications* (Kleppmann) are references to look up the specific gap you hit, not front-to-back reads.

#### 📂 Saturday Randomized DSA Sources

> The company-frequency PDFs in this repo are from ~2021–2022 and are outdated for specific problem selection — companies rotate their banks regularly. Use them only to understand historical *pattern distribution* (e.g. Google skews graph/DP heavy). For actual problem selection, use live sources.

| Source | Signal | Notes |
|--------|--------|-------|
| **LeetCode company filter (Premium), 6-month window** | Highest | Most accurate recency signal; worth the subscription once actively interviewing |
| **NeetCode.io company lists** | High | Curated and kept fresher than static PDFs; free |
| **LeetCode Discuss / Blind** | High | Real candidates posting recent questions; search by company + "2025" or "2026" |
| **Glassdoor interview questions** | Medium | Less technical detail but useful for recency confirmation |

**Company priority for the pool:**

| Tier | Companies | When to focus |
|------|-----------|---------------|
| **Fintech targets** | Stripe, Robinhood, Citadel, Bloomberg, Goldman Sachs, JPMorgan | Late 2026 — interview here first |
| **Big tech** | Google, Amazon, Meta, Microsoft, Apple | Early 2027 — after system design is prepped |
| **Supplementary** | Netflix, Uber, Airbnb, DoorDash, LinkedIn, Databricks | Rotate in for pattern variety |

Don't pull from a company you're actively interviewing at that week — keep those problems as genuine unknowns.

### 🔁 The Weekly Design Question Loop

Spend a full week on **one** design question. Same depth-over-breadth principle as DSA.

| Day | Focus | What to do |
|-----|-------|------------|
| Mon | Requirements + Scale | Clarify functional/non-functional requirements. Estimate QPS, storage, bandwidth. Write these down — don't skip |
| Tue | High-level design | Draw the major components and data flow. API contracts. No deep dives yet |
| Wed | Deep dive: Storage | Pick the database layer. Justify SQL vs NoSQL. Define schema. Think about sharding/replication if scale demands it |
| Thu | Deep dive: Bottlenecks | Where does this system break at 10x load? Add caching, queues, CDN where justified. Explain the tradeoff for each |
| Fri | Full timed mock | Run the full design from scratch in 45 minutes. Use the 5-step framework: Requirements → Scale → High-level → Deep dive → Bottlenecks |

### 🔄 Phase 2 DSA Hybrid Rule

The 15-minute daily maintenance flashcard keeps mastered patterns warm. But not all categories will be fully clean by end of Phase 1. Apply this rule:

| Category status at end of Phase 1 | Phase 2 DSA approach |
|------------------------------------|----------------------|
| Majority Clean (solved cold, correct complexity) | 15-min flashcard only — no new problems needed |
| Majority Shaky/Blank | Continue 1 new problem per week in that category during the weekday active block, alongside design work |
| Backlog spikes above 5 overdue | Pause design block entirely. Run emergency double warmup until cleared. Same rule as Phase 1 |

The Saturday randomized DSA sprint covers the pattern recognition gap regardless of category status — it's always on.

### 📋 Recommended Design Question Order (Phase 2)

Start with fintech-relevant designs — these map directly to interview questions at Stripe, Robinhood, and Two Sigma, and connect to your real-world experience:

1. **Rate limiter** — simplest, teaches token bucket vs sliding window, good warm-up
2. **Payment processing system** — your domain; own this cold
3. **Notification system** — teaches async queues (Kafka/SQS), fan-out patterns
4. **URL shortener** — classic; teaches consistent hashing, caching, DB design
5. **Reconciliation pipeline** — you've built this; narrate your real MS experience then generalize to scale
6. **Distributed ledger / accounting system** — deepest domain advantage; save for late Phase 2

Only move to FAANG-style designs (Twitter, YouTube, Google Drive) after the above 6 are solid. Walk into Stripe talking about reconciliation, not social feeds.

### 🔑 The Narration Rule
Every design session must be narrated out loud — not written silently. Interviewers score your communication, not your diagram. If you can't explain a tradeoff in one sentence, you don't own it yet.

---

## 📅 Revised Phase Plan: June–December 2026

> This supersedes the week numbers in the 8-Block Roadmap below. The block structure is preserved;
> only the ordering and timing are corrected based on actual progress as of June 7, 2026.

| Phase | Approx. Dates | New Problems | Categories |
|---|---|---|---|
| **Recovery + Standard Graphs** | Jun 8–21 | 6–8 | Course Schedule I & II, Pacific Atlantic Water Flow, Surrounded Regions, Graph Valid Tree, Number of Connected Components, Redundant Connection |
| **Heap / Priority Queue + Linked List catch-up** | Jun 22–Jul 5 | 13 | Kth Largest in Stream, Last Stone Weight, K Closest Points to Origin, Task Scheduler, Design Twitter, Find Median from Data Stream, Merge K Sorted Lists; *catch-up:* Encode and Decode Strings (LC 271), Add Two Numbers (LC 2), Copy List with Random Pointer (LC 138), LRU Cache (LC 146), Find the Duplicate Number (LC 287), Reverse Nodes in K-Group (LC 25) |
| **Tries + Tree catch-up** | Jul 6–12 | 8 | Implement Trie, Design Add and Search Words, Word Search II; *catch-up:* Construct Binary Tree from Preorder/Inorder (LC 105), Kth Smallest in BST (LC 230), Binary Tree Maximum Path Sum (LC 124), Serialize and Deserialize Binary Tree (LC 297), Median of Two Sorted Arrays (LC 4) |
| **Advanced Graphs** | Jul 13–Aug 2 | 7 | Network Delay Time (Dijkstra), Swim in Rising Water, Alien Dictionary, Cheapest Flights Within K Stops, Min Cost to Connect All Points, Reconstruct Itinerary, Word Ladder |
| **Sliding Window (finish) + Stack** | Aug 3–23 | 8 | Min Window Substring, Sliding Window Maximum; Min Stack, Evaluate Reverse Polish Notation, Generate Parentheses, Daily Temperatures, Car Fleet, Largest Rectangle in Histogram |
| **Intervals + Greedy** | Aug 24–Sep 13 | 14 | Insert Interval, Merge Intervals, Non-overlapping Intervals, Min Interval to Include Each Query, Meeting Rooms I & II; Jump Game I & II, Gas Station, Hand of Straights, Merge Triplets, Partition Labels, Valid Parenthesis String |
| **Backtracking** | Sep 14–Oct 11 | 9 | Subsets I & II, Combination Sum I & II, Permutations, Word Search, Palindrome Partitioning, Letter Combinations, N-Queens |
| **1D Dynamic Programming** | Oct 12–Nov 8 | 12 | Climbing Stairs, Min Cost Climbing Stairs, House Robber I & II, Longest Palindromic Substring, Palindromic Substrings, Decode Ways, Coin Change, Max Product Subarray, Word Break, Longest Increasing Subsequence, Partition Equal Subset Sum |
| **2D Dynamic Programming** | Nov 9–Dec 6 | 11 | Unique Paths, Longest Common Subsequence, Stock with Cooldown, Coin Change II, Target Sum, Interleaving String, Longest Increasing Path in Matrix, Distinct Subsequences, Edit Distance, Burst Balloons, Regular Expression Matching |
| **Bit Manipulation + Math & Geometry** | Dec 7–28 | 15 | Single Number, # of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers, Reverse Integer; Rotate Image, Spiral Matrix, Set Matrix Zeroes, Happy Number, Pow(x,n), Multiply Strings, Detect Squares |
| **Buffer + Final EOY Review** | Dec 29–31 | — | Sweep `dsa_progress.md` for all 🔴 Blank and 🟡 Shaky solutions. Target: ≤ 10 non-Clean by EOY |

### Post-NC150 — The Steady State (Maintenance · Application · Expansion)

Once the roadmap completes and NC150 is Clean/retired, the mode shifts from **acquiring patterns** to three ongoing threads that run in parallel — this is the permanent steady state and the on-ramp to the competitive-programmer goal:

1. **Maintenance** — spaced repetition keeps NC150 alive: 🏆 retired problems spot-check every 180 days; anything that slips to 🟡/🔴 returns to rotation. Never stops.
2. **Application — *pull, not push*.** Company frequency lists are a **reference pool, not a checklist.** *Pull* problems from them **gated by patterns/techniques already learned** (NC150 + expansion queue), to build **speed and transfer** on your existing foundation. Never march a company list top-to-bottom — your knowledge drives the selection, not the company's list. Log each pull in the tracker: 🟢 confirms transfer works; 🟡/🔴 is a **diagnostic** pointing at a pattern to refresh (not a cue to learn something ad-hoc). The two curated **pull pools** — interview-sourced (during Tier 1) and competitive-style (after, for Tier 2) — live in [`backlog/`](backlog/README.md).
3. **Expansion — keep learning, deliberately.** Continue working the **Knowledge Expansion Queue** (bottom of `dsa_progress.md`): finish Tier 1 advanced (segment tree, KMP, XOR trie, …), then cross the Interview-ROI line into Tier 2 competitive material toward the competitive-programmer goal. New concepts enter **here, in order, deliberately** — never reactively off a company problem.

**The direction of causation always runs from your knowledge outward.** NC150 + expansion queue = what you know → pull application problems that exercise it, and grow the queue on purpose. Nothing external (a company list, a random hard problem) is allowed to *dictate* the curriculum.

### Why Heap Comes Before Advanced Graphs

Dijkstra's algorithm (required for Network Delay Time, Cheapest Flights, Swim in Rising Water) uses `heapq` as its core data structure. Attempting those problems without heapq fluency means learning two things simultaneously. Complete Heap/PQ first so Advanced Graphs is purely about the graph logic.

### Why Tries Slot Between Heap and Advanced Graphs

Tries are 3 problems and complete in roughly one week. Grouping them here keeps the heavy graph block contiguous (Standard Graphs → Tries → Advanced Graphs) rather than fragmenting it later.

### Sorting & DP — the Course Covers It; Extras Live in the KEQ

NC150's 1-D DP (12) and 2-D DP (11) blocks already contain **every DP pattern that matters for interviews** — so **no extra DP weeks**. Teach them through unifying **framework lenses** folded into the existing blocks (zero added scheduling):
- **Knapsack** — 0/1 (`416`, `494`) + unbounded (`322`, `518`) share one "capacity × item" table.
- **Space compression** — the 2D→1D rolling-array pass, taught as an optimization over solved 2-D problems.
- **Interval DP** — `312. Burst Balloons` ("solve inner intervals first, combine outward").
- **LIS core** — `300` is the base; its O(n log n) and multi-dimensional forms are enrichment.

Everything past the course is **not spaced repetition and adds no weeks** — it lives, with full notes, in the **Knowledge Expansion Queue** in `mastery/dsa_progress.md`: the `912` sort variants (Quick/Radix/Counting/Timsort) and `53` D&C, plus DP enrichment (Digit DP, Bitmask DP, LIS O(n log n), the multi-dim LIS cluster `354`/`646`/Building Bridges, broader interval DP like Matrix Chain Multiplication). Pull from it only during a planned deep-dive.

**Sliding window is not DP** — Min Window Substring, Permutation in String, Find All Anagrams are two-pointer + frequency-map; keep them in the Sliding Window block.

### Pace Targets

- **New problems per week (phase-dependent)**:
  - **Now through end of August 2026** (Graphs / Heap / Tries / Sliding Window / Stack — moderate difficulty): **4–5 per week.** Front-load the easier phases to bank a ~5-week lead. Fits the 5/day cap (steady-state reviews ~3.5/day + 5 new ≈ 4.1/day).
  - **September onward, especially the DP phases (Oct–Dec)**: **drop back to 3 per week.** DP problems are individually much harder/slower and each new one spikes the Blank rate; keep intake low so it doesn't trip the overdue-backlog rule.
  - Rationale: at 4–5/week through August then 3/week, NC150 still finishes ~late November 2026 with far less Blank-pileup risk than holding 5/week through DP.
- **Active-block guard**: only ~6 active-block slots exist per week (Sunday = system design). At 5 new/week, 5 slots are consumed by new problems — reserve at least 1 for re-coding Blanks. If Blank re-solves are stacking up, cut new intake that week.
- **Max overdue backlog before pausing new intake**: 5 problems.
- **DP phases (1D + 2D)**: Allow 4–5 weeks each. Do not compress below 4 weeks per phase.

---

## Study Roadmap

### Phase 1: Core Data Structures & Algorithms (Weeks 1–16)
*   **Block 1: Advanced Linear & Recursion (Weeks 1–3)**
    *   *Rotation*: Day 1: Linked Lists | Day 2: Stacks & Monotonic Stacks | Day 3: Recursion Basics
*   **Block 2: The Tree & Graph Connection (Weeks 4–7)**
    *   *Rotation*: Day 1: Trees (DFS/BFS) | Day 2: Matrix Grid Traversal | Day 3: Graph Adjacency Lists
*   **Block 3: Optimization Patterns (Weeks 8–11)**
    *   *Rotation*: Day 1: Sliding Window/Pointers | Day 2: Heaps (`heapq`) | Day 3: Intervals & Greedy
*   **Block 4: Complex Search Spaces & Caching (Weeks 12–16)**
    *   *Rotation*: 
        *   Day 1: Advanced Binary Search (Range hunting)
        *   Day 2: Backtracking (Visualizing decision trees)
        *   Day 3: 1D Dynamic Programming (Adding a flat ` * n` memoization array)
        *   Day 4: 2D Dynamic Programming (Expanding cache to a 2D grid matrix or coordinate tuple dict)

### Phase 2: System Design at Scale (Weeks 17–25)
*   **Block 5: Foundational System Components (Weeks 17–19)**
    *   *Core Concepts*: Vertical vs Horizontal Scaling, Load Balancers, API Gateways.
*   **Block 6: Scaled Storage & Caching (Weeks 20–22)**
    *   *Core Concepts*: SQL vs NoSQL, Database Sharding, Distributed Caching (Redis/Memcached).
*   **Block 7: Communication & Streaming (Weeks 23–25)**
    *   *Core Concepts*: HTTP vs WebSockets, Message Queues (Kafka), API Rate Limiting.

### Phase 3: AI System Engineering & Infrastructure (Weeks 26–29)
> Full pillar guide (ROI-line tiers, cadence, practice backlog, templates): [`../ai_engineering/study_guide.md`](../ai_engineering/study_guide.md). Prerequisite: System Design Tier 1 largely retired.
*   **Block 8: AI Infrastructure & Retrieval (Weeks 26–29)**
    *   *Core Concepts*: 
        *   **Vector Search Foundations**: Text chunking strategies, embeddings pipelines, and index methods (HNSW/IVF) in vector databases like Pinecone.
        *   **Context Window & Token Management**: Context ranking, prompt compression, and semantic caching architectures to limit LLM latency and API costs.
        *   **Agentic Orchestration & Tool Use**: Connecting LLMs deterministically to functions/APIs, structuring predictable JSON outputs, and state tracking.
        *   **Evaluation & Guardrail Architecture**: Programmatic evaluation layers, hallucination checks, and safety proxy layers filtering unsafe input/outputs.

---

## Reference Materials

### 🌐 System Design Resources (Months 5-6)
1. **The Core Blueprint**: Read the open-source [System Design Primer on GitHub by Donne Martin](https://github.com). It is the absolute best free textbook for web fundamentals, performance trade-offs, and database scaling.
2. **Visual & Structural Breakdowns**: Check out Alex Xu's [ByteByteGo Platform](https://bytebytego.com) for bite-sized, highly scannable visual architectural designs.
3. **Real-World Scale Case Studies**: Read the [Netflix Tech Blog](https://netflixtechblog.com) and [Uber Engineering Blog](https://uber.com) specifically searching for terms like *"Distributed Caching"*, *"Kafka Streaming"*, or *"Rate Limiters"* to see how your current block topics look in production.

### 🤖 AI Engineering & Infrastructure Resources (Month 7)
1. **Practical Code & Frameworks**: Use the short courses on [DeepLearning.AI](https://deeplearning.ai). Focus specifically on their specialized micro-courses covering *LangChain for LLM Application Development*, *Vector Databases*, and *Evaluating LLM Applications*.
2. **Production AI Case Studies**: Read the [Pinecone Engineering Blog](https://pinecone.io) to deep-dive into high-performance vector search architecture and production-grade RAG pipelines.
3. **Architectural Frameworks**: Browse the documentation of production orchestration libraries like [LlamaIndex Architecture Guides](https://llamaindex.ai) to learn how data ingestion pipelines operate under the hood.

---

## Week 1 Starter Problems

### 🟢 Day 1: Linked Lists (Refresh Skill)
*   **Problem**: **Remove Nth Node From End of List** (LeetCode 19)
*   **Goal**: Maintain a constant gap of `n` nodes between a `left` and `right` pointer. Use a `dummy` node at the start to protect against deleting the head.

### 🟡 Day 2: Stacks (New Structural Skill)
*   **Problem**: **Valid Parentheses** (LeetCode 20)
*   **Goal**: Match opening/closing brackets using a Python dictionary (`{'}': '{'}`) for clean, fast \(O(1)\) lookup evaluations.

### 🔴 Day 3: Recursion Basics (New Algorithmic Pattern)
*   **Problem**: **Merge Two Sorted Lists** (LeetCode 21)
*   **Goal**: Solve this recursively. Point the smaller current node's `.next` to the result of the next recursive comparison.

### 🔄 Day 4: The 15-Minute Recall & Review
*   **Task**: Clear your screen and rewrite the solution to **Valid Parentheses** completely from scratch on a blank scratchpad without syntax highlighting.

---

## Manual Code Tracing

Debugging in your head or on a whiteboard without running the code is a core interview skill. Apply these techniques when tracing solutions:

### 1. The Variable State Table
Do not track changing pointer values or nested loops in your memory. Create a table in your code comments or scratchpad and manually update rows row-by-line:
```text
Line # |   left   |  right   |  right.next  
-------------------------------------------
Init   |  dummy   |  dummy   |  ListNode(1)
Loop 1 |  dummy   |  Node(1) |  Node(2)
Loop 2 |  dummy   |  Node(2) |  Node(3)   <-- (End of isolated 'n' gap loop)
Loop 3 |  Node(1) |  Node(3) |  Node(4)
```

### 2. Box & Arrow Memory Maps
For data structures that hold physical spatial logic (Linked Lists, Trees, Matrices), you *must* draw shapes. 
* Draw nodes as distinct, numerical boxes.
* Draw references as clean arrow lines pointing to targets.
* When executing reassignments like `left.next = left.next.next`, physically draw an "X" through the original arrow connection and redraw the line routing safely around the deleted node box.

### 3. Minified Edge Cases
Never attempt to execute a manual code trace on huge collections of mock datasets. Test your logic using the three fundamental system breaking thresholds:
* An empty element condition (`None`, `[]`, `""`)
* A structural collection containing exactly **one** item.
* A structural collection containing exactly **two** items.
* *Rule*: If your logical bounds safely step through configurations of size 0, 1, and 2 without firing index exceptions or infinite loops, the foundational implementation is mathematically secure.

### 4. The Conversational "Rubber Duck" Translation
Read syntax out loud, converting mathematical logic definitions into conversational English explanations:
* *Instead of parsing raw characters:* `if stack and stack[-1] == lookup[char]`
* *Say out loud sentences like:* "If my structural track stack contains items, and the structural marker resting at the absolute tip of my memory stack precisely matches the complementary open bracket configuration matching my current character tag..."

### 📊 Recursive Call Stack State Table
* **Tracing Case**: [e.g., Input Data, Target Variables]


| Execution Phase | Active Call Context | Current Node/State | Variables / Counter | What it Returns to the Caller |
| :--- | :--- | :--- | :--- | :--- |
| **1. Dive Down** | `helper(...)` | | - (Paused) | Waiting... |
| **1. Base Case** | `helper(Base)` | | | |
| **2. Pop Up** | `helper(...)` | | | |

---

## Stuck Log Format

See [stuck_log.md](stuck_log.md) for the live log. Template for reference:

```markdown
## ❌ Problem Name: [Insert LeetCode Name & Number]
* **Date**: [Insert Date]
* **Topic(s)**: [e.g., Stack / Monotonic Stack]

### 1. Where did I get stuck?
* [Write a 1-sentence description of the exact roadblock]

### 2. The Core Realization
* [What was the structural trick or pattern from the solution?]

### 3. Code Snippet to Remember
```python
# Paste the specific line of Python or pattern that unlocked the issue
```
```
```

---

## Core Rules
1.  **Strict 45-Minute Cap**: If a new problem isn't solved in 45 minutes, stop, look up the solution, and log it 🔴 Blank. It re-appears in 2 days.
2.  **Quality > Quantity — Hard Comfort Bar**: Aim for 3–4 deeply understood problems per week. A problem is 🟢 Clean only when you can write the complete solution on a blank page with no hints and state the correct time/space complexity unprompted. "Mostly remembered it" = 🟡 Shaky. Every non-Clean result gets logged in `stuck_log.md`: 🔴 Blank gets a full entry naming the conceptual gap; 🟡 Shaky gets a one-liner naming the specific friction point.
3.  **Coding Required for Clean**: 🟢 Clean is earned only by **coding** the solution from a blank page. A no-code blueprint caps at 🟡 Shaky and cannot advance the streak toward retirement; the sole carve-out is a flawless spot check *confirming* an already-🏆 Retired problem.
4.  **Whiteboard Fidelity**: Write the *full* solution from scratch every time — including any `ListNode` / `TreeNode` / `TrieNode` definitions. No shared boilerplate/data-model module to import; re-deriving the scaffolding is part of the rep, exactly as on an interview whiteboard.
5.  **5-Problem Daily Cap**: Never exceed 5 problems in a day. Active block is always protected — trim warmup slots first. When a problem is bumped, assign it a specific future slot in the same edit.
