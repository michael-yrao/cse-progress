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
| **Size-capped heap (time)** *(added Aug 10, 2026, via 703 — 3rd occurrence)* | a heap with an explicit trim: `if len(heap) > CAP: heappop`, where CAP is `k`, a constant, or a fixed-alphabet bound | *"how big does that heap actually get? then what's the log over?"* | **`log CAP`, not `log n`.** The trim means the heap **never holds n**, so each push/pop is `log CAP` and a loop over n costs `O(n log CAP)`. Seen three times on three different problems: **355** (capped at 10 → `O(1)`/op), **621** (capped at 26 → `log 26` = `O(1)`), **703** (capped at `k` → `O(n log k)`). ⚠️ **The trim line is the whole tell** — it's one line, easy to skim past, and it changes the bound |
| **Re-pushed stack bound (space)** *(added Aug 10, 2026, via 503)* | a monotonic stack under a **two-pass / circular** loop (`for i in range(len(nums)*2)`) that pushes on **every** iteration | *"can an index get pushed more than once? then what's the real ceiling?"* | **Not `n`.** Each index is pushed once per pass, so the stack can hold **n+1**. Concrete witness on 503: `[5,4,3,2,1]` — pass 1 fills it to 5, the first pass-2 element drains it to 2, then four more pushes rebuild it to **6**. Still **O(n)**, so the *bound* survives; what fails is the itemization, and "at most n" is exactly the clause an interviewer probes. **Cue: a per-iteration push over a `2n` loop cannot be bounded by `n` without an argument for why things leave** |
| **Bounded state space (time)** *(added Aug 11, 2026, via 202)* | a `while`/recursion that repeatedly applies a **function to a value** (not a walk over the input) with a `seen` set as the halt condition — no `n` anywhere in the loop body | *"after one step, how big can this value still be? and after two?"* | **Constant iterations — the loop count stops depending on `n`.** Compute the collapse: on 202 one step gives ≤ `10·9² = 810`, the next ≤ `3·9² = 243`, so the walk is trapped in 243 values and pigeonhole caps it at 243 steps. What's left is whatever work still scales — the **first digit split**, `O(log n)`. ⚠️ **Same family as 229/269/621** (a constraint collapses a term to a constant) **but inverted**: there the bound was handed to you in the constraints, here you have to *derive it from the operation*. **Cue: say the collapse before quoting the number** — "O(1)" alone reads as hand-waving; "it drops to ≤243 after two steps, so O(1)" reads as reasoning |
| **Binary search on the ANSWER (time)** *(added Aug 9, 2026, via 1011)* | `l, r = <smallest feasible>, <largest feasible>` ranging over **values**, with a feasibility check called inside the loop | *"what are you halving — the array, or the space of possible answers?"* | **O(n · log(hi − lo))**, **not** `O(n log n)`. The `log` is over the **value range**, read off the constraints; `n` enters only through the feasibility scan. The two are **independent quantities**: on 1011, `log(sum(weights)) ≈ 25` against `log n ≈ 16`, and with values to 10⁹ against a 10-element array they diverge completely. `log n` is only right when you binary-search **indices** |
| **Design-object vs per-call space** *(added Aug 13, 2026, via 901)* | the deliverable is a **class**, and `__init__` allocates a structure that **persists across calls** (`self.stack`, `self.heap`, `self.map`) | *"is that O(1) the method's auxiliary, or the object's footprint? say which"* | **Both are true and they are different numbers — name the one being asked.** `next()` on 901 allocates one tuple, so **per-call auxiliary is O(1)**; `self.stack` grows to one entry per call, so the **object is O(n)** (worst case: strictly decreasing input, nothing ever pops). ⚠️ **Design problems flip the default.** On a plain function "space complexity" means auxiliary; on a class it means the footprint, because that is the number that decides whether the thing can be deployed. **Cue: "no extra space" is never right for a design problem** — the structure you built *is* the space. Live on 146 · 155 · 703 · 208 |
| **A string is not O(1)** *(added Aug 13, 2026, via 127)* | slicing, hashing, comparing or **storing** a string inside a loop — `word[:i]`, `pre + '.' + post`, `x in visitedSet`, a dict **keyed by a string** | *"that key is an object of length L — are you counting one of it, or L of it?"* | **Every string touch costs O(L), including the ones that look free.** On 127 this was dropped **twice in one answer** after being charged correctly once: (a) the BFS loop rebuilds the same wildcards as the build loop, so BFS is `O(V·L²)` too and the two phases **tie** — neither dominates; (b) `adjMap` holds `V·L` **keys of length L**, so it is `O(V·L²)` space, not `O(V·L)`. ⚠️ **The free check: time and space came out equal, because build-and-store is one loop doing one kind of work.** A space answer a whole factor of `L` cheaper than the time answer is the tell that a string got counted as a scalar |
| **Amortized vs per-call worst case (time)** *(added Aug 13, 2026, via 901)* | a monotonic stack / union-find / dynamic array where **one call can do O(n) work** but each element is touched a bounded number of times across the whole run | *"how many times can a single element be popped, ever?"* | **State both, lead with amortized.** A single `next()` really is **O(n)** worst case — that answer is not wrong. But each price is pushed exactly once and popped **at most once**, so total pop work over n calls is bounded by n → **amortized O(1) per call, O(n) for the sequence**. ⚠️ **This is the whole reason the design beats the naive backward scan**, which is *also* O(n) worst case per call but **O(n²)** overall — so the per-call worst case cannot distinguish them and the amortized bound is the one carrying the argument. **Cue: when the worst cases tie, the amortized bound is the answer being asked for** |

**⚠ Consistency check — the two bounds must agree.** On a single downward walk, the recursion stack's
depth **is** the number of steps taken, so time and space are the *same* bound. Answering `O(log n)`
time with `O(n)` space (or vice versa) is self-contradictory and is the cheapest tell that a
balance assumption got applied to one and not the other. **Whenever a recursive walk's time and space
come out different, one of them is wrong** — check before you say it out loud.

> ⚠️ **But the consistency check is necessary, not sufficient — proved on 235, Aug 8, 2026.** Jul 29's miss
> was `O(log n)` time with `O(n)` space, and the contradiction *was* the tell. Aug 8's repeat gave
> `O(log n)` for **both** — perfectly consistent, and still wrong, because the balance assumption was now
> applied to *both* halves instead of one. **Consistency only proves you applied the same premise twice; it
> says nothing about whether the premise is true.** So run the height cue on its own — *"balanced, or is a
> chain also legal here?"* — and never let a matching pair of bounds stand in for having asked it.
>
> **Same idea, opposite error, same day:** 100 Same Tree got `O(n)` space (too loose) and 235 got
> `O(log n)` (too tight). Both are the one missing habit — **say `O(h)` first, then say what `h` is on the
> shape you were actually promised.** Reach for `O(h)` as the default phrasing on any tree descent; it is
> correct before you know anything about balance, and it makes the assumption a separate, visible sentence.

> ## ⚠️⚠️ Structural finding (Aug 9, 2026): the per-problem freebie **cannot catch a category that hops problems**
>
> Fixed-alphabet is the **most repeated miss in this file** — 242, 567, 424, 269 (×3), and now 621 — and
> the 🟡 cap has fired for it exactly once, on 269, the only problem where it recurred *on the same
> problem*. Every other occurrence landed on a **fresh** problem and therefore spent a fresh freebie.
>
> **So the enforcement mechanism is blind to precisely the failure mode it most needs to catch.** A gap
> that recurs on one problem is *decay*; a gap that recurs across five different problems is a **missing
> transfer**, which is worse and is the thing the "Recurring categories" table above exists to fix. The
> freebie is keyed to the wrong unit.
>
> **Do not silently start capping on category** — that changes rating semantics and is the learner's call.
> **Raise it at the Aug 10 build as a menu item.** Options worth putting up: (a) leave as-is and rely on the
> cue table; (b) a *category* freebie in addition to the per-problem one, so the 3rd occurrence of a family
> caps regardless of which problem it lands on; (c) fire the category cue **proactively** whenever a
> problem's constraints name a bounded alphabet, treating it as teaching rather than testing.

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
| 621 Task Scheduler | **fixed-alphabet (space AND time)** — *5th of this family* | Space O(n) → **O(1)**; time "O(min(k,i)·n log n)" → **O(N)**. `tasks[i] is an uppercase English letter` ⟹ `k ≤ 26`, so `freqMap`, `maxHeap` and `tasksLeft` are all constant-sized and every `log k` is `log 26`. Total pops across the whole run = `N` (one per task instance), giving `O(N · log 26) = O(N)`. **New disguise for an old family** — 242/567/424 were freq *arrays*, 269 was a *graph*, this is a *heap* | 2026-08-09 | spent |
| 1011 Capacity to Ship | **binary search on the answer (time)** — *new category, see above* | O(n log n) → **O(n · log(sum − max))**. Justification given was *"binary is log n"* — but the search runs over the **capacity range** `[max(weights), sum(weights)]`, not over the array. `n` appears only in `canShip`. Code was otherwise clean: correct bounds, correct lower-bound template, no off-by-one | 2026-08-09 | spent |
| ↳ **✅ TRANSFERRED — 875 Koko, 2026-08-11** | *(not a miss; recorded because a carded cue actually firing on a **different problem** is the outcome this ledger exists to produce)* | **O(n log k), k = max(piles)**, volunteered unprompted with `k` named. The 1011 miss was *"binary is log n"* — the log is over the **value range**, not the array. Two days later, on the sibling problem, the right form came out first try. **This is the freebie ledger working as intended: the unit that decays is the *category*, not the problem** — which is also the open question in build-agenda item #2, pointing the other way | 2026-08-11 | — |
| ↳ **✅ TRANSFERRED — 146 LRU Cache, 2026-08-13** | *(not a miss; recorded because it is the **design-object space convention firing on a different problem the same day it was taught**)* | Space given as *"O(n) — we use a map, so across multiple calls"*. ⭐ **The "across multiple calls" framing is 901's lesson applied cold, unprompted, ~3 hours later** — 901 had been logged as a *phrasing* gap precisely because the learner knew the structure persisted but described it as per-call; here the persistence was named first. `n` was then defined under challenge as the list size and defended, which makes it true; refined to **O(capacity)** — the cap is an input, so the stronger claim is that the cache **does not grow with usage**, which is the whole reason one is deployed. Same family as 703/355/621 (size-capped structure) | 2026-08-13 | — |
| 133 Clone Graph (BFS) | graph traversal (**time**) — *dropped-term variant, mirror of 323* | O(n) → **O(V + E)**. Justification given was *"traverse all nodes"* — true, and it accounts for the outer `while` only. The inner `for neighbor in oldNode.neighbors` runs **2E times in total** across the whole traversal, and `E` is not bounded by `V` (a dense graph has `E ≈ V²/2`). **Space O(V) was fine** as *auxiliary* (map + queue); say which you mean, since counting the constructed clone's adjacency lists makes it O(V+E) | 2026-08-09 | spent |
| 703 Kth Largest in Stream | **size-capped heap (time)** — *3rd of this family, 3rd different problem* | `__init__` O(n log n) → **O(n log k)**. The learner's own `if len(minHeap) > k: heappop` caps the heap at k, so every push/pop costs `log k` and the heap **never holds n**. With k=3, n=10⁴ that is ~1.6·10⁴ ops, not ~1.3·10⁵. *(Space O(k) was correct — and correct **because** the trim happens inside the init loop; the common wrong version pushes all n first and drains after, which is O(n).)* Separately, "heapify makes it O(n)" doesn't land: heapify builds a heap of **all n**, so you still extract down to k and hold O(n) space — best variant is max-heapify + k pops = **O(n + k log n) time, O(n) space**, a space-for-time trade rather than a free win | 2026-08-10 | spent |
| 323 Connected Components (DFS) | graph traversal (**time**) — *multiply-instead-of-add variant* | O(V·E) → **O(V+E)**. **REPEAT on 323** (BFS row, Aug 5, dropped-term variant) — so the rule says this rep caps at 🟡. ⚠️ **CAP WAIVED BY LEARNER OVERRIDE, recorded not silent** (see the note under the table). Needed the full aggregate-counting walkthrough: each node clears the `visited` guard **once ever**, so `Σ deg(u) = 2E` across the whole run and the outer loop adds `V` — nesting only multiplies when the inner loop restarts fresh each time | 2026-08-11 | n/a — repeat |
| 202 Happy Number | **bounded state space (time)** — *new category, see below* | O(1) → **O(log n)**. Space O(1) was right and for the right reason. The bound was supplied, not derived: after one step the value is ≤ 10·9² = **810** whatever `n` was, and anything ≤ 810 has ≤ 3 digits so from step two on it is ≤ 3·9² = **243** — 243 possible values, so the seen-set forces a halt within 243 steps by pigeonhole. What survives that collapse is the **first digit split**, which costs one unit per digit = `log₁₀(n)`. **New problem ⟹ double freebie; no cap.** *Same family as 229/269/621 (a constraint collapses a term to a constant) but inverted — there the alphabet was given in the constraints, here the bound has to be **computed from the operation itself*** | 2026-08-11 | spent |
| 105 Construct Tree from Pre+In | **retained slices + per-node scan (time AND space)** | O(n)/O(n) → **O(n²)/O(n²) worst case** (O(n log n)/O(n) balanced). Two independent costs, both invisible as written: `inorder.index(rootVal)` is a **linear scan re-run at every node**, and the four slices per frame are **copies**, alive while recursing. Skewed tree ⟹ `n + (n-1) + (n-2) + …` for both | 2026-08-09 | spent |
| 127 Word Ladder (BFS) | **string cost (time AND space)** — *new category, see above* | BFS phase `O(V + V·L)` → **`O(V·L²)`** (the loop re-slices exactly as the build does, so the phases tie); space `O(V·L)` → **`O(V·L²)`** (`V·L` keys × `L` chars each). ⭐ **The build phase was priced CORRECTLY and unprompted** — `O(C·L)` with the slicing named — so the category was in hand and then dropped twice downstream. ⭐ **Also volunteered: the fixed-alphabet collapse** — a `.it` bucket holds ≤26 words, which kills the `E` term outright (6th of that family: 242/567/424/269/621). ⚠️ **Separate finding — convention drift:** `L` was held symbolic for time and then collapsed via `L ≤ 10` for space, in the same answer. Pick one and defend it; mixed conventions are indefensible under a follow-up | 2026-08-13 | spent |

### 📌 RECORDED OVERRIDE — 323 DFS, Aug 11, 2026: the 🟡 cap was waived by the learner

The rule fired correctly (repeat miss on 323, first miss Aug 5) and the learner **overrode it to 🟢**, with
a reason worth preserving because it is an argument *from the engine's own logic*, not a plea:

> *"I just want more practice on recognizing it on the other problems, redoing this in 10 days won't really
> help much there."*

**The case for the override.** The unit that failed is the **category**, not the problem — and the category
is re-tested three times inside twelve days on *different* problems (**261 DFS Aug 16 · 133 Aug 19 ·
210 Aug 23**). A fourth rep of 323 itself would measure recall of 323's solution, which was never in doubt;
the code was clean and unhinted. This is the same reasoning as the fast-track's coverage gate — *stop
testing the technique at its weakest instance while harder ones keep doing the work* — and the same
reasoning as per-algorithm phase exit.

**The cost, stated plainly:** 323-DFS was 🟢 s1, so 🟢 makes it **s2 → +60 → Oct 10.** It leaves the board
for two months. That is only safe *if* the category actually gets fired cold on 261/133/210 — so **fire
the complexity gate cold on 261 (Aug 16)**; that rep is now carrying this one's weight.

⚠️ **This is exactly build-agenda item #2 and should be read as evidence for it, not as an exception to
it.** A per-problem freebie could not see the pattern below; a category freebie would have capped the
Aug 5 rep and there would have been nothing to override.

| date | problem | said | actual |
|---|---|---|---|
| Jul 24 | 210 Course Schedule II | **O(V·E)** | O(V+E) |
| Aug 5 | 323 (BFS) | O(E) | O(V+E) |
| Aug 9 | 133 Clone Graph (BFS) | O(n) | O(V+E) |
| Aug 11 | 323 (DFS) | **O(V·E)** | O(V+E) |

**Four misses, three problems, one category, one cap fired** — and it fired only because the category
happened to land on the same problem twice. **Second independent instance of the structural hole**
(fixed-alphabet was the first: 5 misses / 5 problems / 1 cap). Two categories showing it is a much stronger
case than one.

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

> ⚠️ **Missed on 211 again, 2026-08-12 — against this very line, written from this very problem.**
> The Aug 2 rep got the space right and the time wrong; Aug 12 got the time right and the space
> wrong. Reading the sentence was not enough, which suggests the durable form is the **question**,
> not the statement: *"is this loop exploring branches one at a time, or holding them all?"*
> Sequential ⇒ time only. Simultaneous (a BFS queue) ⇒ space too.

**⚠️ UNIT-OF-WORK is the DOMINANT recurring miss — 721 Jul 30 · 271 Aug 2 ×2 · 271 Aug 12 ×3.**
Updated Aug 12, 2026: it was filed as a two-occurrence pattern and is now six, all on the same reflex.
The Aug 12 reps are the sharpest evidence, because the *code* was flawless both times — this is not a
comprehension gap about the algorithm, it is the first noun reached for when naming `n`. Both times the count used was
the number of **containers** (accounts, strings) when the work is per **element inside** them (emails,
characters). **Cue: before naming `n`, ask "what does one unit of work touch?"** — if a single "item" can hold
200 characters, the item is not the unit.
| 18 Four Sum | combination-holding structure (space) | `resultSet` O(n) → **O(n³)** worst case. Verified by running the learner's own code on `[-m…m]`, target 0: n=101 → **27,369** entries (271× n), and n 51→101 multiplies the count by 8.1 ≈ 2³ | 2026-07-27 | spent |
| 721 Accounts Merge | **passed the gate — asked to be taught** (not a miss; carded so the next rep is asked cold) | Whole analysis taught: the unit is **total emails E**, not accounts N; DSU with rank + path compression is `O(α(N))` ≈ free; **time `O(E log E)`** (the sort dominates). Learner then derived both bounds correctly, incl. `O(E+N) → O(E)` (constraints guarantee ≥1 email/account) and the `O(log N)` `find` stack. **Then challenged the sort bound unprompted** — *"isn't it `O(N · E log E)`?"* — the multiply-vs-add trap; resolved via `Σ kᵢ = E`, tight when one group holds everything | 2026-07-30 | **1 of 2** *(new-problem double freebie)* |
| 1584 Min Cost Connect Points | **Multiply-vs-add on accumulated loop work** (time) | Right bound `O(V²)`, wrong derivation: wrote `(V-1)*(V-2)*…*1`, which is **V!**, not V². Work across rounds **accumulates**, it doesn't compound → `(V-1)+(V-2)+…+1 = V(V-1)/2 = O(V²)`. ⚠️ **Same trap the learner caught *unprompted* on 721 the other direction** (Jul 30) — so the concept is there and the slip is directional. Cleaner framing to reach for: **V rounds × two O(V) scans**. Bonus payoff: complete graph ⟹ `E ≈ V²`, so the array version is `O(V²) = O(E)` while a heap would be `O(E log V)` — *worse* | 2026-08-01 | spent |
| 271 Encode and Decode Strings | **unit-of-work** (time, ×2) + **immutable-string concatenation** (time) + **multiply-vs-add** (time) | Three misses, one rep, one freebie. (a) Counted `n` = **number of strings** for both `encode` and `decode`; the unit is **N = total characters** — *same correction taught on 721 four days earlier* (the unit is total emails, not accounts). (b) Assumed `result += string` is O(1); Python strings are **immutable**, so each `+=` copies everything built so far → naive loop is **O(N²)**, fixed to O(N) with `"".join`. (c) On `decode`'s slices, gave **O(N·n)** where the per-string copies **sum** to N | 2026-08-02 | spent |
| 211 Add and Search Words | **branching factor** (time) — multiplied two ceilings that don't compose | Asked for the ≤2-dot bound, gave **`O(n·N)`** — bigger than *either* input ceiling, for a restriction that makes the bound **smaller**. Actual **`O(26^d · L)` → `O(L)`** with `d ≤ 2` (676 as a constant). Everything else was right, incl. the all-dots `O(N)` ceiling *with the correct argument* (a node sits at a fixed depth and `index` advances one per level, so no node is ever visited twice), and both space terms — trie `O(N)`, stack `O(L)` | 2026-08-02 | spent |
| 211 Add and Search Words | **sequential fan-out read as space** — the mirror image of the Aug 2 miss | Time **`O(c·26^d) → O(c)`** correct and unprompted (the Aug 2 miss firing right). Space given as **`O(26^d)`**, then **`O(26)`** — both are the *fan-out*, not the *depth*. The `for child in children.values()` loop is **sequential**: it calls one child and waits, so siblings are pending iterations, never live frames. Stack holds one root-to-current path ⇒ **`O(c)`**. Traced `search("..d")` on bad/dad/mad: 3 frames deep, `d` and `m` untouched | 2026-08-12 | **freebie already spent (2026-08-02) → capped this rep at 🟡** |
| 778 Swim in Rising Water | **passed the gate — asked to be taught** (not a miss; carded so the next rep is asked cold) | Heap terms given unprompted and correct: time **`O(V log V)`**, space **`O(V)`**, `V = n²`. Then said outright *"I don't quite understand how time affects the time complexity"* rather than guessing. **Taught:** the `time += 1` outer loop is bounded by the **value range**, not the grid — it costs `O(V)` *only because* the constraints say `grid[i][j] < n²`. Under `< 10^9` it is 10^9 iterations on a **2×2** grid, i.e. cost decoupled from input size. Textbook Dijkstra never scans: `time = max(time, currentNodeValue)` at each pop jumps to the next real elevation. Total stands at **`O(n² log n)`** time / **`O(n²)`** space | 2026-08-12 | **pass — no freebie spent** |
| 271 Encode and Decode Strings | **unit of work ×3** (the problem's own category, repeating) | `encode` time `O(n)` → **`O(L)`** (`join` copies every char); `encode` space `O(1)` *"we don't count result"* → **`O(n)` extra**, since that list is a **midpoint**, not the return value; `decode` time `O(n)` → `O(n·w)` → **`O(L)`** (slicing copies, and words partition the input so `Σ` not `×` — counterexample `["a"*1000] + 25 singles` gives `n·w = 26,000` vs `L = 1,025`). ✅ **`decode` space was RIGHT and defended under challenge** — `O(1)` extra, because *there* `result` is the output. Same variable name, different accounting, and the learner drew the line themselves | 2026-08-12 | **freebies spent 2026-08-02 → capped this rep at 🟡** |
| 155 Min Stack (**new**) | **structure space vs per-call space** | Time `O(1)` for all five methods, correct. Space given as *"O(1) for each method"* — true for the **incremental** cost of one call, but "space of MinStack" means the structure: **`O(n)`**, holding n pairs. Learner defended the per-call reading (*"n calls meaning having O(n) means O(1) across n calls"*), which is coherent — the fix is to **state which question you are answering**, same convention rule as the output-counting row | 2026-08-12 | **1 of 2** *(new-problem double freebie)* |
| 235 LCA of a BST | **"BST" read as "balanced"** (time *and* space, inconsistently) | Gave `O(n)` space for the recursion stack but `O(log n)` time — the two **contradict**, since stack depth *is* the number of steps walked down. `log n` needs *balance*, which the constraints never promise. Counterexample: `1→2→3→4` all as right children is a legal BST; the mental image is **a sorted list in tree form**. True bound is **O(h)** — `O(log n)` balanced, `O(n)` degenerate | 2026-07-29 | spent · **REPEATED 2026-08-08 → capped that rep at 🟡** |
| 332 Reconstruct Itinerary | **recursion depth = nodes, not edges (space)** | Gave recursion stack as **O(V)**. Wrong unit: airports are **revisited** (`JFK→A→JFK→A…`), so the stack follows the Euler **path** (E edges deep), not the distinct-node count. Depth is **O(E)**; total space **O(E)** (map + stack). The tell: whenever a node can be re-entered, "stack = O(V)" is unsafe — bound the stack by the **longest descent**, which here is every edge. Time was right: **O(E log E)** (heap push/pop per edge) | 2026-08-04 | spent · ⭐ **HALF-TRANSFERRED 2026-08-14 — see below** |

> ### ⭐ 332, Aug 14, 2026 — the number transferred and the reasoning did not
>
> **Unrated rep** (the session was converted to a teach, §2a), so **no freebie spent and no cap applied.**
> Logged anyway, because the *shape* of this one is the argument for the itemized-why-clause rule.
>
> | | Aug 4 | Aug 14 |
> |---|---|---|
> | **Time** | O(E log E) ✅ | O(E log E) ✅ |
> | **Space — the number** | **O(V)** ❌ | **O(E)** ✅ |
> | **Space — the why-clause** | *(the miss)* | *"since we are working on **nodes** and using a heap"* ❌ |
>
> **The Aug 4 correction landed on the answer and not on the explanation.** The word `nodes` — the exact
> error corrected ten days earlier — is still sitting underneath a now-correct `O(E)`, and the two
> contributors named are wrong in both directions:
>
> - **The heap is not a space term at all.** The heaps *are* the adjacency lists (heapified in place);
>   there is no second structure. Naming it inflates the itemization with something that costs nothing.
> - **The recursion stack was never named** — and it is the one that actually costs O(E). The walk
>   consumes tickets and only unwinds once it strands, so the first descent can be *every* edge deep.
>
> ⚠️ **This is why the gate asks for contributors, not a number.** A right number over wrong reasoning is
> indistinguishable from understanding *on this problem*, and fails on the next one in the family —
> reasoning is the half that travels. Had the answer been graded on the number alone, this would have
> read as a clean transfer and the live error would have shipped forward invisibly.
>
> ⭐ **The cross-reference worth carrying:** *"visited holds edges not nodes"* was this learner's own
> pre-code recognition call on the **same rep, two hours earlier** — and is quoted as the model
> picking-feature call in `recognition_gotchas.md`. **The unit that makes the algorithm correct is the
> unit that prices it**, and it did not survive the trip from the recognition gate to the complexity
> gate. That sentence is the durable cue for this problem; fire it cold on the Aug 18 rated rep.
>
> **Also fires build-agenda item #1** (the learner-pinned recursion space/time refresher). The
> recursion-stack family now reads `206 · 235 · 332 ×2 · 261 · 211 · 778 · 104 · 105` — the largest
> cluster in this file, and the only one the learner has asked for by name.
| 261 Graph Valid Tree (DFS) | **omitted the recursion stack (space)** + under-itemized time | Gave space as `adjMap` = O(V+E) only; **missed the DFS call stack**, which on a **path graph** (`0–1–2–…`) is **O(V) deep**. Full space **O(V+E)** (map O(V+E) + stack O(V) + visited O(V)). Time given as `O(E)`; correct is **O(V+E)** — the `for i in range(n)` node loop is the dropped V-term. Both happen to collapse to the same order here only because the `len(edges)!=n-1` guard forces `E=V-1`. Cross-ref the standing rule: **any recursion ⟹ the depth is a space term.** | 2026-08-06 | spent |
| 973 K Closest Points to Origin | **loose bound where the tight one is the algorithm's whole point** (time *and* space) + **"bounded by construction" misread as "average case"** | Gave `O(n log n)` time / `O(n)` space for a heap the code caps at `k` (`while len(heap) > k: heappop`). Both are *true* (`k ≤ n`) and both are **self-defeating**: `O(n log n)` is exactly what sorting all points and slicing gives, so reporting it makes the size-k heap invisible. Tight bounds **`O(n log k)` / `O(k)`**. Then, when pushed, defended it as *"worst case `O(n log n)`, average `O(n log k)`"* — **no.** The cap is structural, not data-dependent: every input does exactly n pushes and n−k pops on a heap never larger than k+1, so `O(n log k)` **is** the worst case. What that intuition was actually reaching for is `k = n`, which is a **parameter value, not a case** — case analysis ranges over *inputs*, and `k` is a given. Contrast quicksort, where the input genuinely decides. | 2026-08-07 | spent |

<!-- Add a row on every first-time complexity miss. A repeat miss on a problem ALREADY here caps that
rep at 🟡 (freebie spent) — note the repeat in the schedule/stuck_log where the rating is recorded.
The card grows only on a NEW problem's first miss, so it stays short. -->
