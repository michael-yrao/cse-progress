# Recognition Gotchas — reference card + miss ledger

The **front-gate** companion to [complexity_gotchas.md](complexity_gotchas.md): that one enforces
analysis at the *end* of a rep, this one enforces **pattern recognition at the start**. Reread it
like a Recall Card; the ledger below tracks which triggers trip the learner.

> **Reference vs scoreboard:** the full trigger→technique catalog (12 cards, drill one/week) lives in
> [recognition_patterns.md](../recognition_patterns.md). *That* file is the reference to reread; *this*
> file is the miss ledger — which triggers you actually got wrong.

## The rule (how recognition is gated)

Before writing any solution code, the learner states **shape → technique + why**:

1. **Shape** = *input structure* (array? sorted array? tree? weighted graph? intervals?) +
   *what's asked* (min/max? count? exists? all-of?).
2. **Technique** = the answer to that shape — plus **the one feature that picks it** over the
   nearest neighbor (e.g. *weighted* edges → Dijkstra, not BFS).

The learner already writes pre-code comments; they paste that comment as the call. Coach
confirms/corrects before coding. A miss (wrong technique, or right technique for the wrong
reason) is corrected and carded below. **Retries are half-spoiled** (method is in the tracker
name) — the measured reps are new problems and cold cues with the label stripped.

> **Can't remember what an algorithm's *name* means?** That's the reverse lookup and it lives in
> [patterns/README.md → Graph algorithms — the name index](../patterns/README.md#graph-algorithms--the-name-index-added-aug-5-2026).
> This file maps *shape → technique*; that one maps *name → the problem it solves*. Added Aug 5, 2026
> after 787, where the mechanism was derived correctly but the label "Bellman-Ford" couldn't be recalled.

## Trigger → technique map (the transfer — this is the part to master)

| Input shape | + What's asked | → Technique | Picking feature |
|---|---|---|---|
| Weighted graph | min cost / time to reach node(s) | **Dijkstra** | edges **weighted** & non-negative (else BFS if uniform, Bellman-Ford if negative / k-stops) |
| Unweighted graph / grid | fewest steps, shortest path | **BFS** | every edge same cost |
| Weighted graph | shortest path, negative weights or ≤k edges | **Bellman-Ford** | negatives allowed / hop limit |
| Sorted array | find element / boundary / min-max feasible value | **Binary search** | monotonic + sorted (or monotonic answer space) |
| Array, contiguous run | longest/shortest/count subarray meeting a condition | **Sliding window** | contiguous + window monotonicity |
| Array/string, pairs from ends | two values meeting a sum/area condition | **Two pointers** | sorted or convergent-from-ends |
| Graph | use **every edge** exactly once | **Eulerian path → Hierholzer** | the thing consumed is an **edge**, not a node — visited-marking goes on edges |
| Graph | visit **every node** exactly once | **Hamiltonian path** (NP-hard; expect backtracking) | the thing consumed is a **node** |

> **The "exactly once" trigger** (added Jul 28, 2026 — carded from a 332 miss). A statement that says
> *"use all the X exactly once"* is naming its own algorithm family, and **the only question that
> matters is what X is.** Edges → Eulerian, and there's a linear-time algorithm. Nodes → Hamiltonian,
> and there isn't. Same sentence shape, opposite tractability.

### Shortest path — the four-way split (added Jul 26, 2026)

The rows above cover this piecemeal; this is the whole decision in one place, because "shortest path"
is the single most over-loaded trigger in graphs. **Ask two questions in order: (1) from one source or
between all pairs? (2) can an edge be negative?**

| Source | Edge weights | → Algorithm | Cost | Why not the neighbor |
|---|---|---|---|---|
| Single | all equal (unweighted) | **BFS** | O(V+E) | Dijkstra works but the heap is wasted — equal weights mean FIFO order *is* cheapest-first |
| Single | non-negative | **Dijkstra** | O(E log V) | fastest that's still correct; settling is safe only because nothing can get cheaper later |
| Single | **negatives allowed**, or a **hop/stop limit** | **Bellman-Ford** | O(V·E) | Dijkstra's settle step is invalid with negatives; and BF's rounds are *indexed by edge count*, so a ≤k-edge cap is a free early stop |
| **All pairs** | any (incl. negative) | **Floyd-Warshall** | O(V³) | running BF from every source is O(V²·E); FW is 3 nested loops and beats it on dense graphs |

**The one-line version:** *unweighted → BFS · non-negative → Dijkstra · negatives or hop-cap →
Bellman-Ford · every-pair → Floyd-Warshall.*

**The purpose framing** (per [[feedback_algorithm_purpose_first]]): each is a **repair of the previous
one's broken assumption.** BFS assumes uniform cost → Dijkstra repairs it with a heap. Dijkstra assumes
no edge can lower a settled distance → Bellman-Ford repairs it by never settling. Bellman-Ford still
answers only one source → Floyd-Warshall repairs it by relaxing through every intermediate node. Learn
the assumptions, not four loops.

> ⚠️ **Known gap as of Jul 26, 2026: Floyd-Warshall has never been repped.** The other three are
> covered (127/994 BFS · 743/778 Dijkstra · 787 Bellman-Ford). **Now scheduled, not parked** —
> LC 1334 was promoted into the Advanced Graphs phase (Jul 26), which runs to Aug 9.

### Sparse vs dense — the *second* question, after the technique is picked (added Aug 11, 2026)

Picking Dijkstra or Prim's doesn't finish the job: **both have two implementations, and the graph's
density picks between them.** Came up on 1584 (Aug 11) — the array version was written, correctly, and
the reasoning behind it was only articulated when asked.

| | Edge count | Prim's / Dijkstra cost | Wins when |
|---|---|---|---|
| **Sparse** | E ≈ V (a few neighbors each, no matter how big V gets) | **heap** — O(E log V) | almost always in practice |
| **Dense** | E ≈ V² (near every pair connected) | **array scan** — O(V²) | E is large enough that `log V` is pure overhead |

**Concretely, at V = 1000 (1584's cap):** complete graph → E ≈ 500k, so heap = 500k · ~10 ≈ **5M** vs
array = **1M**. The array version wins by 5×. Flip to a sparse graph with E = 4V: heap = 4k · 10 = **40k**
vs array = still **1M**. The array version loses by 25×.

**Real-world handles:** road map is sparse (a million intersections, ~4 roads each). Social graph is
sparse (billions of people, hundreds of friends). **A geometry problem where any point can connect to
any other point is dense** — that's 1584, and it's the tell that the array version is right.

⚠️ **The complexity-statement trap this creates.** On a complete graph E = Θ(V²), so `O(V²)` and `O(E)`
are the same number and both "check out." **State it as O(V²) anyway.** `O(E)` claims the cost scales
with edge count — but the array implementation does V rounds of a V-wide scan and never touches an edge
list, so it stays O(V²) on a sparse graph too. The labels agree here by coincidence; only O(V²) survives
the follow-up *"so it's fast on a sparse graph, then?"* **Cue: name the bound after what the loops
actually do, not after what the graph happens to contain.**

## ⚡ Counter semantics in layered BFS — TEACH, Aug 10, 2026 (unrated)

*Written at the teach, per the Aug 10 schedule. Triggered by **127's second consecutive identical
off-by-one** (Jul 18 · Jul 21 · Aug 3, same break each time). Three reps did not fix it, which is a
teaching signal and not a repetition signal — same 540/19 rule that moved the Redis cards to a teach.
**Measured by 127 on Thu Aug 13**; the 3-day gap is deliberate.*

> ✅ **MEASURED Aug 13, 2026 — the teach HELD, cold, after three days.** 127 came back with `depth = 1`, increment **after** the level loop, and — the part that had broken three times — `return depth + 1` at the point of **discovery**, because the neighbour sits one layer below the word being expanded. Traced clean on `hit→hot→dot→dog→cog` → 5. **Zero hints on the counter.** The rep still logged 🟡, but on complexity, not on this — the code half was 🟢-grade. *This is the first teach in the repo to be measured on a deliberate gap and come back intact, and it is the outcome the teach/measure split was designed to produce.*

**⚠️ The lesson is NOT BFS.** 994 was flawless the same day 127 broke. The traversal is fine; the
**counter** is the gap.

### Decision 1 — where does the counter START?

Same path, three defensible answers, and nothing in the graph picks between them:

```
A —— B —— C

3   nodes total          (A, B, C)
2   edges / steps
1   node in between      (B)
```

**Only the question decides.** Start at **0** → you are counting **edges/steps**. Start at **1** → you are
counting **nodes**. Read it off the problem statement before writing the loop.

### Decision 2 — when does it INCREMENT?

**Once per layer drained. Never per node popped.**

```
    A                 layers:  {A} → {B, C} → {D}
   / \                true distance A→D = 2
  B   C
   \ /                per-node counting: pop A, B, C → 3 (or 4 counting D's own pop)
    D
```

**Per-node counting measures how WIDE the graph is. Distance is how DEEP it is.** Put five nodes in that
middle layer and the real distance is still 2, while a per-node counter says 5. Width is irrelevant to
distance, so it must never touch the counter.

The structural fix — snapshot the layer size *before* draining it:

```python
while queue:
    for _ in range(len(queue)):     # len() captured FIRST = exactly this layer
        node = queue.popleft()
        ...push neighbours...        # these land in the NEXT layer, not this one
    steps += 1                       # once per layer, OUTSIDE the inner loop
```

### 🔑 Why this survived three reps — the diagnostic that matters

**"Nodes visited" and "distance" are equal only when every layer holds exactly one node.**

```
LINE                          BRANCHING
A —— B —— C —— D                  A
                                 / \
                                B   C
                                 \ /
                                  D
visited before D:  3          visited before D:  3
distance to D:     3          distance to D:     2
        ↑ AGREE                       ↑ DIVERGE
```

**When you hand-trace, you draw a line** — and a line makes the broken version produce the correct answer.
The trace passes, the code ships wrong, and the next rep repeats it. **The test case that catches it is any
graph with two nodes in one layer.** Trace a branch, not a line.

*(Learner's own closing statement of it, unprompted: "the counter increments upon finishing a layer, not
upon visiting a node.")*

## ⚡ Edge-set / node-set bookkeeping — TEACH, Aug 12, 2026 (unrated)

**Trigger:** two consecutive reps lost to set construction, per the 540/19 rule — 269 (Aug 7, bugs #1
and #4) and 133 (Aug 9). Flagged at the Aug 10 build, run Aug 12. **Measured by 269 on Aug 17** — the
5-day gap is deliberate, and 269 was never opened during the teach.

**Both decisions derived by the learner on throwaway graphs.**

### Decision 1 — the node set comes from the INPUT, not from the edge map

```python
adjMap = {"a": ["b"], "b": ["c"]}
for node in adjMap:      # visits a, b — never c
```

A map keyed by source only contains nodes with **outgoing** edges. Sinks are invisible in it. Build the
node set in its own pass over the input universe.

*This is 269 bug #1: the Kahn's queue was seeded from `adjMap`, so `["ac","ab"]` dropped `a` entirely.*

### Decision 2 — node identity and edge recording are SEPARATE guards

```python
if neighbor not in seen:
    seen[neighbor] = Node(neighbor.val)
    queue.append(neighbor)
    clone.neighbors.append(seen[neighbor])   # WRONG — inside the guard
```

An undirected edge is discovered **twice**, once from each end; a node is created **once**. The guard's
job is *don't clone twice, don't enqueue twice* — it exists to terminate on cycles. Edge recording must
sit outside it, or every edge's second appearance is silently dropped (`1—2` clones to `2'.neighbors == []`).

*This is 133's single bug, and the same shape as 721's redundant `find` guard: one mechanism doing more
jobs than its condition justifies.*

### The test to apply

> **"Have I made this node?" and "Have I recorded this edge?" are different questions. One `if` cannot
> answer both.**

Related, from the same 269 rep (bug #4) — the mirror failure, *over*-recording rather than under: only the
**first** differing position between two words carries an edge. Continuing past it recorded `a→b` *and*
`b→a` from `["ab","ba"]`, a self-invented cycle. Same category: be deliberate about which edges exist.

## Call log — hits AND misses (the denominator)

*Started Aug 9, 2026. **Every fired gate gets a line here, whether or not it was a miss.*** A ledger
that records only misses has no denominator: "no entries" and "never asked" produce an identical file,
so the recognition axis of phase exit ends up judged on absent evidence. Detailed write-ups of misses
stay in the section below; this is the tally.

⚠️ **`R` marks a retry** — the tracker row names the method and the file sits in a pattern-named folder,
so a retry hit is *half-spoiled* and is **not** phase-exit evidence. Only new problems, weekly probes
([[project_recognition_probes]]), and label-stripped cold cues count toward the axis.

| Date | Problem | Call | Result |
|---|---|---|---|
| 2026-07-28 | 332 Reconstruct Itinerary | "BFS with directed edges" | ❌ miss ×2 (see below) |
| 2026-08-04 | 143 Reorder List | "Boyer-Moore" for the midpoint scan | ❌ name-only miss |
| 2026-08-09 | 721 Accounts Merge `R` | Union-Find over **account indices**, keyed by an email→index map; names rejected as keys because they repeat | ✅ hit |
| 2026-08-09 | 105 Construct Tree from Pre+In `R` | — | ⚠️ **gate not fired** — coach's miss, on the same day the gate became step 0. Learner opened the file and coded; no announcement to hook on. **Fire it when the board is restated, not only when they say "starting X."** |
| 2026-08-09 | 621 Task Scheduler `R` | "task with the most freq is the bottleneck → freqMap + maxHeap; n intervals means n+1 unique tasks per cycle, so do min(#tasks, n+1) at a time" | ✅ hit, **pre-code** — bottleneck identified before any structure was chosen, which is the right order |
| 2026-08-09 | 1011 Capacity to Ship `R` | "similar to koko eating banana; max is sum(weights) always works, so binary search max→sum for the min boundary" | ✅ hit, **pre-code** — and named the **sibling problem (875)** unprompted, which is the transfer the consolidation-rep model is built to produce. Bounds derived, not recalled |
| 2026-08-09 | 133 Clone Graph `R` | "connected, so one node at a time; BFS or DFS with an old→new map" | ✅ hit, **pre-code** — first firing under the tightened trigger (gate fired on handover). Traversal + the clone-identity map both named before any code |
| 2026-08-09 | 141 Linked List Cycle `R` | "basic tortoise and hare" | ✅ hit, but **stated after coding, not before** — gate was fired on the handover and the answer arrived with the finished solution. Counts as a hit (correct, and correctly *named*, which is where 143 slipped on Aug 4); doesn't test pre-code recognition |
| 2026-08-10 | **977 Squares of a Sorted Array** 🎯 **PROBE #1** | "squaring and sort is trivial → use two pointers, one at left and one at right, we can easily tell what is the next biggest number" | ✅ hit, **pre-code and unprompted** — written as a comment before any code, with no gate having been fired first. Full phase-exit evidence: unseen problem, label stripped, scaffolded outside `dsa/leetcode/`. 🟢, so **no tracker row** |

| 2026-08-10 | 503 Next Greater Element II `R` | "next greater element = monotonic stack; decreasing, so when something is increasing it *is* the next greater; store the index; circular = go through the array twice" | ✅ hit, **pre-code** — technique, the invariant's *purpose*, index-not-value, and the circularity reduction all named before any code |
| 2026-08-10 | 703 Kth Largest in Stream `R` | "kth largest means a minHeap of size k" | ✅ hit, **pre-code** — and the *size-k* clause is the load-bearing half; it's what makes space O(k) and what the complexity miss then failed to apply to the time bound |
| 2026-08-10 | 66 Plus One `R` | "only special case is the 9s — if 999, change each 9 to a 0 and put a 1 in front; otherwise just add 1" | ✅ hit, **pre-code** — the *entire* problem is the carry case, and it was isolated before any code |
| 2026-08-11 | 1584 Min Cost to Connect All Points `R` | "Minimum Spanning Tree, built via Prim's. Expand the component to the nearest node not yet in it; distance array relaxed against the absorbed candidate; visited set holds what's already in the component; index as the key" | ✅ hit, **pre-code** — the comment was the call, written before any code. Named the technique *and* the invariant (`distance[i]` = cheapest edge from the tree to `i`), which is the part that actually decides whether the code comes out right. See the density note below |
| 2026-08-11 | 323 Connected Components (DFS) `R` | "construct an adjMap, add a visited set, loop on n, DFS to mark visited" | ✅ hit, **pre-code** — though heavily half-spoiled even by retry standards: the tracker row names the method *and* today's rep was announced as the DFS one. Recognition was never in question here; the miss was on the **cost** of the traversal, not its identity |
| 2026-08-11 | 875 Koko Eating Bananas `R` | "h ≥ len(piles) so we can always finish; max(piles) always works; we need at least 1 banana/hr — so the range is 1 to max(piles), min-boundary binary search" | ✅ hit, **pre-code** — and the good part is that the **bounds were derived, not recalled**: both ends were justified from the constraints in the comment before any code. That derivation is what made the complexity answer right too (see the 1011 transfer note in `complexity_gotchas.md`) |
| 2026-08-11 | 150 Evaluate RPN (**new**) | "push when we see a number, pop two when we see an operator" | ⚠️ **not evidence — pre-spoiled.** The scaffold path is `dsa/leetcode/stack/` and the docstring header reads `Pattern: stack`, so the technique was named before the learner opened the file; the coach then walked the RPN notation, which is most of the mechanism. **A new problem is only recognition evidence if nothing named the technique** — logging it as a hit would inflate the denominator with a freebie. This is the `<pattern>/` scaffold-path defect ([[project_upstream_candidates]]) showing up on a *new* problem rather than a retry |
| 2026-08-11 | **202 Happy Number** 🎯 **PROBE #2** | pre-code comment was *"we need to define an end point for both success and failure"* — a plan, not a technique. Correct call (**cycle detection → seen-set**) arrived only after the coach challenged the termination condition | ⚠️ **partial — did not fire cold.** See the write-up below. 🟡, so it **earns a tracker row** |
| 2026-08-12 | 211 Add and Search Words `R` | "Word Data Structure is Trie… searching without wildcard is trivial; with wildcard we skip the current node and look at every child; substring adds complexity so use indices" | ✅ hit, **pre-code** — the comment named the structure, the branching feature `.` forces, *and* the index-not-substring decision. Half-spoiled (retry, folder `trie/`), so **not phase-exit evidence**; the non-obvious half — fan out over `children.values()` rather than index one — was the learner's own |
| 2026-08-12 | 778 Swim in Rising Water `R` | "Dijkstra at a glance because we have an end goal destination… minHeap instead of queue, visited set; no adj map since we just look at the closest 4; we do need to keep track of time vs our min node in the heap" | ✅ hit, **pre-code** — and the last clause is the good part: it names the *tension the problem actually turns on* (water level vs heap minimum) before any code. The bug that followed was event-placement, not recognition. Half-spoiled (retry; tracker row reads *Dijkstra / Min-Heap*) |
| 2026-08-12 | 271 Encode and Decode Strings `R` | "prefix length framing / `len#str`" | ✅ hit, **pre-code** — terse but complete: it names the scheme *and* the frame format, which is the whole design decision. Half-spoiled (retry). The follow-through was the real evidence: slicing by count rather than scanning for the delimiter is what makes a `#` inside the payload a non-issue, and that was never discussed |
| 2026-08-12 | 155 Min Stack (**new**) | — | ⚠️ **not measurable — pre-spoiled.** Scaffold path is `dsa/leetcode/stack/` and the docstring header reads `Pattern: stack`, so the technique was named before the file was opened. Second occurrence of this defect on a *new* problem (150, Aug 11). The un-spoiled half — O(1) `getMin` — was gated separately and **not** solved: deque, then single variable, then asked to be walked through |
| 2026-08-13 | 121 Best Time to Buy/Sell Stock `R` | "two pointer; left moves if and only if right is smaller" | ✅ hit, **pre-code and unprompted** — written as a comment before any code, with no gate fired first. Terse but complete: it names the technique *and* the only invariant that makes it correct (`l` resets to `r` on a new minimum, so `l` is always the running min index). Half-spoiled (retry), so not phase-exit evidence |
| 2026-08-13 | 901 Online Stock Span `R` | "stack of tuples… a decreasing stack where each value holds its own span" | ✅ hit on the **structure**, pre-code — but the gate question (what does *streaming* constrain?) was never answered, and the learner's own words were *"doesn't make sense"*. ⚠️ **Worth separating: naming the structure is not the same as holding the invariant.** The call was right and the *mechanism* — that the pop is a loop and each pop hands its span forward — was coach-supplied. Half-spoiled (retry, folder `stack/`) |
| 2026-08-13 | 680 Valid Palindrome II `R` | "deleting a single element just means we check again after skipping the current unmatched — so standard valid palindrome, but if it's false, check both sides" | ✅ hit, **pre-code** — and the load-bearing half is *"check both sides"*: the mismatch is symmetric and you cannot know which character to drop, so both branches are required. That is the one feature separating this from plain 125. Half-spoiled (retry, folder `two_pointers/`) |
| 2026-08-13 | 127 Word Ladder `R` | "this is just BFS with an extra step of creating the adjMap based on wildcard… moving one character at a time means a word like `hit` can be `.it`, `h.t` or `hi.`" | ✅ hit, **pre-code** — and the second clause is the whole modeling decision: the graph is **not given**, it is *constructed*, and the wildcard is what makes neighbour lookup O(1) instead of an all-pairs scan. Half-spoiled (retry, folder `graphs/`). ⚠️ **See 815 Bus Routes in the expansion queue** — its trigger is `solved:127` and its content is the same modeling axis (are the nodes stops or routes?), now live |
| 2026-08-13 | 146 LRU Cache `R` | "doubly linked list, one side MRU the other LRU, so two dummy nodes… capacity means we track size… a map of key to node" | ✅ hit, **pre-code** — named all three moving parts *and their reasons* before any code. The dummy-nodes clause is the load-bearing half: it is what makes `insert`/`delete` branch-free at the ends, which is where this problem is normally lost. Half-spoiled (retry) |
| 2026-08-13 | 138 Copy List w/ Random Pointer `R` | "deep copy, so we do an old-to-new map" | ✅ hit, **pre-code** — terse, but it is the entire answer to *why `random` is hard*: the target of a random pointer may not exist yet when you reach it, so identity has to be resolved through a map rather than by position. Half-spoiled (retry) |
| 2026-08-14 | 743 Network Delay Time `R` | "Dijkstra’s Algorithm · Min Heap, Visited Set and adjMap" | ✅ hit on the **technique**, pre-code — but ⚠️ **the invariant was not held**: the comment names the `visited` set without saying *when* a node enters it, and the code marked on **push**. Second occurrence of the 901 split — naming the structure is not the same as holding the invariant. Half-spoiled (retry; tracker row reads *Dijkstra*, folder `graphs/`) |
| 2026-08-14 | 155 Min Stack `R` | "we keep the min value at each insert" | ✅ hit, **pre-code** — the whole design in one clause: the min travels *with* each entry, which is what makes `getMin` O(1) without a scan. ⚠️ **Measures Wednesday’s teach, not cold recognition** — this design was coach-supplied Aug 12, so the hit is evidence the teach stuck, not evidence of independent recall. Half-spoiled (retry, folder `stack/`) |
| 2026-08-14 | 739 Daily Temperatures (**new**) | "definitely a monotonic stack problem… we need to go from end to beginning… stack should be monotonically increasing / so we are incrementing when the number goes down" | ⚠️ **partial, and only half-measurable.** ✅ Technique + direction were named pre-code and unaided. ❌ The **picking feature was absent** — the answer is a *distance*, so the stack stores **indices**; the learner had named exactly that on **503 (Aug 10: "store the index")**, so this is a **regression on the same technique**, four days later. Both label clauses are *individually true* (bottom→top decreasing, top→bottom increasing) and therefore **neither is codeable** — the invariant ("every element below the top is warmer than the one above") was never stated. Third occurrence of the `<pattern>/` scaffold-path defect on a **new** problem (150 Aug 11, 155 Aug 12): folder `stack/` + header `Pattern: stack` named the technique before the file was opened, so the ✅ half is **not** phase-exit evidence either. ⚠️ **Coach confirmed the call as a hit on the technique leg alone and did not check the third leg** — see `self_eval_log.md` |
| 2026-08-14 (late) | **332 Reconstruct Itinerary** `R` | "not Dijkstra's, we don't have a destination nor edge weight… start with JFK and the ending node must have nowhere else to go… DFS, get to end node first then take care of call stack… **adjacency map, visited holds edges not nodes**" | ✅ **hit, pre-code, and the strongest call in the ledger on the picking-feature leg.** *Edges not nodes* is the exact Eulerian-vs-Hamiltonian discriminator this file's own gate description uses as its worked example, and *"get to end node first then take care of the call stack"* is the post-order append. Half-spoiled on the technique leg (retry; folder `graphs/`, tracker row reads *Hierholzer*) — but neither of those names the two clauses above, which were the learner's own. ⚠️⚠️ **AND THE REP STILL COULDN'T BE WRITTEN — this is the cleanest recognition/execution split the repo has produced.** Both attempts returned wrong output (2nd returned `[]`); the learner said *"I don't think I have Hierholzer locked down at all"* while their comment demonstrated they had two of its three pieces. **The gap was purely bookkeeping**: `for` + `return` instead of `while` + *delete*, i.e. consuming the edge rather than marking it. **Read this as direct evidence for the two-axis phase-exit gate** — recognition passed and execution failed on the *same rep*, so a single rating could not have expressed it. Converted to a **teach (unrated)**; see the schedule |
| 2026-08-14 (late) | 503 Next Greater Element II `R` | "next greater = monotonically decreasing stack… keep the index in the stack so we can set the next greater for prior index… circular means we need to go through twice" | ⚠️ **NOT MEASURABLE — spoiled by the coach’s own debrief.** All three legs are present and would otherwise be a model ✅ — but the 739 debrief, three messages earlier the same night, **quoted this problem’s Aug 10 call verbatim** (*"store the index"*) while writing up the regression. Leg 3 was handed over, so crediting it would inflate the denominator with a freebie. ⚠️ **New spoiler vector: cross-problem, via my own write-up** — the existing not-measurable rule only covers `<pattern>/` folders and docstring headers. **A debrief that quotes a sibling problem’s pre-code call has spoiled that problem’s next rep; note it at the time.** Execution was genuinely unaided and rated 🟢. See `self_eval_log.md` || 2026-08-15 | 572 Subtree of Another Tree `R` | "subtree means there should be a tree in root such that it is exactly same as subroot… we start matching by checking before we go down recursively… so this is preorder DFS… find where root.val == subroot.val, then recursively go down" | ⚠️ **Partial — and the gap in the comment is *verbatim* the gap in the code.** ✅ Technique (preorder DFS) named pre-code, and the first clause states **both jobs**: *"a tree in root"* (search) and *"exactly same as subRoot"* (identity). ❌ The picking feature — that those are **two different questions and one function can only answer one** — was never drawn, and the code duly implemented both with a single function. It broke twice for that one reason: first committing to the identity check on any value match (self-caught from a counterexample), then calling the *search* function from inside the *match* arm (coach-supplied). ⭐ **The nearest neighbour is 100 Same Tree, which is already in this technique's problem list** — 572 *is* 100 plus an outer search, and naming that relationship is the whole call. Half-spoiled on the technique leg (retry, folder `trees/`) |
| 2026-08-15 | 787 Cheapest Flights Within K Stops `R` | "bellman ford because it is the only shortest path algorithm that allows us to limit number of steps" | ✅ **Hit, pre-code, and it is the picking feature rather than the label.** Bellman-Ford relaxes in **rounds**, and a round *is* one more edge of path length — which is precisely what Dijkstra cannot express, since it settles greedily by cost and holds no handle on hop count. That reason is the discriminator for this problem and it is not written in either spoiler surface. Half-spoiled on the technique leg (retry; folder `graphs/`, tracker row reads *Bellman-Ford*) — but neither names the rounds↔edges correspondence, which was the learner's own || 2026-08-15 | 1334 Find the City `R` | "we know it is floyd warshall but how can I tell by looking at the problem? we are not looking for a specific node to get to, so thats why it is not bellman ford or dijkstra's" | ⚠️ **Miss on the picking feature — and the learner flagged it themselves**, which is the honest version of a spoiled retry: the technique was already known (folder `graphs/`, tracker row reads *Floyd-Warshall*), so they asked for the discriminator instead of pretending to recall it. ❌ *"Not looking for a specific node to get to"* does **not** separate this from Dijkstra — Dijkstra is single-**source**, all-**destinations**, so one run already gives every destination. The real clause is one level up: **every node is a source**, i.e. all-pairs. Coach-supplied. ⭐ **The second half was then taken cleanly**: told that all-pairs does not *force* Floyd-Warshall (Dijkstra-from-every-node is also correct), the learner read the constraint themselves and landed on *"a small enough constraint"* — `n ≤ 100` makes V³ affordable. **The durable form is theirs: all-pairs picks the family, the constraint picks the member** — same axis as 1584's sparse-vs-dense || 2026-08-15 | 853 Car Fleet (**new**) | "isn't 22 a backtracking problem" → then on 853: "we can just consider two indices a fleet once the next value is greater, so this is a monotonic stack problem" | ✅ **Hit on the technique, and the FIRST new problem in the ledger where the scaffold path did not spoil it — because the path was WRONG and the learner overrode it.** 22 Generate Parentheses had been scaffolded into `stack/` (the coach followed NC150's shelving); the learner rejected the label unprompted and asked *"is there a stack method that I should be focused on right now?"* Both halves correct — 22 moved to the Backtracking phase and 853 took the slot. ⚠️ **On 853 itself the invariant was NOT held**: monotonic stack named, but *"the next value is greater"* never said greater **what**, and the answer (time to target) took three exchanges plus a correction that a *meeting point* is a per-PAIR quantity — which is exactly what makes the naive solution O(n²) — where the stack needs a per-CAR one. **4th occurrence of the 901/743/739 split: naming the structure is not holding the invariant.** Execution then stalled and the session was converted to a **teach (unrated)**; rated rep Mon Aug 17 |
| 2026-08-15 | 695 Max Area of Island `R` | "basic bfs/dfs problem… we hold a maxArea variable, go through the grid, if we find land, get that land's area and update maxArea… let's do BFS today" | ✅ **Hit, pre-code and unprompted** — and the load-bearing clause is *"get that land's **area**"*, which is the one feature separating this from 200 Number of Islands (count the components vs measure the largest). Half-spoiled on the technique leg (retry, folder `graphs/`), but the area-vs-count distinction is in neither spoiler surface. ⭐ **Ran BFS on a problem the tracker titles "(DFS)"** — a deliberate variant choice, now dual-credited to Grid BFS in `techniques.yml` || 2026-08-16 | 🎯 **PROBE #3 — 69 Sqrt(x)** (Easy, unseen, label stripped) | "what is square root, it is just y^2 = x where we are solving for y — what if we do binary search on the result… we are looking for the largest number" whose square does not exceed x | ✅ **Hit, cold, and the cleanest recognition evidence the ledger holds.** ⭐ **There is no array in this problem** — nothing to pattern-match a shape against, so the call could only come from seeing the ANSWER SPACE as searchable. The learner derived it from `y² = x` rather than recognising a silhouette, which is the distinction the whole probe mechanism exists to measure. **Fully unspoiled**: `dsa/probes/`, no pattern in the path, no technique in the docstring, and the problem came out of the company-wise pull rather than the coach's pick. Code correct first pass including the `(l + r + 1) // 2` upper-boundary bias — the one thing that breaks this problem — and commented as deliberate. ⭐ **Complexity was O(log x), log of the VALUE not of an array length**, unprompted: that is exactly the 1011 miss from Aug 9 (*"binary is log n"*) firing correctly a week later on a problem with no `n` in it. **🟢 Clean, no tracker row** (probe rule; the learner confirmed the probe's job is the derivation, not coverage). Probes now stand at **3 run / 1 row** || 2026-08-16 | 261 Graph Valid Tree (DFS) `R` | "undirected acyclic graph with n vertices must have n - 1 edges to make a tree… one more thing to verify is if this is acyclic or not" | ⚠️ **Partial, and the technique leg is NOT evidence — the coach spoiled it.** The learner asked whether the variant mattered; answering (DFS, because that is the row due today) named the technique before any call was made. ✅ What IS theirs is the **invariant, pre-code**: `n−1` edges. ⭐ **The second clause is the interesting one** — *"one more thing to verify is if this is acyclic"* records that they knew a gap existed, then wrote code that closes it **implicitly** and asked afterwards why no explicit cycle check was needed. Correct code, unfinished model; the question came after the solve, not instead of it || 2026-08-16 | 496 Next Greater Element I `R` | "next greater element = monotonic stack… decreasing stack and we update greater based on top item in stack… **we should store index here in the stack**" | ✅ **Hit, pre-code.** ⭐ **The last clause is a transfer, two days old**: on 739 (Aug 14) the stack held *temperatures*, the answer was a distance between days, and *store indices* was coach-supplied — the single thing that carried that 🟡. Here it was written before any code. ⚠️ **Worth knowing it was not actually required here**: indices are forced when the answer is a **distance** (739), not when it is a **value** (496), where storing values reads shorter. Over-caution costs nothing; knowing which problems force it is the transferable half. Half-spoiled on the technique leg (retry, folder `stack/`) || 2026-08-16 | 80 Remove Duplicates II `R` | "array is sorted and allowed 1 duplicate… two pointers, **l - 2 is the number that is locked down**, anything before l is valid" | ✅ **Hit, pre-code**, and the second clause is the invariant that *is* this problem — the write pointer compares against `l-2`, not against its neighbour, which is the only thing separating it from 26. Unaided. Half-spoiled (retry, folder `two_pointers/`). ⚠️ **Execution carried a boundary bug the recognition did not predict**: `l = r = 2` returns 2 for a one-element array. See `complexity_gotchas.md` — logged as a boundary finding, not a complexity one || 2026-08-16 | 75 Sort Colors `R` | "Dutch Flag algorithm… everything before l is set in place with 0s, r tracks 2s… everything before t is 0s and 1s set… **when we swap with r, we need to not move t for us to recheck the value**" | ✅ **Hit, pre-code, and the most complete call of the day.** Names the technique, **both** loop invariants, and the trap — the last clause is the single thing that breaks this problem, written before any code, and the `t -= 1` / `t += 1` pairing implements it deliberately rather than by accident. Half-spoiled on the technique leg (retry). ⭐ Exhaustive verification: **every 0/1/2 array up to length 7** (3,280) plus 5,000 randomized, all pass || 2026-08-16 | 98 Validate BST `R` | "binary search tree, **not balanced** binary search tree… set a min and max boundary for each value… if we go left, we set max as root; if we go right, we set min as root" | ✅ **Hit, pre-code**, naming the boundary technique **and** which side updates which bound — the part that separates this from a parent-only comparison. Half-spoiled (retry, folder `trees/`). ⭐ The first clause is the one that mattered: *not balanced* was written before any code and drove the complexity answer |
| 2026-08-17 | 853 Car Fleet `R` (**rated rep after the Aug 15 teach**) | "since we can't pass, starting position actually matters a lot, basically **no one can pass the car in front** — because of this we will sort desc" → "fastest for each car is **(target - carPosition) / carSpeed**… if a car is not to pass, it becomes a second fleet, so we use an increasingStack that will hold **time to finish**" | ✅ **Hit on the technique AND the invariant — the direct repair of the Aug 15 entry above, which was the 4th occurrence of the 901/743/739 split.** On Aug 15 the structure was named and *"the next value is greater"* never said greater **what**, and the per-car quantity took three exchanges plus a coach correction. Today both legs were written pre-code and unaided: the discriminator (*no one can pass the front car* → sort descending by position) and the quantity the stack holds (*time to target*, per car, not the per-pair meeting point). ⭐ **Execution followed the recognition this time** — correct first pass, 10/10 on coach cases including ties and catch-exactly-at-target, which is the opposite of the 332 recognition/execution split. ⚠️ **Measures the teach at a two-day gap, not cold recognition** — same caveat as 155 (Aug 14): this mechanism was coach-supplied Aug 15, so the hit is evidence the teach stuck. That is what the provisional 🟢/Streak-0 (+10, → Aug 27) exists to check. Half-spoiled on the technique leg (retry, folder `stack/`). ⭐ **One thing the learner did NOT notice, coach-raised, no rating effect:** `increasingStack` is never popped and is read only via `[-1]` and `len()` — it is a running maximum plus a counter, so this monotonic-stack problem does not actually need a stack. Space stays O(n) regardless (the `cars` tuple array). Knowing *which* problems in the family force the pops is the transferable half. ⭐ **Comment self-repair:** the pre-code note described *"neuter it and set it to the current car's position and speed"* — machinery the code never built; told so, the learner appended *"we can accomplish this by just doing nothing"* rather than adding the machinery |
| 2026-08-17 | 19 Remove Nth Node — **Postorder Recursion** `R` | "nth node from the end means we want to point **n + 1's next to n - 1**… this is also postorder since we have to **get to the end first before we increment**" | ✅ **Hit, pre-code, and the second clause is the picking feature.** *Get to the end first before you increment* is exactly why this is post-order and not pre-order — distance-from-the-end is not knowable on the way down, which is the whole reason 19 has a parked Preorder variant flagged as "the most contrived direction." The first clause states the pointer surgery in end-distance indexing and is correct as written. Correct first pass, 10/10 on coach cases including both head-removal paths. Complexity **volunteered unasked** and correct on both axes, with the recursion-stack itemization (*O(n) space for the call stack*) — that is the `recursion stack = O(depth)` category from `complexity_gotchas.md` firing unprompted. Half-spoiled on the technique leg (retry; folder `linked_list/`, tracker row reads *Postorder Recursion*) — but the end-distance reasoning is in neither spoiler surface. ⭐ Coach-raised, no rating effect: the inner `if node.next:` guard can never be false, since `nodeCounter == n + 1` implies `n ≥ 1` nodes follow — it is implied by the invariant they had already stated, not defended by it |
| 2026-08-17 | 19 Remove Nth Node — **Iterative** `R` | "n from the end means **len - n from the front**… so len - n - 1's next to len - n + 1… now we try to set from dummyNode onwards, **len is now 1 longer, so plus 1**" | ✅ **Hit, pre-code.** The load-bearing clause is the **index translation** — end-relative to front-relative — which is the one thing this variant needs and the postorder variant does not. The third clause shows the dummy-node offset was reasoned about rather than patched in after a failure, which is where this problem is normally lost. ⭐ **Exhaustively verified: every length 1–12 × every valid n, all pass.** Half-spoiled on the technique leg (retry, tracker row reads *Iterative*). ⚠️ **Complexity axis mislabeled**: *"O(1) space… **O(n) space** to go through the linked list"* — the second is **time**. Both VALUES correct and the O(1) space itemization (dummy + counters) correct, so this is a **wording slip, not an analysis miss** — same class as 143's Boyer-Moore/Floyd name swap (Aug 4), which likewise did not cap the rating. **Freebie NOT spent.** ⭐ Coach-raised, no rating effect: the `else` guarding the advance makes the loop stall one tick after the splice, so termination depends on `counter` being strictly monotonic — safe here, an infinite loop under `>=`. Advancing unconditionally makes termination trivial. ⭐ **This rep produced a coverage finding:** three variants tracked, none of them the **one-pass two-pointer gap** method — now in the Waiting Room on `graduates:19-iterative + graduates:19-postorder` |
| 2026-08-17 | 269 Alien Dictionary `R` | "map first letter where they differ, so make sure to **stop when we find the first diff**… so this is topographical sort since we have to have **certain letters beforehand**… which means we need to create a counter map" | ✅ **Hit, pre-code, all three legs.** *Certain letters beforehand* is the prerequisite relation stated as a property of the problem rather than as a label, and *create a counter map* names Kahn's mechanism (indegree) without being asked. The first clause is the **modeling decision**: the edges are not given, they are *derived* from adjacent word pairs — and only the first differing position carries information. Half-spoiled on the technique leg (retry; folder `graphs/`) — but the first-difference rule is in neither spoiler surface. ⚠️⚠️ **AND THIS IS THE 4th CONSECUTIVE RECOGNITION-PASSES / EXECUTION-FAILS SPLIT ON THIS PROBLEM** — the pre-code comment states the first-difference rule, and the code then **breaks in only one branch** and compares past it. **The learner's own stated invariant was the bug.** Same shape as 332 (Aug 14) and as 743/901/739: naming the invariant is not holding it — but sharper here, because the invariant was not merely unstated, it was **written down and then contradicted eight lines later.** ⭐ **This is the strongest argument in the ledger for the two-axis phase-exit gate**: four reps, recognition clean every time, and `Topological Sort` still has this problem at 🟡. A single rating cannot express that. ⚠️ **Read this as evidence AGAINST re-teaching topological sort** — the concept is not missing. The gap is Kahn's bookkeeping (first-difference-only, completeness check), which is a drill, not a teach. See `stuck_log.md` 2026-08-17 |

### Probe #1 — what it actually measured (Aug 10, 2026)

**The call had all three parts without being asked for them:** the nearest alternative was *named and
priced* (`squaring and sort is trivial` — i.e. correct but O(n log n)), the technique was named
(converging two pointers), and the **picking feature** was stated operationally — *the ends tell you the
next biggest*. That third clause is the one that matters and the one that is usually missing; a call that
stops at "two pointers" is a label, not a recognition.

**What makes it real evidence, unlike a retry:** nothing named the technique in advance. The folder was
`dsa/probes/`, the header said *"you name it"*, and no neighbouring problem was mentioned. Compare the
`R`-marked rows above, which are all half-spoiled by a pattern-named folder and a method-named tracker row.

**Complexity, itemized without a nudge:** O(n) time as *two* passes named separately (the two-pointer
sweep **and** the `reverse`), O(1) space **with the convention stated** (`we don't count result`) rather
than asserted. Stating the convention is the senior form — the exclusion is safe here specifically because
the output is mandatory and write-only, so it carries no information about the algorithm.

⚠️ **Sourcing note.** 977 was picked from the coach's own recall of the LC catalogue, not from the
interview-frequency pool. On the learner's correction (*"pull from the list we discussed from interviews"*)
probe #2 (202 Happy Number) was drawn via `scripts/pull_interview.py` instead. **Future probes come from
the tool** — it excludes tracked problems and gates on learned patterns, which recall cannot guarantee.

### Probe #2 — what it actually measured (Aug 11, 2026)

**Result: 🟡 Shaky, and the first probe to earn a tracker row.**

**The gate did not fire cold, and that is the finding.** The pre-code comment was *"we need to define an
end point for both success and failure"* — a **statement of the sub-goal, not a technique**. Compare 977's
call, which named the alternative, the technique, and the picking feature before any code. A plan-shaped
comment is the failure mode to watch for: it *looks* like a recognition call sitting in the right place in
the file, so it passes a glance, but it commits to no technique and therefore can't be right or wrong.

**Cue: if the comment would still be true for a different algorithm, it isn't a call.** "Define an end
point" is true of every terminating loop ever written.

**What did work — the correction came from being asked to defend, not from being told.** The first draft
terminated on *"a single digit that isn't 1 ⟹ unhappy."* Challenged with *"convince me that's true"*, the
learner immediately abandoned it for **"we need to check if we've seen this number before"** — the real
technique, self-generated. **Keep that move**: challenging the learner's own line produced the insight,
where naming the technique would have spent it.

> 🧾 **Footnote worth keeping, because the first draft was not actually wrong.** *"Single digit ≠ 1 ⟹
> unhappy"* is **true in base 10** — the only cycle is 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4, and it
> passes through 4, so every unhappy chain does hit a single digit. It was abandoned because it was
> **undefendable, not because it was incorrect** — it rests on a number-theoretic fact you'd have to
> already know. That is the right call in an interview: a correct answer you cannot justify reads as a
> memorized trick, and the general mechanism (cycle detection) costs nothing extra here.

**Complexity — new problem, so the double freebie applies; no cap fired.** Called it O(1)/O(1). Space is
right. **Time is O(log n)** — the first digit split is proportional to the digit count, and it is the only
n-dependent work in the whole algorithm. The bounding argument was coach-supplied on request:

> after one step the value is ≤ 10 × 9² = **810** regardless of how large `n` was; anything ≤ 810 has ≤ 3
> digits so from step two onward it is ≤ 3 × 9² = **243**. The walk is therefore confined to 243 possible
> values and the seen-set forces a halt within 243 steps by pigeonhole — **constant, independent of n.**

**Generalizable, and this is the keeper:** *when the state space is bounded by the problem's own
arithmetic, the loop count is constant even though the input isn't.* **Say the collapse before quoting the
number** — "O(1)" alone sounds like hand-waving; "it collapses to ≤243 after two steps, so O(1)" is
visibly reasoned.

⚠️ **Cadence note for the Aug 17 build.** Two probes run, one row created. The standing exception —
*probes bypass the surplus gate because a 🟢 probe costs nothing forever* — is priced on a low
row-creation rate. 202 bills ~73 units/year. **One 🟡 in two is not a trend; it is a data point with a
number attached.** Re-derive the rate at the build rather than renewing or killing the exception on feel.

## Miss ledger

*(dated line per miss: problem · what they called · correct call · the picking feature they missed)*

> ⚠️ **Reading note, Jul 28 → Aug 4.** The 332 entry below names the technique, and **332's rated
> re-rep is Tue Aug 4**. Reading it before that rep spends the measurement. Skip this section until
> Aug 4 if you want that rating to mean anything.

- **2026-07-28 · 332 Reconstruct Itinerary** — called it *"BFS with directed edges."* Correct call:
  **Eulerian path → Hierholzer's** (DFS-based). Two misses in one:
  - **BFS vs DFS** — self-corrected on one push, by reading their own plan back (*pop the smallest
    ticket and follow it, then follow that airport's smallest*) and noticing it commits down a single
    path rather than expanding level by level. **Cue: "what does my own plan actually do — go deep, or
    go wide?"** — the plan was already depth-first before the label was.
  - **Eulerian vs Hamiltonian — never encoded.** Could not name the path class at all. Notably the
    *discriminator* was already correct in the pre-code comment (*"we are marking edges as visited not
    nodes"*), so this was a missing **label**, not a missing concept. Worth separating those two
    failure kinds when rating: a missing name is cheap to fix, a missing discriminator is not.

- **2026-08-04 · 143 Reorder List** — **name-only miss, code was correct.** Called the slow/fast
  midpoint scan **"Boyer-Moore."** Correct call: **Floyd's tortoise and hare.** Boyer-Moore is the
  *voting* algorithm (169 / 229) — and 229 was repped the day before, which is where the crossed wire
  came from. Same failure kind as 332's Eulerian/Hamiltonian slip: a **missing label, not a missing
  discriminator** — the mechanism was implemented correctly on the first pass. Cheap to fix, so it did
  not cap the rating. **Learner's chosen handle: "tortoise and hare."**
  **Cue: two pointer names that both start with a person's name are not interchangeable — Boyer-Moore
  counts votes over an array; Floyd walks a linked structure at two speeds.**

- **2026-08-18 · 332 Reconstruct Itinerary** — ✅ **HIT, cold and unprompted.** Fired before any code:
  *"this is literally an iterative DFS but we are marking edges not nodes."* That is the **discriminator
  itself**, volunteered without the label being asked for, and it is the direct repair of the Jul 28
  entry above — where the same discriminator was already correct in the pre-code comment but the
  **name** (Eulerian vs Hamiltonian) could not be produced at all. The name is now attached to the
  feature. **Caveat on how much this counts:** 332 is a retry and the tracker row names Hierholzer, so
  the technique was half-given — read this as the label finally sticking, not as evidence for the
  recognition axis of phase exit. The measured reps stay **2097** (unseen, start node must be derived)
  and the weekly probes.

- **2026-08-18 · 235 Lowest Common Ancestor of a BST** — ✅ **HIT.** Pre-code comment carried the call and
  the discriminator together: *"BST, so if both are smaller, we go left, if both are bigger we go right"*
  plus *"we allow a node to be its own parent so we need to check equality."* The picking feature is the
  **ordering property**, which turns a search of both subtrees into a pruned descent — the exact thing 236
  (plain binary tree) does not give you. Coded correct on the first pass with zero hints. **Same caveat as
  332 the same day:** a retry names its own technique, so this is the label sticking rather than evidence
  for the recognition axis of phase exit.
