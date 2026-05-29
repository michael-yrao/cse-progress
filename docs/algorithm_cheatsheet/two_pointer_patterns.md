# Two Pointers Patterns

## Quick Reference


| Pattern | Initial Pointer Setup | Pointer Movement | Use Case |
|---------|-----------------------|------------------|----------|
| **Opposite Ends** | `l = 0`, `r = len(arr) - 1` | `l += 1` and/or `r -= 1` | Sorted arrays, searching pairs, checking palindromes |
| **Fast & Slow** | `slow = 0`, `fast = 0` | `slow += 1`, `fast += 2` | Linked lists, cycle detection, finding midpoints |
| **Separation** | `i = 0`, `j = 0` | `j += 1`, `i` moves conditionally | In-place partitioning, removing duplicates |

---

## 1. Opposite Ends Pattern

**Use Case**: Finding pairs or checking symmetries in sorted structural constraints.


| Component | Value |
|-----------|-------|
| **Loop** | `while l < r` |
| **Key Check** | `current_sum = arr[l] + arr[r]` or `arr[l] == arr[r]` |
| **Return** | Indices `[l, r]` or a boolean validation |

**Implementation**:
```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    l, r = 0, len(numbers) - 1
    while l < r:
        cur = numbers[l] + numbers[r]
        if cur == target:
            return [l + 1, r + 1]  # Return 1-indexed positions
        elif cur < target:
            l += 1  # Sum too small, move left pointer rightward
        else:
            r -= 1  # Sum too large, move right pointer leftward
    return []
```

**Example**: [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com)

---

## 2. Fast & Slow Pointer Pattern (Tortoise and Hare)

**Use Case**: Detecting structural loops, intersections, or calculating dynamic midpoints.


| Component | Value |
|-----------|-------|
| **Loop** | `while fast and fast.next` |
| **Key Formula** | `slow = slow.next` and `fast = fast.next.next` |
| **Return** | `True` on collision, or node reference at exit |

**Implementation**:
```python
def has_cycle(head: Optional[ListNode]) -> bool:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next        # Moves 1 node at a time
        fast = fast.next.next   # Moves 2 nodes at a time
        if slow == fast:
            return True         # Fast caught up to slow (cycle detected)
    return False
```

**Example**: [LeetCode 141 - Linked List Cycle](https://leetcode.com)

---

## 3. Separation Pattern

**Use Case**: Modifying arrays in-place while separating elements based on content.


| Component | Value |
|-----------|-------|
| **Loop** | `for fast in range(len(arr))` |
| **Key Formula** | `arr[slow] = arr[fast]` inside condition |
| **Return** | `slow` index or modified bounds |

**Implementation**:
```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums: return 0
    slow = 0  # Points to the last unique element found
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1  # Move unique zone boundary
            nums[slow] = nums[fast]  # Overwrite with new item
    return slow + 1
```

**Example**: [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com)

---

## Understanding Target Adjustments

### What is it?
**Target adjustments** refer to altering pointer movement logic based on an dynamic aggregate metric (e.g., expanding or closing a boundaries gap).

### Why it matters
Choosing the wrong direction or increment rule will trigger out-of-bound errors, duplicate element traps, or absolute infinite loops.

### Real Examples

#### Example 1: Valid Palindrome II (Opposite Ends Expansion/Shrinking)
```python
def valid_palindrome(s: str) -> bool:
    def check(l, r):
        while l < r:
            if s[l] != s[r]: return False
            l, r = l + 1, r - 1
        return True
    
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            # Skip left OR skip right element
            return check(l + 1, r) or check(l, r - 1)
        l, r = l + 1, r - 1
    return True
```

#### Example 2: Move Zeroes (Separation Structure)
```python
def move_zeroes(nums: list[int]) -> None:
    slow = 0  # Tracks non-zero index position
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

### Pattern Recognition


| Context | How to Identify |
|---------|-----------------|
| Sorted Sequence Pairs | Use **Opposite Ends** to close structural gaps |
| Node Loop / Middle Node | Use **Fast & Slow** to identify geometric distances |
| In-place Content Removal | Use **Separation** to stream valid inputs forward |

---

## Key Insights

### Why Sub-problem Checking Matters

- **Skipping elements**: When structural paths diverge (e.g., mismatch in validation), breaking out into a isolated verification helper function allows evaluation of fallback states without destroying state histories.

### Mental Model


| Strategy | Speed Contrast | Key Invariant |
|----------|----------------|---------------|
| **Opposite Ends** | Same velocity, converging vectors | Everything outside `[l, r]` is fully processed |
| **Fast & Slow** | 2x structural variation divergence | Distance between pointers increases by 1 step every loop |
| **Separation** | Fast scans, slow acts as insertion line | Elements before `slow` match target criteria |
