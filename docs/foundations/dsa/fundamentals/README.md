# Fundamentals — the maths under the techniques

Theory the problems actually lean on. **Nothing enters until a rep has needed it** —
same discipline as `techniques.yml`. A textbook table of contents would be longer and
less useful; every card here exists because a session stalled without it.

| Card | Answers | Earned on |
|---|---|---|
| [big_o.md](big_o.md) | growth rates, per-technique costs | — |
| [circuit_rank.md](circuit_rank.md) | `E − V + C` = independent cycles; the rank-0 case is the tree rule | 261, Aug 16 |
| [degree_and_parity.md](degree_and_parity.md) | why a walk strands where it does; Eulerian conditions | 332 / Hierholzer |
| [amortized_analysis.md](amortized_analysis.md) | why one O(n) call can still be O(1) amortized | 901 · 739 · 503 |

## Not yet written — waiting for a rep to demand them

**Monotonic predicates** (why binary search on the answer is valid) · **pigeonhole**
(the 202 collapse) · **exchange argument** (when greedy is provably correct).

⭐ The exchange argument is already half of the **Intervals + Greedy concept primer**
scheduled for the Aug 17 build, so it gets written there and lands here as a byproduct
— see [[feedback_concept_primer]]. That is the intended pattern: primers fill this
folder, rather than this folder being a separate chore.
