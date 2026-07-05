# Patterns Index

Reference notes for DSA patterns, split by **what kind of thing** each one is:

- **`data-structures/`** — the *structure* itself: what it is, its operations, and when to reach for it. Pick these when you know the shape of the data ("this is a linked-list problem," "I need disjoint sets").
- **`techniques/`** — an *approach / algorithmic pattern* applied to data. Pick these when you recognize the move ("this needs a sliding window," "nearest-greater → monotonic stack").
- **`intuition_cheatsheet.md`** — quick recognition table + single-trick techniques (Boyer-Moore, cyclic sort, two heaps, quickselect). Start here when you're not sure what pattern a problem wants.

Every doc follows the same shape: **recognition signal → template → key facts → practice ladder (NC150 flagged) → common pitfalls.**

## Data Structures (`data-structures/`)

| Doc | Use when |
|-----|----------|
| [linked_list](data-structures/linked_list.md) | Pointer rewiring, dummy nodes, in-place list surgery |
| [tree](data-structures/tree.md) | Binary tree/BST traversal, DFS pre/post-order framing |
| [union_find](data-structures/union_find.md) | Connectivity / grouping / cycle detection in undirected graphs |

## Techniques (`techniques/`)

| Doc | Recognition signal |
|-----|--------------------|
| [two_pointer](techniques/two_pointer.md) | Converging/opposite-end or same-direction pointer moves driven by an invariant |
| [fast_slow_pointer](techniques/fast_slow_pointer.md) | Cycle detection, middle of list, find-the-duplicate |
| [sliding_window](techniques/sliding_window.md) | Contiguous subarray/substring with a constraint |
| [binary_search](techniques/binary_search.md) | Sorted data, or "smallest x that works" (min/max boundary) |
| [monotonic_stack](techniques/monotonic_stack.md) | Nearest greater/smaller to one side (+ monotonic-deque for moving-window max/min) |
| [prefix_sum](techniques/prefix_sum.md) | Range sums, "subarrays summing to k" (+ hashmap) |
| [backtracking](techniques/backtracking.md) | Enumerate all subsets/permutations/combinations; choose-explore-unchoose |
| [recursion](techniques/recursion.md) | Self-similar subproblems; trust-the-recursion framing |
| [memoization](techniques/memoization.md) | Overlapping subproblems → cache results (top-down DP) |
| [topological_sort](techniques/topological_sort.md) | Ordering with dependencies on a DAG (Kahn's / DFS) |

> Boundary note: a few live between the two (a monotonic stack *uses* a stack; union-find *is* a structure but *is applied like* a technique). They're filed by how you **reach for them** — you think "monotonic stack technique," but "union-find, the structure." When in doubt, the cheatsheet links both.
