# Stuck Log

Log every non-Clean result. Add new entries at the top. Format is proportional to severity:

**🔴 Blank** — full entry (conceptual gap worth documenting):
```
## 🔴 [Number]. [Title] — [Date]
**Topic**: ...
### Where did I get stuck?
### Core Realization
### Code Snippet
```

**🟡 Shaky** — one-liner (name the specific friction point only):
```
## 🟡 [Number]. [Title] — [Date]
**Sticking point**: one sentence describing exactly what tripped you up.
```

---

## 🟡 141. Linked List Cycle — Jul 1, 2026
**Sticking point**: Fuzzy on the loop guard for Floyd's. `while fast and fast.next` is required because `fast = fast.next.next` dereferences two levels, so both must be non-null before the jump. Fast reaching null = finite list terminated = no cycle (a cyclic list never ends, so fast can never fall off); that's why hitting null returns False.

---

## 🔴 621. Task Scheduler — Jun 30, 2026
**Topic**: Greedy / heap / frequency map (new problem)

### Where did I get stuck?
No idea how to start until we discussed. Once given "greedy + frequency map," the map + max-heap was reachable, but the real block was **how the cooldown `n` enters the algorithm** — didn't see that you process time in windows of `n+1` slots.

### Core Realization
The most frequent task is the bottleneck, so greedily schedule the highest-count tasks first. `n` is tracked *structurally*, not per-task: pop up to `n+1` tasks per cycle and hold them aside (so none can repeat until the cycle ends — that IS the cooldown), then push survivors back. `n+1` = one full repeating unit (the task + its `n`-slot gap = room for `n+1` distinct tasks). Two bugs to remember: (1) counts are stored negated in the max-heap, so re-add survivors when counter `< 0`, not `> 0`; (2) the final cycle must not count trailing idles — early-return when the heap empties and there are no leftovers.

### Code Snippet
```python
freqMap = Counter(tasks)
maxHeap = [(-v, k) for k, v in freqMap.items()]
heapq.heapify(maxHeap)
result = 0
while maxHeap:
    leftover = []
    for _ in range(n + 1):
        if maxHeap:
            cnt, task = heapq.heappop(maxHeap)
            cnt += 1                    # decrement (negated)
            result += 1
            if cnt < 0:
                leftover.append((cnt, task))
        else:
            if not leftover:            # nothing left → no trailing idles
                return result
            result += 1                 # idle
    for item in leftover:
        heapq.heappush(maxHeap, item)
return result
```

---

## 🟡 36. Valid Sudoku — Jun 30, 2026 (conceptual/no-code)
**Sticking point**: Over-complicated the box tracking with `row%3, col%3` — only the box id `(row//3, col//3)` is needed to key each sub-box's set; intra-box position is irrelevant to the duplicate check.

---

## 🟡 20. Valid Parentheses — Jun 30, 2026
**Sticking point**: Missed the empty-stack guard before popping — a closing bracket that arrives with an empty stack has nothing to match and must return False immediately (also catches the "more closers than openers" case).

---

## 🔴 98. Validate Binary Search Tree — Jun 30, 2026
**Topic**: Trees / inorder traversal

### Where did I get stuck?
First reached for the "build the inorder list, then check sorted + unique" approach — which is O(n log n) and had several bugs (appending `dfs()` return values, appending nodes not values, `set != list`, `list.sorted()`). Even after recognizing inorder-of-valid-BST is already sorted, the hard part was converting the "check as you traverse" idea into code: carrying a running `prevValue` / `callerValue` across the recursion and knowing the comparison happens *between* the left recursion and the right recursion.

### Core Realization
You don't need to store or sort anything. Do a normal inorder DFS, but keep a `nonlocal` running value of the last node visited (init `-inf`). At each node — *after* recursing left, *before* recursing right — assert `node.val > prevValue`, then update it. The left recursion must fully pass before you check the current node; a single failure short-circuits back up. This is the O(n), O(h)-space version.

### Code Snippet
```python
callerValue = -math.inf
def inorderDFS(node):
    nonlocal callerValue
    if not node:
        return True
    if not inorderDFS(node.left):   # left first
        return False
    if node.val <= callerValue:     # then check current
        return False
    callerValue = node.val
    return inorderDFS(node.right)    # then right
return inorderDFS(root)
```

---

## 🟡 19. Remove Nth Node From End of List (Iterative) — Jun 30, 2026
**Sticking point**: Built a dummy node but then traversed from `head`, making the head's predecessor (the dummy) unreachable — so removing the head (n == length) silently failed. Fix: start the walk from `dummy` with counter at -1.

---

## 🟡 42. Trapping Rain Water — Jun 29, 2026
**Sticking point**: Logic was right (leftMax/rightMax prefix arrays) — the bug was mixing init styles: pre-sized the walls with `[0]*n` but then used `.append()`, which appends past the zeros instead of assigning by index. Pick one: index-assign into a pre-sized list, or append into an empty one.

---

## 🟡 261. Graph Valid Tree (Union-Find) — Jun 29, 2026
**Sticking point**: Forgot the `len(edges) != n - 1` guard — Union-Find only catches cycles, not disconnected nodes; the edge count check is what rules out both at once.

---

## 🟡 229. Majority Element II — Jun 29, 2026
**Sticking point**: Can't use map values directly for the final count check — decrementing during the voting phase means the map is dirty; need a fresh recount over the original array to confirm candidates actually appear > n/3 times.

---

## 🟡 75. Sort Colors (Dutch Flag) — Jun 28, 2026
**Sticking point**: Missed that everything between `l` and `i` is always 1s — that invariant is why swapping from `l` never brings back a 2, and why `i` doesn't need to re-examine after a 0-swap.

---

## 🟡 19. Remove Nth Node From End of List (Recursion) — Jun 28, 2026
**Sticking point**: Needed to be walked through the dual-return-value problem — returning index alone drops the rewired node reference, so you need either a tuple or nonlocal counter.

---

## 🔴 229. Majority Element II — Jun 27, 2026
**Topic**: Boyer-Moore Majority Vote (generalized)
### Where did I get stuck?
Couldn't recall the approach — didn't know Boyer-Moore generalizes to 2 candidates for elements appearing > n/3 times.
### Core Realization
At most 2 elements can appear > n/3 times. Track 2 candidates + 2 counts. When a new element matches neither candidate and both counts > 0, decrement both counts (cancel out). After the pass, verify both candidates actually exceed n/3.
### Code Snippet
```python
c1, c2, cnt1, cnt2 = 0, 1, 0, 0
for n in nums:
    if n == c1: cnt1 += 1
    elif n == c2: cnt2 += 1
    elif cnt1 == 0: c1, cnt1 = n, 1
    elif cnt2 == 0: c2, cnt2 = n, 1
    else: cnt1 -= 1; cnt2 -= 1
```

---

## 🔴 128. Longest Consecutive Sequence — Jun 27, 2026
**Topic**: Hash Set / Sequence counting
### Where did I get stuck?
Tried a `lenMap` approach instead of the standard HashSet pattern.
### Core Realization
Only start counting forward from sequence starts (where `n-1` is not in the set). This avoids O(n²) by ensuring each sequence is walked exactly once.
### Code Snippet
```python
for n in nums:
    if n - 1 not in num_set:   # only start of a sequence
        length = 1
        while n + length in num_set:
            length += 1
        longest = max(longest, length)
```

---

## 🟡 355. Design Twitter — Jun 26, 2026
**Sticking point**: Naming — `following` Set was ambiguous about what it stores; should be `subscribedTo` or similar to make the relationship obvious.

---

## 🟡 27. Remove Element — Jun 26, 2026
**Sticking point**: Two pointer problems still hit-or-miss; confident in the pattern but not fully automatic yet.

---

## 🔴 80. Remove Duplicates from Sorted Array II — Jun 25, 2026
**Topic**: Two Pointers / Write Pointer
### Where did I get stuck?
Couldn't recall the approach — no clear mental model for the "at most k duplicates" pattern.
### Core Realization
Use a write pointer `k` starting at 2 (first two elements are always valid). For every element from index 2 onward, only copy it forward if `nums[i] != nums[k-2]`. Comparing to `k-2` (two spots behind the write pointer) is what enforces the "at most 2" constraint — if the element matches what's two spots back, a third duplicate would be written.
### Code Snippet
```python
def removeDuplicates(self, nums):
    k = 2
    for i in range(2, len(nums)):
        if nums[i] != nums[k-2]:
            nums[k] = nums[i]
            k += 1
    return k
```

---

## 🔴 543. Diameter of Binary Tree — Jun 24, 2026
**Topic**: Binary Tree / DFS / Postorder
### Where did I get stuck?
Confusing what `dfs` returns (height) vs what we're maximizing (diameter). Kept returning `1 + left + right` which counts nodes, not computing height.
### Core Realization
`dfs` serves two roles simultaneously:
- **Updates** a nonlocal `diameter = max(diameter, left + right)` — the candidate passing through this node
- **Returns** `1 + max(left, right)` — the height, so the parent can use it

The diameter is never "returned up" — it's tracked separately and updated at every node.
### Code Snippet
```python
def diameterOfBinaryTree(self, root):
    diameter = 0
    def dfs(node):
        nonlocal diameter
        if not node:
            return 0
        left = dfs(node.left)
        right = dfs(node.right)
        diameter = max(diameter, left + right)  # candidate at this node
        return 1 + max(left, right)             # height for parent
    dfs(root)
    return diameter
```

---

## 🔴 994. Rotting Oranges — Jun 6, 2026
**Topic**: Graph / Multi-Source BFS / Wavefront Batching
### Where did I get stuck?
Tracked minutes incorrectly — loop incremented time after processing a single node instead of treating all simultaneous infection origins as one generation wave.
### Core Realization
Multi-source BFS problems tracking dynamic steps require batch-wave processing. Take a snapshot of queue length at the start of each layer and loop exactly that many times before incrementing the time counter.
### Code Snippet
```python
while rottenQueue and freshOrangeCounter > 0:
    numberOfRottenOranges = len(rottenQueue)  # Freeze generation size
    for _ in range(numberOfRottenOranges):    # Loop exactly that many steps safely
        currentRow, currentCol = rottenQueue.popleft()
        # ... neighbor calculations and counters ...
    minute += 1  # Increment only when the entire generation wavefront finishes
```

---

## 🔴 133. Clone Graph (DFS) — Jun 4, 2026
**Topic**: Graph / DFS / Deep Copy
### Where did I get stuck?
Struggled to conceptualize how recursive deep copy separates node traversal from connection wiring, and how return values propagate up without erasing intermediate graph progress.
### Core Realization
Bottom-up recursion pattern. The execution stack creates nodes on the way down, then wires connections (.append()) on the way back up as frames unwind. The old-to-new hash map acts as both a visited set and a clone cache.
### Code Snippet
```python
if curr_node in old_to_new:
    return old_to_new[curr_node]  # Guardrail returns existing clone address

copy = Node(curr_node.val)
old_to_new[curr_node] = copy      # Map old address to new instance

for neighbor in curr_node.neighbors:
    copy.neighbors.append(dfs(neighbor))

return copy  # Triggers on EVERY node to hand its memory address backward
```

---

## 🔴 200. Number of Islands (BFS) — Jun 1, 2026
**Topic**: Graph / BFS / Matrix Grid
### Where did I get stuck?
Queue expanded exponentially causing MLE — was marking nodes visited after popping instead of immediately when appending.
### Core Realization
In BFS matrix traversal, mark a neighbor visited the moment it's pushed to the queue, not when it's popped. Otherwise adjacent nodes will push duplicate coordinates onto the queue.
### Code Snippet
```python
for rowTraversal, colTraversal in directions:
    neighborRow = row + rowTraversal
    neighborCol = col + colTraversal
    if (0 <= neighborRow < rows and 0 <= neighborCol < cols
            and (neighborRow, neighborCol) not in visited
            and grid[neighborRow][neighborCol] == '1'):
        visited.add((neighborRow, neighborCol))  # Mark immediately on push
        queue.append((neighborRow, neighborCol))
```

---

## 🔴 200. Number of Islands (DFS) — May 31, 2026
**Topic**: Graph Traversal / DFS / Base Case Handling
### Where did I get stuck?
Didn't properly short-circuit before visiting water or going out of bounds, making recursion logic hard to follow.
### Core Realization
The DFS helper must guard in this order: out of bounds → water cell → mark visited → recurse on 4 neighbors.
### Code Snippet
```python
def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if grid[r][c] == '0':
        return
    grid[r][c] = '0'
    dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
```

---

## 🔴 21. Merge Two Sorted Lists (Recursive) — May 20, 2026
**Topic**: Recursion / Linked List Forward Traversal
### Where did I get stuck?
Struggled to understand why each frame returns itself (`return list1/list2`) rather than a single final head at the end.
### Core Realization
In forward-traversal recursion each frame is an isolated worker. The winning node glues its `.next` to the result of the next recursive call, then returns itself — because it is now the head of that verified sorted segment.
### Code Snippet
```python
if list1.val < list2.val:
    list1.next = self.mergeTwoLists(list1.next, list2)
    return list1
else:
    list2.next = self.mergeTwoLists(list1, list2.next)
    return list2
```

---

## 🔴 20. Valid Parentheses — May 19, 2026
**Topic**: Stacks / Set-Membership Optimization
### Where did I get stuck?
Used `if char in openToCloseMap.values()` — hidden O(n) linear scan through dict values on every character.
### Core Realization
Decouple values into a pre-calculated Set for O(1) membership checks while keeping the readable forward map.
### Code Snippet
```python
openToCloseMap = {'(': ')', '{': '}', '[': ']'}
closing_set = set(openToCloseMap.values())

for char in s:
    if char in closing_set:
        if not stack or openToCloseMap[stack[-1]] != char: return False
        stack.pop()
    elif char in openToCloseMap:
        stack.append(char)
```

---

## 🔴 19. Remove Nth Node From End of List (Recursive) — May 18, 2026
**Topic**: Recursion / Call Stack Traversal
### Where did I get stuck?
Couldn't visualize how recursion counts from the end of a singly linked list without a `prev` pointer.
### Core Realization
The call stack is a natural memory engine. Placing `counter += 1` *after* the recursive call makes it execute in reverse order as frames pop — effectively counting backward from the tail.
### Code Snippet
```python
head.next = removeFromEnd(node.next)  # 1. Go all the way to the end first
counter += 1                          # 2. Increments from the back on the way up
```
