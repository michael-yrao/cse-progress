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
| **Dropped term — the do-nothing scan (time)** | an outer `for node in range(n)` that mostly hits `if node in visited: continue` | *"that outer loop runs V times whether or not it does anything — where's the V in your answer?"* | **Keep the `V`.** Constant work **per iteration** × `V` iterations = `O(V)`. The test case that exposes it: `n = 2000, edges = [[0,1]]` — `E` is 1, `V` is 2000, so an `O(E)` answer is off by three orders of magnitude. **A term doesn't vanish because each step is cheap** |
| **Combination-holding structure** | a set/list accumulating *k-tuples* of elements (k-Sum results, pair lists, subsets) | *"you're storing combinations of k elements, not elements — how many are there?"* | **O(n^(k−1))** for k-Sum — pick k−1 freely, the last is forced. 3Sum O(n²), 4Sum O(n³). **Not O(n)** — `n` is a false anchor from the input's length |

| **Partitioned work (time)** | a loop over *groups* with a sort/scan **inside** each group | *"does every group see the whole input, or a slice of it?"* | **Add, don't multiply.** Groups partition the input, so `Σ kᵢ = E` and the total is `Σ kᵢ log kᵢ ≤ E log E` — **not** `groups × E log E`. More groups forces smaller groups; the two are coupled, not independent. Bound is tight when one group holds everything. Reductio: 12 singleton groups would cost `12 × 12log12` ≈ 516 ops to sort 12 items whose true cost is 0 |
| **Tree height (time *and* space)** | walking down one path of a tree — BST descent, insert, search | *"balanced, or is a chain also legal here?"* | **O(h)** — `O(log n)` **only if balanced**, `O(n)` degenerate. "It's a BST" does not give you balance; a chain like `1→2→3→4` (all right children) is a legal BST — *a sorted list in tree form*. Balance is an **assumption you state**, not a freebie |
| **Branching factor (time)** | a `for child in node.children` that **recurses**, sitting next to a branch that recurses on **one** child | *"at this character, how many children do you step into — one, or all of them?"* | **O(b^d · L)** where `b` = fan-out, `d` = how many times you fan out. Fan-out **does not accumulate across the walk** — a step that picks one child collapses the paths back to one. Only *consecutive* fan-outs compound. Read `d` off the **constraints**, not off `L` |
| **Sequential fan-out (space)** | same `for`-loop recursion as above | *"how many of those paths are alive at once?"* | **O(depth), not O(b^d)** — DFS walks one path to the bottom, returns, and **reuses the frames**. Explored-sequentially branching is a *time* cost only. You'd pay it in space only by holding all paths simultaneously (BFS with a queue) |

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
| 778 Swim in Rising Water | 2D structure (space) | O(n) → **O(n²)** | 2026-07-23 | **spent → REPEAT MISS 2026-08-02 (capped that rep at 🟡)** |
| 206 Reverse Linked List (Recursion) | recursion stack (space) | O(1) → **O(n)** | 2026-07-24 | spent |
| 567 Permutation in String | fixed-alphabet array (space) | O(n) → **O(1)** | 2026-07-24 | spent |
| 229 Majority Element II | bounded structure (space) | O(n) → **O(1)** (map capped at ≤2) | 2026-07-24 | spent |
| 210 Course Schedule II | graph traversal (**time**) | O(V·E) → **O(V+E)** (Kahn's/topo) | 2026-07-24 | spent |
| 743 Network Delay Time (Dijkstra) | heap ops per-edge (**time**) | O(V log E) → **O(E log V)** (E pushes/pops dominate) | 2026-07-25 | **spent → REPEAT MISS 2026-08-04 (capped that rep at 🟡)** |
| 355 Design Twitter | list-membership scan (**time**) + squared-dims/phantom-log (**time**) | `follow` O(1) → **O(F)** (list `in` scan; set→O(1)); `getNewsFeed` O(n²logn) → **O(F·T)** (heap capped at 10 = O(1)/op, no square) | 2026-07-25 | spent |
| 424 Longest Repeating Char Replacement | fixed-alphabet array (space) | O(n) → **O(1)** (freqMap ≤ 26 keys — uppercase-only constraint) | 2026-07-27 | spent |
| 104 Max Depth of Binary Tree | full-traversal vs search (**time**) | O(log n) → **O(n)** — recursing into *both* children never discards a subtree; O(log n) requires each step to *throw half away* (binary search, BST descent). Computing a property **of the whole tree** ≠ searching **for a node** | 2026-07-27 | spent |
| 269 Alien Dictionary | fixed-alphabet graph (**time + space**) | time "no idea" → **O(C)** (C = total chars; the graph work is O(1)); space O(V+E) → **O(1)** — `V ≤ 26`, `E ≤ 26² = 676` by the lowercase-only constraint, so both collapse to constants. *Same fixed-alphabet family as 242/567/424, first time it appeared on a **graph** rather than a freq array* | 2026-07-27 | **spent → REPEAT ×2: 2026-07-29 and 2026-08-07 (each capped its rep at 🟡)** |
| 323 Connected Components (BFS) | graph traversal (**time**) — *dropped-term variant* | O(E) → **O(V + E)**. Space `O(V+E)` was correct; time lost the `V` entirely. Reasoning given: *"if they are not connected, it is a constant time run"* — true **per iteration** of `for node in range(n)`, but there are `V` such iterations, so the constant-work scan is still `O(V)` in total | 2026-08-05 | spent |

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

**⚠️ 778's repeat miss (Aug 2) is the SAME cue fired in the opposite direction — and that symmetry is the
lesson.** The rep's outer loop increments `time` one unit at a time until the heap drains, so its iteration
count is bounded by the largest elevation in the grid. Asked what that costs, the learner answered
**"n ≤ 50 and `grid[i][j] < n² = 2500`, so it's constant"** — and held that answer when asked directly
whether it still stood at n = 1000.

- **The ceiling here MOVES.** `2500` is `n²`, not a literal. At n = 1000 it is 1,000,000. So the loop is
  `O(n²) = O(N)` — dominated by the heap's `O(N log N)`, which is why the final bound was right anyway.
  **Being right about the bound while wrong about the term is exactly what the itemized why-clause exists
  to catch**; a bare "O(N log N)" would have passed.
- **The discriminator against 269:** 269's `26` is fixed by the **alphabet**, so it is genuinely `O(1)`.
  778's `2500` is fixed by **n**, so it is not. *Same question, opposite answer* — the question is never
  "is there a stated ceiling?", it is **"is the ceiling a function of the input?"**
- **The test that settles it in one line — the argument proves too much.** If "n ≤ 50, therefore constant"
  were valid, then `N ≤ 2500` too and the entire function is `O(1)`. Any reasoning that collapses the whole
  analysis to `O(1)` has just told you it is the wrong reasoning. **Reach for this whenever a constraint
  from the problem statement is doing the work in a complexity claim.**

**⚠️ MULTIPLY-VS-ADD is now a three-occurrence pattern (Jul 30 · Aug 1 · Aug 2) and the direction is what's
unstable — the concept is demonstrably present.** On **721** (Jul 30) the learner challenged the sort bound
*unprompted* — *"isn't it `O(N · E log E)`?"* — and resolved it correctly via `Σ kᵢ = E`. On **1584** (Aug 1)
the same trap ran the other way: `(V-1)·(V-2)·…·1`, which is `V!`, for work that **sums** to `V(V-1)/2 = O(V²)`.
On **271** (Aug 2) again: `O(N·n)` for per-string slices whose costs **sum** to `N`.

**Cue:** work done across *successive iterations* **accumulates → add**. It **multiplies** only when one loop
runs fully **inside** another, i.e. the inner work repeats *per* outer step rather than dividing the total
between steps. Test to say aloud: *"does each iteration handle a **share** of the input, or **all** of it?"* —
a share means sum, all of it means product.

**⚠️ 211 (Aug 2) is a FOURTH occurrence, in a new shape: multiplying two *ceilings* rather than two loops.**
Asked to tighten the wildcard bound using the "at most 2 dots" constraint, the learner answered `O(n·N)` —
the product of the search-word length and the whole trie. The two prior shapes were about loop nesting; this
one has no second loop at all. It is reflex reaching for `×` whenever two symbols are in play.

**The sanity check that kills it instantly, and it's free: compare the answer to the ceilings you already
have.** `O(N)` was already established as a true upper bound. `O(n·N)` is *larger than `O(N)`* — so it cannot
be a tightening, and a bound that exceeds a bound you already proved is wrong on arithmetic alone, before
any algorithmic reasoning. **Direction is checkable without understanding the algorithm.** Add to the gate:
after stating a bound, ask *"is this bigger or smaller than the last bound I gave, and is that the direction
I intended?"* — a constraint that **restricts** the input can only move a bound **down**.

Related and worth keeping separate: fan-out is a **time** cost, not a **space** one (see the two new
Branching-factor rows above). 676 paths, but only one alive at a time.

**⚠️ UNIT-OF-WORK is now a two-occurrence pattern (721 Jul 30 · 271 Aug 2 ×2).** Both times the count used was
the number of **containers** (accounts, strings) when the work is per **element inside** them (emails,
characters). **Cue: before naming `n`, ask "what does one unit of work touch?"** — if a single "item" can hold
200 characters, the item is not the unit.
| 18 Four Sum | combination-holding structure (space) | `resultSet` O(n) → **O(n³)** worst case. Verified by running the learner's own code on `[-m…m]`, target 0: n=101 → **27,369** entries (271× n), and n 51→101 multiplies the count by 8.1 ≈ 2³ | 2026-07-27 | spent |
| 721 Accounts Merge | **passed the gate — asked to be taught** (not a miss; carded so the next rep is asked cold) | Whole analysis taught: the unit is **total emails E**, not accounts N; DSU with rank + path compression is `O(α(N))` ≈ free; **time `O(E log E)`** (the sort dominates). Learner then derived both bounds correctly, incl. `O(E+N) → O(E)` (constraints guarantee ≥1 email/account) and the `O(log N)` `find` stack. **Then challenged the sort bound unprompted** — *"isn't it `O(N · E log E)`?"* — the multiply-vs-add trap; resolved via `Σ kᵢ = E`, tight when one group holds everything | 2026-07-30 | **1 of 2** *(new-problem double freebie)* |
| 1584 Min Cost Connect Points | **Multiply-vs-add on accumulated loop work** (time) | Right bound `O(V²)`, wrong derivation: wrote `(V-1)*(V-2)*…*1`, which is **V!**, not V². Work across rounds **accumulates**, it doesn't compound → `(V-1)+(V-2)+…+1 = V(V-1)/2 = O(V²)`. ⚠️ **Same trap the learner caught *unprompted* on 721 the other direction** (Jul 30) — so the concept is there and the slip is directional. Cleaner framing to reach for: **V rounds × two O(V) scans**. Bonus payoff: complete graph ⟹ `E ≈ V²`, so the array version is `O(V²) = O(E)` while a heap would be `O(E log V)` — *worse* | 2026-08-01 | spent |
| 271 Encode and Decode Strings | **unit-of-work** (time, ×2) + **immutable-string concatenation** (time) + **multiply-vs-add** (time) | Three misses, one rep, one freebie. (a) Counted `n` = **number of strings** for both `encode` and `decode`; the unit is **N = total characters** — *same correction taught on 721 four days earlier* (the unit is total emails, not accounts). (b) Assumed `result += string` is O(1); Python strings are **immutable**, so each `+=` copies everything built so far → naive loop is **O(N²)**, fixed to O(N) with `"".join`. (c) On `decode`'s slices, gave **O(N·n)** where the per-string copies **sum** to N | 2026-08-02 | spent |
| 211 Add and Search Words | **branching factor** (time) — multiplied two ceilings that don't compose | Asked for the ≤2-dot bound, gave **`O(n·N)`** — bigger than *either* input ceiling, for a restriction that makes the bound **smaller**. Actual **`O(26^d · L)` → `O(L)`** with `d ≤ 2` (676 as a constant). Everything else was right, incl. the all-dots `O(N)` ceiling *with the correct argument* (a node sits at a fixed depth and `index` advances one per level, so no node is ever visited twice), and both space terms — trie `O(N)`, stack `O(L)` | 2026-08-02 | spent |
| 235 LCA of a BST | **"BST" read as "balanced"** (time *and* space, inconsistently) | Gave `O(n)` space for the recursion stack but `O(log n)` time — the two **contradict**, since stack depth *is* the number of steps walked down. `log n` needs *balance*, which the constraints never promise. Counterexample: `1→2→3→4` all as right children is a legal BST; the mental image is **a sorted list in tree form**. True bound is **O(h)** — `O(log n)` balanced, `O(n)` degenerate | 2026-07-29 | spent |
| 332 Reconstruct Itinerary | **recursion depth = nodes, not edges (space)** | Gave recursion stack as **O(V)**. Wrong unit: airports are **revisited** (`JFK→A→JFK→A…`), so the stack follows the Euler **path** (E edges deep), not the distinct-node count. Depth is **O(E)**; total space **O(E)** (map + stack). The tell: whenever a node can be re-entered, "stack = O(V)" is unsafe — bound the stack by the **longest descent**, which here is every edge. Time was right: **O(E log E)** (heap push/pop per edge) | 2026-08-04 | spent |
| 261 Graph Valid Tree (DFS) | **omitted the recursion stack (space)** + under-itemized time | Gave space as `adjMap` = O(V+E) only; **missed the DFS call stack**, which on a **path graph** (`0–1–2–…`) is **O(V) deep**. Full space **O(V+E)** (map O(V+E) + stack O(V) + visited O(V)). Time given as `O(E)`; correct is **O(V+E)** — the `for i in range(n)` node loop is the dropped V-term. Both happen to collapse to the same order here only because the `len(edges)!=n-1` guard forces `E=V-1`. Cross-ref the standing rule: **any recursion ⟹ the depth is a space term.** | 2026-08-06 | spent |
| 973 K Closest Points to Origin | **loose bound where the tight one is the algorithm's whole point** (time *and* space) + **"bounded by construction" misread as "average case"** | Gave `O(n log n)` time / `O(n)` space for a heap the code caps at `k` (`while len(heap) > k: heappop`). Both are *true* (`k ≤ n`) and both are **self-defeating**: `O(n log n)` is exactly what sorting all points and slicing gives, so reporting it makes the size-k heap invisible. Tight bounds **`O(n log k)` / `O(k)`**. Then, when pushed, defended it as *"worst case `O(n log n)`, average `O(n log k)`"* — **no.** The cap is structural, not data-dependent: every input does exactly n pushes and n−k pops on a heap never larger than k+1, so `O(n log k)` **is** the worst case. What that intuition was actually reaching for is `k = n`, which is a **parameter value, not a case** — case analysis ranges over *inputs*, and `k` is a given. Contrast quicksort, where the input genuinely decides. | 2026-08-07 | spent |

<!-- Add a row on every first-time complexity miss. A repeat miss on a problem ALREADY here caps that
rep at 🟡 (freebie spent) — note the repeat in the schedule/stuck_log where the rating is recorded.
The card grows only on a NEW problem's first miss, so it stays short. -->
