---
name: project-recognition-probes
description: Weekly cold recognition probe — one unseen LC problem/week from an already-🟢 technique, label stripped, disposable (no tracker row on 🟢)
metadata:
  type: project
reconciled: 2026-09-03
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
| **Which problem** | **pick the TECHNIQUE first**, then the easiest *unseen* problem that genuinely forces it — see the difficulty rule below. Difficulty is a consequence of the technique, never a dial set in advance |
| **Tracker row** | **none if 🟢** — a disposable rep ([[project_library_carrying_capacity]]). Only 🟡/🔴 earns a row, because only a gap needs repetition |
| **Always logged** | the *recognition* outcome → `recognition_gotchas.md`, regardless of rating |

⚠️ **Never probe a technique that is 🟡 or has no 🟢** (Dijkstra, Bellman-Ford, Floyd-Warshall,
Hierholzer, Prim's, BFS-on-implicit-graph…). Those need **conversion reps**, not probes — a probe there
just manufactures a 🟡 row at ~73 units/year on a Medium. The pool that is safe today: Binary Search 🎓 ·
Tree DFS 🎓 · Grid BFS 🎓 · Linked List Merge 🎓 · Sliding Window · Union-Find · Heap · Monotonic Stack ·
Topological Sort · Hash Set Membership.

## Difficulty follows the TECHNIQUE (settled Aug 17, 2026)

**The rule was always "Medium or below"; practice drifted to Easy-only.** Probes #1–3 were all Easy,
and the Aug 17 board hardcoded "Easy" into the probe rows. Nothing ever decided that — it accreted.

⚠️ **An Easy-only pool structurally cannot probe most of what is banked.** Of the 44 techniques at
🟢/🎓, the majority have **no unseen Easy problem at all**: Topological Sort, Union-Find, Trie, Binary
Search on Answer, Monotonic Stack, LRU, Dutch National Flag, Kadane, Multi-source BFS, Deep Copy via
Hash Map, Prefix/Suffix Products, Tree Construction. Those techniques exist only at Medium+. Easy-only
leaves roughly ten probeable techniques — Tree DFS, Binary Search, Two Pointers, Hash Set/Map,
Frequency Counting, Linked List basics, Array fundamentals — and probes them forever.

⭐ **And the bias runs the wrong way.** The techniques with no Easy option are disproportionately the
ones where *recognition is the hard part* (Binary Search on Answer, Monotonic Stack, Topological Sort,
Union-Find), while the Easy pool concentrates in techniques whose recognition is near-trivial (two
pointers on a sorted array, DFS on a tree). So an Easy-only diet measures the **easy half of the axis
the probe exists to measure**. Probe #3 is the proof by contrast: 69 Sqrt(x) was Easy but
recognition-rich *because it had no array shape to match* — a quality that is common at Medium and
rare at Easy.

**The rule:**

1. **Pick the technique, then the problem.** Take the easiest unseen problem that genuinely *forces*
   that technique. For a third of the pool that is necessarily a Medium.
2. **Per-technique ratchet.** A technique probed at Easy that came back 🟢 gets its **next** probe at
   Medium. Recognition proven at Easy is not proven at Medium.
3. **Cap at Medium. No Hard probes.** Two reasons, and the second is the load-bearing one: a 🔴 Hard is
   the most expensive object in the system (4.5 units on the day, plus a +2 interval), and Hards
   typically fail on **execution**, which contaminates a measurement whose whole subject is the
   pre-code call. Revisit only if the Medium pool saturates.
4. ⚠️ **Verify the "no Easy exists" claim when picking.** The list above is from knowledge of the LC
   catalog, not a live query.

**Budget consequence — a Medium probe is 2.0, not 1.0** (🟡-equivalent × Medium 1.0). At the **8.0**
ceiling that is a real slot, not the "fits the spare, costs nothing" an Easy probe was. Price it at the
weekly build; it will sometimes displace a due review, and that is the trade being made deliberately.

## ⚠️ The scaffold path is a spoiler — this rep needs its own root

`new_problem.py` writes to `dsa/leetcode/<pattern>/<number>_<name>.py`. **The path names the technique**,
so scaffolding a probe the normal way hands over the answer before the statement is read. Use the neutral
root **`dsa/probes/`**, which **does double duty**: a root outside `solutions.roots` is also the
preferred way to stop `update_review_dates.py` auto-resurrecting a row for a problem deliberately left
untracked (the discovery-resurrection trap that bites both disposable reps and graduation).

⚠️ **This once said `dsa/leetcode/probes/` — corrected Aug 21, 2026. That path is INSIDE
`solutions.roots: ["dsa/leetcode"]`**, so every probe ever run would have been discovered and given a
tracker row, which is the exact cost the neutral root exists to avoid. The live directory has always
been `dsa/probes/` (see [`dsa/probes/README.md`](../../dsa/probes/README.md), which states the rule
correctly); only this file was wrong.

⭐ **And the converse rule, learned Aug 21, 2026 on 202: when a probe comes back 🟡/🔴 and earns a row,
MOVE the file into `dsa/leetcode/<pattern>/` in the same edit.** Left in `dsa/probes/`, it becomes a
tracked problem that **neither retry script can reach** — `new_problem.py` resolves retries under
`solutions.roots` and would mint a second file, forking the attempt history; `restore_history.py` keys
stashes back by the same glob and would orphan them. The probe root protects an *untracked* rep; once a
row exists the protection is over and the file belongs with the tracked problems.

**Also strip the label everywhere else:** don't name the pattern, the topic tag, or the neighbouring
problems when presenting it. The learner states **shape → technique → the one feature that picks it**
cold, and *that statement is the thing being measured* — the code is secondary.

## The free diagnostic

Because a 🟢 creates no row and a 🟡/🔴 does, **the row-creation rate over a rolling ~15 probes IS the
measurement of whether the pool still teaches**: ≥85% 🟢 → the pool has stopped teaching; ≤70% 🟢 →
real gaps remain, keep consolidating.

⚠️ **Two levers answer "≥85% 🟢", and they are ORDERED — cheapest first (Aug 17, 2026).**

1. **Raise difficulty inside the pool you already own** (Easy → Medium, per the ratchet above). Adds
   **zero** permanent demand: no new technique to maintain, and a 🟢 probe still creates no row.
2. **Only when the Medium pool is also ≥85% 🟢**, open the next expansion tier.

The original rule jumped straight to (2), which is the expensive lever — every new technique is
maintenance demand forever, and the deficit is already negative. Exhaust the free one first.

## Standing exception to record at each weekly build

The fill table says **surplus ≤0 → no consolidation reps**, and surplus is negative — **recomputed
Aug 30, 2026: demand 9.27 units/day against the 8.0 ceiling, i.e. −1.27/day (−8.9/week)**, so the
gate is still shut and the exception is still the thing that lets a probe run. (The figure here read
a stale **−9.6** until this pass; a hold justified by a number expires the moment the number moves —
recompute it at every build rather than copying this one forward.) This runs as a
**deliberate, arithmetic-backed exception**, not a quiet override: the gate exists to stop *permanent*
demand growth, and a disposable probe adds one slot once and **zero forever after**. Restate the
reasoning at each build rather than letting it become invisible precedent — and if the probe's
row-creation rate runs high (lots of 🟡), the exception has stopped being cheap and should be revisited.
