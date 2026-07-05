# Top-Down Memoization Patterns

## Quick Reference


| Pattern | Key State Configuration | Cache Storage Type | Use Case |
|---------|-------------------------|--------------------|----------|
| **State Snapshot** | Unique tuple `(var1, var2)` | `dict` value mapping | Traditional overlapping boolean calculations |
| **Pruning Boundaries** | Vector dimensions `(l, r)` | `dict` resource value mapping | Truncating tracks that fail metric comparisons |

---

## 1. State Snapshot Memoization

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

**Example**: [LeetCode 680 - Valid Palindrome II (Extended Variant)](https://leetcode.com)

---

## 2. Pruning Boundaries Memoization

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
