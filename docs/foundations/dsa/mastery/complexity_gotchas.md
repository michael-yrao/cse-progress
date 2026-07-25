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

Almost every miss so far is **space**, in one of these buckets. Time has been consistently correct.

| Category | Code trigger | Coach cue (fire this) | Right answer |
|---|---|---|---|
| **Fixed-alphabet array** | `[0]*26`, `[0]*128`, a bounded freq dict | *"that array — bounded by input, or by the alphabet?"* | **O(1)** — bounded by the alphabet, not `n` |
| **Recursion stack** | any `self.f(...)` / recursive helper | *"count the stack — how deep does it go?"* | **O(depth)** — O(n) for a list/skewed tree, O(log n) balanced |
| **2D structures** | grid `visited` set / heap of cells | *"your frontier — a line or an area?"* | **O(n²)** — the set/heap can hold nearly every cell |
| **Output counting** | returns a built list/structure | *"counting the output, or extra-only?"* | state the convention: "O(1) *extra*" vs "O(n) incl. output" |
| **Graph traversal (time)** | adjacency list + visit-each-node loop (BFS/DFS/topo) | *"each node once, each edge once — do those add or multiply?"* | **O(V + E)** — visits add, they don't multiply; O(V·E) would mean re-walking every edge per node |

**Space-contributors checklist (run before answering):**
(a) extra data structures — bounded by *input* or by a *constant alphabet*?
(b) recursion — how deep does the stack go?
(c) am I counting the output?

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

<!-- Add a row on every first-time complexity miss. A repeat miss on a problem ALREADY here caps that
rep at 🟡 (freebie spent) — note the repeat in the schedule/stuck_log where the rating is recorded.
The card grows only on a NEW problem's first miss, so it stays short. -->
