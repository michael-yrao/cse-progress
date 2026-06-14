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