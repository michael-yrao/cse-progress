# Stuck Log

## 1. LeetCode 19 - Remove Nth Node From End of List (Recursive)
* **Date**: May 18, 2026
* **Topic(s)**: Recursion / Call Stack Traversal

### a. Where did I get stuck?
* **Visualizing backward counting**: I couldn't wrap my head around how recursion counts from the end of a singly linked list without a `prev` pointer.

### b. The Core Realization
* The computer's call stack acts as a natural memory engine. By placing the `counter += 1` statement *after* the recursive function call, the code executes in exact reverse order (backwards from the tail) as the function execution contexts pop off the stack. 

### c. Code Snippet to Remember
```python
# The recursive reverse execution pattern:
head.next = removeFromEnd(node.next) # 1. Go all the way to the end first
counter += 1             # 2. This increments from the back on the way up
```

Refer to the drawing in the surface for traces

---

## 2. ❌ LeetCode 20 - Valid Parentheses (Intuitive Set Filter)
* **Date**: May 19, 2026
* **Topic(s)**: Stacks / Set-Membership Optimization

### a. Where did I get stuck?
* **Hidden Inner Loops**: My initial design used `if char in openToCloseMap.values()`. This introduced a hidden sequential lookup time because Python must linearly scan through a dictionary's values on every single character iteration.

### b. The Core Realization
* Readability and intuition are paramount. To keep my intuitive, forward-facing map configuration (`openToCloseMap = {'(': ')'}`), I can decouple the values into an independent, pre-calculated Python Set (`closing_set = set(openToCloseMap.values())`). Because Sets leverage internal hash tables, checking `if char in closing_set` runs in pure \(O(1)\) constant time. This keeps my logic deeply readable to me while preserving mathematically flawless execution speed.

### c. Code Snippet to Remember
```python
openToCloseMap = {'(': ')', '{': '}', '[': ']'}
closing_set = set(openToCloseMap.values()) # Pre-calculate once for O(1) searches

for char in s:
    if char in closing_set:         # Pure O(1) Set Lookup
        if not stack or openToCloseMap[stack[-1]] != char: return False
        stack.pop()
    elif char in openToCloseMap:    # Pure O(1) Key Lookup
        stack.append(char)
```
## 3. ❌ LeetCode 21 - Merge Two Sorted Lists (Recursive)
* **Date**: May 20, 2026
* **Topic(s)**: Recursion / Linked List Forward Traversal

### 1. Where did I get stuck?
* **Visualizing Return Values**: I struggled to understand why we need to explicitly run `return list1` or `return list2` inside the decision blocks, rather than returning a single final head at the end.

### 2. The Core Realization
* In forward-traversal recursion, each stack frame acts like an isolated construction worker. Whichever node wins the current comparison gets its `.next` pointer glued to the result of the next recursive call. Once that connection is secure, the frame's job is complete, so it returns itself (`return list1/list2`) because it is the head of that newly verified sorted pipeline segment.

### 3. Code Snippet to Remember
```python
if list1.val < list2.val:
    list1.next = self.mergeTwoLists(list1.next, list2)
    return list1  # Job complete on list1, hand it backward
else:
    list2.next = self.mergeTwoLists(list1, list2.next)
    return list2  # Job complete on list2, hand it backward
```

---

## 4. ✅ LeetCode 200 - Number of Islands (DFS)
* **Date**: May 31, 2026
* **Topic(s)**: Graph Traversal / DFS / Base Case Handling

### 1. Where did I get stuck?
* **DFS base-case misses**: I didn't properly stop before visiting water or going out of bounds, which made the recursion logic much harder to follow.

### 2. The Core Realization
* The DFS helper must short-circuit immediately for invalid positions and for `0` cells. The correct ordering is:
  - if row or col is out of bounds, return
  - if grid[row][col] is `0`, return
  - mark the cell visited
  - recurse on all four neighbors

### 3. Code Snippet to Remember
```python
def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if grid[r][c] == '0':
        return
    if visited:
        return
    grid[r][c] = '0'
    dfs(r+1, c)
    dfs(r-1, c)
    dfs(r, c+1)
    dfs(r, c-1)
```

---