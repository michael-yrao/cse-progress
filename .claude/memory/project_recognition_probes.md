---
name: project-recognition-probes
description: Weekly cold recognition probe — one unseen LC problem/week from an already-🟢 technique, label stripped, disposable (no tracker row on 🟢)
metadata:
  type: project
---

**Adopted by the learner Aug 9, 2026:** *"I want to improve my ability to recognize patterns in a
problem… one problem a week for now from LC in topics that we've already covered so I can try to
determine what is the pattern and solve it cold."*

**The hole it fills.** Phase exit grades two axes, recognition and execution. The tracker measures
execution well and recognition **barely at all**, because *a retry names its own technique* —
`dsa_progress.md` reads "743 Network Delay Time (Dijkstra)" and the file sits in `advanced_graphs/`.
The learner is told the answer before opening the file. Recognition evidence is supposed to come from
**new problems and cold cues**, and the board carries almost no new problems. So the axis they want to
train is the one the current system structurally cannot test. See [[feedback_recognition_gate]].

## The design

| | |
|---|---|
| **Cadence** | 1/week for now (a **consolidation rep** — separate ≤2/wk budget, does **not** count against new-algorithm intake, [[feedback_consolidation_reps]]) |
| **Source pool** | techniques already at **🟢 or 🎓** in `technique_coverage.md`, **Medium or below** |
| **Tracker row** | **none if 🟢** — a disposable rep ([[project_library_carrying_capacity]]). Only 🟡/🔴 earns a row, because only a gap needs repetition |
| **Always logged** | the *recognition* outcome → `recognition_gotchas.md`, regardless of rating |

⚠️ **Never probe a technique that is 🟡 or has no 🟢** (Dijkstra, Bellman-Ford, Floyd-Warshall,
Hierholzer, Prim's, BFS-on-implicit-graph…). Those need **conversion reps**, not probes — a probe there
just manufactures a 🟡 row at ~73 units/year on a Medium. The pool that is safe today: Binary Search 🎓 ·
Tree DFS 🎓 · Grid BFS 🎓 · Linked List Merge 🎓 · Sliding Window · Union-Find · Heap · Monotonic Stack ·
Topological Sort · Hash Set Membership.

## ⚠️ The scaffold path is a spoiler — this rep needs its own root

`new_problem.py` writes to `dsa/leetcode/<pattern>/<number>_<name>.py`. **The path names the technique**,
so scaffolding a probe the normal way hands over the answer before the statement is read. Use a neutral
root (`dsa/leetcode/probes/`), which **does double duty**: a root outside `solutions.roots` is also the
preferred way to stop `update_review_dates.py` auto-resurrecting a row for a problem deliberately left
untracked (the discovery-resurrection trap that bites both disposable reps and graduation).

**Also strip the label everywhere else:** don't name the pattern, the topic tag, or the neighbouring
problems when presenting it. The learner states **shape → technique → the one feature that picks it**
cold, and *that statement is the thing being measured* — the code is secondary.

## The free diagnostic

Because a 🟢 creates no row and a 🟡/🔴 does, **the row-creation rate over a rolling ~15 probes IS the
measurement of whether the pool still teaches**: ≥85% 🟢 → the pool has stopped teaching, open the next
expansion tier; ≤70% 🟢 → real gaps remain, keep consolidating.

## Standing exception to record at each weekly build

The fill table says **surplus ≤0 → no consolidation reps**, and surplus is **−9.6**. This runs as a
**deliberate, arithmetic-backed exception**, not a quiet override: the gate exists to stop *permanent*
demand growth, and a disposable probe adds one slot once and **zero forever after**. Restate the
reasoning at each build rather than letting it become invisible precedent — and if the probe's
row-creation rate runs high (lots of 🟡), the exception has stopped being cheap and should be revisited.
