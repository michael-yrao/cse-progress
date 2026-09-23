# Top-Down Memoization Patterns

## When to reach for it

A recursive search re-solves the same sub-state many times — cache the answer per state so each state is computed once, turning exponential branching into polynomial work.

- Overlapping subproblems / "min/max/count ways" with optimal substructure
- Subproblem inputs match exactly regardless of branch path
- Space coordinates are identical but resource budgets shift

## Picking feature

Overlapping subproblems with optimal substructure: the same (index, budget, …) state recurs, and the whole answer is built from the answers to parts. If states never repeat, it is plain backtracking.

- **not backtracking** — every candidate must be LISTED, not counted or optimized — a cache cannot shrink an output that is itself exponential
- **not sliding-window** — the question is about a CONTIGUOUS subarray — that is a window, not a subsequence

## Quick Reference


| Pattern | Key State Configuration | Cache Storage Type | Use Case |
|---------|-------------------------|--------------------|----------|
| **State Snapshot** | Unique tuple `(var1, var2)` | `dict` value mapping | Traditional overlapping boolean calculations |
| **Pruning Boundaries** | Vector dimensions `(l, r)` | `dict` resource value mapping | Truncating tracks that fail metric comparisons |

---

## Template: State Snapshot Memoization

*When:* Caching multi-variable combinations to completely skip computing previously encountered paths.

**Use Case**: Caching multi-variable combinations to completely skip computing previously encountered paths.


| Component | Value |
|-----------|-------|
| **Key Assembly** | `state = (l, r, skips_remaining)` |
| **Cache Check** | `if state in memo: return memo[state]` |
| **Cache Write** | `memo[state] = branch_a or branch_b` |

**Implementation**:
```python
def valid_palindrome_snapshot(s: str, skip: int) -> bool:
    memo = {}

    def backtrack(l: int, r: int, skips_remaining: int) -> bool:
        state = (l, r, skips_remaining)  # Snapshot of current context status
        if state in memo: return memo[state]
        if skips_remaining < 0: return False
        
        while l < r:
            if s[l] == s[r]:
                l, r = l + 1, r - 1
            else:
                memo[state] = (backtrack(l + 1, r, skips_remaining - 1) or 
                               backtrack(l, r - 1, skips_remaining - 1))
                return memo[state]
        return True
    return backtrack(0, len(s) - 1, skip)
```
Complexity: O(n² · k) time · O(n² · k) space — each (l, r, skips) triple is solved once and cached; the memo can hold every triple

**Example**: [LeetCode 680 - Valid Palindrome II (Extended Variant)](https://leetcode.com)

---

## Template: Pruning Boundaries Memoization

*When:* Optimizing multi-dimensional space bounds by tracking and comparing resource variables.

**Use Case**: Optimizing multi-dimensional space bounds by tracking and comparing resource variables.


| Component | Value |
|-----------|-------|
| **Key Assembly** | `(l, r)` exclusively |
| **Prune Rule** | `if memo[(l, r)] >= current_resource: return False` |
| **Cache Write** | `memo[(l, r)] = current_resource` |

**Implementation**:
```python
def valid_palindrome_pruned(s: str, skip: int) -> bool:
    memo = {}  # Maps (l, r) -> max skips remaining achieved here

    def backtrack(l: int, r: int, skips_remaining: int) -> bool:
        if skips_remaining < 0: return False
        # Prune: Exit immediately if a past path reached here with more resources
        if (l, r) in memo and memo[(l, r)] >= skips_remaining:
            return False
            
        while l < r:
            if s[l] == s[r]:
                l, r = l + 1, r - 1
            else:
                memo[(l, r)] = skips_remaining  # Record resource benchmark
                return (backtrack(l + 1, r, skips_remaining - 1) or 
                        backtrack(l, r - 1, skips_remaining - 1))
        return True
    return backtrack(0, len(s) - 1, skip)
```
Complexity: O(n²) time · O(n²) space — the memo is keyed by (l, r) only — a revisit with no more budget than before is cut off, so each pair expands at most once per improving budget

**Example**: [LeetCode 680 - Valid Palindrome II (Pruned Variant)](https://leetcode.com)

---

## Understanding Deterministic Overlapping States

### What is it?
**Deterministic overlapping states** represent isolated subproblems within a recursion tree that arrive at identical inputs across completely different choice pathways.

### Why it matters
Failing to capture overlapping configurations leaves the algorithm bounded by exponential timelines, causing your code to trigger time-limit errors on massive search depths.

### Real Examples

#### Example 1: Climb Stairs (Linear Fibonacci Memoization)
```python
def climb_stairs(n: int) -> int:
    memo = {}
    def helper(steps):
        if steps in memo: return memo[steps]
        if steps == 1: return 1
        if steps == 2: return 2
        
        memo[steps] = helper(steps - 1) + helper(steps - 2)
        return memo[steps]
    return helper(n)
```

#### Example 2: House Robber (Maximum Value Selection Memoization)
```python
def rob(nums: list[int]) -> int:
    memo = {}
    def dfs(i):
        if i in memo: return memo[i]
        if i >= len(nums): return 0
        
        # Choice: Rob house and skip next, or skip current house entirely
        memo[i] = max(nums[i] + dfs(i + 2), dfs(i + 1))
        return memo[i]
    return dfs(0)
```

### Pattern Recognition


| Context | How to Identify |
|---------|-----------------|
| Subproblem inputs match exactly regardless of branch path | Apply **Snapshot Key Tuples** mapping parameters directly to true outcomes |
| Space coordinates are identical but resource budgets shift | Apply **Resource Pruning Comparison Tables** inside structural boundary checks |

---

## Key Insights

### The Cache Key Invariant Rule
- **The Value Mutation Trap**: Never put a mutable object like a raw Python `list` into your state dictionary parameters. Keys must be strictly hashable immutable items like integers, strings, or tuple configurations.

### Mental Model


| Strategy | First Time Encountering State | Subsequent Visits to State |
|----------|-------------------------------|----------------------------|
| **Un-memoized Search** | Runs deep subproblem analysis to completion | Re-runs the exact same deep analysis from scratch |
| **Memoized Search** | Runs deep analysis and saves value to `dict` | Hits the `dict` and returns the value instantly in \(O(1)\) |

## Practice

- LC 680 — Valid Palindrome II

## Common pitfalls

- Wrong base cases — the most common cause of off-by-one errors in DP
- Under-specified state — if two different situations share the same key, the memo returns wrong answers
- Confusing subsequence (DP, non-contiguous) with subarray (sliding window, contiguous)
- Memoizing on a key that omits a variable the answer depends on (e.g. caching (l, r) when the skip budget matters) — the pruned form is only correct because it stores the BEST budget seen
