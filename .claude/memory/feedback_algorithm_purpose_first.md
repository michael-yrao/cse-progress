---
name: feedback-algorithm-purpose-first
description: When teaching or explaining any algorithm, lead with the PROBLEM it solves and why it had to exist (what the prior algorithm couldn't do) — never with its mechanism
metadata:
  type: feedback
reconciled: 2026-08-17
---

**Set by the learner Jul 26, 2026** (during 787 / Bellman-Ford). When explaining any named algorithm,
**state the problem it solves before any mechanism**, in this order:

1. **The problem statement** — the input, the output, and the constraint that makes it non-trivial.
   *"Single-source shortest paths on a weighted directed graph where edges may be negative."*
2. **Why it exists at all** — what the obvious/earlier algorithm can't do here. An algorithm is almost
   always a **repair of a specific broken assumption** in a simpler one. Name the broken assumption.
   *"Dijkstra settles the cheapest node and never revisits; a negative edge can reduce an already-settled
   distance, so that step is invalid."*
3. **What it costs** — generality is bought with something, usually time. *"O(V·E) vs O(E log V)."*
4. *Only then* the mechanism.

**Why:** the learner asked for this directly after a spine-first explanation that led with mechanism
("relax every edge V−1 times") — correct, and still not what they needed. Mechanism tells you *how to
run it*; purpose tells you **when to reach for it**, which is what recognition (and the interview's
first two minutes) actually grades. Two algorithms with the same shape are told apart by the assumption
each one repairs, not by their loops. Without purpose, an algorithm is a memorized procedure with no
retrieval cue — which is exactly how it comes back 🔴.

**How to apply:** this **refines [[feedback_spine_first]], it does not replace it** — still 2–3
load-bearing facts, then stop. The change is *which* facts are load-bearing: for an algorithm, fact 1
is the problem and the broken assumption, not the loop. Compatible with
[[feedback_procedure_first]]: when the learner is **coding** an algorithm they don't know, procedure
still leads — but purpose is one sentence *before* it, not an optional epilogue. Ties to
[[feedback_recognition_gate]]: "what problem does this solve" and "why is this the technique here"
are the same question asked from opposite ends.

⚠️ **Promoted to a scheduled event Aug 16, 2026 — see [[feedback_concept_primer]].** This rule is correct and was still not enough, because it only fires *while you are already explaining*, which in practice means after a rep has gone wrong. The primer moves the front half of it — the object, its name, and the discriminator — **before the first attempt**, as a weekly-build step. 332 is the worked example: five sessions, because its first attempt was the introduction to Eulerian paths.

