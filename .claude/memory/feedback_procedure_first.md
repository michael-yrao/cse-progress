---
name: feedback-procedure-first
description: Teach a new/unfamiliar algorithm procedure-first in plain operational language — the literal loop, run by hand on a tiny example — and add the correctness proof / complexity / jargon only later, only if asked
metadata:
  type: feedback
---

**When the learner is trying to understand or code an algorithm they don't know, teach it
procedure-first, not proof-first.** Lead with the literal, imperative loop in plain operational
language — *"each round: pick the unvisited node with the smallest number, mark it done, update its
neighbors"* — then run it **by hand on a tiny (3–4 element) example as concrete numbers**. Only after
they can execute it, and only if they ask "but why does this work?", introduce the correctness proof,
complexity analysis, and named concepts.

**Order that works:** operational steps → hand-trace on concrete numbers → (optional, on request) why
it's correct / complexity / the proper names.

**Order that failed (Prim's, 1584, Jul 18 2026):** opened with the cut-property swap proof, "settled"
nodes, a Dijkstra analogy, and O(V² log V) vs O(V²) — *before* the learner could execute a single step.
Buried the plain 3-step loop until after three rounds of theory. Piled on jargon (blob, settled,
high-water mark, crossing edge, component). It made a hard algorithm much harder; the learner said
"this makes no sense" and, tellingly, their *own* code comments were far clearer than my prose:
*"get the closest node we haven't visited," "relax every other node relative to it"* — zero jargon,
pure operation.

**Rules:**
- **Separate "execute it" from "why it's optimal."** Two different lessons. Get execution first; the
  justification (esp. greedy-correctness proofs — the hardest part) is optional and later. It is *not*
  needed to write the code.
- **Answer a mechanics question with mechanics,** never with more concept. "How do I find the smallest
  unvisited node?" → the scan, not another layer of framing.
- **Strip jargon** unless the learner asks for the name. Say "the unvisited node with the smallest
  number," not "the settled node minimizing the key."
- **The tell:** when they say "this makes no sense," strip DOWN to the concrete procedure — do not add
  another layer of *why*.

**Why:** for an algorithm-you're-coding, the load-bearing thing is the **procedure**, not the
correctness theorem. This refines [[feedback-spine-first]] — I mistook the *proof* for the spine; the
spine is the operational loop. Also an instance of [[feedback-turn-economy]] (don't bury the answer
under layers). Applies to any new DSA algorithm, and to SD/AI mechanisms the learner is implementing.
