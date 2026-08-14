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

## 🟡 150. Evaluate Reverse Polish Notation — 2026-08-11 *(first exposure; phase intake)*
**Sticking point**: **not the stack — the spec.** The algorithm was in hand within a minute of
understanding the notation; all three bugs were places where *the problem statement disagreed with a
language default and it went unnoticed.* (1) **Operand order** — `numsArray[0]` is the *first pop*, which
is the **right-hand** operand, so `13 5 /` computed `5/13`; matters only for `-` and `/`, so it hides
behind `+`/`*`. (2) **`//` floors, the spec truncates toward zero** — they differ only when the quotient
is negative, so examples 1 and 2 pass and example 3 (already in the docstring) is the one that fails:
`6 // -132 = -1`, wanted `0`. ⚠️ **This one took two rounds** — flagged, not fixed, and then `6 // -132`
was still read as `0` when asked directly. (3) `["5"]` — a single operand is valid input, the loop never
runs an operator, and the early return meant the function fell off the end.
**The fix was theirs and is better than the usual one:** switching `//` → `/` leaves a float on the stack,
and since every pop already goes through `int()`, the truncation-toward-zero happens for free — no
`int(a/b)` special-case needed.
**Cue: when a problem's statement bothers to *specify* an arithmetic behaviour (rounding direction, overflow,
tie-breaks), that is a warning that your language's default is the other one. Go check it, don't assume.**
*(Complexity was fine — O(n)/O(n), no freebie spent. One framing correction: `n/2` **is** O(n), not "O(n)
for simplicity" — big-O discards constant factors by definition. The nice itemization is "at most ~n/2,
since a valid RPN with k operands has exactly k−1 operators.")*
*(⚠️ Recognition was NOT measurable here — the scaffold path `stack/` and the docstring's `Pattern: stack`
named the technique, and the coach then walked the notation. Logged as not-evidence.)*

---

## 🟡 202. Happy Number — 2026-08-11 *(🎯 recognition probe #2; first exposure)*
**Sticking point**: **shared mutable state — `seen` was declared as a class attribute**, so it was created
once at import and survived across calls. `Solution().isHappy(19)` then a *brand-new* `Solution().isHappy(82)`
returns False, and 82 is happy. Not self-caught; the failing pair was supplied. First instinct on the fix was
also the wrong direction — *"it should have lived outside the class"* — which is the same lifetime, just
wider. Landed correctly on a local + closure once the scope ladder (module → class → instance → local) was laid out.
**Cue: a container holding the working state of ONE question must be born and die with that question. If it
sits at class or module level it outlives the answer, and the second caller inherits the first caller's set.**
*(Secondary: the recognition call never fired cold — see `recognition_gotchas.md` probe #2 write-up. The
pre-code comment stated a sub-goal, not a technique.)*

---

## 🟡 1334. Find the City (Floyd-Warshall) — 2026-08-05 *(2nd attempt; measurement half of the Jul 31 teach)*
**Sticking point**: **the teach took on recognition, not on the data structure.** Named Floyd-Warshall cold
from "all pairs + n ≤ 100" before writing a line, and stated the relaxation premise correctly in the pre-code
comment — then started building a `defaultdict` **adjacency map**, which cannot answer `dist[i][j]` for a
non-adjacent pair. Redirect to the n×n matrix was supplied; the three init cases (`inf` / `0` / weight) were
prompted rather than derived. Loop ordering (midpoint outermost) was correct unaided. Two bugs in the final
scan, neither self-caught: (1) `return city` instead of `return minCity` — returns the loop variable, i.e.
always `n-1`, which *accidentally passes Example 1*; (2) strict `<` on the count comparison, so ties kept the
**smallest** index when the problem asks for the **greatest** — Example 1 is built to catch exactly this.
Complexity correct unaided (O(n³) / O(n²), both with itemized why-clauses).
**Cue: Floyd-Warshall never traverses — it never asks "who are i's neighbours?", it asks "what is the best
known cost i→j?" for every pair, adjacent or not. An adjacency list cannot answer that. If you reach for
`defaultdict(list)` on an all-pairs problem, you have reached for the wrong shape.**
*(Secondary, recurring: the tie-break direction was also missed on the Jul 31 first exposure — see that entry's
section (a). Same problem, same clause, second miss. Read the tie-break sentence twice on any "if there are
multiple, return the X" problem.)*

---

## 🟡 787. Cheapest Flights Within K Stops (Bellman-Ford) — 2026-08-05 *(4th attempt)*
**Sticking point**: `for _ in range(k)` instead of `range(k+1)` — **`k` counts stops (intermediate cities),
not edges**, so `k` stops is `k+1` flights and therefore `k+1` relaxation rounds. Failed LC example 1 (returned
`-1`, expected `700`) and, more sharply, `k=0` with a direct `src→dst` flight returned `-1` instead of the
direct price — zero rounds means zero edges relaxed. Everything else was correct cold from a blank page,
including the hard part (read the frozen `prices`, write to `workingPrices`, swap at round end), and the
technique was derived unaided in the pre-code comment. Needed three nudges to localise, after being told it
was semantic rather than a typo. **Not a Bellman-Ford gap — a problem-statement-vocabulary gap.**
**Cue: whenever a problem caps a path length, write down what the cap counts — nodes, edges, or intermediate
stops — before writing the loop. "Stops" is the off-by-one trap; `k` stops = `k+1` edges.**
*(Name-only miss, uncapped: could not recall the algorithm was called "Bellman-Ford" despite implementing it
correctly — same failure kind as 332's Eulerian and 143's tortoise-and-hare. Prompted the algorithm name-index
table now in [`patterns/README.md`](../../patterns/README.md).)*

---

## 🔴 155. Min Stack — 2026-08-12 *(1st attempt, NEW)*

**Where stuck:** getting `getMin()` to O(1). `push`/`pop`/`top` were never in question.

**Path taken.** (1) Proposed a **deque with the min at the left** — then diagnosed its own flaw
unprompted: LIFO removal from a sorted structure is O(n), because the element leaving is at neither end.
(2) Proposed a **single `min` variable** — correct for `push`, dies on `pop`, and they identified that too
once asked where `-2` comes back from. (3) Asked to be walked through the algorithm.

**Core realization — COACH-SUPPLIED, which is why this is 🔴.** Pops are LIFO, so the *history of minima*
is also LIFO. Store a pair per element: `(value, min of everything at or below it)`. `getMin` reads the top
pair's second field. Deleting the top pair uncovers the previous answer with no recomputation.

```python
def push(self, value):
    currentMin = self.stack[-1][1] if self.stack else value
    self.stack.append((value, min(currentMin, value)))
```

**Then three index bugs, none self-caught:** `self.stack[0]` used in `push`, `top` and `getMin`. Python's
`append`/`pop` operate on the END, so the top is `[-1]`. One fact fixed all three. The `push` case was the
non-obvious one — `stack[0][1]` is always just the first value ever pushed, so `push(5), push(1), push(3)`
stored `(3,3)` instead of `(3,1)`.

**Complexity:** time O(1) all five methods, correct. Space answered "O(1) per method" — true for
*incremental* per call, but the structure is **O(n)** (n pairs). New problem, 2 freebies, 1 spent.

**Verified:** LC examples plus 2000 randomized op-sequences against a reference list.

**Next rep (+2, Aug 14) is measuring whether the teaching stuck, not retention** — the design was handed
over, so a 🟢 there is the first real evidence. Recognition was **not measurable**: scaffold path is
`dsa/leetcode/stack/` and the docstring says `Pattern: stack` — the same pre-spoiling defect logged for 150
on Aug 11 ([[project_upstream_candidates]]).

## 🟡 271. Encode and Decode Strings — 2026-08-12 *(6th attempt)*

**The code was not the problem.** Correct first pass, zero hints, written fast. Length-prefix framing
(`len#str`) named in the pre-code comment. Verified: 10 hand-picked cases (empty list, empty strings,
payloads containing `#`, all-`#` strings, the self-referential `"4#hi"`, digit-only words) plus 3000
randomized round-trips over an alphabet including `#` and quotes — all pass. The `j = i + 1` start is
safe: the first character of a length is always a digit, never the separator.

**Sticking point: unit of work, three times in one gate.** Every first answer counted *containers*
where the work is per *character inside* them:

| Asked | First answer | Correct |
|---|---|---|
| `encode` time | `O(n)`, n = number of strings | **`O(L)`** — `"".join` copies every character |
| `encode` space | `O(1)` — *"we don't count result"* | **`O(n)` extra** — `result` is a **midpoint**, not the output |
| `decode` time | `O(n)`, then `O(n·w)` | **`O(L)`** — slicing copies; and words partition the input, so `Σ` not `×` |
| `decode` space | `O(1)`, wobbled to `O(w)`, settled `O(1)` | **`O(1)` extra** ✅ — `result` here *is* the output |

**The one they got right is the interesting one.** `encode` and `decode` both build a list called
`result`, and the correct accounting differs: encode's is a midpoint (counts), decode's is the return
value (free). The learner drew that distinction themselves and pushed back correctly when challenged —
*"but result is the actual result, it doesn't count."* Same name, different accounting.

**The `O(n·w)` step was the multiply-vs-add trap**, which they have solved before: 721 on Jul 30, where
they raised `O(N · E log E)` unprompted and resolved it with `Σkᵢ = E`. Counterexample that killed it
here: `["a"*1000] + 25 single-char words` → `n·w = 26,000` against a true `L = 1,025`.

**Category status: unit-of-work is now the dominant recurring miss** — 721 (Jul 30), 271 (Aug 2 ×2),
271 (today ×3). 271's freebies were spent Aug 2, hence the 🟡. Each correction landed after a single
cue, which is faster than Aug 2, but the *first* answer was containers-not-characters every time.
**Cue to fire cold next rep: before naming `n`, ask what one unit of work touches.**

## 🟡 778. Swim in Rising Water — 2026-08-12 *(3rd attempt)*

**Sticking point: the return check was hung on the wrong event.** Structure was right first pass —
min-heap keyed on elevation, `visited` marked at pop, no adjacency map. But the destination check sat in
the *neighbour-discovery* loop (`return time` at push). Discovery of a cell happens a fixed number of
times, once per adjacent neighbour, and **early**; enterability happens **later**, when the water rises to
it. On `[[0,2],[1,3]]` that returned 1 instead of 3.

**The instructive part is the first fix, which was reasonable and still wrong.** Adding
`grid[nr][nc] <= time` to the discovery check made the condition correct but left it on the wrong event:
the destination's two discoveries both happen at t=1 and t=2, and by t=3 — when it finally *is* enterable —
there is no discovery event left to fire. It gets popped as an ordinary node, the heap drains, `time += 1`
runs once more, and it falls out returning 4. Fixed by moving the check to the **pop**, which is the moment
a cell becomes enterable and is exactly why `visited` is marked there.

**Cue to carry:** *when a check misfires, ask whether the condition is wrong or the **event** is wrong.*
Two rounds were spent sharpening a condition that was already right.

**Complexity — passed, not missed** (same call as 721 Jul 30): gave heap time `O(V log V)` and space `O(V)`
unprompted and correct, then said outright they didn't understand the `time += 1` term rather than guessing.
Taught: the outer loop is bounded by the **value range**, not the grid — `O(V)` only because the constraints
say `grid[i][j] < n²`. Under `< 10^9` it is 10^9 iterations on a 2×2 grid. Textbook Dijkstra avoids it by
setting `time = max(time, currentNodeValue)` at each pop. **Ask this one cold next rep.**

**Verified** against both examples, `n=1`, and 300 random grids cross-checked against a brute-force
lowest-`t` flood fill — 0 mismatches.

## 🟡 211. Design Add and Search Words Data Structure — 2026-08-12 *(6th attempt)*

**Code was not the sticking point** — written clean from a blank page, zero hints, all four of this
problem's standard failure modes handled (no fall-through after the `.` branch, indices not substrings,
hit propagated out of the recursion, and `return trieNode.isWord` rather than a bare `True`).

**Sticking point: recursion *space*.** Gave the search stack as `O(26^d)`, then `O(26)` — both are the
**fan-out at a node**, not the **depth of the stack**. The `for child in children.values()` loop is
sequential (call, wait, return, next), so siblings are pending loop iterations, never simultaneous frames;
the stack is one root-to-current path, `O(c)`. Freebie for 211 was already spent Aug 2, so this capped the
rep at 🟡 — the learner declined to override, reasoning that unlike 323 (whose category gets three more
cold shots on 261/133/210) the trie-wildcard version has no other rep to test it. Correct on the substance:
208 is the only other trie problem and it has no wildcard.

**The pattern worth watching is bigger than this rep.** Fourth recursion-space miss in three weeks —
235 (Jul 29, height read as balanced) · 332 (Aug 4, depth = nodes not edges) · 261 (Aug 6, stack omitted
entirely) · 211 (today, fan-out read as depth). Four different surface forms, one underlying question:
*what is on the stack at a single instant?*

**Note the mirror.** Aug 2 on this same problem: space right, time wrong (`O(n·N)`). Today: time right
(`O(c·26^d) → O(c)`, unprompted — a genuine correction of that miss), space wrong.

## 🟡 211. Design Add and Search Words Data Structure — 2026-08-02 *(5th attempt; provisional 🟢 lock-down — failed)*
**Sticking point**: the whole trie + wildcard-DFS structure came out clean from a blank page — `addWord`, the
fan-out over `node.children.values()` on `'.'`, the `i + 1` recursion, the early `return False` on a dead
branch. The single bug was the **terminal check reading the wrong variable**: `return traversal.isWord` where
`traversal` is the *root* captured by the closure, never advanced. Only `node` moves during the walk, so the
function answered "is the empty string a word?" on every path. Self-caught nothing here — I flagged the line.
```python
# the closure trap: two names for "current node", only one of them moves
traversal = self.root
def dfs(node, index):
    ...
    node = node.children[word[i]]   # ← this one advances
    return traversal.isWord         # ✗ root, always False   → node.isWord
```
**Pattern to watch**: a closure that captures an outer cursor *and* takes the same cursor as a parameter.
Inside the nested function, the outer name is a stale snapshot — shadow it or don't capture it at all.
Cheapest fix at write-time: name them differently enough that `traversal` inside `dfs` looks obviously wrong.
**Complexity** (gate was asked late, after the rating — my miss): one miss, freebie spent, carded in
`complexity_gotchas.md` — `O(n·N)` for the ≤2-dot bound, i.e. a *tightening* that came out **larger than the
ceiling already proven**. Both space terms and the all-dots `O(N)` argument were correct and unaided.

---

## 🟡 875. Koko Eating Bananas — 2026-08-02 *(5th attempt, 4th consecutive 🟡)*
**Sticking point**: **the search-space endpoints, again — and `l = 0` is a verbatim repeat of Jul 23**, whose
entry names the identical failing case (`piles=[1], h=1` → speed 0 → `ZeroDivisionError`). Line 45 was wrong
three times in a row before it was right: first `l, r = 0, len(piles) - 1` (searching **indices**, not speeds,
despite the pre-code comment stating the range correctly), then `0, max(piles) - 1`, then `1, max(piles) - 1`.
The `- 1` is the `len(arr) - 1` reflex from **index** binary search bleeding into an **answer-space** search
where `max(piles)` is a legal answer. All three supplied. Also stated the monotone direction inverted at the
front gate — *"if we cannot finish at k, cut off possibilities **above** k"* — self-corrected to "at and below"
when handed `k=1` on `[3,6,7,11], h=8`.
**⚠️ Not a §2a teach trigger, and re-repping will not fix it.** Binary-search-on-answer is plainly encoded:
technique named instantly, upper bound `max(piles)` derived, the **min-boundary loop shape** (`r = m` on
success, `l = m + 1` on failure, return `l`) correct first pass, and `canFinish` correct first pass — which is
where *both* Jul 3 (TLE from a decrementing loop) and Jul 13 (`ceil(pile // speed)` floors first) failed. The
failure has migrated to one place and stayed there. ✅ **Genuine movement**: Jul 23 also logged a complexity
miss (*"said n log n; it's n·log(max pile)"*) — today `O(n log k)` was **volunteered unprompted with a
why-clause** in the pre-code comment.
**Rule to carry — say the endpoints aloud, then read line 1 of the loop against that sentence.** *"The answer
lives in `[1, max(piles)]`, both inclusive"* was **stated correctly at the gate and then not honoured by the
code.** The gap is between saying it and typing it, so the check belongs *after* typing: **write the range
sentence, write the init, then diff them.** And ask what each endpoint *means* — `r` here is a **speed**, not
an index, so there is nothing for a `- 1` to do.

---

## 🟡 271. Encode and Decode Strings — 2026-08-02 *(5th attempt)*
**Sticking point**: the technique came instantly (length-prefix framing) but the **discriminator was the wrong
kind of argument** — rejected a `#` delimiter for *cost* ("having to read char until the next `#`") rather than
for *correctness*. Supplied via `["a#b","c"]`: any delimiter you pick is legal payload, so no rarer choice fixes
it. **Rule to carry: the sentence is "any delimiter can appear inside the data, so the boundary must be stated
out-of-band" — the delimiter scheme isn't slower, it's wrong.** One supplied bug: `while j != '#'` compared the
*index* to the character (infinite loop) — ⚠️ **same family as 778's dead `visited` check the same morning**,
both "comparing the wrong kind of thing," neither an algorithm error. The two-pointer parse itself was right on
the first structural pass and survived 3000 random round-trips incl. all 256 ASCII chars as payload.
**⚠️ `while j != '#'` is a VERBATIM repeat of the Jul 3, 2026 entry** ("decode wrote `while j != '#'` (comparing
the index int)"), supplied both times, a month apart — on a problem whose framing logic has been solid since
Jul 3. Like [[875]], the algorithm is not the gap; a specific mechanical slip is.

---

## 🟡 778. Swim in Rising Water (Dijkstra / Min-Heap) — 2026-08-02 *(2nd attempt)*
**Sticking point**: the opening plan was *"step to the cheapest neighbour, DFS until stuck, wait for the water"* —
correct instinct, one hole: **the next cell to enter need not touch the one you're standing on.** Surfaced by a
counterexample grid where the cheap route sits beside the *start*, not beside the current cell; the min-heap
(and therefore "keep the whole frontier, not the local neighbours") was the learner's own once the hole was
visible. **Rule to carry: whenever a greedy walk can dead-end, ask what the candidate set actually is — if it's
everything reached so far, it's a heap, not a walk.** Three supplied bugs, all mechanical, none algorithmic:
(1) `visited` held `(r,c)` tuples but the membership test passed `grid[nr][nc]`, an int — so the set was dead
code and never blocked a push; (2) the source was pushed as `(0,0,0)`, hardcoding its elevation to 0 — the
source is *on* the path, failing case `[[3,2],[1,0]]` → 1 instead of 3; (3) the inner `while time >= minHeap[0][0]`
peeked at an empty heap, `IndexError` on `[[0]]`. Discrimination vs Prim's was cold and correct and is the
keeper: **Prim's has no source and no target, and its key is one edge's weight, spent on absorption; a key that
carries the whole path's history is a path cost.**

---

## 🟡 1584. Min Cost to Connect All Points (Prim's) — 2026-08-01
**Sticking point**: `updateDistance` **assigned** instead of `min`'d, so `distance[i]` quietly meant "distance
to the node just added" rather than "cheapest edge attaching `i` to the component" — the pre-code comment said
the former, which is where the bug came from. Secondary: `for i in range(size)` read as meaningless, because
`i` is a pure round-counter and never a node; `while len(visited) < size` is the honest form. **Rule to carry:
when an array's meaning is relative to a growing set, the write is a `min`/`max`, never an assignment** — and
a comment stating an invariant should also state what the invariant *forbids*.

---

## 🔴 1334. Find the City (Floyd-Warshall) — 2026-07-31 *(NEW — first exposure, became a full teaching session)*
**Topic**: Floyd-Warshall / all-pairs shortest path. Full note written live:
[`patterns/techniques/floyd_warshall.md`](../patterns/techniques/floyd_warshall.md).

### Where did I get stuck?
Two distinct places, and only the second was the algorithm.

**(a) Reading the question.** Asked for a plain restatement before any approach — the confusion was that
"neighbor" reads as *directly connected*, when the problem means *reachable within a total-weight budget*.
Also missed on first read that the tie-break returns the **largest** city index. Cleared by hand-tracing
Example 1 into a per-city count table; no algorithmic content was supplied at this stage.

**(b) The algorithm itself — not known at all.** Correct instinct that every node takes a turn as the
source. Proposed **DFS from each node**, which fails on weights: a visited set assumes the first arrival
at a node is the cheapest, which is only true unweighted. Given the threshold-6 counterexample, correctly
identified that pruning over-budget paths is legitimate *and* that it doesn't rescue the visited problem.
Next proposed **tracking edges per path** — which does fix correctness, but enumerates simple paths
(exponential). At that point asked to be taught the algorithm outright.

### Core Realization
Taught, not derived — record it as supplied:

> A boolean `visited` is the wrong per-node fact. Not *whether* you reached it, nor *by which route*, but
> **what it cost**.

And the invariant that makes Floyd-Warshall work: after stopovers `k = 0…K`, `dist[i][j]` is the shortest
path allowed to pass through only `{0…K}` as intermediates. Each new `k` splits into "path avoids k" (the
current value) vs "path uses k exactly once" (`dist[i][k] + dist[k][j]`, both halves already correct).
**This is why `k` must be the outermost loop** — the induction runs over the stopover set, which has to
grow across the whole table at once.

### Code Snippet
```python
for mid in range(n):              # stopover — MUST be outermost
    for start in range(n):
        for end in range(n):
            if distance[start][mid] + distance[mid][end] < distance[start][end]:
                distance[start][end] = distance[start][mid] + distance[mid][end]
```

### Bugs supplied (5)
1. **Edges never loaded** — allocated `inf`, seeded the diagonal, then ran the algorithm on a graph with no
   roads. Step 1 is *three* parts: allocate, diagonal, **write the edge weights in**.
2. **Undirected double-write missing** — `distance[dst][src] = weight` absent, so the table described a
   one-way network.
3. `currentCount = math.inf` then `+= 1` — `inf + 1` is `inf`. A counter starts at zero.
4. **Returned the count, not the city** — `min()` discarded the identity being asked for.
5. **Tie-break `<` instead of `<=`** — scanning ascending, strict `<` keeps the *first* winner; the problem
   wants the *largest* index. Example 1 returns 0 instead of 3.

Bugs 3–5 all sit in the final counting loop, i.e. in the part that was *not* taught — worth noting, since
the taught triple loop was translated correctly on the first try (with better naming: `mid`/`start`/`end`).

### Follow-up
⚠️ **+2 deliberately overridden → rated re-rep Wed Aug 5** (tracker will read **2026-08-02**; ignore it,
the schedule is source of truth). Same reasoning as 332 on Jul 28: a rep 36 hours after the teaching
measures recall of the conversation, not retention, and an inflated rating there corrupts every interval
computed from it (§2a). Complexity was **passed and taught** — new-problem freebie, 1 of 2; both bounds
were then stated correctly.

**On the re-rep, watch:** whether the table seeding is complete without prompting (bugs 1–2 were both
seeding), and whether `k`-outermost survives. The counting-loop bugs are ordinary and not the signal.

## 🟡 503. Next Greater Element II — 2026-07-31 *(3rd attempt)*
**Sticking point**: two supplied bugs, different in kind. (a) `i % 2` instead of `i % len(nums)` — a **slip, not a gap**: the pre-code comment already said "go through the array twice via modular arithmetic," so the intent was right and only the code disagreed; it silently visited indices 0 and 1 forever. (b) The `-math.inf` sentinel was **never mapped back to the required `-1`** — the design was deliberate and correct, but the output contract was left unconverted, which is what would have failed the judge. Everything structural was cold and correct: monotonic stack recognition, double-pass modular circularity, storing *indices* not values with the reason, and — the subtle one — the `-inf` + overwrite-guard pairing, which is load-bearing here because pushing on all `2n` iterations means an index can be popped twice, and which can't be replaced by a `-1` init since `-1` is a legal value in `nums`. Complexity passed both bounds; the amortized "each index pushed ≤ 2×, popped ≤ 2×" framing was taught after (the stated why was per-op cost, not the aggregate argument). **Watch next rep:** whether the sentinel gets converted without prompting.

## 🟡 721. Accounts Merge — 2026-07-30 *(NEW — first exposure)*
**Sticking point**: not the algorithm — **five supplied bugs, and every one was list-mutate-vs-return Python API**:
(1) `find` read/wrote `rankMap` where it meant `parentMap` (localized by coach, diagnosed by learner);
(2) `nodeMap[email].append(accounts[i][0])` appended the **name** instead of the index `i`, though their own
plan comment one line above said "map of node to *indices*" — would `KeyError` on `parentMap["John"]`, and
silently merges same-name-different-people; (3) `list(emails).sort()` → `None` (`.sort()` mutates, returns
nothing); (4) `resultArray += name` — `+=` on a list is `extend`, so a string splats to `['J','o','h','n']`;
(5) same line initially fed it `parent` (an int index) instead of `accounts[parent][0]`.
**What came back clean, cold, on a first exposure**: recognition (components → Union-Find, written in the
pre-code comment before any prompt), the modeling decision to union **account indices**, the email→indices
map as the driver of which unions to run, the entire DSU (union by rank + path compression, incl. the
equal-rank tiebreak and the `False` on already-joined), and a **self-caught** `accounts`/`accts` shadowing
bug the coach had spotted and deliberately not mentioned. Bringing the algorithm *and* the modeling on a
new-technique problem is the hard half — this is why it isn't 🔴.
**Mechanism inventory fired and worked**: learner proposed "a set and a minHeap" before justifying either.
Set survived (dedupe within a component); heap was cut — same O(k log k) as `sorted()` but a structure to
build and drain, and heaps earn their keep only for *incremental/partial* order (streams, top-k, k-way
merge). Also cut a vestigial `if len(accts) > 1` guard (`range(1,1)` is already empty).
**Result-assembly was hinted**: learner was stuck on getting from parent pointers to output rows, asked for
a hint, and produced "root parent -> nodes mapping?" after a hand-trace on 4 concrete accounts.
**Complexity**: learner **passed and asked to be taught** — so this was taught, not recalled (new problem,
double freebie, no rating hit; 1 of 2 spent). They then stepped both bounds correctly with the framework:
space `O(E)` (and spotted, once prompted, that `O(E+N)` collapses because the constraints guarantee ≥1 email
per account, plus the `O(log N)` `find` stack), time `O(E log E)`. Best moment of the night: they challenged
the sort bound unprompted — *"is it not O(N · E log E) since we loop N keys?"* — the exact multiply-vs-add
trap. Resolved with `Σ kᵢ = E` and the reductio that 12 singleton groups would cost 516 ops to sort 12 emails.
**⚠️ Coach note — the real finding.** The algorithmic reasoning was clean end to end and **100% of the
failures were Python list API**: mutate-in-place vs return-new. Third occurrence in a week (912 was
`append` vs `extend`, 235's was different, this is `.sort()`/`sorted()` + `+=`/`append`). This is **not** a
Union-Find gap and must not be re-repped as one — the Aug 9 rep should be read against the API axis, not
the algorithm axis. Candidate intervention: a short `mutate-vs-return` reference card (proposed, not yet
created — learner's call).

## 🟡 235. Lowest Common Ancestor of a BST — 2026-07-29 *(4th attempt, 3rd consecutive 🟡)*
**Sticking point**: **the identical bug as Jul 19** — the recursive descent calls discarded their return value (`self.lca(root.left, p, q)` with no `return`), so any input whose answer wasn't at the root fell off the end of the function and returned `None`. Diagnosed with example 2 (`p=2, q=4` → `None`, expected node `2`). ⚠️ **Same failure two reps running** — see Coach note.
**What came back clean**: recognition cold and correct, written as a pre-code comment (BST ordering → decide direction from values alone, walk one path instead of searching both subtrees). Direction correct this time — **the Jul 19 inversion did not recur**. And on the mechanism-inventory prompt they *removed* their own rule 4 (an explicit equality check), correctly seeing the `else` branch already covers `root == p`.
**Complexity**: first miss on this problem → **freebie spent, no rating hit** (the 🟡 came from the bug). Gave `O(n)` space for the recursion stack but `O(log n)` time — the two contradict, since stack depth *is* the number of steps walked. Root cause: treated **BST as implying balanced**. Settled on the concrete counterexample `1→2→3→4` (all right children, a legal BST); learner then produced the right mental image unprompted — *"it could just be a sorted list in tree form."* Correct bound is **O(h)**: `O(log n)` balanced, `O(n)` degenerate.
**Coach note**: the missing-`return` bug is now **2-for-2 across Jul 19 and Jul 29**, and both times it was supplied rather than self-caught. Per §2a this is the *never-encoded* pattern, not decay — the gap is not BST logic (which is solid and got cleaner) but **how a recursive function relays a value up the call chain**. Tonight's fix was an explanation, so the next rep is a *measurement* of that explanation and needs a real forgetting gap. If a 3rd `return`-plumbing miss lands, stop re-repping 235 and teach recursion return-plumbing on its own, against a problem that isn't 235.

## 🟡 269. Alien Dictionary — 2026-07-29 *(🔴 → 🟡; Monday's re-rep)*
**Sticking point**: two bugs, neither self-caught. (a) `firstWord = words[i]` / `secondWord = words[i]` — compared each word to **itself**, so `adjMap` came out empty and every char read indegree 0; (b) **duplicate edges double-counted** — `adjMap` is a `set` and silently absorbs a repeat, but `rankMap[...] += 1` fired anyway, so a graph with one `b→c` edge gave `c` indegree 2 and the cycle check falsely tripped (`["ab","ac","xb","xc"]` → `""` instead of `"abxc"`). Guard the increment on the edge being new.
**What came back clean** (worth recording — Monday's four failures were all *modeling*): recognition (first-differing-letter → adjacency → topo, stated in the pre-code comment), the **prefix-invalid rule** (`["abc","ab"]` → `""`), the full Kahn's loop, and the `len(result) == len(rankMap)` cycle check. Also self-initiated the array→dict fix on the indegree map, for the right reason (a 26-slot array emits letters that never appear in the input).
**Complexity**: repeat miss, freebie already spent Jul 27 → capped the rep at 🟡. See the annotated 269 entry in [`complexity_gotchas.md`](complexity_gotchas.md) — named the 26-key ceiling and *still* wrote O(C), then charged `adjMap`'s build at O(E) (output size, not work done).
**Coach note**: the hand-over sentence pre-localized Monday's failure category as "graph modeling" — a stuck-log recap at the start of a retry, logged in `self_eval_log.md`. Factored into the rating.

## 🟡 912. Sort an Array (Merge Sort) — 2026-07-29 *(rated measurement of the Jul 25 D&C teaching session)*
**Sticking point**: `result.append(leftArray[li:])` instead of `extend` — appended the leftover *slice as one element*, so `merge([5],[2])` returned `[2, [5], []]`. **Not** a D&C failure: the skeleton (base case, split, recurse both, merge the two returns, uniform return contract) came back cold and correct, which is what Jul 25 taught. The residual gap has moved from **conceptual → Python API**, so the §2a "teach it again" reflex does *not* apply here; watch `append` vs `extend` on the next rep, not the recursion.

## 🟡 235. Lowest Common Ancestor of a BST — 2026-08-08
**Sticking point**: **not the code — the complexity.** The solution was 🟢-quality: derived cold, no hints, and the split-point test `p.val <= root.val <= q.val or q.val <= root.val <= p.val` covers both orderings *and* the self-ancestor case in one line, which is what makes the following "both smaller → left, else right" sound. **Capped at 🟡 by a repeat complexity miss** — *"it's a BST so we're always dividing by two"* → `O(log n)` time and space. A BST gives **ordering, not balance**; `1→2→3→4` as all-right-children is legal, so the bound is **O(h)**. Same miss as 2026-07-29, freebie already spent → 🟡 per the ledger rule. Learner accepted the correction immediately and restated `O(h)` unaided.

⚠️ **The shape of the miss changed, and that matters more than the repeat.** Jul 29 was `O(log n)` time with `O(n)` space — *inconsistent*, and the card's consistency check catches that. Aug 8 gave `O(log n)` for **both** — consistent, and still wrong. **The consistency check only verifies the same premise was applied twice; it cannot test the premise.** Card updated with this. **Fix to drill: say `O(h)` first, then say what `h` is on the shape you were promised** — correct before balance is known, and it makes the assumption a separate visible sentence.

⚠️ **Mirror-image error the same day on 100 Same Tree**: `O(n)` space (too loose) where 235 was `O(log n)` (too tight). One missing habit, two directions. **This IS a genuine repeating gap** — unlike 560 and 912 the same session, whose repeated 🟡s had unrelated causes. Tree-height is the one thing today that earns a teach trigger if it misses again.

## 🟡 560. Subarray Sum Equals K — 2026-08-08
**Sticking point**: `diff = abs(k - runningSum)` — both the **direction** (`k - S` rather than `S - k`) and the `abs` that hid it. The lookup target is the *earlier prefix sum* `E` satisfying `S - E = k`, i.e. `E = S - k`, which is **signed** and routinely negative; `abs` folds a negative target onto a positive prefix sum that really is in the map, inventing matches. Failing case: `nums=[4,2], k=10` → returned 1, answer 0 (at `S=6`, `abs(10-6)=4` collides with the stored prefix sum 4). Needed the failing case supplied plus several exchanges — two wrong hypotheses first (checking against the current index; then `E = k - nums[i]`, pulling the current element into a relationship it isn't part of) — before the `S - E = k` algebra landed.

⚠️ **Root cause is the NAME, and this is the thing to fix before the Aug 18 rep**: `diffMap` holds **prefix sums**, not diffs (the comment still reads "a map of diff and counter"). A "diff" reads as unsigned, so `abs` looks harmless on it; *"which earlier prefix sum am I looking for"* has an obviously signed answer. Rename to `prefixCount`/`seenSums` and the bug is hard to write.

✅ **Jul 29's two failures did NOT recur** — the running sum is built as you go (no whole-array pre-count) and the `diffMap[0] = 1` seed was present from the first line with correct justification. **Three 🟡s on 560, three different causes** — the learner's own hypothesis going in was that it was one repeating mistake, and the record says otherwise. This is *not* a teach trigger; it is not one unencoded thing.

## 🟡 560. Subarray Sum Equals K — 2026-07-29
**Sticking point**: two nudges, both on the *map's contents* rather than the technique — (a) the opening plan pre-counted `Counter(prefixSum)` over the **whole** array, so a lookup could match a prefix sum lying to its *right*; (b) after correcting to a running sum built as you go, the `diffMap[0] = 1` empty-prefix seed was missing, so every subarray starting at index 0 was invisible. Also **mis-localized** the missing case on first trace (said the second pair of 1s; it was the first). Prefix-sum-minus-k itself was derived cold and correct.

## 🔴 332. Reconstruct Itinerary (Hierholzer) — 2026-07-28 *(2nd consecutive 🔴 → became a teaching session)*
**Topic**: Eulerian path / Hierholzer's

### Where did I get stuck?
Three separate places, in order:

1. **Recognition.** Called it "BFS with directed edges." Self-corrected to DFS on one push, but could
   not name *Eulerian path* — and had never encoded the Eulerian-vs-Hamiltonian split. The
   edges-not-nodes discriminator was stated correctly **in the pre-code comment**, so the concept was
   there without the label.
2. **The post-order append.** Appended each airport on *arrival*. Greedy-smallest-first then strands at
   a dead end with tickets unused. Reached the "append on the way out, reverse at the end" idea through
   a guided derivation — not cold.
3. **Exhausting a node's edges — the actual never-encoded piece.** Even after the post-order fix, each
   call popped **one** ticket and returned, so every airport used exactly one of its tickets. Needed a
   `while` loop, and needed the append to move from `currentChild` to `node`. This was supplied outright.

### Core Realization
Two rules, and rule 2 does all the work:
- while this airport still has an unused ticket → pop the smallest, fly it, finish that trip entirely;
- when it has none left → **append the airport itself**, then back out.

The first airport to run out is the last stop, so the list builds end-to-front → reverse.

**Why exhausting is safe (the correctness spine):** every airport except start and end has as many
tickets in as out, so the *only* place you can strand is the final airport. Therefore any tickets still
left at a node when you come back up must form a **cycle returning to that node** — and a cycle splices
in cleanly wherever its airport already appears. That is why greedy-smallest-first never needs
backtracking: it can strand you, but it cannot make the remainder unfixable.

### Code Snippet
```python
def dfs(node):
    while adjMap[node]:                       # exhaust ALL tickets, not one
        dfs(heapq.heappop(adjMap[node]))      # smallest first; heappop IS the consumption
    result.append(node)                       # append SELF, after the loop — no guard, no return value

dfs("JFK")
result.reverse()
```

### Cross-problem pattern (flagged same day)
Invented a propagated return value (`returnNode`) where the call's **own post-order position** was the
real carrier of information — **twice in one session**, here and in 19 Remove Nth Node that morning. In
both cases the return value was assigned, passed up, and never read. Watch for this shape: reaching for
a value to hand upward when the answer is "do the work on the way back out, using this call's own
variable."

### Follow-up
+2 **overridden** → rated re-rep **Tue Aug 4** (7-day forgetting gap; a Thursday rep would measure
recall of this conversation). If Aug 4 blanks again, stop re-repping and change format.

---

## 🟡 19. Remove Nth Node From End (Postorder Recursion) — 2026-07-28
**Sticking point**: postorder counter counts **from the tail** (tail = 1), but was compared against `n - 1`, which is front-indexed — the predecessor of the nth-from-end node sits at `n + 1`. Structure, dummy, and increment placement were all correct; only the comparison value was wrong. *(Same variant was 🟡 Jul 18 on a different sticking point — the counting direction itself.)*

---

## 🔴 269. Alien Dictionary — 2026-07-27
**Topic**: Topological Sort (Kahn's) / graph *modeling*

### Where did I get stuck?
**Not the algorithm — the modeling.** Kahn's itself was recalled unprompted ("increment the
dependencies like course schedule"), and the recognition call (graph + produce an ordering → topo
sort) was cold and correct. Every single failure was in the four steps *before* the graph exists:

1. **The edge-extraction rule.** Opening plan was "from each letter of each word, build an adjacency
   map to the next word" — i.e. an edge at *every* differing position. Correctly said `["wrt","wrf"]`
   yields only `t→f` when asked, but attributed it to *"t and f are at the end, so the loop naturally
   stops"* — a coincidence of that example, not the rule. Needed the `apple`/`banana` derivation
   (does it tell you anything about `p` vs `a`?) and then the statement's own words (*"at the **first
   position** where they differ"*) before it landed.
2. **Where the letter set comes from.** Seeded `rankMap` from `adjMap` three separate times — first
   before `adjMap` was populated (`{}`), then after it (wiping the counts), then still keyed on
   `adjMap` (which only holds edge *sources*). `["az","bz"]` silently dropped `z`. Had to be told
   outright: **the letters come from `words`, not from the graph.**
3. **`break` on the first *difference*, not the first *new edge*.** Break was nested inside the
   dedupe guard, so a duplicate edge fell through and kept scanning meaningless later positions —
   fabricating constraints. `["axp","ayq","bxp","byq"]` invented `p→q`.
4. **Cycle detection.** Asked twice, unanswered until the third prompt; the plan was to *"build the
   rest in order of rank where rank > 0"* rather than recognizing leftover indegree as "no valid
   order exists." `["a","b","ca","cb","b"]` returned `'a'` instead of `''`.

Zero bugs self-caught. Also proposed the DFS lane first, then switched to BFS mid-plan — both were
half-specified at the moment of the switch.

### Core Realization
**269 is a modeling problem wearing a topo-sort costume.** The graph is the easy half; the hard half
is that *nothing in the input is a node or an edge yet*. Three separate derivations have to happen
before Kahn's can start:

- **Nodes** = every distinct char across all of `words` — **not** the keys of the adjacency map.
  Letters with no ordering constraint still belong in the output.
- **Edges** = **exactly one per adjacent word pair**, at the first differing position, then stop.
  Lexicographic comparison short-circuits at the first difference, so every later position is
  *unconstrained*, not equal. Proof: `azzz` < `baaa` despite `z` "after" `a` at position 1.
- **Invalid input has two shapes** — the prefix violation (`["abc","ab"]`, caught pre-graph) and the
  cycle (caught post-BFS by `len(result) != len(rankMap)`). Missing either returns a plausible
  wrong answer rather than crashing.

The partial-order point also had to be surfaced: disconnected letters have *no* provable relative
order, which is why the problem says "return any of them."

### Code Snippet
```python
# Nodes come from `words`, NOT from adjMap — letters with no edges still ship.
adjMap  = {char: set() for word in words for char in word}
rankMap = {char: 0     for char in adjMap}

def buildAdjMap(firstWord, secondWord):
    if len(firstWord) > len(secondWord) and firstWord[:len(secondWord)] == secondWord:
        return ""                                  # prefix violation — invalid #1
    for i in range(min(len(firstWord), len(secondWord))):
        if firstWord[i] != secondWord[i]:
            if secondWord[i] not in adjMap[firstWord[i]]:   # dedupe the EDGE...
                adjMap[firstWord[i]].add(secondWord[i])
                rankMap[secondWord[i]] += 1
            break            # ...but break on the DIFFERENCE, outside the guard

# ... Kahn's ...
if len(rankMap) != len(result):
    return ""                                      # cycle — invalid #2
```

**Next rep — the four checkpoints, in order:** (1) nodes from `words`; (2) one edge per pair, break
on the difference; (3) prefix check before the loop; (4) length check after the loop. If the graph
is built right, Kahn's is muscle memory from 207/210.

## 🟡 540. Single Element in a Sorted Array — 2026-07-27
**Sticking point**: had the parity crux in the code already (`m % 2 == 0` → single is right of `m`), but stalled on turning it into a *safe* discard. Two bugs needed flagging: (1) `l = m` on the even branch never advances → infinite loop (correct jump is `m + 2`, since `m` is a pair *start* so `nums[m]`/`nums[m+1]` are both spoken for); first instinct on the fix was `m - 2`, direction flipped. (2) `return l` returned the index, not the value — caught on `[3,3,7,7,10,11,11]` → 4 instead of 10 (Example 1 hides it: the answer's index and value are both 2). Complexity clean both ways, freebie unspent. **Watch:** 5th attempt, still 🟡 — the pair-start-parity invariant (*even before the single, odd after*) has never once come back cold. If the next rep needs it supplied again, that's never-encoded, not decaying, and it wants a teaching pass rather than another +10.

## 🟡 787. Cheapest Flights Within K Stops (Bellman-Ford) — 2026-07-26
**Sticking point**: recognition was fully cold and correct — including the snapshot (global/local copy), which *is* the algorithm. The cost was a **vestigial queue**: the plan carried a BFS queue whose layering job the snapshot already did, so most of the session went to maintaining it (infinite loop from unconditional `append`, level-size capture, counter placement). Two real bugs needed flagging: (1) `if iteration == k: break` fired *before* the round's work, so `k=1` ran zero rounds; (2) relaxation compared against `distance[destination]` (the stale snapshot) instead of `workingDistance[destination]`, so a worse edge later in the same round overwrote a better value already written — caught via `[[0,1,10],[0,2,20],[1,3,5],[2,3,100]]`, k=1 → 120 instead of 15. Derived `k+1` and the working-copy fix himself once pointed at a failing case. Complexity clean both ways (freebie unspent). **Lesson for the next rep: the snapshot alone gives you the layering — no queue.**

## 🟡 143. Reorder List — 2026-07-25
**Sticking point**: decomposition (Floyd middle + reverse 2nd half + weave) was cold and correct; stalled on the merge loop's pointer-advance and asked for a hint before spotting it was a typo on the last two assignments (`head = headNext; secondHead = secondHeadNext`). Structure solid, execution slip.

## 🟡 743. Network Delay Time (Dijkstra) — 2026-07-25
**Sticking point**: marked `visited` on push instead of pop (locked in the first-discovered, non-shortest distance); after fixing that, missed the pop-time stale-entry guard (`if node in visited: continue`) — a node reached by two edges before being popped gets two heap entries. Recognition + structure cold; both bugs were `visited`-placement in the lazy heap.

## 🟡 229. Majority Element II — Jul 24, 2026
**Sticking point**: Boyer-Moore n/3 (≤2 candidates) was correct, but the `for n in nums` loop variable leaked — used `minSize = n // 3` (last element) instead of `len(nums) // 3`, so the threshold was garbage (returned `[1,2]` on `[1,1,2]`). Also space miss: called the freq map O(n) when it's capped at ≤2 entries → O(1) (freebie, carded).

## 🟡 778. Swim in Rising Water — Jul 23, 2026
**Sticking point**: first exposure to grid-Dijkstra (max-of-path). Derived the min-heap frontier cold (jump `t` to the min blocked neighbor, not +1), but (1) initially thought the frontier was only the current cell's 4 neighbors — it's the whole 2D boundary, O(n²), which is *why* a heap beats a scan; (2) empty-heap `IndexError` from peeking `minHeap[0]` between inner-loop pops; (3) never checked for reaching the destination, so it drained the grid and returned an overshot `level`. Cleaner form = modified Dijkstra (answer = running max elevation, return on popping the end). Space Big-O: said O(n), actually O(n²).

## 🟡 875. Koko Eating Bananas — Jul 23, 2026
**Sticking point**: binary-search-on-answer was clean, but set `l = 0` — speed 0 is invalid and `math.ceil(pile/0)` divides by zero (crashes on `piles=[1], h=1`, where the first `m` is 0). Lower bound must be `l = 1`. Also stated complexity as n log n; it's n·log(max pile) — the search is over the value range, not the array.

## 🟡 271. Encode and Decode Strings — Jul 23, 2026
**Sticking point**: encode was clean; `decode` mixed a `for j in range(...)` with the two-pointer jump, so the `for` marched `j` through every index and the `i = j+1+lenStr` skip never drove the loop (re-scanned words, then `int('')` crash). Fix: make `i` the driver — `while i < len(s)`, inner `while` finds the `#`.

## 🔴 332. Reconstruct Itinerary (Hierholzer) — Jul 22, 2026
**Topic**: Eulerian path — a walk that uses every **edge** exactly once — via Hierholzer's algorithm. First exposure to the technique.

### Where did I get stuck?
Set up the representation well cold — `adjMap: source -> min-heap(destinations)`, DFS not BFS, "consume the edge by popping." But the traversal came apart in two places:
1. Used an `if adjMap[node]` that popped **one** neighbor and recursed — a node with 2+ tickets only ever spent one, and the walk stopped at the first dead end with tickets unused.
2. Appended greedily **inside** the walk (pre-order), so the lexically-smallest neighbor got locked into `result` even when it was a dead end that belonged **last**. On `[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` this returned `["JFK","KUL"]` instead of `["JFK","NRT","JFK","KUL"]`.

Self-derived: edges-not-nodes, DFS, "drain all tickets," and *sensed* pre-order append was wrong. Supplied by coach: the post-order + reverse core, and why greedy-forward strands you.

### Core Realization
- Don't **pick** a neighbor — **drain** them all: `while adjMap[node]:` pop smallest, recurse. Every edge gets used, smallest-first.
- **Post-order append is the trick.** A node you enter with no exits left can only be the *end* of the trip → append a node only *after* its heap empties. Dead-ends land in `result` first.
- Since dead-ends land first and the true start (`JFK`) drains last, `result` comes out reversed → one `result.reverse()` at the end.
- No `visited` set: popping off the heap *is* the "mark used." No pre-seed of `JFK` either — every node is added by the post-order append.

### Code Snippet
```python
def dfs(node):
    while adjMap[node]:
        dfs(heapq.heappop(adjMap[node]))
    result.append(node)   # post-order: append when the node has no exits left
dfs("JFK")
result.reverse()
```
Complexity: **O(E log E)** time (each of E tickets pushed+popped from a heap, O(log) each), **O(E)** space. Big-O time was initially given as O(E) — the heap's log factor was the miss.

## 🟡 127. Word Ladder (BFS) — Aug 3, 2026
**Sticking point**: ⚠️ **same off-by-one as Jul 21, plus a regression.** Graph modeling was cold and
unaided again (wildcard-bucket adjacency, unweighted → BFS — lines 44–49 written before any code). Two
execution misses: (1) **no layer loop at all** — `iteration += 1` fired once per *pop*, counting nodes
instead of levels, which Jul 21 had gotten right unaided; (2) after adding the level-size loop, the
**identical `level = 0` / `return level + 1` off-by-one from Jul 21** — `beginWord` is already word #1
when popped, so the counter starts at 1. Both fixed by the learner from a failing case + one Socratic
nudge each; neither was supplied. **3rd attempt, 2nd consecutive occurrence of the same off-by-one →
teaching signal, not a repetition signal** (same rule applied to 540 and 19). What decays is *"what does
my counter mean and when does it increment"*, not the graph framing — evidenced by 994 the same day,
where the layered BFS and its counter were both perfect. Complexity correct unaided: O(n·c²) time and
space, with `c` (word length) correctly refused as a constant.

## 🟡 127. Word Ladder (BFS) — Jul 21, 2026
**Sticking point**: 🔴→🟡 — full structure rebuilt cold (wildcard-bucket adjacency + layered BFS came back unaided; the Jul 18 teaching stuck). Only miss: off-by-one on the BFS level init — started `level = 0` and returned `level + 1`, undercounting by one (`beginWord` is already word #1 when popped, so the counter must start at 1).

## 🔴 211. Design Add and Search Words Data Structure — Jul 21, 2026
**Topic**: Trie with wildcard (`.`) search — the DFS that matches "any single char" against all children.

### Where did I get stuck?
`addWord` was clean. The wildcard `search` came apart two ways: (1) walked the trie by
**reassigning `self.root`** down the tree — permanently corrupts the root, so a *second*
search starts from the wrong node; (2) on a `.`, looped `j` over **positions in the word**
and re-`search`ed suffixes from the root, instead of trying the **children of the current
node**. Root cause: `search(word)` always begins at the root, so there's no way to carry
*"resume from THIS node at THIS index"* into the recursion — the missing state is **(node, index)**.

### Core Realization
The fix is a helper `dfs(node, i)` answering one question: *"can I match `word[i:]` starting
from `node`?"* — and `search(word)` is just `return dfs(self.root, 0)`. Three cases:
- `i == len(word)` → the word is fully consumed; hit only if `node.isWord`.
- normal letter → if `word[i]` is a child, the answer **is** `dfs(node.children[word[i]], i+1)`; else `False`.
- `.` → try every child: `any(dfs(child, i+1) for child in node.children.values())`.

Node and index advance **together** every call; `self.root` is never touched (a parameter
carries the position), so the trie survives across searches — which also kills the mutation bug.

### Code Snippet (the shape — not to peek at before re-rep; written for the concept)
```
def dfs(node, i):
    if i == len(word): return node.isWord
    c = word[i]
    if c == '.':  return any(dfs(ch, i+1) for ch in node.children.values())
    return c in node.children and dfs(node.children[c], i+1)
```

## 🟡 503. Next Greater Element II — Jul 21, 2026
**Sticking point**: approach was clean (decreasing stack + double-loop for circular) but four small bugs I didn't self-catch — inverted `while` guard (`not stack` → crashes empty), unwrapped `nums[i]` on the 2nd lap (needs `i%length`), inverted assignment guard (`!= inf` wrote only filled slots), and `math.inf` sentinel never converted to `-1`.

## 🟡 543. Diameter of Binary Tree — Jul 20, 2026
**Sticking point**: recurring problem — first only measured the path bending at the root (missed that the diameter can bend at any node → needs a global max updated inside the `depth` recursion); after fixing that, defined the nested `depth` helper but never called it, so returned 0.

## 🟡 1584. Min Cost to Connect All Points (Prim's MST) — Jul 20, 2026
**Sticking point**: had the eager array-Prim approach from memory but stalled reaching for the "missing data structure" (nearly went heap); needed a nudge that the `dist` array + linear min-scan *is* the frontier, no heap required. `getClosestNode` then came unaided.

## 🔴 127. Word Ladder (BFS) — Jul 18, 2026
**Topic**: BFS shortest path on an implicit word graph + the wildcard-bucket adjacency trick. First
exposure. Learner self-rated 🔴 on hint volume — the spine was recalled, but the optimization was taught
and the BFS had four bugs.

### Where the struggle actually was
Not the top-level framing — the learner **got that unaided**: "beginning and end, find a path one letter
at a time → graph, shortest path." The stumbles were three layers down:
1. **Algorithm choice.** Reached for Dijkstra. Needed the nudge that every edge costs 1 (equal weight) ⟹
   BFS *is* the shortest-path algorithm here; Dijkstra is just a slower BFS on an unweighted graph.
2. **Neighbor test.** Proposed a **frequency array** to decide "one letter apart" — that measures multiset
   difference, so `dot`/`tod` would falsely count as neighbors. Position matters → char-by-char, count
   positions that differ, valid iff exactly 1.
3. **The wildcard-bucket adjacency was fully taught**, not recalled. Learner was heading toward O(N²·L)
   pairwise comparison. The trick — bucket every word under its `*`-patterns (`h*t`, `ho*`, `*ot`); two
   words in the same bucket are automatically one letter apart — dropped build+BFS to O(N·L²).
4. **Four BFS bugs, cleared one at a time:**
   - `level = len(queue)` used as the *depth* counter — that's frontier *size*, not depth. Fix: snapshot
     `len(queue)` as the level batch size, drain exactly that many per `level += 1`.
   - Added neighbors to `visited` but never *checked* `visited` before enqueue → words re-enqueued; also
     `beginWord` never marked visited.
   - **Off-by-one**: `endWord` is discovered as a *neighbor* (enqueue time), one level below the word being
     processed, so returning `level` is one short. Fix: `return level + 1` at the moment `nextWord == endWord`.
   - **Injected `endWord` into the graph** (`allWords.append(endWord)` unconditionally) → Example 2
     (endWord not in wordList, answer 0) wrongly returned a path. `endWord` is a node only if `wordList`
     already contains it.

### Core Realization
Two that the learner should carry to the retry: **(a)** equal edge weight ⟹ plain BFS gives shortest path
(don't reach for Dijkstra); **(b)** to avoid O(N²) neighbor-finding, bucket words by `*`-wildcard pattern —
sharing a bucket *is* the one-letter-apart relation, computed without any pairwise comparison. And the BFS
counting contract: depth is counted per *level batch*, and the target is found the moment it's *enqueued*,
so its depth is `current level + 1`.

### Code Snippet (the shape to rebuild from a blank page)
```python
# build: word -> its L wildcard patterns -> bucket of words
wildcardMap = collections.defaultdict(set)
for word in [beginWord] + wordList:            # NOT endWord unless it's in wordList
    for i in range(len(word)):
        wildcardMap[word[:i] + '*' + word[i+1:]].add(word)

visited = {beginWord}
queue = collections.deque([beginWord])
level = 0
while queue:
    level += 1
    for _ in range(len(queue)):                # snapshot frontier size = this level
        cur = queue.popleft()
        for i in range(len(cur)):
            for nxt in wildcardMap[cur[:i] + '*' + cur[i+1:]]:
                if nxt == endWord:
                    return level + 1           # found at enqueue → one level deeper
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
return 0
```

### Meta
Same first-exposure-🔴 pattern as 743/787/1584 (a new graph algorithm taught, not recalled). But note the
contrast: here the learner **owned the paradigm** (graph + BFS) and only needed the *optimization* + bug
fixes — further along than the MST/shortest-path 🔴s where the paradigm itself was the gap. Retry Jul 20.

## 🟡 235. Lowest Common Ancestor of a BST — Jul 19, 2026
**Sticking point**: BST ordering logic sound (in-between → LCA; else descend), but two bugs, neither self-caught: (1) the recursive descent calls discarded their return value (`self.lca(root.left, …)` with no `return`), then unconditionally `return root` — so any descent handed back the current node, not the found LCA. (2) Direction inverted: root smaller than both went left, root bigger than both went right — backwards (smaller-than-both → targets are right; bigger-than-both → left). Notably the learner's *verbal* reasoning had the direction right; only the code disagreed. Fix: `return self.lca(right)` when `root < both`, `return self.lca(left)` when `root > both`.

## 🟡 417. Pacific Atlantic Water Flow — Jul 19, 2026
**Sticking point**: Approach owned cold (reverse-BFS from each ocean's border, intersect the two reachable sets). Two silly bugs, neither self-caught: (1) visited-guard looked up `heights[nr][nc] not in canReach…` — a *height value* against a set of *coordinate tuples*, so it never actually blocked re-visits; should be `(nr,nc) not in …`. (2) Strict `>` on the height step dropped equal-height cells — reverse flow steps to a neighbor with height `>=` current, since water flows `<=`. Both are read-what-you-store / off-by-equality slips, not conceptual.

## 🟡 261. Graph Valid Tree (Union-Find) — Jul 18, 2026
**Sticking point**: UF machinery clean (path-compressed `find`, union-by-rank returning False on cycle, n−1 edge-count guard up front). The miss was the *connectivity* half: used `len(visited) == n` where `visited` = "nodes that appeared in an edge" — not actual connectivity, and it wrongly fails the valid single-node tree (n=1, edges=[] → 0==1 → False). Key theorem to own: **an acyclic graph (forest) with n nodes and c components has exactly n−c edges**; so forcing edges = n−1 AND proving acyclic (UF) ⟹ n−1 = n−c ⟹ c=1 (connected). The connectivity check is therefore free — just `return True` after the guard + union loop. (If an explicit check is wanted, count distinct roots == 1, which also handles n=1.)

## 🟡 19. Remove Nth Node From End (Postorder Recursion) — Jul 18, 2026
**Sticking point**: Recursion-rewiring cluster again (cf. 143, 206). Two rounds: (1) counted with a `nonlocal` incremented *before* recursing → every frame on the way up sees the same max count, so `== n` can't identify any node; postorder count-from-back must accumulate on the way UP via the return value (`count = removeNode(node.next) + 1`). (2) Off-by-one + no-op removal: stopped at `count == n` (the target itself, un-removable in a singly list) instead of `n + 1` (the predecessor), and the "removal" was `node.next = node.next` (self-assign). Fix: at `count == n+1`, `node.next = node.next.next`. Dummy correctly handles head removal (becomes the predecessor at count n+1). Contract to say out loud: postorder count rides the return value up; act on the predecessor, not the target.

## 🟡 424. Longest Repeating Character Replacement — Jul 17, 2026
**Sticking point**: Sliding-window skeleton + `windowLen - maxFreq > k` invalidity test + shrink all correct — and window bounds (`r-l+1`) were clean (progress on the boundary cluster). The one miss was the central insight: set `maxFreq = freqMap[s[r]]` (count of the *current* char) instead of the running high-water max `max(maxFreq, freqMap[s[r]])`. Also recomputed maxFreq inside the shrink loop (pointless — `s[r]` fixed while `l` moves). Key concept to own for the retry: **maxFreq is a high-water mark, not the live window max — it's allowed to go "stale" (higher than the current window's true max), because the answer only grows when a new high is hit, and a smaller maxFreq would only shrink the window, which never improves a *longest*-window answer.** That's why the classic form is an `if`-slide with no downward update. Verified 0/3200 vs brute force after fix.

## 🟡 540. Single Element in a Sorted Array — Jul 17, 2026
**Sticking point**: Binary-search skeleton recalled, but decided direction by *parity of the normalized index alone* — which can't tell an intact even-aligned pair from the single element sitting at an even index (both make `m` even), so it jumped `l=m+2` over the answer. Fix: after fixing `m` even, compare `nums[m]==nums[m+1]` — equal → pairing intact, go right; else break is at/left, `r=m`. Second miss: returned `l` (index) instead of `nums[l]` (value) — masked when index and value coincide. Verified correct vs brute force after both fixes.

## 🟡 18. Four Sum — Jul 17, 2026
**Sticking point**: Approach recalled cold (sort → two outer loops → two-pointer inner two-sum → set dedup), but four execution bugs, two in the boundary/pointer cluster: (1) outer bounds `range(n-4)` and `for b in range(a,...)` — first misses a minimal 4-element input, second reuses index a → `range(n-3)` / `range(a+1, n-2)`; (2) inner helper returned a bool but the quad was built from the untouched `nums[c]`/`nums[d]`; (3) even after returning indices, they weren't captured; (4) collect-all loop appended on a match but didn't advance both pointers → infinite loop. Pattern: the *algorithm* is there; the failures are all bounds + pointer bookkeeping (cf. 75, 424, 901). Say the two-pointer invariant out loud: on a match, record AND move both inward.

## 🔴 1584. Min Cost to Connect All Points (Prim's MST) — Jul 18, 2026 (retry #1, still 🔴)
**Topic**: MST / Prim's, dense-array lane. 2nd 🔴 — got a correct solution running (verified 0/2000 vs
reference) but only after full pseudocode + a step-by-step walkthrough. Taught, not recalled.

### Where the struggle actually was
Not boundary arithmetic (that's the other cluster) — this was the **greedy paradigm itself** and
**maintaining state across rounds**. Two recurring wrong structures before the right one:
1. **Fused select and relax.** Kept writing a nested `for i / for j in range(i+1,…)` that walked index
   pairs in order, instead of *each round* scanning the whole `distance[]` scoreboard for the cheapest
   unvisited node, then relaxing from it. Select must **read** `distance[]`; relax is the **only** place
   distances are computed. Fusing them = "connect each point to the previous / to node 0" = a path/star,
   not an MST.
2. **`visited.add(0)` without relaxing from 0** → round-1 select saw all-∞ and died. Insight the learner
   reached themselves: *settling a node = mark visited AND relax, always together*; marking visited alone
   leaves the scoreboard blind to that node's edges. Cleanest fix: don't pre-add 0; seed only
   `distance[0]=0` and let the loop pull it in (glues the two actions).

### Good signs (understanding forming even though recall isn't)
Learner's *own* probing questions were sharp: "wouldn't select return -1 if everything's ∞?" (base case)
and "why can't I add node 0 to visited immediately?" (found the settle=visited+relax tension). The model
is building; cold production isn't there yet — expected for a hard greedy algorithm across 2 exposures.

### The shape to recall (not memorize the code)
`distance=[inf]*n; distance[0]=0; visited={}`. Repeat until all visited: **select** cheapest unvisited
(read scoreboard) → **pull in** (mark visited, bank cost) → **relax** every remaining node from it. One
line to carry: *one component grows; each round settle the cheapest edge crossing out of it.*

### Meta (teaching)
This retry exposed a coaching flaw — taught proof-first (cut property, "settled", complexity) before
procedure. See [[feedback-procedure-first]]: lead with the literal loop in plain language + a hand-trace,
proof only if asked. Next retry: start from the operational loop, not the theorem.

## 🔴 1584. Min Cost to Connect All Points (Prim's MST) — Jul 16, 2026
**Topic**: Minimum Spanning Tree / Prim's — first exposure. Taught, not recalled (same shape as 743 Dijkstra Jul 13 and 787 Bellman-Ford Jul 14, both 🔴 on first exposure).

### Where did I get stuck?
Everything above the code. Didn't know what an MST was, or what Prim's was. Needed: the MST definition, Prim's greedy move, that a min-heap serves "cheapest edge leaving the blob", what to seed the heap with, and where the neighbor index `j` comes from. Wrote the loop correctly once the pieces were named. Self-reported: *"this did not feel very intuitive at all."*

**Three concrete reasons it fought intuition** (worth re-reading before the retry):
1. **The graph is invisible.** Every prior graph problem hands you edges (743 `times`, 787 `flights`, 207 `prerequisites`). Here you get *points* and manufacture the graph — kept hunting for an edge list / adjmap that doesn't exist. `range(n)` **is** the adjacency list; every other point is a neighbor.
2. **Prim's doesn't walk.** BFS/DFS/Dijkstra feel like traversal — you're somewhere, you step to a neighbor. Prim's dumps every option in a bag and takes the globally cheapest, so it *teleports* across the graph. "You don't pick — the heap picks" fights the traversal instinct.
3. **Dijkstra's skeleton, different soul.** Same heap + visited + greedy shape, but the push means something else. Near-miss similarity misleads harder than something wholly new.

### Core Realization
**MST** = spanning (touches every node) + tree (no cycles → exactly `n-1` edges) + minimum (least total weight). Cycles are always removable: a loop means one edge is redundant, so drop the priciest and stay connected for less.
**Prim's** = grow ONE blob from any seed; repeatedly take the cheapest edge from blob → outside; stop when all `n` are in. Greedy is *provably* optimal here (crossing-edge property), so no backtracking. Seed `(0, 0)` — node arbitrary (MST spans all, so the start can't change the total), cost 0 (the seed isn't paid for), and it removes the empty-blob special case.
**Prim vs Kruskal**: Kruskal sorts all edges + Union-Find (many blobs merging); Prim grows one blob + min-heap + a plain `visited` set. Prim suits 1584 — dense/complete graph, sorting ~500k edges is wasteful.
**⚠️ Prim vs Dijkstra — the trap**: Dijkstra pushes `cost + edge` (cumulative from source); **Prim pushes the bare `edge`**. Prim doesn't care how far you are from the start, only what it costs to drag a node into the blob. (Avoided this one live.)
**O(n²) is inherent, not a flaw** — a complete graph has ~n²/2 edges; `n ≤ 1000` is the tell that O(n² log n) is intended.

### Code Snippet
The bug at the end: passed **indices** where coordinates were wanted —
```python
distance = manhattanDistance(node, neighbor)        # node/neighbor are ints -> TypeError
distance = manhattanDistance(points[node], points[neighbor])   # need the lookup
```
Retry (Sat Jul 18) will use the **dense/array lane** by choice — `minDist=[inf]*n`, scan for the min unvisited, relax `minDist[v]=min(minDist[v], dist(u,v))`. O(n²), O(n) space, and it maps onto Bellman-Ford's relax-an-array shape which came back clean Jul 16. **Lane may change; the derivation (one blob, cheapest crossing edge is safe) must be there cold.**

## 🟡 912. Sort an Array (Merge Sort) — Jul 15, 2026
**Sticking point**: Concept was solid; the block was *writing* it. Switched from index-based in-place (Idiom A) to return-based slices (Idiom B) — merge step then came out clean and correct first try. One boundary slip: split as `nums[:middle]` / `nums[middle+1:]`, dropping `nums[middle]` — the `+1` is correct in A (right half is `[m+1, r]`) but wrong in B, where slices are right-exclusive so right must start at `middle`. Invariant: the two slices must tile the array gap-free — *left ends where right begins, at `middle`, no `+1`*. First time off 🔴 (Blank since Jan). Boundary-arithmetic weakness cluster (424, 75, 901).

## 🟡 143. Reorder List — Jul 15, 2026
**Sticking point**: Floyd + reverse + weave structure was sound; both bugs were the same pattern — a pointer set to *where it came from* instead of *where it's going*, creating a cycle. Self-caught the weave bug (`secondHalf.next = firstHalf` → `firstHalfTmp`). Missed the recursive-reverse bug: `node = node.next` rebinds a local and does nothing — must be `node.next = None` to sever the forward link (else the tail stays in a 2-cycle). Recurring recursive-linked-list-rewiring weakness — see 206 (🟡 Apr 24 → Jul 3 → Jul 14). Iterative-reverse motor drill scheduled Thu Jul 16 to make the fallback reflex.

## 🟡 355. Design Twitter — Jul 15, 2026
**Sticking point**: Data model was clean; `getNewsFeed` shipped a mixed heap model — pushed `(-time, tweetId)` (a max-heap key) but bolted on a bounded-heap cap *and* a final reverse (both belong to the `+time` design). With `-time`, the `len > 10` cap `heappop`s the *most recent* tweet, silently dropping the newest. Compounded by `return returnList.reverse()` returning `None` (in-place reverse), masked by a `# type: ignore`. Pick one lane: `-time` max-heap → no cap, no reverse; or `+time` bounded min-heap → cap + reverse. And never `# type: ignore` a return-type warning — it was flagging the real bug.

## 🟡 743. Network Delay Time (Dijkstra) — Jul 15, 2026
**Sticking point**: Dropped the pop-time `if node in visited: continue` guard, relying only on the push-time `neighbor not in visited` filter. But `visited` is populated at pop, so two entries for the same node can both be pushed while it's un-popped; the stale larger copy then poisoned `minTime` via `max()`. First pop = settled; every later pop is stale and must be skipped — that guard is load-bearing, not the push-time filter.

## 🔴 787. Cheapest Flights Within K Stops (Bellman-Ford) — Jul 14, 2026
**Topic**: Advanced Graphs — Bellman-Ford, shortest path under a hop limit (first exposure)

### Where did I get stuck?
Reached for the whole Dijkstra/BFS toolkit — adjacency map, min-heap, **visited set** — none of
which Bellman-Ford uses. The approach was taught, not recalled: that you relax the flat `flights`
edge list directly (no adjacency map, no traversal), that the number of rounds *is* the flight
budget, and — the real trap — that each round must read from a **frozen snapshot** of the previous
round. Hit the chaining bug and fixed it the wrong way *twice*: first left the relaxation reading
the live copy, then "made it consistent" by pointing **both** reads at the live copy, which silently
deletes the snapshot (a copy you also read from is just in-place mutation). The correct split —
read `source` from frozen `prices`, write `target` to the working copy — only landed on the third try.

### Core Realization
**Bellman-Ford is Dijkstra with the cleverness removed: no heap, no visited, no adjacency — just
"relax every edge, `k+1` times." Two mechanisms cooperate, and I conflated them:**
- the **`k+1` loop bound** sets the flight budget (≤ `k+1` edges = `k` stops);
- the **two-generation snapshot** makes each round spend *exactly one* hop, so "round count = flight
  count" is actually true. Without the snapshot, one round chains multiple hops and the budget is a lie.

The chaining is a **read/write timing** bug, not a fan-in bug: a node written as a *target* early in a
round, then read as a *source* later in the same round, rides two fresh flights in one round. The fix
is to read every source from last round's finalized board (`prices[source]`), so a relaxation always
extends an `(i-1)`-hop value into an `i`-hop value — never `i+1`. A **visited set is poison here**
(unlike Dijkstra): nodes *must* stay open to a cheaper, more-hops value in a later round.

This is the exact crack 743's note predicted — Dijkstra's settle-on-pop dies when a future push can
undercut a finalized distance; the hop limit is that undercut, which is *why* Bellman-Ford exists.

### Code Snippet
```python
prices = [math.inf] * n
prices[src] = 0
for _ in range(k + 1):                       # rounds = flight budget
    unsettledPrices = prices.copy()          # working copy = next generation
    for source, target, price in flights:    # sweep the flat edge list, no adjacency map
        if prices[source] == math.inf:
            continue                          # unreachable source can't relax anything (optimization)
        if unsettledPrices[target] > prices[source] + price:   # read source FROZEN, write target to copy
            unsettledPrices[target] = prices[source] + price
    prices = unsettledPrices                 # promote the generation
return prices[dst] if prices[dst] != math.inf else -1
```

## 🟡 206. Reverse Linked List (Recursion) — Jul 14, 2026
**Sticking point**: Reached for `returnNode.next = head` again — conflating the *returned head* (the original tail, pass-through cargo, same object at every level) with the node to attach to (the sublist's **tail**, which is still reachable as `head.next`). Fix that holds: bind `tail = head.next` as its own name before rewiring, so the two roles can't collide. Same fork as Jul 3.

## 🔴 743. Network Delay Time (Dijkstra) — Jul 13, 2026
**Topic**: Advanced Graphs — Dijkstra, single-source shortest path on non-negative weights (first exposure)

### Where did I get stuck?
Read it as BFS and reached for a **FIFO queue**. The whole algorithm was taught, not recalled: why the queue becomes a min-heap, what "settled" means, and why a node is marked settled **on pop, not on push**. Self-derived only the 743-specific half — that the answer is the *max* over the shortest distances, and that `len(settled) == n` is the reachability test.

### Core Realization
**Dijkstra is BFS with two substitutions: the FIFO queue becomes a min-heap keyed on distance, and `+1 per hop` becomes `+w per edge`.**

BFS is correct on unweighted graphs only because "fewest edges" and "shortest distance" are the same thing there. Weights break that: one edge of weight 100 is longer than five of weight 1. A FIFO pops in *insertion* order, which says nothing about distance — so you need a structure that returns the smallest accumulated distance on demand. That's the heap.

**A push is a claim; a pop is a verdict.** Marking visited on push (which BFS gets away with) locks in a distance that may not be final:
> `A→B` = 100, `A→C` = 1, `C→B` = 1. Relaxing `A` pushes `(100, B)` and `(1, C)`. Mark-on-push freezes B at 100; the real answer, `A→C→B` = 2, is then discarded. Mark on **pop** and B settles at 2.

**Why the last pop is the maximum** (what makes `minTime = dist` on every iteration a free `max()`): every future heap entry has the form `dist[settled] + w`, where `dist[settled] ≥` the value just popped and `w ≥ 0`. So nothing smaller than the current pop can *ever enter the heap* — pops come out in non-decreasing order. **This is exactly where non-negative weights are load-bearing**: allow `w < 0` and a future push could undercut a finalized distance, which kills settle-on-pop. That crack is why Bellman-Ford exists (787, Jul 14).

### Code Snippet
```python
adjMap = collections.defaultdict(list)          # static lookup: node → [(neighbor, weight)]
for source, target, weight in times:
    adjMap[source].append((target, weight))

hasShortest = set()                             # settled = answer locked in
minHeap = [(0, k)]                              # dynamic frontier: (distance, node)
minTime = 0

while minHeap:
    cumulativeWeightToNode, node = heapq.heappop(minHeap)
    if node in hasShortest:                     # stale duplicate — a better route already settled it
        continue
    hasShortest.add(node)                       # settle on POP, never on push
    minTime = cumulativeWeightToNode            # pops are non-decreasing → this is a running max

    for neighborNode, neighborWeight in adjMap[node]:
        if neighborNode not in hasShortest:
            heapq.heappush(minHeap, (neighborWeight + cumulativeWeightToNode, neighborNode))

return minTime if len(hasShortest) == n else -1  # unreachable node never settles
```
`O(E log V)`. An unreachable node is never pushed, so it never settles — which is the whole `-1` check.

## 🟡 74. Search a 2D Matrix — Jul 13, 2026
**Sticking point**: Both binary searches initialized `r` as **exclusive** (`len(...)`) while the loop bodies treated it as **inclusive** (`l = m` in the row search, `l <= r` in the value search), so `m` could reach `len(...)` → IndexError on a 1-row matrix and on any miss. **5th boundary-arithmetic failure** (after 424, 75, 567, 901) — approach right, boundary expression wrong. Invariant to state before writing the loop: `r` inclusive ⇒ start at `len - 1`; `r` a never-dereferenced sentinel ⇒ start at `len` (the `while l < r` / `r = m` shape, which he used correctly in 875 the same day).

## 🟡 875. Koko Eating Bananas — Jul 13, 2026
**Sticking point**: Binary search was right (search space `[1, max(piles)+1)`, lower-bound shrink `r = m`, return `l`) — the feasibility check wasn't: `ceil(pile // speed)` floors *first*, so `ceil` rounds an already-integer value and does nothing (`3 // 4 == 0`, not 1). Partial hours vanish, `canFinish` approves speeds that are too slow. Needs true division so there's a fraction left for `ceil` to round up; Koko can't span two piles in one hour, so every leftover costs a full hour.

## 🟡 271. Encode and Decode Strings — Jul 13, 2026
**Sticking point**: `decode` had the right chunk-parsing (scan to `#`, read the length prefix, slice `lenStr` chars) but drove it with `for i in range(len(s))` — which steps `i` by 1, so after the first word it restarted mid-chunk and `int()` choked on non-digits. Chunk walking needs a `while` so you can set `i = j + 1 + lenStr` yourself. Also returned `string` (the last chunk) instead of `result`.

## 🟡 124. Binary Tree Maximum Path Sum — Jul 13, 2026
**Sticking point**: Postorder skeleton came out clean from a blank page (`nonlocal` accumulator, return one branch upward), but both correctness details were missed and neither was self-caught: the peak candidate omitted `node.val` (`max(maxPath, leftSum + rightSum)` — `[1,2,3]` → 5, not 6), and negative child sums weren't clamped with `max(..., 0)`, so a losing branch drags the parent down (`[2,-1]` → 1, not 2).

## 🟡 146. LRU Cache — Jul 7, 2026
**Sticking point**: Recalled the whole design cold (hashmap + DLL with two sentinels, get-promotes, evict `tail.prev` + `del map[node.key]`) — big jump from the Jul 4 🔴. Friction was peripheral: needed the type-checker error explained (untyped param = `Any` = silent; annotating `delete(node: ListNode)` surfaced the unprovable `.prev is not None` invariant → resolve with `assert`).

## 🟡 1448. Count Good Nodes in Binary Tree — Jul 10, 2026
**Sticking point**: Conflated "not a good node" with "dead end" — combined base case `if not node or node.val < currentMax: return 0` pruned the whole subtree under any non-good node, missing good descendants below it (e.g. `3→1→5`: 5 is good but 1 isn't, so 1's `return 0` skipped 5). Fix: only null stops recursion; a non-good node counts 0 but still recurses. Goodness is per-node, not a traversal gate.

## 🟡 424. Longest Repeating Character Replacement — Jul 10, 2026
**Sticking point**: Had the sliding-window idea + the incremental `maxFreq` optimization, but botched three details: (1) shrink condition inverted — `maxFreq + k > r - l + 1` instead of `(r - l + 1) - maxFreq > k`, so `l` ran off the end (index error); (2) forgot `r += 1` on the outer loop; (3) answer used `maxFreq + k` instead of the window size `r - l + 1`. Window is *invalid* when `windowLen - maxFreq > k`; shrink then; answer is the max valid window length.

## 🟡 567. Permutation in String — Jul 12, 2026
**Sticking point**: Sliding window + 26-slot freq arrays were fully correct; the window-length expression was off by two — `r - l - 1 > len(s1)` instead of `r - l + 1 > len(s1)`. An inclusive `[l, r]` window has length `r - l + 1`, so the window grew to `len(s1)+2` and the freq map never matched. (Same family as 424's inverted shrink test — window-boundary arithmetic is the recurring slip.)

## 🟡 229. Majority Element II — Jul 12, 2026
**Sticking point**: Reached for a heap first instead of a count map — needed a hint to land the right structure. (Majority-II is a counting problem: hashmap of counts, or Boyer-Moore with two candidates; a heap solves the wrong question.)

## 🔴 901. Online Stock Span — Jul 12, 2026
**Topic**: Monotonic stack — stack entries carry accumulated state (new)

### Where did I get stuck?
Had the monotonic-decreasing-stack intuition ("pop while current price beats the top, accumulate") but **could not see how to persist the count across calls** — knew a result had to be stored, but the idea of putting it *on the stack* as a tuple never surfaced. Needed the `(price, span)` pair handed over. Also had the boundary strict (`>` instead of `>=`).

### Core Realization
**The stack entry is a compressed receipt, not just a value.** Push `(price, span)` — each entry carries the count of everything it already absorbed. On a new price: start `span = 1`, then while `price >= stack[-1][0]`, pop and `span += poppedSpan`, then push `(price, span)` and return it.

Why absorbing the popped span is valid: the popped entry already swallowed days that were all ≤ *its* price; since its price ≤ today's, transitivity makes them all ≤ today's too. So you inherit its entire count in **one O(1) pop** instead of re-walking those days. That's the whole trick — and it's the general lesson: **when a monotonic stack needs to answer "how many," store the running count alongside the value rather than recomputing it.**

Boundary: `>=`, not `>`. Equal prices count toward the span (a day priced the same as today is still ≤ today).

### Code Snippet
```python
class StockSpanner:
    def __init__(self):
        self.stack = []                    # (price, span)

    def next(self, price: int) -> int:
        span = 1                           # today always counts
        while self.stack and price >= self.stack[-1][0]:   # >= not >
            _, priorSpan = self.stack.pop()
            span += priorSpan              # inherit the receipt
        self.stack.append((price, span))
        return span
```
Trace `[7,2,1,2,4]` → `[1,1,1,3,4]`. At `next(4)`, one pop of `(2,3)` picks up 3 days at once — the days `2,1,2` are never re-walked.

## 🔴 124. Binary Tree Maximum Path Sum — Jul 11, 2026
**Topic**: Trees / postorder DFS with a side-channel accumulator (new, Hard)

### Where did I get stuck?
Got the postorder DFS shape and correctly returned "one child" upward — but needed three separate fixes, all flagged: (1) the global max never considered the path that *peaks* at a node using **both** children; (2) negative child contributions weren't clamped to 0; (3) `maxPath` initialized to `0` instead of `-inf`, breaking all-negative trees.

### Core Realization
**The recursion returns something different from what you're computing.** Unlike every other tree DFS so far (104, 110, 1448 — where `return dfs(root)` *is* the answer), here `dfs` returns the best path it can **hand upward** (node + at most ONE child, because a path continuing to the parent can't also branch), while the **answer** is the best path that **peaks** at some node (node + BOTH children, closed off — it can't extend up). Two different quantities in one function: one flows up the call stack, the other accumulates in a `nonlocal` side variable. That's why you can't write it as a pure return-the-answer recursion.

Both quantities trace back to the no-branching path rule: a node touches ≤ 3 edges (parent, left, right) and a path can use at most 2 of them.

Two sign traps:
- **A branch is optional** — clamp each child's gain with `max(gain, 0)` ("take this branch only if it helps").
- **All-negative trees are legal** — init the global max to `-inf`, not `0`, or a lone `-3` node wrongly answers `0`.

### Code Snippet
```python
def maxPathSum(self, root):
    maxPath = float('-inf')          # NOT 0 — all-negative trees are valid

    def dfs(node):
        nonlocal maxPath
        if not node:
            return 0
        left  = max(dfs(node.left), 0)    # decline a branch that hurts
        right = max(dfs(node.right), 0)
        maxPath = max(maxPath, node.val + left + right)   # PEAK here: both children
        return node.val + max(left, right)                # HAND UP: one child only

    dfs(root)
    return maxPath
```

## 🟡 503. Next Greater Element II — Jul 11, 2026
**Sticking point**: Had the 496 monotonic-stack pattern cold; stuck only on the circular wrap. Hint unblocked it — simulate the wrap by iterating `2*n` with `i % n` (don't physically double the array), and only push indices during the first lap (`i < n`); the second lap just resolves leftovers.

## 🟡 211. Design Add and Search Words (retry) — Jul 11, 2026
**Sticking point**: Structure recalled (loop for concrete chars, recurse+fork at `.`), but two slips resurfaced: (1) `search` didn't `return dfs(...)` — threw away the answer, returns `None`; (2) first pass had the wildcard quantifier inverted (`if not dfs(): return False` = `all()`) before fixing to `if dfs(): return True` + trailing `return False` = `any()`. The `any` semantics (succeed if any child branch reaches an `isWord` end) took a beat to re-derive.

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

---

## 🟡 743. Network Delay Time (Dijkstra) — Aug 4, 2026
**Sticking point**: not the algorithm — Dijkstra was recognized cold and the whole scaffold (adjacency
map, heap seeding, `visited` marked on *pop* with the skip-guard) was correct from a blank page. The
miss was the **aggregation semantics**: accumulated `totalTime += currentWeight` instead of taking the
**last arrival**. Summed per-node arrival times that were never meant to combine. Self-reported as
"stuck on where to do the visited" — the `visited` placement was already right; the real defect was
one line below it.

## 🟡 138. Copy List with Random Pointer (hashmap two-pass) — Aug 4, 2026
**Sticking point**: map approach was correct, but three bugs surfaced by coach, not self-caught —
(1) `next` pointers never wired (copy was 5 isolated nodes, not a list); (2) `oldToNewMap[old.random]`
KeyError'd on `random=None`; (3) `oldToNewMap[head]` KeyError'd on empty head. All three are the
*None-guard family* — core algorithm fine, misses were unhandled null edges.

## 🟡 332. Reconstruct Itinerary (Hierholzer) — Aug 4, 2026
**Sticking point**: teaching measurement after 2× 🔴 — the teaching took. Hierholzer recalled cold
(postorder append, reverse, "final node has nowhere to go"). One nudge needed: **forgot the
lexicographic-smallest requirement entirely** → prompted, immediately reached for a per-airport
min-heap. Also left a **vestigial `visited` set** in after switching to `heappop` — harmless (verified
correct over 4000 random multigraphs vs brute force) but dead weight, since popping already consumes the
edge. Mechanism-inventory miss, not a correctness bug. Execution axis still lacks a 🟢 for Hierholzer.

### 2026-08-06 · 261 Graph Valid Tree (DFS) 🟡
**Sticking point**: two bugs I flagged (not self-caught). (1) `if i in visited` / `visited.add(i)`
inside `dfs` used the **outer loop variable `i`** instead of `currentNode` — the traversed node was
never recorded, so cycle detection ran on the wrong identity. (2) `dfs(neighbor, currentNode)` **discarded
its return value** — a deeper `False` (cycle found) never propagated up. Recognition was clean (undirected
+ "is it a tree" → DFS cycle + connectivity), parent-skip for the back-edge was correct, and the design
was clean (edge-count guard + cycle check ⟹ connectivity implied, no redundant guard). Complexity: missed
the **recursion stack** as a space term (path graph → O(V) deep) — carded, freebie.

### 2026-08-06 · 496 Next Greater Element I 🟡
**Sticking point**: the monotonic-stack pass (next-greater for every nums2 position) was correct and
complete unaided. Stuck on the **bridge** — results were keyed by nums2 *index* while nums1 supplies
*values*, so the nums1 lookup had no path. Nudge given: the "all integers unique" constraint makes value↔answer
1:1, so **key the results map by value, not index** → nums1 becomes a direct lookup (also what unlocks the
O(n1+n2) follow-up). Complexity was strong and self-derived: amortized O(n) time (each element pushed/popped
once), O(n) space; no miss.

### 2026-08-07 · 19 Remove Nth Node From End (Postorder Recursion) 🟡
**Sticking point**: the counter was right this time — `n + 1` from the end, incremented postorder, with
the reasoning written out in a pre-code comment. The bug was the **traversal root**: `dfs(dummy.next)`
started at `head`, so the dummy was never visited and the one case where the dummy *is* the surgeon
(`n == sz`, remove the head) was unreachable — `[1], n=1` returned `[1]` instead of `[]`. Nudge given
was the failing case only; fix found instantly and unaided. Also a vestigial `returnNode = dfs(...)`
assignment (dfs returns nothing) — dead, flagged, not a correctness bug. Complexity self-derived and
correct: O(n) time one pass, O(n) space for the recursion stack; no miss.
**Note for the next rep**: this is the 3rd consecutive 🟡 on the postorder variant but the **first**
whose cause is not the counter's origin. Learner declined the teach ("caught it instantly") — re-rep,
not teach. If the *next* one misses on the counter again, the original trigger stands.

### 2026-08-07 · 269 Alien Dictionary 🟡
**Sticking point**: recognition was clean and unprompted — the pre-code comment names topological sort and
reaches for Kahn's (indegree counter + adjacency map + queue) before any code, and the prefix failure case
(`["abc","ab"] → ""`) was handled correctly *first*, unaided. Four execution bugs, none self-caught:
1. **Node set built from the wrong map.** Queue seeded by iterating `adjMap`, which only holds letters with
   *outgoing* edges — so a letter with no edges at all is never emitted. `["ac","ab"] → "cb"`, missing `a`.
2. **No cycle detection.** Kahn's detects a cycle by *finishing early*, not by failing; the final
   `len(result) == len(counterMap)` guard was absent. `["x","a","b","a"] → "x"` instead of `""`.
3. **`for char in range(len(word))`** on the init pass — iterated indices, not characters, so `counterMap`
   was keyed by ints and the first edge raised `KeyError`.
4. **No `break` after the first differing position.** Kept comparing past it and recorded `a→b` *and* `b→a`
   from `["ab","ba"]` — a self-invented cycle. **Only the first difference carries information.**
Verified after the fixes: 3000 random inputs vs brute-force permutation check, plus 10 edge cases, all clean.
**Complexity: 3rd miss on 269, all the same fixed-alphabet family** (Jul 27 freebie, Jul 29 repeat, tonight).
Time `O(c)` was right and the unit was right (total characters, not word count — the 721/271 lesson holding).
Space given as `O(c)`; it is **`O(1)`** — lowercase-only means `V ≤ 26`, `E ≤ 676`, neither growing with `c`.
**Note for the Aug 10 build**: #1 and #4 are both *set-construction* errors (which nodes exist / which edges
exist), and #4 is the same edge-set bookkeeping flagged as the open gap after Jul 29. That is now two
consecutive reps failing on edge bookkeeping — a teach signal by the 540/19 rule. #2 was closed by
explanation this session (why Kahn's needs no `visited`), so the next rep measures whether that took.

## 2026-08-09 · 133 Clone Graph (BFS) — 🟢 s1 → 🟡

**Sticking point (one bug):** the edge append lived *inside* the `if neighbor not in oldToNewMap` guard,
so an edge was only recorded the first time its far end was met. In an **undirected** graph every edge is
met twice, once from each side, and the second meeting always finds the far node already cloned — so
**every edge's second appearance was silently dropped**. Two-node graph `1—2` cloned to `1' → 2'` with
`2'.neighbors == []`.

**The framing that fixed it:** the guard's real job is *don't clone twice, don't enqueue twice* (it exists
to terminate on cycles). **Node identity and edge recording are separate concerns** and were fused —
"have I made this node?" is a different question from "have I recorded this edge?". Same shape as 721's
redundant `find` guard earlier the same day: a mechanism doing more jobs than its condition justifies.

**Also of note:** first **BFS** solve of this problem; the three prior attempts were DFS. `techniques.yml`
names the technique *"Graph Clone (DFS + Hash Map)"*, which the learner spotted as over-specified — the
map-as-clone-identity idea is traversal-agnostic. **Vocabulary item for the Aug 10 build**, alongside the
721-is-not-pure-Union-Find finding from the same session.

**Complexity:** said `O(n)` time; actual **`O(V+E)`** — the inner neighbour loop runs 2E times and `E` is
not bounded by `V`. **Mirror image of the Aug 5 323 miss** (there: `O(E)`, dropped the `V`). Freebie spent.
Cue to carry: *a graph traversal touches two things, so its bound almost always has two terms — a one-term
answer means something was dropped.*

---

## 901. Online Stock Span — 🟡 Shaky (2026-08-13)

**Sticking point:** had the right structure unprompted (*"stack of tuples… decreasing stack where each value holds its own span"*) and had even performed **one** absorption correctly by hand — `(70, 2)`, taking the popped `60`'s span with it — but read the pop as a **single check rather than a loop**, so `75 → 4` looked unreachable. Unstuck by being handed the stack state at `75` and asked to apply *their own* rule repeatedly. **The rule was theirs; the iteration was coach-supplied.**

**Cue to carry:** *if you can do the step once, ask what stops you doing it again* — a monotonic stack's pop is always `while`, never `if`, because the element you just uncovered gets the same question as the one you removed.

---

## 127. Word Ladder — 🟡 Shaky (2026-08-13)

**Sticking point:** ⭐ **not the code — the code was 🟢-grade.** Blank page, zero hints, correct first pass, and **Monday's counter teach held cold across the deliberate 3-day gap**, including the `return depth + 1` at *discovery* that had broken on all three prior reps (Jul 18 · Jul 21 · Aug 3).

**What capped it was complexity, and it took three corrections.** The build phase was priced correctly and unprompted — `O(C·L)`, with the slicing cost named — and the learner then **volunteered the fixed-alphabet collapse** (a `.it` bucket holds ≤26 words, so the `E` term dies). Then the same string cost was dropped twice: the BFS loop re-slices identically to the build loop (so the phases **tie** at `O(V·L²)`, neither dominates), and `adjMap` holds `V·L` keys **of length L** (so space is `O(V·L²)`, not `O(V·L)`). Separately, `L` was held symbolic for time then collapsed via `L ≤ 10` for space — mixed conventions in one answer.

**Cue to carry:** *a string is not O(1)* — slicing, hashing, comparing and **storing** one all cost `O(L)`. And the free check that would have caught it unaided: **build-and-store is one loop doing one kind of work, so time and space should come out equal.** A space answer a factor of `L` cheaper than the time answer is the tell.

**Learner's own read, and it is scheduled:** *"this is a very hard problem to knock down for Big O, we should definitely practice it more."* Carried to the Aug 17 build as a complexity-drill item.
