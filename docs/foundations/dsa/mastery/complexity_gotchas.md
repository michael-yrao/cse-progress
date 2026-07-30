# Complexity Gotchas — reference card + freebie ledger

Two jobs in one file: **teach** the recurring time/space traps (reread it like a Recall Card),
and **enforce** them (the ledger below *is* the per-problem freebie state).

## The rule (how complexity is enforced)

1. **Gate — every rep, no skip.** State **time AND space, each with an itemized why-clause** —
   *"O(1), one fixed 26-array"*, not a bare *"O(1)"*. Naming each contributor is what catches the
   miss. No rep is logged until this is answered (or explicitly passed).
2. **Per-problem freebie, then it counts.** Each miss on a problem → corrected + added to the ledger.
   No rating hit **until the freebie is spent**, then a further miss on the **same problem** → **caps
   that rep at 🟡**.
   - **Review problem: 1 freebie.**
   - **New problem (first-ever attempt): 2 freebies** — first exposure means learning the algorithm
     *and* its analysis at once, so it gets extra grace.

3. **Guide, don't just catch.** At complexity time, use the trigger→cue map below to *prompt* the right
   analysis (the cue, never the answer). On a **new problem** cue **proactively, before they answer**
   (teaching); on a **review** ask **cold** and cue the *why* only on a bare symbol or a miss (testing).

The gate and the correction always happen; the freebie only governs the *rating consequence*.

## Recurring categories (the transfer — this is the part to master)

Almost every miss so far is **space**, in one of these buckets. Time was consistently correct until
Jul 29 (235), where **time** was the wrong one and space was right — see the tree-height row.

| Category | Code trigger | Coach cue (fire this) | Right answer |
|---|---|---|---|
| **Fixed-alphabet array** | `[0]*26`, `[0]*128`, a bounded freq dict | *"that array — bounded by input, or by the alphabet?"* | **O(1)** — bounded by the alphabet, not `n` |
| **Recursion stack** | any `self.f(...)` / recursive helper | *"count the stack — how deep does it go?"* | **O(depth)** — O(n) for a list/skewed tree, O(log n) balanced |
| **2D structures** | grid `visited` set / heap of cells | *"your frontier — a line or an area?"* | **O(n²)** — the set/heap can hold nearly every cell |
| **Output counting** | returns a built list/structure | *"counting the output, or extra-only?"* | state the convention: "O(1) *extra*" vs "O(n) incl. output" |
| **Graph traversal (time)** | adjacency list + visit-each-node loop (BFS/DFS/topo) | *"each node once, each edge once — do those add or multiply?"* | **O(V + E)** — visits add, they don't multiply; O(V·E) would mean re-walking every edge per node |
| **Combination-holding structure** | a set/list accumulating *k-tuples* of elements (k-Sum results, pair lists, subsets) | *"you're storing combinations of k elements, not elements — how many are there?"* | **O(n^(k−1))** for k-Sum — pick k−1 freely, the last is forced. 3Sum O(n²), 4Sum O(n³). **Not O(n)** — `n` is a false anchor from the input's length |

| **Tree height (time *and* space)** | walking down one path of a tree — BST descent, insert, search | *"balanced, or is a chain also legal here?"* | **O(h)** — `O(log n)` **only if balanced**, `O(n)` degenerate. "It's a BST" does not give you balance; a chain like `1→2→3→4` (all right children) is a legal BST — *a sorted list in tree form*. Balance is an **assumption you state**, not a freebie |

**⚠ Consistency check — the two bounds must agree.** On a single downward walk, the recursion stack's
depth **is** the number of steps taken, so time and space are the *same* bound. Answering `O(log n)`
time with `O(n)` space (or vice versa) is self-contradictory and is the cheapest tell that a
balance assumption got applied to one and not the other. **Whenever a recursive walk's time and space
come out different, one of them is wrong** — check before you say it out loud.

**Space-contributors checklist (run before answering):**
(a) extra data structures — bounded by *input* or by a *constant alphabet*?
(b) recursion — how deep does the stack go?
(c) am I counting the output?

### Reference — heap costs, and the language to describe them (added Jul 26, 2026, via 1046)

Not a miss (the numbers were right), but the *phrasing* was: "the heap needs **reconstructing** each
iteration." It doesn't, and an interviewer will poke at that.

| Operation | Cost | Say this |
|---|---|---|
| `heappush` | O(log n) | appends at the bottom, **sifts up** — swaps with its parent while out of order |
| `heappop` | O(log n) | takes the root, moves the last element there, **sifts down** — swaps with the larger child |
| `heapify(list)` | **O(n)** | sifts down every node bottom-up; cost is each node's *height above the leaves* |
| n × `heappush` | **O(n log n)** | the naive build — worth knowing it's beatable |

**The load-bearing word is _path_.** A heap is a complete binary tree of height log n, and push/pop
restore the invariant by walking **one root-to-leaf path** — a chain of parent-child swaps. "Reconstruct"
implies touching the whole structure, which would be O(n).

**Why heapify is O(n) — the asymmetry:** sift-**up** starts at a leaf, the point *farthest* from the
root, so nearly every push pays the full log n. Sift-**down** costs a node's height above the leaves,
and **half the nodes are leaves and cost zero**. At n=15: 8 leaves × 0 + 4 × 1 + 2 × 2 + 1 × 3 = **11
operations, not 15 × 4 = 60**. In general Σ (n/2^(h+1))·h = (n/2)·Σ h/2^h = (n/2)·2 = **n** — the series
converges to 2 regardless of n, so the total is linear. Only the root ever pays log n; the expensive
nodes are rare.

> **Interview line:** *"Heapify is O(n), not O(n log n), because sift-down cost is a node's height above
> the leaves and half the nodes are leaves. The expensive nodes are rare — only the root pays log n."*

## Ledger (freebie state — being here = freebie spent)

A problem in this table has used its one free complexity miss. The **next** miss on it caps the rep at 🟡.

| Problem | Category | Said → Actual | First-miss date | Freebie |
|---|---|---|---|---|
| 242 Valid Anagram | fixed-alphabet array (space) | O(n) → **O(1)** | 2026-07-22 | spent |
| 778 Swim in Rising Water | 2D structure (space) | O(n) → **O(n²)** | 2026-07-23 | spent |
| 206 Reverse Linked List (Recursion) | recursion stack (space) | O(1) → **O(n)** | 2026-07-24 | spent |
| 567 Permutation in String | fixed-alphabet array (space) | O(n) → **O(1)** | 2026-07-24 | spent |
| 229 Majority Element II | bounded structure (space) | O(n) → **O(1)** (map capped at ≤2) | 2026-07-24 | spent |
| 210 Course Schedule II | graph traversal (**time**) | O(V·E) → **O(V+E)** (Kahn's/topo) | 2026-07-24 | spent |
| 743 Network Delay Time (Dijkstra) | heap ops per-edge (**time**) | O(V log E) → **O(E log V)** (E pushes/pops dominate) | 2026-07-25 | spent |
| 355 Design Twitter | list-membership scan (**time**) + squared-dims/phantom-log (**time**) | `follow` O(1) → **O(F)** (list `in` scan; set→O(1)); `getNewsFeed` O(n²logn) → **O(F·T)** (heap capped at 10 = O(1)/op, no square) | 2026-07-25 | spent |
| 424 Longest Repeating Char Replacement | fixed-alphabet array (space) | O(n) → **O(1)** (freqMap ≤ 26 keys — uppercase-only constraint) | 2026-07-27 | spent |
| 104 Max Depth of Binary Tree | full-traversal vs search (**time**) | O(log n) → **O(n)** — recursing into *both* children never discards a subtree; O(log n) requires each step to *throw half away* (binary search, BST descent). Computing a property **of the whole tree** ≠ searching **for a node** | 2026-07-27 | spent |
| 269 Alien Dictionary | fixed-alphabet graph (**time + space**) | time "no idea" → **O(C)** (C = total chars; the graph work is O(1)); space O(V+E) → **O(1)** — `V ≤ 26`, `E ≤ 26² = 676` by the lowercase-only constraint, so both collapse to constants. *Same fixed-alphabet family as 242/567/424, first time it appeared on a **graph** rather than a freq array* | 2026-07-27 | **spent → REPEAT MISS 2026-07-29 (capped that rep at 🟡)** |

**⚠️ 269's repeat miss (Jul 29) took a specific shape worth naming, because it is the shape this whole
category takes.** The learner correctly derived *"`rankMap` holds at most 26 keys"* — the load-bearing
fact — and then still answered **space O(C)**, then **"O(V) where V maxes at 26"**. Two distinct
sub-errors, neither of them the ceiling:

1. **Naming a constant ceiling and still writing a growing term.** `O(26)` is `O(1)`; a bound that
   doesn't move when the input grows is not a variable. Knowing the ceiling and applying it are
   separate steps, and only the second one was missing.
2. **Charging *output size* as *work done*.** Said building `adjMap` costs `O(E)`. E is how many edges
   come out; the work is scanning adjacent word pairs character by character → `O(C)`.

**Cue for next time:** after you name a ceiling, immediately ask *"does this number move when the input
gets 1000× bigger?"* — if no, write O(1) and stop. And when timing a build step, count **what you
touch**, not **what you produce**.
| 18 Four Sum | combination-holding structure (space) | `resultSet` O(n) → **O(n³)** worst case. Verified by running the learner's own code on `[-m…m]`, target 0: n=101 → **27,369** entries (271× n), and n 51→101 multiplies the count by 8.1 ≈ 2³ | 2026-07-27 | spent |
| 235 LCA of a BST | **"BST" read as "balanced"** (time *and* space, inconsistently) | Gave `O(n)` space for the recursion stack but `O(log n)` time — the two **contradict**, since stack depth *is* the number of steps walked down. `log n` needs *balance*, which the constraints never promise. Counterexample: `1→2→3→4` all as right children is a legal BST; the mental image is **a sorted list in tree form**. True bound is **O(h)** — `O(log n)` balanced, `O(n)` degenerate | 2026-07-29 | spent |

<!-- Add a row on every first-time complexity miss. A repeat miss on a problem ALREADY here caps that
rep at 🟡 (freebie spent) — note the repeat in the schedule/stuck_log where the rating is recorded.
The card grows only on a NEW problem's first miss, so it stays short. -->
