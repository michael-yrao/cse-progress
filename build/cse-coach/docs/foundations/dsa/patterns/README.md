# Patterns

Two ways in, one source of truth:

- **`techniques/`** — the actual content. Each file is **one atomic technique**: recognition signal → template → key facts → practice ladder (NC150 flagged) → pitfalls. This is where you learn the move.
- **`data-structures/`** — **hub pages**, not content. Each says "for this kind of data, here are the techniques you reach for," linking into `techniques/`. Use these when you know the *shape* of the data but not the move.
- **`intuition_cheatsheet.md`** — recognition tables + single-trick techniques (Boyer-Moore, cyclic sort, two heaps, quickselect). Start here when you don't know what a problem wants.
- **[`../fundamentals/big_o.md`](../fundamentals/big_o.md)** — time/space complexity of every technique + data structure here, in one table.

Rule of thumb: **know the move → open a technique. Know the shape → open a hub. Know neither → cheatsheet.** Techniques are never duplicated; hubs only link.

## By data structure (the "shape" lens)

| Hub | Techniques it points to |
|-----|-------------------------|
| [linked_list](data-structures/linked_list.md) | dummy_node · fast_slow_pointer · in_place_reversal · recursion |
| [tree](data-structures/tree.md) | tree_dfs · tree_bfs · recursion · memoization |
| [graph](data-structures/graph.md) | union_find · topological_sort · BFS/DFS traversal |
| [array_string](data-structures/array_string.md) | two_pointer · sliding_window · prefix_sum · binary_search · monotonic_stack |
| [stack_queue](data-structures/stack_queue.md) | monotonic_stack · monotonic_deque · plain stack · BFS queue |

## By technique (the "move" lens — A→Z)

| Technique | One-line trigger |
|-----------|------------------|
| [backtracking](techniques/backtracking.md) | Enumerate subsets/permutations/combinations; choose-explore-unchoose |
| [binary_search](techniques/binary_search.md) | Sorted data, or "smallest x that works" (min/max boundary) |
| [dummy_node](techniques/dummy_node.md) | Linked-list head may change; building/merging a list |
| [fast_slow_pointer](techniques/fast_slow_pointer.md) | Cycle detection, middle of list, find-the-duplicate |
| [in_place_reversal](techniques/in_place_reversal.md) | Reverse a list/sublist by rewiring `next` |
| [memoization](techniques/memoization.md) | Overlapping subproblems → cache (top-down DP) |
| [monotonic_stack](techniques/monotonic_stack.md) | Nearest greater/smaller (+ deque for moving-window max/min) |
| [prefix_sum](techniques/prefix_sum.md) | Range sums; "subarrays summing to k" (+ hashmap) |
| [recursion](techniques/recursion.md) | Self-similar subproblems; trust-the-recursion |
| [sliding_window](techniques/sliding_window.md) | Contiguous subarray/substring with a constraint |
| [topological_sort](techniques/topological_sort.md) | Ordering with dependencies on a DAG |
| [tree_bfs](techniques/tree_bfs.md) | Level order, min depth, side views |
| [tree_dfs](techniques/tree_dfs.md) | Pre/in/post traversal; property from children |
| [two_pointer](techniques/two_pointer.md) | Converging or same-direction pointers driven by an invariant |
| [union_find](techniques/union_find.md) | Connectivity / grouping / undirected cycle detection |
