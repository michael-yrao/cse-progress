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
5. **Tier 2 "further horizon"** (Knowledge Expansion Queue) — sweep line, max-flow, LCA, Mo's algorithm, SOS DP, suffix automaton, Aho-Corasick, persistent structures, etc. Pursue **only** after interview-readiness is solid, and **only** for competitive-programming ambition — near-zero interview payoff. *"Interview-readiness is solid" resolves to the measurable gate in "When to open Tier 1 expansion" below (pull rate + coverage + surplus) — never to an offer or an interview outcome.*
6. **Tier 3 "competitive / research horizon"** (Knowledge Expansion Queue) — the deepest layer: HLD, centroid decomposition, link-cut trees, suffix automaton/Eertree, FFT/NTT, MCMF & min-cut modeling, D&C DP / Aliens trick, segment tree beats, 2-SAT, advanced geometry, Sprague–Grundy. ICPC/Codeforces territory — pursued deliberately over months for true competitive-programmer depth. See the Tier 3 section in `mastery/dsa_progress.md`.

**How to use the line:** when deciding whether to learn something, ask *"which side of the line is it, and am I currently optimizing for interviews or competitive depth?"* Don't spend interview-prep time below the line; don't mistake below-the-line mastery for interview readiness. Finish NC150 + Tier 1 before crossing.

---

## Weekly Review Priority

Every Sunday, open `docs/foundations/dsa/mastery/dsa_progress.md` and sweep for all problems whose `Next Review Date ≤ end of the coming week`. Slot them into the upcoming schedule before filling active blocks or new content. Use this priority order for warmup slots:

1. **Priority 1 (High Risk)**: 🔴 Blank — oldest Latest Attempt Date first.
2. **Priority 2 (Medium Risk)**: 🟡 Shaky — oldest Latest Attempt Date first.
3. **Priority 3 (Maintenance)**: 🟢 Clean — due this week. No-code review is allowed, but it **caps at 🟡 Shaky** — to hold or advance 🟢 Clean toward graduation you must code it. Coding your way to 🎓 Graduated is what buys cheap no-code maintenance later.
4. **Priority 4 (Spot Check)**: 🎓 Graduated — due every 180 days; a flawless no-code blueprint *confirms* retention (stays 🎓). This is the one place a blueprint holds a status.

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

> **Coding is required for 🟢 Clean.** A no-code blueprint **cannot** log Clean — the best a no-code rep earns is 🟡 Shaky, no matter how flawless. To *reach* or *advance* Clean (increment the streak toward graduation), you must **code it** — in the 45-min active block, or as an Easy problem coded in-warmup. "Mostly remembered it out loud" is not mastery. The one carve-out is below (🎓 Graduated spot checks).

* **Blueprint flawless but not coded** → 🟡 Shaky. Keeps the problem warm (+10 days); code it to restore/advance 🟢.
* **Needed a nudge or wasn't fully confident** → 🟡 Shaky. Streak resets to 0; next review in +10 days.
* **Completely forgot the approach** → 🔴 Blank. Streak resets to 0; next review in +2 days.
* **🎓 Graduated spot check (the carve-out)** → a flawless no-code blueprint on an already-Graduated problem *confirms* it (stays 🎓, +180 days). Graduation — earned by repeated **coded** Cleans — is the one status a blueprint can hold; everything below it needs code to reach or keep 🟢.

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

## Daily Structure: Design Phase (Blocks 5–7)
*Use this structure from Week 17 onward to protect your DSA knowledge.*

> **📍 SD source of truth = [`senior_ramp.md`](../system_design/senior_ramp.md)** (question order, phases,
> exit gates, the 7-point rubric) and [`study_guide.md`](../system_design/study_guide.md) (the mock
> mechanics). **Rebuilt Aug 13, 2026: SD is now mock interviews on HelloInterview's question board** —
> the learner studies independently, the coach interviews. This section is kept for the daily-loop
> mechanics and the company-targeting strategy, not as a second design plan. Where they differ, the SD
> files win.
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

**Company targeting, the tier route, the "why," and the apply gates now live in
[`../career_strategy.md`](../career_strategy.md)** — the single cross-track home for the goal (relocated out
of this guide Aug 6, 2026 so it stops drifting across copies). This guide is *how to study DSA*; the north
star is one click away.

For **problem-pull** purposes only: fintech (Stripe/Bloomberg/Citadel…) and data-platform
(Snowflake/Databricks/Datadog…) are the calibration/next-hop sources, big-tech/MANGA is the end goal — full
reasoning and the apply gates are in `career_strategy.md`.

Don't pull from a company you're actively interviewing at that week — keep those problems as genuine unknowns.

### 🔁 Design reps — one question, one cold mock, one rating

**One HelloInterview question = one tracked row = one ~45-min cold mock, in a single sitting.** A design
spread across sittings cannot be rated cold. The full framework runs *within* the session: **Requirements
→ Estimation → API/data model → High-level → Deep-dive forks → Failure modes → Evolve/operate.**

Mechanics (the split, the two slots, the protocol, the debrief) →
[`../system_design/study_guide.md`](../system_design/study_guide.md). Question order, phases and the
7-point rubric → [`../system_design/senior_ramp.md`](../system_design/senior_ramp.md). Rows →
[`../system_design/mastery/design_progress.md`](../system_design/mastery/design_progress.md).

### 🔄 Phase 2 DSA Hybrid Rule

The 15-minute daily maintenance flashcard keeps mastered patterns warm. But not all categories will be fully clean by end of Phase 1. Apply this rule:

| Category status at end of Phase 1 | Phase 2 DSA approach |
|------------------------------------|----------------------|
| Majority Clean (solved cold, correct complexity) | 15-min flashcard only — no new problems needed |
| Majority Shaky/Blank | Continue 1 new problem per week in that category during the weekday active block, alongside design work |
| Backlog spikes above 5 overdue | Pause design block entirely. Run emergency double warmup until cleared. Same rule as Phase 1 |

The Saturday randomized DSA sprint covers the pattern recognition gap regardless of category status — it's always on.

### 📋 Design Question Order — see the ramp

> **The design list, order, and exit gates now live in [`senior_ramp.md`](../system_design/senior_ramp.md).**
> Do not maintain a second order here (the old fintech-first list was retired Aug 6, 2026 with the re-aim
> to big tech).

**Source: [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/problem-breakdowns)**
— their 31 question breakdowns plus 4 no-write-up practice questions, at their own tiers. **No fintech
weighting**: Payment System and Robinhood sit off the rotation behind `waypoint_loop:fintech`.

**The prerequisite-tech gate is gone** (Aug 13, 2026) along with the study lanes — the learner studies
ahead of the board on HelloInterview, so a mock that lands on unfamiliar technology is information, not a
wasted session. Phase ordering (A: framework fluency → B: senior signals → C: simulation), the 7-point
rubric, and the apply trigger are all in the ramp.

**Still walk in talking tradeoffs, not diagrams** — the narration rule below is unchanged.

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
| **Advanced Graphs** | Jul 13–**Aug 16** | **11** | Network Delay Time (Dijkstra), Swim in Rising Water, Alien Dictionary, Cheapest Flights Within K Stops, Min Cost to Connect All Points, Reconstruct Itinerary, Word Ladder, **+ 1334 Find the City (Floyd-Warshall), + 721 Accounts Merge** *(new-technique)*, **+ 1631 Path With Minimum Effort, + 1514 Path with Maximum Probability** *(consolidation reps)* |
| **Sliding Window (finish) + Stack** | Aug 3–23 | 8 | Min Window Substring, Sliding Window Maximum; Min Stack, Evaluate Reverse Polish Notation, Generate Parentheses, Daily Temperatures, Car Fleet, Largest Rectangle in Histogram |
| **Intervals + Greedy** | Aug 24–Sep 13 | 14 | Insert Interval, Merge Intervals, Non-overlapping Intervals, Min Interval to Include Each Query, Meeting Rooms I & II; Jump Game I & II, Gas Station, Hand of Straights, Merge Triplets, Partition Labels, Valid Parenthesis String |
| **Backtracking** | Sep 14–Oct 11 | 9 | Subsets I & II, Combination Sum I & II, Permutations, Word Search, Palindrome Partitioning, Letter Combinations, N-Queens |
| **1D Dynamic Programming** | Oct 12–Nov 8 | 12 | Climbing Stairs, Min Cost Climbing Stairs, House Robber I & II, Longest Palindromic Substring, Palindromic Substrings, Decode Ways, Coin Change, Max Product Subarray, Word Break, Longest Increasing Subsequence, Partition Equal Subset Sum |
| **2D Dynamic Programming** | Nov 9–Dec 6 | 11 | Unique Paths, Longest Common Subsequence, Stock with Cooldown, Coin Change II, Target Sum, Interleaving String, Longest Increasing Path in Matrix, Distinct Subsequences, Edit Distance, Burst Balloons, Regular Expression Matching |
| **Bit Manipulation + Math & Geometry** | Dec 7–28 | 15 | Single Number, # of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers, Reverse Integer; Rotate Image, Spiral Matrix, Set Matrix Zeroes, Happy Number, Pow(x,n), Multiply Strings, Detect Squares |
| **Buffer + Final EOY Review** | Dec 29–31 | — | Sweep `dsa_progress.md` for all 🔴 Blank and 🟡 Shaky solutions. Target: ≤ 10 non-Clean by EOY |

> **🏖️ TWO NOVEMBER BREAKS — flagged Aug 6, 2026; the Oct/Nov weekly builds MUST sequence DP around
> these** (see [[project_november_breaks]]). ~1 week at **start of Nov (~Nov 1–7)** and ~1 week at **end
> of Nov (~Nov 24–30)**, both **light-maintenance, not full-offline** (flashcard-level at most). Both land
> **inside the DP phases** — start-of-Nov eats 1D DP's last week, end-of-Nov eats a week of 2D DP. Effects:
> **(1)** DP slips ~2 weeks → completion ~mid-to-late Dec, and "DSA → maintenance" (plus the earliest
> big-tech apply gate) moves with it — a **normal carry per [[feedback_phase_dates_are_advisory]]**, not a
> failure. **(2)** The load-bearing lever: **do NOT teach a brand-new DP pattern in the 2–3 days before
> either break** — a just-taught pattern + a week untouched = the never-encoded→gap→🔴 failure. Front-load
> new DP right after returning; leave pre-break days for review/consolidation. **(3)** Re-entry days after
> each break run **review-heavy** (double warmups) to drain the spaced-rep bulge; cap-7 is the drain
> capacity. Light maintenance during the weeks keeps the bulge small.

### Post-NC150 — The Steady State (Maintenance · Application · Expansion)

Once the roadmap completes and NC150 is Clean/retired, the mode shifts from **acquiring patterns** to three ongoing threads that run in parallel — this is the permanent steady state and the on-ramp to the competitive-programmer goal:

1. **Maintenance** — spaced repetition keeps NC150 alive: 🎓 graduated problems spot-check every 180 days; anything that slips to 🟡/🔴 returns to rotation. Never stops.
2. **Application — *pull, not push*.** Company frequency lists are a **reference pool, not a checklist.** *Pull* problems from them **gated by patterns/techniques already learned** (NC150 + expansion queue), to build **speed and transfer** on your existing foundation. Never march a company list top-to-bottom — your knowledge drives the selection, not the company's list. Log each pull in the tracker: 🟢 confirms transfer works; 🟡/🔴 is a **diagnostic** pointing at a pattern to refresh (not a cue to learn something ad-hoc). The two curated **pull pools** — interview-sourced (during Tier 1) and competitive-style (after, for Tier 2) — live in [`backlog/`](backlog/README.md). **Pulls are gated on measured review-capacity surplus, not on NC150 being finished** — see "Review capacity math" above; the surplus is expected to open around Oct–Dec 2026, while the roadmap is still running.
3. **Expansion — keep learning, deliberately.** Continue working the **Knowledge Expansion Queue** (bottom of `dsa_progress.md`): finish Tier 1 advanced (segment tree, KMP, XOR trie, …), then cross the Interview-ROI line into Tier 2 competitive material toward the competitive-programmer goal. New concepts enter **here, in order, deliberately** — never reactively off a company problem.

**The direction of causation always runs from your knowledge outward.** NC150 + expansion queue = what you know → pull application problems that exercise it, and grow the queue on purpose. Nothing external (a company list, a random hard problem) is allowed to *dictate* the curriculum.

### Two non-NC150 additions to Advanced Graphs (Jul 26, 2026)

Added under the standing rule that **NC150 is the floor of the high-ROI set, not its ceiling** — real
interview ROI earns a curriculum slot regardless of list membership.

- **LC 1334 — Find the City With the Smallest Number of Neighbors (Floyd-Warshall).** This closes a
  *family* gap, not just adds a problem. Shortest path has four cases and three were covered — BFS
  (unweighted), Dijkstra (non-negative), Bellman-Ford (negatives / hop-cap) — with **all-pairs
  entirely unrepped**. Floyd-Warshall is ~5 lines and the cheapest algorithm in the whole graph block
  to learn; leaving the family three-quarters complete was the expensive option. Decision table lives
  in [`mastery/recognition_gotchas.md`](mastery/recognition_gotchas.md).
- **LC 721 — Accounts Merge.** A perennial interview problem where Union-Find *mechanics* are the easy
  part and the **modeling** is the test — deciding that an email, not an account, is the node. The
  mechanics are already 🟢 across 323/684/261, so this exercises the step those don't.

**Two more added the same day as consolidation reps** (reversing an earlier decline — see "Two kinds
of new problem" below; *"near-duplicate of something already done"* turned out to be an argument
**for** scheduling, not against):

- **LC 1631 — Path With Minimum Effort.** Dijkstra where path cost is a **max over edges**, not a sum.
- **LC 1514 — Path with Maximum Probability.** Relaxation that **multiplies and maximizes** instead of
  adding and minimizing.

Together with 743 and 778 that's four Dijkstra-family problems whose differences are exactly what the
recognition gate tests: sum vs max vs product, minimize vs maximize. One instance of a technique
teaches "743 is the Dijkstra one" — a lookup. Four teaches the technique.

**Cost, stated plainly:** the phase goes **7 → 11 problems**, end date **Aug 2 → Aug 16**, pushing
Sliding Window/Stack back two weeks. Note the budget split: 1334 and 721 spend **new-technique**
intake (capped 3/wk); 1631 and 1514 are **consolidation reps** against the separate ≤2/wk budget,
gated on 778/743 sitting at 🟡+ — which they do.

> **⚠️ Reconciled at the Jul 27 weekly build — two rules written the same day collide, and the surplus
> rule wins.** Measured surplus came back **−7.3**, and the fill table permits reviews plus cap-level
> new intake *only* at ≤0 — **no consolidation reps.** The projection doesn't open surplus until
> Oct–Dec, so **1631 and 1514 will not land inside the Aug 16 window**; they become the first items
> scheduled when surplus turns positive.
>
> **This does not move the exit bar**, because exit is judged **per algorithm** (≥1 🟢 + recognition),
> not per problem — and Dijkstra already has 743 + 778. The consolidation reps deepen an algorithm
> that already clears the bar rather than being needed to reach it. **So Advanced Graphs is scheduled
> on 9 and exits on its 8 algorithms;** 1631/1514 stay in scope, just not in this window.
>
> The general shape worth remembering: **curriculum scope and schedulability are separate questions,
> and capacity decides the second.** Promoting something into a phase says it's worth doing, never
> that there's room for it this month.

### Phase exit standard — per algorithm, not per problem (set Jul 26, 2026)

**The goal at the end of a phase: every algorithm in it is locked down — recognized *and* executable.**

The old framing, *"phase completion = every associated problem 🎓 Graduated,"* cannot be met and therefore
gates nothing. 🎓 requires streak 3: a coded 🟢, then +30, then +60 — **90+ days minimum per problem.**
Advanced Graphs runs Jul 13–Aug 16. Nothing in it *can* be Retired by the exit date, so the rule
would either stall the roadmap permanently or be quietly ignored. It was being quietly ignored.

**The enforceable standard, measured per algorithm on two axes:**

| Axis | What it means | Evidence |
|---|---|---|
| **Recognition** | Given the problem cold with the method label stripped, the shape → algorithm + picking feature comes out right | a clean cold cue; no unresolved entry in [`recognition_gotchas.md`](mastery/recognition_gotchas.md) for that trigger |
| **Execution** | It can be written from a blank page, correct, with correct complexity | **≥1 problem for that algorithm at 🟢**, coded |

Both are required. Recognition without execution is knowing the name of the thing; execution without
recognition is a solution waiting for someone to tell it which problem it belongs to. **The interview
grades recognition in the first two minutes and execution for the next thirty.**

**On "slightly amiss" — tolerated, but only if named.** We do *not* wait for every problem to retire
before advancing; that stalls the roadmap for no benefit. A lingering 🟡 on a *second or third* problem
of an already-🟢 algorithm is acceptable. What is **not** acceptable is an algorithm with **zero** 🟢s,
or a recognition trigger that's still missing. Anything carried out of a phase must be **written into
the next phase's review load explicitly** — a carried gap that isn't scheduled is just a forgotten one.

**Report at phase close per algorithm, not per problem:**

> *Advanced Graphs — 8 algorithms: Dijkstra ✅(🟢 778) · Bellman-Ford ⚠️(🟡 787 only) · Prim/MST ⚠️ ·
> Hierholzer ❌(🔴 332) · Topo sort ✅ · BFS-transform ✅ · Floyd-Warshall — · Union-Find modeling —.
> Carrying: Hierholzer + Bellman-Ford into the Stack phase's warmups.*

Per-problem counts hide exactly the thing that matters: eleven problems can look healthy while one
*algorithm* is entirely unlearned.

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

#### 🎚️ Category Difficulty Tiers — the adjustable intake table

**This table is the single source of truth for weekly new-problem intake. To re-pace a category,
change its Tier here** — the agent reads this when building each week's schedule; nothing else needs
editing. A category earns a harder tier when its new problems consistently log 🔴 on first exposure
(the *blank tax*, below).

| Roadmap category | Tier | New/week | Notes |
|---|---|---|---|
| Standard Graphs | Moderate | 4–5 | |
| Heap / Priority Queue | Moderate | 4–5 | |
| Tries | Moderate | 4–5 | 3 problems; ~1 week |
| **Advanced Graphs** | **Hardest** | **3** | Hard→Hardest Jul 18, 2026: 1584 Prim still 🔴 after 2 exposures + review-saturated weeks; new-algorithm-per-problem at DP-level blank rate (was moderate→Hard/4 Jul 14) |
| Sliding Window | Moderate | 4–5 | |
| Stack | Moderate | 4–5 | |
| Intervals + Greedy | Moderate | 4–5 | |
| **Backtracking** | **Hard** | **4** | New decision-tree pattern per problem |
| **1D Dynamic Programming** | **Hardest** | **3** | Hardest + slowest; do not compress phase below 4 weeks |
| **2D Dynamic Programming** | **Hardest** | **3** | Hardest + slowest; do not compress phase below 4 weeks |
| Bit Manipulation + Math/Geometry | Moderate | 4–5 | Many are Easy-tier |

**Tier definitions:** **Moderate** = pattern reused across problems, first attempt often 🟡 not 🔴 → **4–5/week**.
**Hard** = a *new algorithm per problem*, first attempt almost always 🔴 → **4/week**.
**Hardest** = new-algorithm-per-problem *and* DP-level blank rate / slowest to settle → **3/week**
(**Advanced Graphs**, 1D DP, 2D DP).

- **New problems per week (difficulty-tiered, not just phase-dependent)** — per the table above:
  - **Moderate categories** (Standard Graphs / Heap / Tries / Sliding Window / Stack / Intervals+Greedy / Bit-Math): **4–5 per week.** Front-load these easier phases to bank a lead. Fits the 5/day cap (steady-state reviews ~3.5/day + 5 new ≈ 4.1/day).
  - **Hard, algorithm-dense categories** (**Backtracking**): **4 per week — not 5.** A *new decision-tree pattern per problem*, so the first attempt often logs 🔴, and every 🔴 spawns a +2-day retry that eats a warmup slot. Hold intake at 4 so the blank cascade has room to settle before the next new problem lands.
  - **Hardest categories** (**Advanced Graphs**, **1D DP** Oct, **2D DP** Nov): **3 per week.** Hardest and slowest, highest blank rate. Advanced Graphs was re-paced Hard→Hardest on Jul 18, 2026: it's a *new algorithm per problem* (Dijkstra, Bellman-Ford, MST/Prim, Eulerian…) **and** proving as blank-heavy as DP — 1584 Prim was still 🔴 after two exposures, and the +2 retry cascade collided with review-saturated weeks (Jul 20–26 was at 27/28 warmup slots on reviews alone). Keep intake at 3 so the blanks settle and it doesn't trip the overdue-backlog rule.
  - **Rationale — the blank tax.** A new problem is not a 1-slot commitment. A 🔴 costs 1 active slot *plus* ~2–3 follow-up warmup slots over the next fortnight as its +2 retries settle to 🟡. At 5 hard-category new/week, that cascade consumes ~40% of the 28 weekly warmup slots servicing *recent* material, starving the backlog (which is why the 🟢 pile sits at 35 and won't drain). Dropping hard categories to 4 returns roughly one warmup slot/week to genuine review. **Evidence this tier was real:** Advanced Graphs was mis-bucketed as "moderate" (4–5) and produced back-to-back 🔴 on 743 (Dijkstra) and 787 (Bellman-Ford) in one week — reclassified to hard on Jul 14, 2026.
  - **Net effect on the roadmap:** ~late-November NC150 completion holds, with far less Blank-pileup risk than 5/week through the hard blocks.
### Two kinds of new problem — the cap only governs one (added Jul 26, 2026)

The tiers above were calibrated on **new-algorithm** problems, and the blank-tax rationale says so
outright: *"a 🔴 costs 1 active slot plus ~2–3 follow-up warmup slots as its +2 retries settle."*
That is the cost of **learning an algorithm**, not the cost of *a problem*. So intake splits in two:

| Class | What it is | Expected first result | Cascade | Counts against the tier cap? |
|---|---|---|---|---|
| **New-technique** | first problem of an algorithm (Dijkstra, Hierholzer, Floyd-Warshall…) | 🔴 | yes — ~2–3 warmup slots over a fortnight | **Yes.** This is what 3/4/5 governs |
| **Consolidation rep** | *another* problem in a technique already at 🟡+ | 🟡, often 🟢 | none | **No.** Separate budget: **≤2/week** on top |

**Why consolidation reps are non-negotiable, not enrichment.** One problem per technique trains
**recall of that problem's solution**. It cannot train the technique, because there's no variation to
generalize across — you learn "743 is the Dijkstra one," which is a lookup, not a skill. Transfer
needs multiple surface forms of one underlying idea, and the *minor differences between near-identical
problems are the training signal, not noise*: cost-is-a-max vs cost-is-a-sum, multiplicative vs
additive relaxation, hop-capped vs unbounded. That discrimination is precisely what the
**recognition front-gate** grades, and it is untrainable from a single instance. A problem being
"similar enough to one already done" is therefore an argument **for** scheduling it, not against.

**The one gate: the base technique must be at 🟡 or better.** A sibling problem consolidates a
half-formed technique — that's the point, and interleaving while it's still settling is what makes it
stick. But if the base is 🔴 (never encoded), a sibling just double-blanks. Teach first (§ teach/measure),
*then* consolidate.

**Slotting:** consolidation reps don't need the full 45-min active block the way a new algorithm does —
they're closer to a review of a technique than an intake of one. Put them in an active block when the
problem is Hard, a generous warmup when it isn't.

- **Active-block guard**: only ~6 active-block slots exist per week (Sunday = system design). At 5 new/week, 5 slots are consumed by new problems — reserve at least 1 for re-coding Blanks. If Blank re-solves are stacking up, cut new intake that week.
- **Max overdue backlog before pausing new intake**: 5 problems.

### Review capacity math — and why intake becomes surplus-triggered (added Jul 26, 2026)

Review demand is not a headcount, it's a **rate**: each tracked row generates `1 / interval` reps per
day. Maturing a problem doesn't just mark it mastered — it **removes it from the schedule**.

| Status | Interval | Demand per row | Relative |
|---|---|---|---|
| 🔴 Blank | +2 | 0.500 /day | ×83 |
| 🟡 Shaky | +10 | 0.100 /day | ×17 |
| 🟢 streak 1 | +30 | 0.033 /day | ×6 |
| 🟢 streak 2 | +60 | 0.017 /day | ×3 |
| 🎓 Graduated | +180 | 0.006 /day | ×1 |

**Weekly capacity ≈ 28 problem-slots**: 7 days × 2 warmup slots × ~2 problems (≈28) − ~6 consumed by
the three SD lanes + ~6 active blocks (Sunday is SD).

**Calibration, Jul 26, 2026:** 69 streak-1 + 17 streak-2 + 19 🟡 + 1 🔴 ≈ **35.6/wk demand vs 28
capacity → −8 over-subscribed.** That deficit *is* the 23-item stale 🟢 pile; it isn't neglect, it's
arithmetic, and no amount of diligence drains it while demand exceeds capacity.

**The projection — the hole opens AFTER NC150, not before:**

| Point | Rows | Demand | vs capacity |
|---|---|---|---|
| Jul 2026 | 107 | ~36/wk | −8 over |
| Oct 2026 | ~150 | ~27/wk | at capacity |
| Dec 2026 (NC150 done) | ~190 | ~27/wk | at capacity |
| Mar 2027 | 190 | ~18/wk | **+10 idle** |
| Jun 2027 | 190 | ~11/wk | **+17 idle** |
| Late 2027 | 190 | ~7/wk | **+21 idle (75%)** |

Through the roadmap, new intake keeps feeding fresh streak-1 rows (+30 is a *heavy* rate), holding
demand near capacity. **The collapse comes when intake stops and the population matures to +60/+180
with nothing replacing it.** At full maturity, maintaining all of NC150 costs ~7 problems/week — a
quarter of the schedule.

**⇒ The rule: application pulls and extra intake are gated on MEASURED SURPLUS, not on a date.**
This supersedes *"no pulls during the NC150 milestone."* That phrasing is correct today only because
we're at −8; it silently becomes wrong the moment demand crosses below capacity, which the table above
puts around Oct–Dec 2026 — *while two phases are still open*.

**Measure it at weekly schedule build**, before slotting anything: sum `1/interval` over the tracker,
×7, compare to 28.

> **⚠️ Then check the per-day distribution — the surplus measures the WEEK, not the DAY.**
> A negative weekly surplus does **not** mean every day is full. SD lanes and doubled warmups land
> unevenly, so a −7 week routinely contains days sitting at 1–2 problems against a cap of 5. Slipping
> reviews off a week that still has slack days is a **false shortage**, and it costs real reps.
>
> **Before accepting any slip list, write the per-day row:**
>
> | | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
> |---|---|---|---|---|---|---|---|
> | DSA problems | | | | | | | |
> | Other (SD lanes, one-offs) | | | | | | | |
>
> Any day under the cap absorbs items back off the slip list — **prefer ones already due that day**,
> since those aren't being pulled forward at all, they simply stop slipping. Only then is the slip
> list final.
>
> *(Found Jul 27, 2026: a −7.3 build slipped 12 🟢 while Wed carried 1 problem and Sun carried 2.
> Four came straight back. The weekly total was correct and the conclusion drawn from it was not.)*

| Measured surplus | Fill with, in order |
|---|---|
| **≤ 0** (over-subscribed) | Nothing. Reviews only; hold intake at the tier cap and let the backlog drain |
| **1–5 slots** | **Consolidation reps** — techniques at 🟡+ that have fewer than 3 problems |
| **6–12 slots** | Consolidation reps, **then** application pulls (`pull_interview.py`, gated on learned patterns) |
| **13+ slots** | The above, **then** open Tier 1 advanced expansion early — don't wait for NC150 to formally close |

**Consolidation reps are the first filler for a reason:** the backlog is large (NC150 supplies 1–2
problems per technique where 3–4 are needed), it is directly aimed at the phase-exit standard, and it
is higher-ROI than reaching for Tier 2 material early. Reach past it only once that queue is genuinely
short.

### Library carrying capacity — graduation and disposable reps (added Jul 26, 2026)

**The constraint:** a tracked problem never stops costing. Even fully retired at +180 it bills
**0.039 slots/week forever.** At 28 slots/week the library has a **carrying capacity of ~500–600
problems**, past which maintenance eats everything and intake must stop. Sustainable intake *decays*
as the library grows:

| Library size | Maintenance | Sustainable new intake |
|---|---|---|
| 190 (NC150 done) | ~7/wk | ~3/week |
| ~350 | ~14/wk | ~2/week |
| ~500 | ~20/wk | ~1/week |
| ~700 | 28/wk | **zero** |

Left alone, "keep adding problems" strangles itself in about three years. Two mechanisms prevent that.

#### 🏆 Retirement — the terminal tier, above 🎓

🎓 Graduated still bills a spot check every 180 days, forever. Retirement is the step past it, and
**how many spot checks it takes depends on how the problem reached 🎓:**

| Path to 🎓 | Spot checks needed to retire | Why |
|---|---|---|
| **Standard** — climbed s1 → s2 → s3 | **two** clean (≈1 year at 🎓, ~2.5 years from first Clean) | nothing else is testing this technique; the second check is the evidence |
| **Over-learned fast-track** | **one** clean | the **coverage gate** already supplied that evidence — harder problems are still testing the technique on the normal ladder |

> On retiring, the row leaves the review table for the `🏆 Retired` list — no interval, no
> next-review date, no ongoing cost. If it ever resurfaces (a pull, a real interview) and fails, it
> re-enters at 🟡 like anything else.

**Why the fast-track needs only one** (decided Jul 26, 2026): the standard path's second spot check
exists because a problem that climbed the ladder normally has no *other* evidence behind it — the
ladder is the only thing vouching for it. A fast-tracked problem was admitted to 🎓 precisely *because*
the technique is under active test elsewhere (condition 3, the coverage gate). That gate is a standing
guarantee, not a one-time check, so it does the second check's job continuously. Requiring two would
be asking the same question twice.

This is the release valve. Without it the carrying capacity is a hard wall.

**Mechanical requirement — do not skip this.** Discovery in `update_review_dates.py` scans
`dsa/leetcode/**` and re-adds any problem it can't find a row for. A graduated problem still has its
`.py` file, so **removing the row alone will silently resurrect it on the next commit.** Graduating
requires *both*: move the row to the Graduated list **and** add the number to `discovery_skip` in
`cse.config.yml`. Keep the Graduated list in **plain bullet form**, not the 7-column table, so the
tracker parser doesn't pick it up.

#### Disposable reps — the answer to staleness

This one changes an assumption the system currently makes silently: *every problem solved gets a
permanent tracker row.* It doesn't need to.

For **consolidation reps** and **application pulls**, the thing under test is whether the *technique*
transfers. The specific problem is a **probe, not an asset**.

> **Solve it → record the outcome against the *technique's* ledger (`recognition_gotchas.md` /
> `complexity_gotchas.md`) → create no review row.** A 🟢 means the technique is confirmed and that
> problem is done forever. **Only a 🟡/🔴 earns a tracker row**, because only a gap needs repetition.

**Why this is the real fix for freshness:** it makes new problems nearly free. You can run 3–5 fresh
pulls a week indefinitely and maintenance barely moves, because you're maintaining **~30 techniques,
not 700 problems**. It also matches reality — nobody re-solves the same Dijkstra problem a fifth time
in year three; they solve a *new* one and confirm the technique still fires.

**Mechanical requirement:** discovery would auto-add a probe the moment its file lands under
`dsa/leetcode/`. Two options — **(a)** scaffold probes into a separate root (e.g. `dsa/probes/`) that
isn't in `solutions.roots`, so discovery never sees them (needs a `--probe` flag on
`new_problem.py`); or **(b)** leave them under `dsa/leetcode/` and add each to `discovery_skip`, which
works today with no code change but grows that list without bound. **(a) is the right design; (b) is
the stopgap.**

#### ⚡ The over-learned fast-track (added Jul 26, 2026)

Some problems cannot plausibly decay. Standard binary search, after four clean reps, is a motor skill
rather than a recalled algorithm — and **the ladder's only job is to catch decay**, so climbing
s1 → s2 → s3 on it spends slots for nothing. The stale 🟢 pile is almost entirely this: 1929, 217, 26,
344, 125, 1768, 88, 100, 14.

**A problem may skip straight to 🎓 Graduated (Streak 3, +180) on its next clean rep when all three hold:**

1. It's **🟢 and has been cleaned before** — not a first success.
2. The learner **declares it over-learned.** Self-reported, like Comfort.
3. **Coverage gate — the technique appears in at least one *harder* tracked problem still on the
   normal ladder.**

**Condition 3 is what makes it safe**, and it's the whole rule. You're not stopping testing the
technique; you're stopping testing it **at its easiest instance** while harder ones still do the work.
Same logic as per-algorithm phase exit: *the technique is the unit, not the problem.* If the technique
has no harder representative, the easy problem **is** the coverage and the fast-track is refused.

**Worked example — 704 Binary Search, Jul 26, 2026** (the first application): 🟢 s1, cleaned four times
since March, and binary search is carried by **seven** harder tracked problems (74, 875, 540, 33, 153,
2300, 1011) of which **two were 🟡 at the time**. Fast-tracked to 🎓, next look Jan 22 2027. Load drops
from 0.033 to 0.006 slots/day — about **6×**.

**Retires after ONE clean spot check, not the standard two** (decided Jul 26, 2026) — the coverage
gate is a standing guarantee that the technique stays under test elsewhere, so it does the second
check's job continuously. For 704 that means: graduated Jul 26 2026 → spot check **Jan 22, 2027** →
if clean, **retired that day** rather than waiting for a second check in mid-2027.

#### When to open Tier 1 expansion — the pull-rate trigger

Consolidation is **a phase, not a steady state.** ~30 NC150 techniques × 2–3 confirming pulls each is
**60–90 pulls total**; at ~10/week once surplus opens, that pool is exhausted of diagnostic value in
**6–9 weeks.** So "what comes after consolidation" needs its own trigger.

**Primary signal — the pull diagnostic rate.** A pull's 🟢 confirms transfer; a 🟡/🔴 is a diagnostic
pointing at a pattern to refresh. So the pool's *teaching value* is measurable directly:

> Over a rolling window of **~15 pulls**, if **≥85% come back 🟢**, the pull pool has stopped teaching
> anything — it's maintenance now, not learning. **That's the cue to open Tier 1 advanced.**
> Below **~70% 🟢**, real gaps remain and Tier 1 would be front-running them: keep consolidating.

**This metric is free, courtesy of disposable reps.** A 🟡/🔴 pull creates a tracker row and a 🟢
doesn't — so **the row-creation rate over a window *is* the diagnostic rate.** Nothing extra to track;
just count how many of the last 15 pulls left a row behind.

**Two supporting conditions** (they should converge; if they don't, the pull rate governs — capacity
without confirmed transfer just means room to learn new things on a shaky base):

1. **Coverage** — every NC150 technique at ≥1 🟢 with ≥3 problems of evidence. The per-algorithm exit
   standard applied to the whole roadmap rather than one phase.
2. **Capacity** — ≥10–13 surplus slots. Tier 1 is *new-technique* intake (segment tree, KMP,
   Manacher's are dense), so it reinstates the blank tax: ~2/week × ~3 slots each ≈ 6 sustained, plus
   headroom. Projected around Mar–May 2027.

> ### ⚠️ Gate on internal state, never on job outcomes
>
> **No milestone in this system — phase exit, ROI-line crossing, Tier 1 or Tier 2 opening — is ever
> gated on an offer, an interview result, or an application date.** Those matter financially, but they
> depend on outside factors that can't be predicted or controlled, and hanging a study trigger on one
> means the plan stalls or lurches for reasons that have nothing to do with what's actually been
> learned.
>
> Every gate here resolves against something **measurable in this repo**: a comfort rating, a streak, a
> surplus computation, a pull rate. The job-search timeline lives in `career/career_trajectory.md` and
> the company-tier tables above — it informs *what* is worth learning (interview ROI), never *when*
> you're ready to move on.

#### What this does to the tracker's meaning

Today `dsa_progress.md` is *"everything I've solved."* After this it becomes **"everything still
unproven"** — a work queue, not a trophy case. Row count stops being a measure of progress and starts
being a measure of *remaining debt*, so a **shrinking** tracker is the healthy direction. The record
of what's been accomplished moves to two places: the **🏆 Retired list**, and the **technique
ledgers** that disposable reps write into.
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

*(Phase 3 — AI System Engineering & Infrastructure — was removed Aug 13, 2026. It was never started and
had no sessions. LLM-serving content is not gone from the plan: **ChatGPT** is a Hard row on the SD
board and covers token streaming, context-window management, batching and quotas as a design.)*

---

## Reference Materials

### 🌐 System Design Resources
1. **The syllabus, and the only one that matters for the board**: [HelloInterview — System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction). Core Concepts · Key Technologies · Patterns · the question breakdowns. Study this ahead of the mocks; the breakdown for the *next* question is the one thing to leave unread.
2. **Depth, when a mock exposes a real gap**: Alex Xu's [ByteByteGo](https://bytebytego.com) for visual architectural breakdowns; the [System Design Primer](https://github.com/donnemartin/system-design-primer) for fundamentals.
3. **Real-world scale**: the [Netflix Tech Blog](https://netflixtechblog.com) and Uber Engineering, searched for the specific thing you just got pushed on — *"distributed caching"*, *"Kafka streaming"*, *"rate limiters"*.


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
3.  **Coding Required for Clean**: 🟢 Clean is earned only by **coding** the solution from a blank page. A no-code blueprint caps at 🟡 Shaky and cannot advance the streak toward graduation; the sole carve-out is a flawless spot check *confirming* an already-🎓 Graduated problem.
4.  **Whiteboard Fidelity**: Write the *full* solution from scratch every time — including any `ListNode` / `TreeNode` / `TrieNode` definitions. No shared boilerplate/data-model module to import; re-deriving the scaffolding is part of the rep, exactly as on an interview whiteboard.
5.  **5-Problem Daily Cap**: Never exceed 5 problems in a day. Active block is always protected — trim warmup slots first. When a problem is bumped, assign it a specific future slot in the same edit.
