# Recognition Gotchas — reference card + miss ledger

The **front-gate** companion to [complexity_gotchas.md](complexity_gotchas.md): that one enforces
analysis at the *end* of a rep, this one enforces **pattern recognition at the start**. Reread it
like a Recall Card; the ledger below tracks which triggers trip the learner.

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

## Miss ledger

*(dated line per miss: problem · what they called · correct call · the picking feature they missed)*

_None yet — started Jul 25, 2026._
