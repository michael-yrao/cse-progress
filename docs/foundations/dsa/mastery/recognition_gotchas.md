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

## Trigger → technique map (the transfer — this is the part to master)

| Input shape | + What's asked | → Technique | Picking feature |
|---|---|---|---|
| Weighted graph | min cost / time to reach node(s) | **Dijkstra** | edges **weighted** & non-negative (else BFS if uniform, Bellman-Ford if negative / k-stops) |
| Unweighted graph / grid | fewest steps, shortest path | **BFS** | every edge same cost |
| Weighted graph | shortest path, negative weights or ≤k edges | **Bellman-Ford** | negatives allowed / hop limit |
| Sorted array | find element / boundary / min-max feasible value | **Binary search** | monotonic + sorted (or monotonic answer space) |
| Array, contiguous run | longest/shortest/count subarray meeting a condition | **Sliding window** | contiguous + window monotonicity |
| Array/string, pairs from ends | two values meeting a sum/area condition | **Two pointers** | sorted or convergent-from-ends |

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

## Miss ledger

*(dated line per miss: problem · what they called · correct call · the picking feature they missed)*

_None yet — started Jul 25, 2026._
