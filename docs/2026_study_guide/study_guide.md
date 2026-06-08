# 📅 The Ultimate 8-Block Technical Study Master Plan

# 📅 The 5-Day Backlog Rotation & Retention Protocol

## 🚨 THE PRIORITY ROTATION ENGINE
Every Sunday night, look at your spreadsheet backlog and select **5 older problems** to populate Monday through Friday's 15-minute warmup slots. Select them using this strict algorithmic filter:
1. **Priority 1 (High Risk)**: Problems marked `Mastered: N` with the oldest "Latest Attempt Date" (e.g., *36. Valid Sudoku* from Jan 25).
2. **Priority 2 (Medium Risk)**: Problems marked `Mastered: N` with more recent dates (e.g., *75. Sort Colors* from April 1).
3. **Priority 3 (Maintenance)**: Problems marked `Mastered: Y` that you haven't touched in over 30 days (e.g., *238. Product of Array Except Self* from April 13).
---

## 🚨 BACKLOG RECOVERY PROTOCOL

**Trigger**: Any time the Next Review Date is 7+ days overdue with no new attempt logged.

### Emergency Double Session Rule

When triggered, run **two 15-minute warmup blocks per day** (morning + evening) until the overdue list is cleared. Do not start any new problems in your active block until the Critical tier is fully resolved.

#### Critical (4+ weeks overdue as of June 7)
- [ ] 21. Merge Two Sorted Lists (Iterative) — due Apr 28
- [ ] 162. Find Peak Element — due May 4
- [ ] 540. Single Element in a Sorted Array — due May 4
- [ ] 572. Subtree of Another Tree — due May 4
- [ ] 102. Binary Tree Level Order Traversal — due May 5
- [ ] 235. Lowest Common Ancestor of a BST — due May 5
- [ ] 1011. Capacity to Ship Packages Within D Days — due May 5
- [ ] 2300. Successful Pairs of Spells and Potions — due May 5
- [ ] 199. Binary Tree Right Side View — due May 11
- [ ] 21. Merge Two Sorted Lists (Recursion) — due May 23
- [ ] 19. Remove Nth Node From End of List (Recursion) — due May 23

#### High (2–4 weeks overdue as of June 7)
- [ ] 206. Reverse Linked List (Iterative) — due May 28
- [ ] 33. Search in Rotated Sorted Array — due May 31
- [ ] 18. Four Sum — last attempt Jan 23, never revisited
- [ ] 167. Two Sum II — last attempt Jan 19, never revisited

#### Recent (< 2 weeks overdue as of June 7)
- [ ] 680. Valid Palindrome II — due Jun 1
- [ ] 1216. Valid Palindrome III (backtracking) — due Jun 2
- [ ] 1216. Valid Palindrome III (1DP) — due Jun 2
- [ ] 695. Max Area of Island — due Jun 3
- [ ] 200. Number of Islands (DFS) — due Jun 4
- [ ] 543. Diameter of Binary Tree — due Jun 4
- [ ] 283. Move Zeroes — due Jun 4

### Permanent Backlog Rule

If the overdue count ever exceeds **5 problems**, suspend new problem intake entirely. Run double warmup sessions daily until it drops below 5, then resume at half pace (1–2 new per week) until fully cleared.

## ⏱️ The 15-Minute "No-Code" Warmup Execution
Because 15 minutes passes incredibly fast, **never write code during a backlog warmup**. Code writing is reserved for your 45-minute active block. Optimize your 15 minutes like this:
* **00:00–00:05 | The Read**: Open the LeetCode prompt. Analyze the sample inputs and outputs.
* **00:05–00:12 | The Conceptual Blueprint**: Out loud, state the optimal Time/Space complexity and the core structural trick. (e.g., *"This is Top K Frequent. I count frequencies with a Hash Map, then use Bucket Sort where array indices represent frequencies to guarantee O(n) runtime."*)
* **00:12–00:15 | The Verification**: Open your past successful code or your "Why I Got Stuck" log entry to verify if your mental blueprint was 100% accurate.

### 📋 Post-Warmup Spreadsheet Updates:
* **If your blueprint was flawless**: Update status to `Mastered: Y` and change the "Latest Attempt Date" to today.
* **If you completely forgot the trick**: Keep status as `Mastered: N`, change the date to today, and flag it to reappear in the warmup slot in exactly 3 days.

### ⚡ Easy Problem Exception

For problems marked **Easy**, the no-code rule is lifted:

* **During warmup**: Code the solution directly. Target **2 easy problems per 15-minute slot** (~7 min each). If you finish the first and still have time, pull the next Easy from the backlog immediately — do not stop at one.
* **During the active block**: Target **2 easy problems per session** instead of 1. Use the time saved to run the Speed Demon Protocol (edge cases + alternative solutions) on at least one of them.
* **Mastery bar is the same**: Easy does not lower the standard. Both problems must be completable from a blank page with correct complexity before marking `Mastered: Y`.

---

## 🗂️ The New Weekly Macro-Schedule

*   **Monday – Friday | The Split Focus Routine**:
    *   *00:00–00:15*: 15-Minute No-Code Backlog Warmup (Managed by the Priority Engine above).
    *   *00:15–01:00*: 45-Minute Road-Map Deep Dive (Your active block for new/current problems).
*   **Saturday | The Blind Code Sprint (30–45 Mins)**:
    *   Pick **one** random problem from your past week's logs. Clear your monitor, open a blank text file, and write the Python solution from memory under a 20-minute timer.
*   **Sunday | Strict Lockout**:
    *   Do not open a code editor. Allow your brain to consolidate short-term data into long-term structures.

---

## ⏱️ Daily Routine 1: The DSA Phase (Blocks 1–4)
*Use this structure for the first 16 weeks of your study journey.*
*   **00:00–00:15 | Recall Warm-up**: Open a problem solved 2–3 days ago. Do not rewrite code; trace its variable state changes on paper or in comments.
*   **00:15–00:30 | Whiteboard & Ideate**: Read a new problem. Sketch the approach, constraints, and edge cases in plain English. No code!
*   **00:30–00:45 | Look up / Validate**: If completely stuck or your logic loops, stop. Watch the NeetCode video explanation immediately.
*   **00:45–01:00 | Python Implementation**: Type out the clean code, trace logic line-by-line, and add comments explaining the "why".

## ⚡ THE SPEED DEMON PROTOCOL (If you finish a problem in 10-15 minutes)
Do not log off early and do not move on to a brand-new coding problem. Spend the remaining 45 minutes on deep optimization:
*   **Min 15–30 | Run the 3 System-Breaking Edge Cases Manually**: Trace your solution using the Mental Compiler Framework on: 1) An input of size one, 2) An input where the head must be removed, and 3) An input where the tail must be removed. Ensure no `NoneType` errors occur.
*   **Min 30–45 | Hunt for Alternative Python Solutions**: Go to the LeetCode Solutions tab. Find a solution that uses less memory or cleaner logic. Study how senior engineers minimized their variable assignments.
*   **Min 45–60 | Scale it up to System Design**: Ask yourself how this logic applies to the real world. (e.g., *If this Linked List represented user browser history, how would a backend system safely delete the last N nodes from a database for millions of users without locking up the database server?*)

---

## ⏱️ Daily Routine 2: The Design & AI Phase (Blocks 5–8)
*Use this structure from Week 17 onward to protect your DSA knowledge.*
*   **00:00–00:15 | DSA Maintenance Flashcard**: Look at a random past LeetCode prompt. Explain the data structure pattern and optimal Time/Space complexity out loud.
*   **00:15–01:00 | Architecture Deep Dive**: Spend 45 minutes learning your current block's design or AI concepts via engineering blogs or videos.

---

## 📅 Revised Phase Plan: June–December 2026

> This supersedes the week numbers in the 8-Block Roadmap below. The block structure is preserved;
> only the ordering and timing are corrected based on actual progress as of June 7, 2026.

| Phase | Approx. Dates | New Problems | Categories |
|---|---|---|---|
| **Recovery + Standard Graphs** | Jun 8–21 | 6–8 | Course Schedule I & II, Pacific Atlantic Water Flow, Surrounded Regions, Graph Valid Tree, Number of Connected Components, Redundant Connection |
| **Heap / Priority Queue** | Jun 22–Jul 5 | 7 | Kth Largest in Stream, Last Stone Weight, K Closest Points to Origin, Task Scheduler, Design Twitter, Find Median from Data Stream, Merge K Sorted Lists |
| **Tries** | Jul 6–12 | 3 | Implement Trie, Design Add and Search Words, Word Search II |
| **Advanced Graphs** | Jul 13–Aug 2 | 6 | Network Delay Time (Dijkstra), Swim in Rising Water, Alien Dictionary, Cheapest Flights Within K Stops, Min Cost to Connect All Points, Reconstruct Itinerary |
| **Sliding Window (finish) + Stack** | Aug 3–23 | 8 | Min Window Substring, Sliding Window Maximum; Min Stack, Evaluate Reverse Polish Notation, Generate Parentheses, Daily Temperatures, Car Fleet, Largest Rectangle in Histogram |
| **Intervals + Greedy** | Aug 24–Sep 13 | 14 | Insert Interval, Merge Intervals, Non-overlapping Intervals, Min Interval to Include Each Query, Meeting Rooms I & II; Jump Game I & II, Gas Station, Hand of Straights, Merge Triplets, Partition Labels, Valid Parenthesis String |
| **Backtracking** | Sep 14–Oct 11 | 9 | Subsets I & II, Combination Sum I & II, Permutations, Word Search, Palindrome Partitioning, Letter Combinations, N-Queens |
| **1D Dynamic Programming** | Oct 12–Nov 8 | 12 | Climbing Stairs, Min Cost Climbing Stairs, House Robber I & II, Longest Palindromic Substring, Palindromic Substrings, Decode Ways, Coin Change, Max Product Subarray, Word Break, Longest Increasing Subsequence, Partition Equal Subset Sum |
| **2D Dynamic Programming** | Nov 9–Dec 6 | 11 | Unique Paths, Longest Common Subsequence, Stock with Cooldown, Coin Change II, Target Sum, Interleaving String, Longest Increasing Path in Matrix, Distinct Subsequences, Edit Distance, Burst Balloons, Regular Expression Matching |
| **Bit Manipulation + Math & Geometry** | Dec 7–28 | 15 | Single Number, # of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers, Reverse Integer; Rotate Image, Spiral Matrix, Set Matrix Zeroes, Happy Number, Pow(x,n), Multiply Strings, Detect Squares |
| **Buffer + Final EOY Review** | Dec 29–31 | — | Review all `Mastered: N` problems. Target: ≤ 20 unmastered at EOY |

### Why Heap Comes Before Advanced Graphs

Dijkstra's algorithm (required for Network Delay Time, Cheapest Flights, Swim in Rising Water) uses `heapq` as its core data structure. Attempting those problems without heapq fluency means learning two things simultaneously. Complete Heap/PQ first so Advanced Graphs is purely about the graph logic.

### Why Tries Slot Between Heap and Advanced Graphs

Tries are 3 problems and complete in roughly one week. Grouping them here keeps the heavy graph block contiguous (Standard Graphs → Tries → Advanced Graphs) rather than fragmenting it later.

### Sort Algorithm Variants — Trimmed

`912. Sort an Array` variants are capped at two: **Merge Sort** (already done) and **Quick Sort**. The remaining variants (Radix, Counting, Timsort, Divide and Conquer) are not NeetCode 150 problems and consume week slots needed for the EOY goal. Remove them from the active tracker.

### Pace Targets

- **New problems per week**: 3–4. Do not exceed 4 unless the current category is trivially easy.
- **Max overdue backlog before pausing new intake**: 5 problems.
- **DP phases (1D + 2D)**: Allow 4–5 weeks each. Do not compress below 4 weeks per phase.

---

## 🗺️ The 8-Block Linear Roadmap

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
*   **Block 8: AI Infrastructure & Retrieval (Weeks 26–29)**
    *   *Core Concepts*: 
        *   **Vector Search Foundations**: Text chunking strategies, embeddings pipelines, and index methods (HNSW/IVF) in vector databases like Pinecone.
        *   **Context Window & Token Management**: Context ranking, prompt compression, and semantic caching architectures to limit LLM latency and API costs.
        *   **Agentic Orchestration & Tool Use**: Connecting LLMs deterministically to functions/APIs, structuring predictable JSON outputs, and state tracking.
        *   **Evaluation & Guardrail Architecture**: Programmatic evaluation layers, hallucination checks, and safety proxy layers filtering unsafe input/outputs.

---

## 🚀 Recommended Study & Reference Guides

### 🌐 System Design Resources (Months 5-6)
1. **The Core Blueprint**: Read the open-source [System Design Primer on GitHub by Donne Martin](https://github.com). It is the absolute best free textbook for web fundamentals, performance trade-offs, and database scaling.
2. **Visual & Structural Breakdowns**: Check out Alex Xu's [ByteByteGo Platform](https://bytebytego.com) for bite-sized, highly scannable visual architectural designs.
3. **Real-World Scale Case Studies**: Read the [Netflix Tech Blog](https://netflixtechblog.com) and [Uber Engineering Blog](https://uber.com) specifically searching for terms like *"Distributed Caching"*, *"Kafka Streaming"*, or *"Rate Limiters"* to see how your current block topics look in production.

### 🤖 AI Engineering & Infrastructure Resources (Month 7)
1. **Practical Code & Frameworks**: Use the short courses on [DeepLearning.AI](https://deeplearning.ai). Focus specifically on their specialized micro-courses covering *LangChain for LLM Application Development*, *Vector Databases*, and *Evaluating LLM Applications*.
2. **Production AI Case Studies**: Read the [Pinecone Engineering Blog](https://pinecone.io) to deep-dive into high-performance vector search architecture and production-grade RAG pipelines.
3. **Architectural Frameworks**: Browse the documentation of production orchestration libraries like [LlamaIndex Architecture Guides](https://llamaindex.ai) to learn how data ingestion pipelines operate under the hood.

---

## 🚀 Week 1 Problems: Block 1 Starter Pack

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

## 👁️ The Mental Compiler: Manual Code Tracing Framework
Mastering the art of debugging in your head or on a whiteboard without hitting the "Run" button is what sets elite engineers apart. Apply these techniques daily:

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

## 📓 "Why I Got Stuck" Log Template
Create a running notebook using this format. Review this document every Saturday morning to find your retention leaks.

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

## 🚫 Core Rules for Success
1.  **Strict 45-Minute Cap**: If a new problem isn't solved in 45 minutes, stop, look up the solution, and make it tomorrow's 15-minute recall warm-up.
2.  **Quality > Quantity — Hard Mastery Bar**: Aim for 3 to 4 perfectly understood problems per week. A problem is `Mastered: Y` only when you can write the complete solution on a blank page with no hints and state the correct time/space complexity unprompted. "Mostly remembered it" = `N`. If a problem has 3+ attempts and is still `N`, it has a specific conceptual gap — create or update its stuck log entry rather than scheduling another repetition without first naming the gap.
3.  **Sunday Lockout**: Do not open a code editor on Sundays. Give your neural pathways a break so short-term data transitions into long-term memory structures.
