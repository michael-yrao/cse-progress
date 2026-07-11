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

## 🟡 146. LRU Cache — Jul 7, 2026
**Sticking point**: Recalled the whole design cold (hashmap + DLL with two sentinels, get-promotes, evict `tail.prev` + `del map[node.key]`) — big jump from the Jul 4 🔴. Friction was peripheral: needed the type-checker error explained (untyped param = `Any` = silent; annotating `delete(node: ListNode)` surfaced the unprovable `.prev is not None` invariant → resolve with `assert`).

## 🟡 1448. Count Good Nodes in Binary Tree — Jul 10, 2026
**Sticking point**: Conflated "not a good node" with "dead end" — combined base case `if not node or node.val < currentMax: return 0` pruned the whole subtree under any non-good node, missing good descendants below it (e.g. `3→1→5`: 5 is good but 1 isn't, so 1's `return 0` skipped 5). Fix: only null stops recursion; a non-good node counts 0 but still recurses. Goodness is per-node, not a traversal gate.

## 🟡 424. Longest Repeating Character Replacement — Jul 10, 2026
**Sticking point**: Had the sliding-window idea + the incremental `maxFreq` optimization, but botched three details: (1) shrink condition inverted — `maxFreq + k > r - l + 1` instead of `(r - l + 1) - maxFreq > k`, so `l` ran off the end (index error); (2) forgot `r += 1` on the outer loop; (3) answer used `maxFreq + k` instead of the window size `r - l + 1`. Window is *invalid* when `windowLen - maxFreq > k`; shrink then; answer is the max valid window length.

## 🔴 211. Design Add and Search Words — Jul 9, 2026
**Topic**: Trie + DFS backtracking (new; builds on 208)

### Where did I get stuck?
`addWord` was trivial (identical to 208 insert). `search` with the `.` wildcard blanked me — thought it needed "regex" and couldn't see how to structure the wildcard branch. Also had an index bug: recursed with `dfs(i+1, child)` (i = frame's start index, constant) instead of `dfs(j+1, child)` (j = live cursor) — re-consumed the wildcard position instead of advancing past it.

### Core Realization
It's not regex — it's a tree walk with a **fork at the wildcard**, and it's *both* iterative and recursive:
- **Loop = the forced path.** A concrete char has exactly one child to follow → plain loop, one node per char (just like 208 `search`).
- **Recursion = the fork.** A `.` could be *any* letter → try **every child**, each resuming the walk on the rest of the word (`j+1`). DFS: dive down child #1; if that whole branch fails, back out and try child #2. Succeed if *any* branch reaches a real word (`isWord`).
- One-liner: **the loop handles the letters you know; recursion handles the letters you have to guess.**

Index discipline: at a wildcard at position `j`, recurse on `j+1` (past the current char), NOT `i+1` (i is the frame's origin and only equals j when the wildcard is the frame's first char).

### Code Snippet
```python
def search(self, word):
    def dfs(j, node):
        cur = node
        for i in range(j, len(word)):
            c = word[i]
            if c == '.':
                for child in cur.children.values():
                    if dfs(i + 1, child):    # i is the live cursor here
                        return True
                return False
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return cur.isWord
    return dfs(0, self.root)
```
(Note: in this skeleton the loop var is `i` and start is `j` — the recurse must pass `i+1`, the live cursor. Whatever you name them, recurse on the *cursor*+1, not the *frame-start*+1.)

## 🟡 261. Graph Valid Tree (Union-Find) — Jul 9, 2026
**Sticking point**: Core UF (edges == n-1 guard + cycle check) was solid, but bolted on a node-coverage check (à la DFS's `len(visited) == n`) that UF doesn't need — the `n-1` guard + global cycle scan already prove connectivity, so the extra check caused issues. Coverage-verify belongs to single-source DFS, not UF.

## 🔴 105. Construct Binary Tree from Preorder and Inorder — Jul 8, 2026
**Topic**: Trees / divide & conquer (new)

### Where did I get stuck?
Blanked on how to reconstruct the tree. Two misconceptions blocked it: (1) reached for heap array-indexing (`left = 2n+1`, `right = 2n+2`) — irrelevant here; this builds a *pointer-based* tree of arbitrary shape, not a flat array. (2) Understood inorder's split but couldn't see how the `mid` from inorder maps onto slicing **preorder**.

### Core Realization
Two facts drive the whole thing:
- **Preorder gives the root:** layout is `[root, (whole left subtree), (whole right subtree)]` → `preorder[0]` is always the current root.
- **Inorder gives the split:** layout is `[(left subtree), root, (right subtree)]` → find the root's value in inorder at index `mid`; everything left of it is the left subtree, everything right is the right subtree.

`mid` = **count of left-subtree nodes**. That count is the bridge: an entire subtree is **contiguous** in preorder, so knowing the left subtree has `mid` nodes lets you carve preorder without knowing its internal shape. Skip 1 for the root, take the next `mid` for the left block, the rest is the right block. Same nodes, two orderings — inorder *counts* them, preorder *stores them contiguously*.

Slicing: inorder split skips the root (`[:mid]` / `[mid+1:]`); preorder split skips index 0 (`[1:1+mid]` / `[1+mid:]`). `1+mid` is the single boundary between left and right blocks.

### Code Snippet
```python
def build(preorder, inorder):
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])          # count of left-subtree nodes
    root.left  = build(preorder[1:1+mid], inorder[:mid])
    root.right = build(preorder[1+mid:],  inorder[mid+1:])
    return root
```
Optimization for later (not needed first pass): value→index dict for inorder + integer bounds instead of slicing → O(n) instead of O(n²).

## 🟡 19. Remove Nth Node From End (Recursion) — Jul 8, 2026
**Sticking point**: Postorder count-from-end logic was right, but removal-by-predecessor can't touch the head (head has no predecessor, and returning `postorder(head)` always hands back the same node) → `n == length` fails. Fix: sentinel `dummy = ListNode(0, head)`; recurse on dummy for its rewiring side-effects; `return dummy.next`. Rule: any "remove a node" problem where the head can go → use a dummy.

## 🟡 75. Sort Colors (Dutch Flag) — Jul 8, 2026
**Sticking point**: Three-way partition logic correct, but loop bound was `traversal < right` instead of `<= right` — the element sitting at `right` (where the next 2 lands) never gets processed, leaving the last position unsorted (e.g. `[2,0,1]` → `[1,0,2]`).

## 🟡 208. Implement Trie (Prefix Tree) — Jul 8, 2026
**Sticking point**: Recalled the two-field node (`map` + `isWord`) and all three walks, but the "node stores no char" model was still shaky — took in a vestigial `char` param out of old reflex, and needed the node-vs-edge visualization ("the char is the *edge label* = the dict key; a node's identity is its path, not a stored letter") to fully settle why the root can be "empty" yet have a `'c'` child.

## 🔴 208. Implement Trie (Prefix Tree) — Jul 6, 2026
**Topic**: Trie / prefix tree (first exposure — new)

### Where did I get stuck?
Couldn't start from a blank page. Had the right high-level model ("trie is a tree with an empty root sentinel") but the **node design was wrong**: reached for `TrieNode(val, children=[])` — a node that stores its own character plus a *list* of children. That framing made insert/search feel impossible to write.

### Core Realization
**The character lives in the path, not the node.** A node stores no `val` — the parent knows each child *by its character*, so `children` is a **dict keyed by char** (`char -> TrieNode`), giving O(1) "does this node have child `c`?" via `c in node.children`. A node needs exactly two fields: `children = {}` and `isEnd = False`. `isEnd` marks a **word boundary** — it's what lets `"app"` be a real word while `"ap"` (a mere waypoint on the path to `"apple"`) is not.

All three operations are the **same walk** from the root, char by char; only the ending differs:
- **insert**: create missing child nodes as you go, then set `cur.isEnd = True` at the end.
- **search**: return `False` on the first missing char; at the end return `cur.isEnd` (must be a complete inserted word).
- **startsWith**: identical walk, but at the end return `True` (path exists = prefix exists; `isEnd` irrelevant).

The `search` vs `startsWith` distinction (`return cur.isEnd` vs `return True`) is the whole reason both methods exist.

### Code Snippet
```python
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode  (char is implicit in the key)
        self.isEnd = False      # word boundary marker

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.isEnd = True

    def search(self, word):
        cur = self.root
        for c in word:
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return cur.isEnd        # exact word

    def startsWith(self, prefix):
        cur = self.root
        for c in prefix:
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return True             # prefix only
```

## 🟡 355. Design Twitter — Jul 6, 2026
**Sticking point**: Heap design and self-dedup fully recalled, but returned the size-10 min-heap drained ascending (oldest-first) — forgot the news feed wants newest-first, so needed the `result[::-1]` fix pointed out. Spec-detail miss, not an approach gap.

## 🟡 143. Reorder List — Jul 6, 2026
**Sticking point**: Concept solid (Floyd → reverse → merge), but factoring reverse into a helper lost the new-head return, and forgot to sever `slow.next = None` before reversing — leaving the middle node pointing into the reversed half, which closes a cycle after the merge.

## 🔴 146. LRU Cache — Jul 4, 2026
**Topic**: Design / hashmap + doubly linked list (new)

### Where did I get stuck?
Knew "move to most-recently-used on access, evict least-recently-used," but reached for a `deque` — whose `remove`/`in` are O(n), breaking the O(1) requirement. Needed the whole design walked through: why a doubly linked list, why two sentinels, and the get-must-promote subtlety.

### Core Realization
Two structures working together: **`cache: key -> Node`** for O(1) *find*, and a **doubly linked list with head+tail sentinels** for O(1) *move/evict*. The DLL exists purely so you can unlink a node from the middle in O(1) via its `prev`/`next` (a deque can't). Two dummy nodes turn every boundary into an interior case (no None checks). "Move to MRU" = `remove(node)` + `insert(node)`. **`get` must also promote** (read = use), else it's evict-least-recently-*inserted*, not *used*. On eviction, purge BOTH: `remove(tail.prev)` and `del cache[node.key]` — which is why `Node` stores `key`.

### Code Snippet
```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}                      # key -> Node
        self.head, self.tail = Node(-1,-1), Node(-1,-1)   # MRU, LRU sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def remove(self, node):                  # unlink (O(1), never None thanks to sentinels)
        node.prev.next, node.next.prev = node.next, node.prev

    def insert(self, node):                  # splice right after head (MRU)
        nxt = self.head.next
        self.head.next = node; node.prev = self.head
        node.next = nxt; nxt.prev = node

    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]
        self.remove(node); self.insert(node)   # promote
        return node.val

    def put(self, key, value):
        if key in self.cache:
            self.remove(self.cache[key])
        node = Node(key, value)
        self.insert(node); self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self.remove(lru); del self.cache[lru.key]
```

---

## 🔴 496. Next Greater Element I — Jul 4, 2026
**Topic**: Stack / monotonic stack (new — first monotonic stack ever)

### Where did I get stuck?
Didn't understand the problem *or* the technique on first read. Needed the whole thing explained plain-English.

### Core Realization
Two ideas. (1) Precompute the next-greater for **every** element of `nums2` into a map in one pass, then answer each `nums1` element with an O(1) lookup. (2) The one-pass is a **monotonic stack**: the stack holds indices of elements still *waiting* for a bigger number to their right, kept in decreasing value order. When a new value `x` arrives, it resolves everyone on the stack shorter than it (they've found their next-greater = `x`) — pop them and record; then push `x`. Anything left at the end has no next-greater → -1. "Line of people waiting for a taller person to walk by."

### Code Snippet
```python
def nextGreaterElement(self, nums1, nums2):
    nge = {}
    stack = []                       # values still waiting (indices not needed here)
    for x in nums2:
        while stack and stack[-1] < x:
            nge[stack.pop()] = x     # x is the popped value's next-greater
        stack.append(x)
    for leftover in stack:
        nge[leftover] = -1
    return [nge[v] for v in nums1]
```
(Values can be stored directly here since nums2 has distinct values and we don't need distances; the index/distance form is for problems like Daily Temperatures.)

---

## 🟡 206. Reverse Linked List (Recursion) — Jul 3, 2026
**Sticking point**: The returned `newHead` felt pointless because no frame *uses* it. Key reframe: return value and work are separate jobs. The rewiring (`head.next.next = head; head.next = None`) is a side effect each frame does with its own `head`/`head.next`; `newHead` is just the answer (original tail = new head), found once at the base case and *relayed* up the stack unchanged so the top-level caller gets it. It's a pass-through payload, not logic.

---

## 🟡 121. Best Time to Buy and Sell Stock — Jul 3, 2026
**Sticking point**: Not intuitive as "two pointer." Better frame: running-minimum one-pass — carry cheapest-price-so-far, and at each day ask "profit if I sold today = price − minSoFar." Best sell at day i depends only on the min before i (same family as Kadane's running-aggregate, not nested pair comparison).

---

## 🔴 138. Copy List with Random Pointer — Jul 3, 2026
**Topic**: Linked List / hash map (new problem)

### Where did I get stuck?
Fully stumped on approach — the `random` pointer can point to a node that hasn't been copied yet (forward reference), so wiring it up in a single front-to-back pass is impossible. Didn't see the fix without hints.

### Core Realization
Decouple "create the nodes" from "wire the pointers" using a dict `{original → copy}`. **Pass 1:** create every copy node (value only), store `original → copy`. **Pass 2:** walk again and set `copy.next = dict[orig.next]` and `copy.random = dict[orig.random]` — every target copy already exists, so the forward reference is gone. Seed `{None: None}` (or guard) so null pointers don't KeyError; return `dict[head]`. O(n) time, O(n) space. Slicker O(1) interleaving variant exists — learn later.

### Code Snippet
```python
def copyRandomList(self, head):
    if not head:
        return None
    old_to_new = {None: None}
    cur = head
    while cur:                      # pass 1: create copies
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                      # pass 2: wire next + random
        copy = old_to_new[cur]
        copy.next = old_to_new[cur.next]
        copy.random = old_to_new[cur.random]
        cur = cur.next
    return old_to_new[head]
```

---

## 🟡 74. Search a 2D Matrix — Jul 3, 2026
**Sticking point**: Mixed up the two binary-search flavors. Row search is max-boundary (keeps candidate with `l = m`) so it needs the **ceil** midpoint `(l + r + 1) // 2` — floor stalls into an infinite loop when the window is 2 wide. Also had rows/cols swapped in the bounds, and used `while l < r` on the exact-match column search (needs `<=` or it skips the last cell). Precedence note: must be `(l + r + 1) // 2`, not `l + r + 1 // 2`.

---

## 🟡 875. Koko Eating Bananas — Jul 3, 2026
**Sticking point**: Binary search was correct (min-boundary), but `canFinish` counted hours per pile with a `while bananas > 0: bananas -= m` loop → O(bananas/m) per pile, TLE. Fix: hours per pile = ceil division `(bananas + m - 1) // m` in O(1) (partial pile still costs a full hour since Koko can't switch mid-hour).

---

## 🟡 271. Encode and Decode Strings (retry) — Jul 3, 2026
**Sticking point**: Two silly slips on the reconstruction — encode built `<len>#` but forgot to append the string itself; decode wrote `while j != '#'` (comparing the index int) instead of `while s[j] != '#'`. Framing logic itself was solid. Out of Blank.

---

## 🟡 141. Linked List Cycle — Jul 1, 2026
**Sticking point**: Fuzzy on the loop guard for Floyd's. `while fast and fast.next` is required because `fast = fast.next.next` dereferences two levels, so both must be non-null before the jump. Fast reaching null = finite list terminated = no cycle (a cyclic list never ends, so fast can never fall off); that's why hitting null returns False.

---

## 🟡 424. Longest Repeating Character Replacement — Jul 2, 2026
**Sticking point**: Keyed the freq map by index (`freqMap[r]`/`freqMap[l]`) instead of character (`freqMap[s[r]]`/`freqMap[s[l]]`) — so every count was 1 and mostFreq was meaningless. The O(26n) `max(freqMap.values())` version worked once fixed; the O(n) "let maxFreq go stale (never decrement it)" optimization is still not intuitive — revisit.

---

## 🟡 567. Permutation in String — Jul 2, 2026
**Sticking point**: Pre-filled the window freq array with the counts of the *entire* s2 instead of building it incrementally — a sliding window array must only ever hold what's between l and r, so add s2[r] as r advances and remove s2[l] when the window exceeds len(s1). No prefill of the whole string.

---

## 🟡 323. Number of Connected Components (DFS) — Jul 2, 2026
**Sticking point**: Inside the recursive `dfs`, used the outer loop variable `i` instead of the parameter `node` (`visited.add(i)`, `adjMap[i]`) — closure capture bug that caused infinite recursion; also double-marked (outer loop + dfs) which short-circuited the count. Rule: recursive helpers act on the parameter passed in, and pick one owner for marking visited.

---

## 🟡 98. Validate Binary Search Tree (retry) — Jul 2, 2026
**Sticking point**: Named the inorder idea but didn't implement it as a true inorder initially — the running-`prevValue` check has to sit *between* the left recursion and the right recursion (left → compare current → right), not before/after both. Once the compare was placed mid-traversal it worked.

---

## 🔴 271. Encode and Decode Strings — Jul 1, 2026
**Topic**: Arrays / strings — message framing (new problem)

### Where did I get stuck?
Didn't see the core idea (needed the "what makes decoding unambiguous?" nudge), first reached for a non-ASCII sentinel delimiter (works in Python but fragile/dodges the point), and didn't arrive at the O(n) two-index decode without heavy guidance — first pass used `split('#')` per word, which is O(n²).

### Core Realization
This is a **length-prefix framing** problem (same technique as TCP/HTTP `Content-Length`, protobuf, netstrings). Encode each string as `<len>#<str>`; the decoder reads the length first, then grabs *exactly* that many chars — so the payload can contain any character, including `#`, because the decoder never scans inside the word for boundaries. Length framing is *out-of-band* (decoupled from content), which is why it beats any delimiter scheme. O(n) decode needs a cursor + short lookahead scan, NOT `split` (split touches the whole string → O(n²) in a loop).

### Code Snippet
```python
def encode(self, strs):
    out = ""
    for word in strs:
        out += str(len(word)) + '#' + word
    return out

def decode(self, s):
    result = []
    j = 0
    while j < len(s):
        i = j
        while s[i] != '#':      # scan only the length digits
            i += 1
        length = int(s[j:i])
        wordStart = i + 1
        wordEnd = wordStart + length
        result.append(s[wordStart:wordEnd])
        j = wordEnd             # jump past the whole record
    return result
```
Note: it's a cursor-parse, not true two-pointer (no invariant-driven pointer choice — just lookahead + jump).

---

## 🟡 621. Task Scheduler (retry) — Jul 1, 2026
**Sticking point**: Approach reconstructed correctly (window of n+1 + max-heap), but it's cognitively heavy to hold together and had a `for k,v in freqMap:` crash (must be `.items()`). Submitted successfully after fix.

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
