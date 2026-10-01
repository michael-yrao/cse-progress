<!-- reconciled: 2026-09-30 -->
# DSA mock interviews

One unseen Medium/Hard problem run cold, then a level raiser. The coach interviews; the learner codes.
Mechanics: [`dsa-mock.md`](../../../../.claude/skills/cse-coach/references/dsa-mock.md).

| | |
|---|---|
| **Cadence** | `dsa_mock.every_days` in `cse.config.yml`; first mock at `dsa_mock.first_due`, afterwards the last row of the Log below |
| **Slot** | Sunday, first row of the day (`🎤 Mock interview (<Diff>)`); that week has no 🎯 probe |
| **Pick** | unseen, in `company_demand.md`'s bigtech top-100 with ≥3 companies; technique 🟢/🎓; family rotates |
| **Ratchet** | first Medium · Medium 🟢 → Hard · Hard 🟢 → Hard · any 🟡/🔴 → Medium; the raiser verdict never moves it |
| **Written where** | base problem → tracker row + `dsa/leetcode/<category>/`; debrief → this folder; Log row → below; ledgers → `mastery/` |

## Log

| # | Date | Problem | Diff | Base | Level raiser | Debrief |
|---|---|---|---|---|---|---|

## Move bank

Move numbers are the taxonomy in `dsa-mock.md`: 1 stream · 2 scale out · 3 repeated queries ·
4 generalize · 5 tighten the bound · 6 relax an assumption · 7 productionize.

| Family | Moves that fit | Notes |
|---|---|---|
| Sliding window | 1, 3, 4, 6 | the window grows by one element at a time; k windows instead of one |
| Two pointers | 4, 5, 6 | the input arrives unsorted; negatives appear |
| Binary search | 3, 4, 6 | the condition changes; the queries repeat many times |
| BFS / DFS | 2, 4, 6 | the grid is split across machines; the graph has cycles |
| Heap | 1, 2, 4 | values arrive one at a time; the data is split across machines |
| Intervals | 1, 3, 6 | intervals arrive unsorted, one at a time; the same set is queried repeatedly |
| Prefix-sum | 1, 3, 4 | values are updated between queries; the array becomes 2-D |
| Trie | 2, 4, 7 | words are deleted; the dictionary no longer fits in memory |
| Union-find | 1, 2, 4 | edges arrive one at a time; the nodes are split across machines |
| Monotonic stack | 1, 5, 6 | elements arrive one at a time; the extra space is capped at O(1) |
| Backtracking | 4, 5, 6 | the input contains duplicates; the search must run without recursion |
