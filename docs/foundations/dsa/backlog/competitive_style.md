# Competitive-Style Backlog — pull pool for the post-expansion phase

> **This is a pull pool, not a checklist.** Pull a problem only when it exercises
> a pattern you've already learned (NC150 + Tier 1, and the Tier-2 technique it
> maps to). A 🟡/🔴 result is a diagnostic — it names a technique to refresh, not
> a reason to learn something ad-hoc. Read [`README.md`](README.md) first.

**When:** after knowledge expansion — once NC150 + Tier 1 are largely retired and
you've begun crossing the Interview-ROI line into Tier 2 for competitive depth.
Near-zero interview payoff; this is competitive-programming growth.

**How to use:** on a competitive session, pull *one* problem whose mapped
technique you want to pressure-test. Log it in `dsa_progress.md` like any other
problem (🟢/🟡/🔴, spaced-repetition dates). These are harder and slower than
NC150 — expect a lower Clean rate and a higher review cadence at first.

Organized by the Tier-2 technique each exercises (see the Knowledge Expansion
Queue in [`../mastery/dsa_progress.md`](../mastery/dsa_progress.md)).

## Graph & flow

| Problem | Technique | Notes |
|---|---|---|
| [1595. Minimum Cost to Connect Two Groups of Points](https://leetcode.com/problems/minimum-cost-to-connect-two-groups-of-points/) | bitmask DP / min-cost matching | Assignment-flavored; bridges matching and DP. |
| [1820. Maximum Number of Accepted Invitations](https://leetcode.com/problems/maximum-number-of-accepted-invitations/) | bipartite matching | Hungarian / Hopcroft-Karp entry point. |
| [1697. Checking Existence of Edge Length Limited Paths](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/) | offline queries + union-find | Sort edges & queries, answer offline. |
| [1489. Find Critical and Pseudo-Critical Edges in MST](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) | MST + edge classification | Kruskal with include/exclude probing. |

## Trees & LCA

| Problem | Technique | Notes |
|---|---|---|
| [1483. Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | binary lifting | The canonical LCA/ancestor lift. |
| [2846. Minimum Edge Weight Equilibrium Queries in a Tree](https://leetcode.com/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/) | LCA + path aggregation | Path stats via LCA jump tables. |
| [2836. Maximize Value of Function in a Ball Passing Game](https://leetcode.com/problems/maximize-value-of-function-in-a-ball-passing-game/) | functional-graph binary lifting | Jump-table over a "next" function. |

## Range structures

| Problem | Technique | Notes |
|---|---|---|
| [1157. Online Majority Element in Subarray](https://leetcode.com/problems/online-majority-element-in-subarray/) | sqrt decomposition / random + segment | Classic Mo's / sqrt entry point. |
| [2213. Longest Substring of One Repeating Character](https://leetcode.com/problems/longest-substring-of-one-repeating-character/) | segment tree with merge info | Interval-merge segment tree. |
| [699. Falling Squares](https://leetcode.com/problems/falling-squares/) | coordinate compression + segment tree | Range-assign / range-max. |

## Strings (deep end)

| Problem | Technique | Notes |
|---|---|---|
| [1044. Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | suffix array / binary search + rolling hash | Full-text substring search. |
| [1032. Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | Aho-Corasick | Multi-pattern streaming match. |
| [3008. Find Beautiful Indices in the Given Array II](https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-ii/) | Z-algorithm / KMP | Two-pattern index alignment. |

## DP optimizations

| Problem | Technique | Notes |
|---|---|---|
| [1547. Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/) | interval DP (Knuth candidate) | Interval DP that Knuth optimization sharpens. |
| [1000. Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/) | interval DP with step constraint | Harder interval DP. |
| [1994. The Number of Good Subsets](https://leetcode.com/problems/the-number-of-good-subsets/) | SOS / subset DP | Sum-over-subsets aggregation. |

---

*Beyond LeetCode:* for topics with few clean LC instances (persistent structures,
treaps, heavy flow), move to **Codeforces** (Div. 2 C–E), **AtCoder** (ABC/ARC),
or the **USACO** archives. The tracker still owns spaced repetition regardless of
source.
