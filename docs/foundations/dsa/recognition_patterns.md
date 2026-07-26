# Recognition Patterns — the "when I see X, reach for Y" catalog

NC150 is organized by **data structure**. Interviews hand you a problem with **no label** and
grade, in the first two minutes, whether you can map its *shape* to a technique. This catalog is
that map — the cross-cutting reflex the by-category layout hides.

**How to use it.** This is the reference behind the **recognition front-gate**: before coding any
problem, state its **shape → technique + why** (your pre-code comment). Drill **one card per week**
as a warmup note — zero new-problem load, since every anchor is a problem you already own. When you
misjudge one live, it gets carded in [recognition_gotchas.md](mastery/recognition_gotchas.md) (the
miss ledger); this file is the *reference*, that one is the *scoreboard*.

**The load-bearing part of each card is the picking feature** — the single trait that separates the
technique from its nearest neighbor. Memorizing "743 = Dijkstra" is worthless; memorizing "weighted
edges → Dijkstra, uniform → BFS" fires on fifty problems you've never seen.

---

| # | You see (trigger) | Reach for | Picking feature (say this out loud) | Anchors |
|---|---|---|---|---|
| 1 | subarray sum / count of subarrays = k | prefix-sum + hashmap of running sums | contiguous **and** an exact-sum target (not a shrinkable window) | 560, 238 |
| 2 | nearest greater/smaller, histogram, span, car fleet | monotonic stack / deque | need the **nearest** larger/smaller, resolving in stack order | 739, 84, 901, 853 |
| 3 | "smallest speed/capacity that works", min feasible value | **binary search on the answer** | the answer is monotonic (feasible ⇒ all larger feasible), even if input isn't sorted | 875, 1011, 410 |
| 4 | cycle detection, find-the-duplicate, middle of list | fast/slow pointers (Floyd) | linked structure / implicit `next()`, **O(1) space** required | 141, 287, 143 |
| 5 | components, redundant edge, valid tree, connectivity | union-find (DSU) | you keep **merging** groups and asking "connected?" (undirected) | 684, 261, 323 |
| 6 | valid order under dependencies, course schedule | topological sort (Kahn / DFS post-order) | a **DAG** + "produce a valid linear order" / "is one possible?" | 207, 210, 269 |
| 7 | running median, balance two halves of a stream | two heaps (max-heap low, min-heap high) | streaming + repeated **median/kth** query, O(log n) insert | 295, 480 |
| 8 | "find all subsets/permutations/ways" | backtracking (choose → recurse → un-choose) | must **enumerate** solutions (not just count/optimize), prunable | 78, 46, 39, 79 |
| 9 | longest/shortest **contiguous** run meeting a condition | sliding window | contiguous **and** condition monotonic as window grows/shrinks | 3, 424, 76, 239 |
| 10 | k most/least frequent, k largest, k closest | heap of size k (or bucket sort → O(n)) | want **top-k**, not a full sort — heap wins when k ≪ n | 347, 973, 215 |
| 11 | fewest steps / shortest path, **unweighted** | BFS (level-order) | every edge costs the **same** — uniform cost is what makes BFS shortest | 200, 994, 127, 286 |
| 12 | minimum cost/time over a **weighted** graph | Dijkstra (min-heap) | edges weighted & non-negative (uniform → BFS; negative/k-hop → Bellman-Ford) | 743, 787, 778 |

---

**The three shortest-path neighbors (cards 11–12 + the extension)** trip people most — one clean fork:

- unweighted / uniform cost → **BFS**
- weighted, non-negative → **Dijkstra**
- weighted, negatives or ≤k hops → **Bellman-Ford**

The single feature that routes you: *are the edges weighted, and can weights be negative?*

> Notes area — as you drill each card, add your own failing-case or mnemonic beneath it. The card is
> the reference; your note is what makes it stick.
