# Intuition Cheatsheet

Fast triage: scan the **signal** column for a clue that matches your problem, then jump to the technique. Use this when you don't yet know what a problem wants. (Know the move → open a [technique](techniques/) directly; know the data shape → open a [hub](data-structures/).)

## Signal → technique

| What you see in the prompt | Reach for | Doc |
|----------------------------|-----------|-----|
| **Sorted** array + "find a pair/triple summing to target" | two pointers (converge from ends) | [two_pointer](techniques/two_pointer.md) |
| **Sorted**, or "smallest/largest x that works", or "find position" | binary search (min/max boundary) | [binary_search](techniques/binary_search.md) |
| "**Contiguous** subarray/substring" + a constraint (≤ k distinct, sum, longest/shortest) | sliding window | [sliding_window](techniques/sliding_window.md) |
| "Subarray **sums to k**" / many range-sum queries | prefix sum (+ hashmap) | [prefix_sum](techniques/prefix_sum.md) |
| "**Next greater/smaller**", spans, histogram, temperatures | monotonic stack | [monotonic_stack](techniques/monotonic_stack.md) |
| "**Max/min in every window** of size k" | monotonic deque | [monotonic_stack](techniques/monotonic_stack.md) |
| Linked list: "**cycle?**", "**middle**", "find the duplicate number" | fast & slow pointers | [fast_slow_pointer](techniques/fast_slow_pointer.md) |
| Linked list: "**reverse**", reorder, palindrome | in-place reversal | [in_place_reversal](techniques/in_place_reversal.md) |
| Linked list: head may change (insert/delete at front, merge) | dummy node | [dummy_node](techniques/dummy_node.md) |
| "**Connected?**", "how many groups/components", cycle in an **undirected** graph | union-find | [union_find](techniques/union_find.md) |
| "**Prerequisites**", "ordering", "can you finish" (a DAG) | topological sort | [topological_sort](techniques/topological_sort.md) |
| "**Shortest # of steps**" / "level by level" (unweighted) | BFS | [tree_bfs](techniques/tree_bfs.md) |
| Tree property that **depends on children** (height, balanced, diameter) | DFS postorder | [tree_dfs](techniques/tree_dfs.md) |
| **BST** "sorted output" or "validate" | DFS inorder | [tree_dfs](techniques/tree_dfs.md) |
| "**All** subsets / permutations / combinations", "find every way" | backtracking | [backtracking](techniques/backtracking.md) |
| Overlapping subproblems / "min/max/count ways" with optimal substructure | DP (memoization) | [memoization](techniques/memoization.md) |
| "**Kth largest / smallest**", "top k", "k closest" | heap | [big_o](../fundamentals/big_o.md) |
| "**Majority** element" (> n/2 or > n/3) | Boyer-Moore voting | *below* |
| Array of `1..n`, find the **missing / duplicate** | cyclic sort | *below* |
| "**Running median**" of a stream | two heaps | *below* |
| "Kth largest" and you want O(n) average, no full sort | quickselect | *below* |

When totally stuck: **can I sort?** If the answer is a count, order doesn't matter, validity is monotonic, or brute force is O(n²) — sorting often unlocks two-pointer / binary-search / greedy.

## Single-trick techniques (recall by name)

Each is one clever idea, not a broad pattern — no dedicated doc; memorize the trigger and the trick.

| Technique | Trigger | The trick | Problems |
|-----------|---------|-----------|----------|
| **Boyer-Moore voting** | Majority element (> n/2, or > n/3) | Keep `candidate` + `count`; ++ on match, -- on mismatch, swap candidate at 0 — the majority survives cancellation. For > n/3, track **two** candidates. Re-verify at the end. | 169, 229 |
| **Cyclic sort** | Array holds `1..n`; find missing/duplicate | Swap each value to its home index (`nums[i]` → index `nums[i]-1`). The first index where `nums[i] != i+1` is the answer. O(n) / O(1). | 268, 287, 41 |
| **Two heaps** | Running median / balance a stream around the middle | Max-heap for the lower half, min-heap for the upper half; keep sizes within 1. Median = the top(s). | 295 |
| **Quickselect** | Kth largest/smallest without a full sort | Partition like quicksort, but recurse into **one** side only. O(n) average, O(1) extra. | 215 |

## Grading your own attempt

| You... | Comfort |
|--------|---------|
| solved from a blank page, right complexity, no hints, no second-guessing | 🟢 Clean |
| got it but needed a nudge / peeked / weren't sure mid-way | 🟡 Shaky |
| couldn't recall the approach, had to look it up | 🔴 Blank |
