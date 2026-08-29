# 🎯 Recognition probes

**One unseen LeetCode problem per week, label stripped, solved cold.** Adopted Aug 9, 2026 — full
rationale in `.claude/memory/project_recognition_probes.md`.

## Why this directory exists at all

Two reasons, and both are structural rather than cosmetic.

**1. The normal scaffold path is a spoiler.** `new_problem.py` writes to
`dsa/leetcode/<pattern>/<number>_<name>.py` — so the *folder name tells you the technique* before you
have read the problem statement. For every other rep that is harmless. For a probe it destroys the only
thing being measured.

**2. It keeps probes out of the tracker automatically.** `cse.config.yml` sets
`solutions.roots: ["dsa/leetcode"]`, and `update_review_dates.py` auto-creates a tracker row for any
file it discovers under those roots. `dsa/probes/` sits **outside** that root, so a probe file is never
discovered and no `discovery_skip` entry is ever needed. That is the preferred handling for
**disposable reps** — the stopgap is `discovery_skip`, and stopgaps rot.

> ⚠️ **Never move this directory under `dsa/leetcode/`, and never add `dsa/probes` to
> `solutions.roots`.** Either change silently resurrects a tracker row for every probe ever run, which
> is the whole cost this design avoids.

## The rules

| | |
|---|---|
| **Cadence** | 1/week, in the Sunday slot unless the week says otherwise |
| **Pull from** | techniques already at **🟢 or 🎓** in `technique_coverage.md`, **Medium or below** |
| **Pick order** | **technique first, then problem** — the easiest *unseen* problem that genuinely forces it. Difficulty is a consequence, never a dial |
| **Difficulty** | ratchets **per technique**: probed Easy → 🟢 → next probe of that technique is **Medium**. **Cap at Medium**, no Hard |
| **Never pull from** | anything 🟡 or with no 🟢 — those need *conversion reps*, and a probe there just manufactures a 🟡 row at ~73 units/year |
| **Label** | stripped. No pattern name, no topic tag, no "this is like problem X" |
| **The measured thing** | the **pre-code call** — shape → technique → the one feature that picks it. The code is secondary |

## What gets logged

- **Always** → the recognition call (hit or miss) to
  [`recognition_gotchas.md`](../../docs/foundations/dsa/mastery/recognition_gotchas.md), **and a row in
  the [Probe log](#-probe-log--the-tally) below** (the only place a disposable 🟢 probe is counted).
- **🟢 → no tracker row.** The probe was a test of whether the *technique* transfers, not an asset to
  maintain.
- **🟡 / 🔴 → it earns a row**, because only a gap needs repetition.

## The free diagnostic

Because a 🟢 creates no row and a 🟡/🔴 does, **the row-creation rate over a rolling ~15 probes *is* the
measure of whether the pool still teaches anything**:

- **≥85% 🟢** → the pool has stopped teaching. **Two ordered levers, cheapest first:** raise difficulty
  inside the pool you already own (adds zero permanent demand), and *only* when Medium is also ≥85% 🟢,
  open the next expansion tier (every new technique is maintenance demand forever).
- **≤70% 🟢** → real gaps remain; keep consolidating.

## 📒 Probe log — the tally

Every probe gets a row here, **hand-added when it runs** (same discipline as the recognition ledger).
This is the only place probes are *counted*: a 🟢 probe is disposable and creates no tracker row, so
without this table it vanishes from every "problems solved" figure. Two jobs:

1. **Counts the rowless probes.** A clean 🟢 is a unique problem solved that the 107-row tracker never
   sees. Add the `🟢 · —` rows here to any "unique problems solved" total.
2. **Gives the free diagnostic its denominator.** The row-creation rate above is computed over this
   table — without it, "rate over ~15 probes" has no bottom.

| # | Date | Problem | Technique | Result | Tracker row? |
|---|---|---|---|---|---|
| 1 | 2026-08-10 | 977 Squares of a Sorted Array | Two Pointers | 🟢 | — |
| 2 | 2026-08-11 | 202 Happy Number | Cycle Detection (iterated seq) | 🟡 | ✅ earned |
| 3 | 2026-08-16 | 69 Sqrt(x) | Binary Search on Answer | 🟢 | — |
| 4 | 2026-08-19 | 643 Maximum Average Subarray I | Sliding Window | 🟡 | — *(learner overrode the row)* |
| 5 | 2026-08-21 | 205 Isomorphic Strings | Hash-map bijection | 🟢 | — |
| 6 | 2026-08-28 | 637 Average of Levels in Binary Tree | Tree BFS (level order) | 🟢 | — |

**Tally (6 run):** 4 clean 🟢 · 1 earned a row (202) · 1 🟡 overridden (643). **Row-creation rate
1/6 = 17%** — well under the 85% "pool has stopped teaching" line, so the pool still teaches.
**Rowless-but-solved: 5** (977, 69, 643, 205, 637) — these are the unique problems the tracker's 121
does not count.

⚠️ **Difficulty ratchet is now armed for Tree BFS** — probe #6 was an Easy and came back 🟢, so the
next probe of this technique is a **Medium** (cap at Medium, never Hard). See the ratchet rule above.

## 🎣 Queued probe candidates — named, gated, not yet eligible

A candidate is parked here **with a state trigger, never a date** — the pull rules gate on comfort, so
a candidate named while its technique is 🟡 must not silently become due just because time passed.

| Candidate | Technique | Trigger | Why it is a good probe |
|---|---|---|---|
| **452 Minimum Number of Arrows to Burst Balloons** (Medium) | Intervals — *Interval scheduling (sort by end)* | **`green:435`** | Learner's pick, Aug 28, 2026. ⭐ It is **435's exact procedure wearing different words** — balloons and arrows rather than intervals to remove — so it tests whether the *sort-by-end greedy* transfers, not whether 435 is remembered. That surface-change-only property is what makes a probe measure recognition instead of recall. ⚠️ **Not eligible yet:** Intervals is **zero-green** (56 · 57 · 435 all 🟡), and the standing rule is never to probe a 🟡 or no-🟢 technique — that manufactures a review row on ground the learner has not yet held, at ~73 units/year for a Medium. Convert 435 first; the probe is the *reward* for that, not a substitute |

## ⚠️ Easy-only cannot reach most of the pool

Probes #1–3 were all Easy. Nothing decided that — the rule always said *Medium or below*, and practice
drifted. Of the 44 techniques at 🟢/🎓, the **majority have no unseen Easy problem at all** (Topological
Sort, Union-Find, Trie, Binary Search on Answer, Monotonic Stack, LRU, Dutch National Flag, Kadane,
Multi-source BFS, Deep Copy via Hash Map, Prefix/Suffix Products, Tree Construction). Worse, those are
disproportionately the techniques where **recognition is the hard part**, while the Easy pool
concentrates where recognition is near-trivial. Easy-only measures the easy half of the axis.

**Budget:** a Medium probe is **2.0 units**, not the 1.0 an Easy costs, against an **8.0** ceiling.
Price it at the weekly build — it is a real slot and will sometimes displace a due review.

Full reasoning: `.claude/memory/project_recognition_probes.md`.
