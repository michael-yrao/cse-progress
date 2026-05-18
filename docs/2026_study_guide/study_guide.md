# 📅 The Ultimate 8-Block Technical Study Master Plan

## 🧠 THE RETENTION PROTOCOL (Non-Negotiable)
To guarantee your knowledge permanently sticks over Months 1–7, you must follow the **Spaced Repetition Rule**:
1. **Never skip the 15-minute warm-up**: It is mathematically more important to retain an old problem than to solve a new one.
2. **The 2–3 Day Sweet Spot**: Your warm-up problem must always be something you struggled with 2–3 days ago. This is the cognitive science "sweet spot." It is far enough out that your brain must struggle to recall it (building long-term neural pathways), but close enough that you don't have to completely relearn it from scratch. You are practicing pattern retrieval, not rote syntax memorization.
3. **The Saturday Code Sprint**: In later system design blocks, you *must* code one random past DSA problem from scratch under a 20-minute timer to maintain raw muscle memory.

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
2.  **Quality > Quantity**: Aim for 3 to 4 perfectly understood problems per week instead of rushing.
3.  **Sunday Lockout**: Do not open a code editor on Sundays. Give your neural pathways a break so short-term data transitions into long-term memory structures.
