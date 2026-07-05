# Intuition Cheatsheet

## Quick Reference

### General Techniques

| Pattern | When to use | Why it helps |
|--------|-------------|--------------|
| Sorting | Count values above/below threshold | Turns threshold checks into efficient range counts |
| Threshold search (binary search) | Find first valid item | Efficiently locates the boundary in sorted data |
| Two pointers | Relative positions or sliding window | Maintain structure with `l,r` without nested loops |

### Data Structure Specific

| Pattern | When to use | Why it helps |
|--------|-------------|--------------|
| DFS postorder (trees) | Parent depends on children | Combine child results when unwinding recursion |
| DFS preorder (trees) | Need carry-down state | Process node before exploring subtree |
| Dummy node (linked lists) | Head may change | Makes insert/delete uniform by adding sentinel |

### Single-trick techniques (recall these by name)

Each is one clever idea, not a broad pattern — worth memorizing the trigger and the trick.

| Technique | Trigger | The trick | Problems |
|--------|---------|-----------|----------|
| **Boyer-Moore voting** | Find the majority element (> n/2, or > n/3) | Keep a `candidate` + `count`; ++ on match, -- on mismatch, swap candidate at 0. Majority survives cancellation. For > n/3, track **two** candidates. Re-verify at the end. | 169, 229 |
| **Cyclic sort** | Array holds numbers in range `1..n`; find missing/duplicate | Place each value at its "home" index (`nums[i]` → index `nums[i]-1`) by swapping. Then the first index where `nums[i] != i+1` reveals the answer. O(n)/O(1). | 268, 287, 41 |
| **Two heaps** | Running median / balance a stream around the middle | Max-heap for the lower half, min-heap for the upper half; keep sizes within 1. Median = top(s). | 295 |
| **Quickselect** | Kth largest/smallest, no full sort needed | Partition like quicksort but recurse into **one** side only. O(n) average, O(1) extra. | 215 |

---

## Can I sort?

### How to spot sorting

| Signal | Meaning |
|--------|---------|
| Answer is a count | Sort can turn checks into suffix counts |
| Order does not matter | Values can be reordered freely |
| Condition is monotonic | Validity holds for all later elements |
| Query asks for first valid item | Binary search fits |
| Brute force is O(n^2) or worse| Can't hurt to try sorting |