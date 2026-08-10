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
