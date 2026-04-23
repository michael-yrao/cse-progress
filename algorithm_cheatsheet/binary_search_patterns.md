# Binary Search Patterns

## Quick Reference

| Pattern | Loop | Midpoint | Use Case |
|---------|------|----------|----------|
| **Exact Value** | `while l <= r` | `(l + r) // 2` | Find exact match |
| **Min Boundary** | `while l < r` | `(l + r) // 2` | Find first true |
| **Max Boundary** | `while l < r` | `(l + r + 1) // 2` | Find last true |

---

## 1. Exact Value Search

**Use Case**: Find an exact target value in the array

| Component | Value |
|-----------|-------|
| **Loop** | `while l <= r` |
| **Midpoint** | `mid = (l + r) // 2` |
| **Return** | `l` at exit or when found |

**Update Rules**:
```python
if matrix[mid] == target:
    return mid  # Found exact match
elif matrix[mid] > target:
    r = mid - 1  # Search left
else:
    l = mid + 1  # Search right
```

**Example**: [LeetCode 704 - Binary Search](https://leetcode.com/problems/binary-search/)

---

## 2. Minimum Boundary Search (First True Position)

**Use Case**: Find the leftmost position where a monotonic predicate is true

| Component | Value |
|-----------|-------|
| **Loop** | `while l < r` |
| **Midpoint** | `mid = (l + r) // 2` (left-biased) |
| **Return** | `l` at loop exit |

**Update Rules**:
```python
if is_valid(mid):  # Predicate is true
    r = mid  # Keep mid as candidate, search left
else:  # Predicate is false
    l = mid + 1  # Move past mid, search right
```

**Example**: [LeetCode 34 - Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

---

## 3. Maximum Boundary Search (Last True Position)

**Use Case**: Find the rightmost position where a monotonic predicate is true

| Component | Value |
|-----------|-------|
| **Loop** | `while l < r` |
| **Midpoint** | `mid = (l + r + 1) // 2` (right-biased) |
| **Return** | `l` at loop exit |

**Update Rules**:
```python
if is_valid(mid):  # Predicate is true
    l = mid  # Keep mid as candidate, search right
else:  # Predicate is false
    r = mid - 1  # Move before mid, search left
```

**Example**: [LeetCode 74 - Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

---

## Key Insights

### Why Bias Matters

- **Left-biased** `mid = (l + r) // 2`: Naturally tends toward the lower half when interval is even
  - Use with `r = mid` to find the **first true** position
  - Prevents infinite loops when `mid == l`

- **Right-biased** `mid = (l + r + 1) // 2`: Naturally tends toward the upper half when interval is even
  - Use with `l = mid` to find the **last true** position
  - Prevents infinite loops when `mid == r`

### Mental Model

| Scenario | Pattern | Midpoint | When Valid | When Invalid |
|----------|---------|----------|-----------|--------------|
| Exact match | `l <= r` | `(l+r)//2` | Return/Found | Move away from mid |
| First true | `l < r` | `(l+r)//2` | `r = mid` | `l = mid+1` |
| Last true | `l < r` | `(l+r+1)//2` | `l = mid` | `r = mid-1` |

The bias ensures the loop converges to the correct boundary **without getting stuck**.