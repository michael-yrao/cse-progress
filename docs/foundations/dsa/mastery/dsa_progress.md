# DSA Progress

<!--
Notes for future agents:
- The table columns are now: Difficulty, Problem, Comfort, Streak, Next Review Date, Latest Rep Date, Rep Dates.
- ⚠️ **Renamed Aug 9, 2026: "Attempt" → "Rep"** (header stat, both date columns). An *attempt* connotes
  trying and possibly failing; the code gets written every rep, and what varies is the **rating**, not
  whether a solution happened. `update_review_dates.py` still **recognizes** both older header spellings
  and upgrades whichever it finds, so an un-migrated tracker parses fine — do not delete those constants.
  The in-file `# ── Attempt · <date> ──` banners in solution files were deliberately **not** renamed.
- `Streak` tracks consecutive Clean results. Increments on Clean, resets to 0 on Shaky or Blank.
- `Rep Dates` is a collapsed summary of the original Attempt 1–5 columns.
- `Next Review Date` is **computed, never typed** — the pre-commit hook runs
  `scripts/update_review_dates.py`, which reads the intervals from `cse.config.yml`. **The numbers are
  stated there and nowhere else** (see *Single source of truth* in `CLAUDE.md`); this legend gives the
  ladder, not the values:
  - 🟢 Clean, **Streak 0 (provisional — first Clean directly after a 🔴 Blank)**: shortest Clean interval, a lock-down check; not yet trusted
  - 🟢 Clean, Streak 1 → longer · Streak 2 → longer still
  - 🎓 Graduated (`graduate_at_streak`+): longest, a recurring spot check
  - 🟡 Shaky (any streak): short, reset Streak to 0
  - 🔴 Blank (any streak): shortest of all, reset Streak to 0
- **Provisional Clean (🟢 + Streak 0):** log a 🟢 that *directly follows a 🔴* with **Streak 0**, not 1 — it
  gets a short lock-down to verify the Blank→Clean actually stuck. If it survives (Clean again), log it
  Streak 1 and it rejoins the normal ladder; if it slips to 🟡/🔴, it resets as usual. A 🟢 after a
  🟡 (not a 🔴) is logged Streak 1 as normal — only Blank→Clean is provisional. Do NOT "fix" a 🟢/Streak-0 to
  Streak 1; that silently removes the lock-down.
- ⚠️ NAMES SWAPPED Jul 26, 2026 — you GRADUATE, then you RETIRE. 🎓 Graduated is the `graduate_at_streak` tier
  that still comes back on the longest interval; 🏆 Retired is TERMINAL. The labels were originally the other
  way round, which read backwards against the ordinary meaning of the words.
- When a problem reaches `graduate_at_streak` (see `cse.config.yml`), change Comfort to 🎓 to graduate it out of regular rotation.
- Graduated problems return for a spot check on the longest interval. Still Clean → stays 🎓 at that same interval.
  Shaky/Blank → back to active rotation. A legacy 🏆 row still parses and is treated as 🎓.
- **🏆 Retirement (added Jul 26, 2026) — the TERMINAL tier, above 🎓.** A 🎓 problem that clears its
  spot checks retires — **two** clean if it climbed the ladder normally, **ONE** if it arrived by the
  over-learned fast-track (its coverage gate already supplies what the second check would): move its row out of the review table into the
  `## 🏆 Retired` list at the bottom and **add its number to `discovery_skip` in `cse.config.yml`**.
  ⚠️ **Both steps, always.** Discovery re-adds any problem under `dsa/leetcode/**` that has no row, so
  removing the row alone silently resurrects it on the next commit. The Retired list is deliberately a
  **plain bullet list, not the 7-column table**, so this parser ignores it. Rationale: 🎓 is not terminal —
  it still bills 0.039 slots/week forever; at ~28 slots/week the library caps out around 500–600 problems
  without a release valve. See `study_guide.md` → "Library carrying capacity". If a retired problem
  ever resurfaces and fails, it re-enters at 🟡 like anything else.
- **Disposable reps (added Jul 26, 2026) — not every solved problem gets a row.** A **consolidation rep**
  or **application pull** is a probe testing whether a *technique* transfers, not an asset to maintain.
  Solve it → log the outcome to the technique's ledger (`recognition_gotchas.md` / `complexity_gotchas.md`)
  → **create no review row if it came back 🟢**. Only 🟡/🔴 earns a row, because only a gap needs
  repetition. ⚠️ Same discovery caveat: a probe's file under `dsa/leetcode/**` is auto-added, so probes
  need either a separate root outside `solutions.roots` (preferred) or a `discovery_skip` entry (stopgap).
- **What this file means now:** it is **"everything still unproven"**, not "everything I've solved" — a
  work queue, not a trophy case. A *shrinking* row count is the healthy direction. The accomplishment
  record lives in the 🏆 Retired list and the technique ledgers.
- This Markdown file is generated from current row data by `scripts/update_review_dates.py`.
- The script also discovers LeetCode problems defined under `dsa/leetcode/*` and adds missing rows automatically.
- Problem titles in this table should include the method used, such as `(BFS)` or `(DFS)`.
- If a method is mentioned and the table already contains the same LeetCode number with a different method, a new row should be added rather than overwriting the existing entry.
- When run from git commit, the helper only scans staged source files to discover newly added or changed problems.
- The helper also auto-fills the current date for staged review rows that are missing `Latest Rep Date`.
- The pre-commit hook now triggers when `docs/foundations/dsa/mastery/dsa_progress.md` or any `dsa/leetcode/*.py` file is staged.
- The review table is sorted by Latest Rep Date descending whenever the script runs.
- A local git pre-commit hook has been installed to auto-run the script when `docs/foundations/dsa/mastery/dsa_progress.md` is staged.
- When a LeetCode problem is added here or a review row is updated, the file should be refreshed automatically and should not require an explicit ask.
- Run `python scripts/update_review_dates.py` or `npm run update-review-progression` if you edit the file outside of a commit flow.
- When we are doing LeetCode review, any problems mentioned should be logged in this file.
 - If any LeetCode problem is mentioned anywhere in the repo or during a review session, it should be added to this file.
-->

> **Auto-refresh note:** this table is regenerated automatically when `docs/foundations/dsa/mastery/dsa_progress.md` is staged for commit or when the helper script is run.

> **107** problems &nbsp;·&nbsp; **117** solutions &nbsp;·&nbsp; **472** reps

| | 🏆 Retired | 🎓 Graduated | 🟢 Clean | 🟡 Shaky | 🔴 Blank |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Solutions** | 0 | 6 | 94 | 15 | 2 |

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |
|---|---|---|---|---|---|---|
| Hard | [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | 🔴 | 0 | 2026-08-22 | 2026-08-20 | 2026-08-20 |
| Medium | [53. Maximum Subarray (Prefix Sum)](https://leetcode.com/problems/maximum-subarray/) | 🔴 | 0 | 2026-08-22 | 2026-08-20 | 2026-01-08, 2026-04-01, 2026-06-27, 2026-08-20 |
| Medium | [323. Number of Connected Components (Union-Find)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 2 | 2026-10-18 | 2026-08-19 | 2026-06-19, 2026-06-29, 2026-08-19 |
| Medium | [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | 🟡 | 0 | 2026-08-29 | 2026-08-19 | 2026-06-04, 2026-06-05, 2026-06-07, 2026-08-09, 2026-08-19 |
| Medium | [1448. Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | 🟢 | 2 | 2026-10-18 | 2026-08-19 | 2026-05-15, 2026-06-18, 2026-07-10, 2026-07-20, 2026-08-19 |
| Easy | [206. Reverse Linked List (Recursion)](https://leetcode.com/problems/reverse-linked-list/) | 🟢 | 2 | 2026-10-18 | 2026-08-19 | 2026-04-24, 2026-07-03, 2026-07-14, 2026-07-24, 2026-08-19 |
| Medium | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 🟢 | 2 | 2026-10-18 | 2026-08-19 | 2026-01-24, 2026-04-13, 2026-07-24, 2026-08-19 |
| Hard | [332. Reconstruct Itinerary (pre-sorted adjacency)](https://leetcode.com/problems/reconstruct-itinerary/) | 🟡 | 0 | 2026-08-28 | 2026-08-18 | 2026-08-18 |
| Medium | [235. Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 🟢 | 1 | 2026-09-17 | 2026-08-18 | 2026-05-03, 2026-06-12, 2026-07-19, 2026-07-29, 2026-08-08, 2026-08-18 |
| Medium | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 🟢 | 1 | 2026-09-17 | 2026-08-18 | 2026-04-05, 2026-06-26, 2026-06-28, 2026-07-29, 2026-08-08, 2026-08-18 |
| Medium | [2300. Successful Pairs of Spells and Potions](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/) | 🟢 | 2 | 2026-10-17 | 2026-08-18 | 2026-05-03, 2026-06-12, 2026-06-19, 2026-08-18 |
| Medium | [853. Car Fleet](https://leetcode.com/problems/car-fleet/) | 🟢 | 0 | 2026-08-27 | 2026-08-17 | 2026-08-15, 2026-08-17 |
| Medium | [19. Remove Nth Node From End of List (Postorder Recursion)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟢 | 1 | 2026-09-16 | 2026-08-17 | 2026-05-18, 2026-05-21, 2026-06-18, 2026-06-28, 2026-07-08, 2026-07-18, 2026-07-28, 2026-08-07, 2026-08-17 |
| Medium | [19. Remove Nth Node From End of List (Iterative)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟢 | 2 | 2026-10-16 | 2026-08-17 | 2026-04-29, 2026-05-18, 2026-06-30, 2026-07-09, 2026-08-17 |
| Hard | [269. Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | 🟡 | 0 | 2026-08-27 | 2026-08-17 | 2026-07-27, 2026-07-29, 2026-08-07, 2026-08-17 |
| Medium | [261. Graph Valid Tree (DFS)](https://neetcode.io/problems/valid-tree) | 🟢 | 1 | 2026-09-15 | 2026-08-16 | 2026-06-15, 2026-06-17, 2026-06-21, 2026-06-23, 2026-08-06, 2026-08-16 |
| Easy | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | 🟢 | 1 | 2026-09-15 | 2026-08-16 | 2026-07-04, 2026-07-06, 2026-08-06, 2026-08-16 |
| Medium | [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | 🟢 | 2 | 2026-10-15 | 2026-08-16 | 2026-07-06, 2026-07-08, 2026-07-17, 2026-08-16 |
| Medium | [75. Sort Colors (Dutch Flag)](https://leetcode.com/problems/sort-colors/) | 🟢 | 2 | 2026-10-15 | 2026-08-16 | 2026-01-08, 2026-04-01, 2026-05-26, 2026-05-28, 2026-06-28, 2026-07-08, 2026-07-17, 2026-08-16 |
| Medium | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 🟢 | 2 | 2026-10-15 | 2026-08-16 | 2026-05-16, 2026-05-20, 2026-06-30, 2026-07-02, 2026-07-11, 2026-08-16 |
| Medium | [80. Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) | 🟢 | 2 | 2026-10-15 | 2026-08-16 | 2026-01-13, 2026-04-13, 2026-06-25, 2026-06-27, 2026-07-11, 2026-08-16 |
| Medium | [787. Cheapest Flights Within K Stops (Bellman-Ford)](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 🟢 | 1 | 2026-09-14 | 2026-08-15 | 2026-07-14, 2026-07-16, 2026-07-26, 2026-08-05, 2026-08-15 |
| Medium | [572. Subtree Of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | 🟡 | 0 | 2026-08-25 | 2026-08-15 | 2026-05-02, 2026-06-12, 2026-08-15 |
| Medium | [1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance (Floyd-Warshall)](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | 🟡 | 0 | 2026-08-25 | 2026-08-15 | 2026-07-31, 2026-08-05, 2026-08-15 |
| Medium | [695. Max Area Of Island (DFS)](https://leetcode.com/problems/max-area-of-island/) | 🟢 | 2 | 2026-10-14 | 2026-08-15 | 2026-06-01, 2026-06-17, 2026-08-15 |
| Medium | [743. Network Delay Time (Dijkstra)](https://leetcode.com/problems/network-delay-time/) | 🟡 | 0 | 2026-08-24 | 2026-08-14 | 2026-07-13, 2026-07-15, 2026-07-25, 2026-08-04, 2026-08-14 |
| Medium | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | 🟡 | 0 | 2026-08-24 | 2026-08-14 | 2026-08-14 |
| Medium | [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | 🟢 | 2 | 2026-10-13 | 2026-08-14 | 2026-07-11, 2026-07-21, 2026-07-31, 2026-08-10, 2026-08-14 |
| Medium | [155. Min Stack (Pair with Min-So-Far)](https://leetcode.com/problems/min-stack/) | 🟢 | 0 | 2026-08-24 | 2026-08-14 | 2026-08-12, 2026-08-14 |
| Medium | [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | 🟢 | 1 | 2026-09-12 | 2026-08-13 | 2026-07-03, 2026-07-05, 2026-08-04, 2026-08-13 |
| Hard | [127. Word Ladder (BFS)](https://leetcode.com/problems/word-ladder/) | 🟡 | 0 | 2026-08-23 | 2026-08-13 | 2026-07-18, 2026-07-21, 2026-08-03, 2026-08-13 |
| Medium | [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | 🟢 | 2 | 2026-10-12 | 2026-08-13 | 2026-07-04, 2026-07-07, 2026-07-16, 2026-08-13 |
| Medium | [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | 🟡 | 0 | 2026-08-23 | 2026-08-13 | 2026-07-12, 2026-07-14, 2026-08-13 |
| Easy | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 🟢 | 2 | 2026-10-12 | 2026-08-13 | 2026-04-15, 2026-06-25, 2026-07-03, 2026-07-14, 2026-08-13 |
| Easy | [680. Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) | 🟢 | 2 | 2026-10-12 | 2026-08-13 | 2026-04-05, 2026-05-28, 2026-05-30, 2026-06-12, 2026-08-13 |
| Hard | [778. Swim in Rising Water (Dijkstra / Min-Heap)](https://leetcode.com/problems/swim-in-rising-water/) | 🟡 | 0 | 2026-08-22 | 2026-08-12 | 2026-07-23, 2026-08-02, 2026-08-12 |
| Medium | [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 🟡 | 0 | 2026-08-22 | 2026-08-12 | 2026-07-09, 2026-07-11, 2026-07-21, 2026-07-23, 2026-08-02, 2026-08-12 |
| Medium | [271. Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) | 🟡 | 0 | 2026-08-22 | 2026-08-12 | 2026-07-01, 2026-07-03, 2026-07-13, 2026-07-23, 2026-08-02, 2026-08-12 |
| Medium | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 🟢 | 1 | 2026-09-10 | 2026-08-11 | 2026-04-22, 2026-07-03, 2026-07-13, 2026-07-23, 2026-08-02, 2026-08-11 |
| Medium | [1584. Min Cost to Connect All Points (Prim's MST)](https://leetcode.com/problems/min-cost-to-connect-all-points/) | 🟢 | 1 | 2026-09-10 | 2026-08-11 | 2026-07-16, 2026-07-18, 2026-07-20, 2026-08-01, 2026-08-11 |
| Medium | [323. Number of Connected Components (DFS)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 2 | 2026-10-10 | 2026-08-11 | 2026-07-02, 2026-07-12, 2026-08-11 |
| Easy | [202. Happy Number (Seen-Set)](https://leetcode.com/problems/happy-number/) | 🟡 | 0 | 2026-08-21 | 2026-08-11 | 2026-08-11 |
| Medium | [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | 🟡 | 0 | 2026-08-21 | 2026-08-11 | 2026-08-11 |
| Easy | [66. Plus One](https://leetcode.com/problems/plus-one/) | 🟢 | 2 | 2026-10-09 | 2026-08-10 | 2026-01-02, 2026-03-25, 2026-06-22, 2026-07-01, 2026-08-10 |
| Easy | [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | 🟢 | 2 | 2026-10-09 | 2026-08-10 | 2026-06-22, 2026-07-02, 2026-08-10 |
| Medium | [721. Accounts Merge (Union-Find)](https://leetcode.com/problems/accounts-merge/) | 🟢 | 1 | 2026-09-08 | 2026-08-09 | 2026-07-30, 2026-08-09 |
| Easy | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 🟢 | 2 | 2026-10-08 | 2026-08-09 | 2026-04-26, 2026-07-01, 2026-07-10, 2026-08-09 |
| Medium | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/) | 🟢 | 2 | 2026-10-08 | 2026-08-09 | 2026-06-30, 2026-07-01, 2026-07-10, 2026-08-09 |
| Medium | [105. Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 🟢 | 2 | 2026-10-08 | 2026-08-09 | 2026-07-08, 2026-07-10, 2026-08-09 |
| Medium | [1011. Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | 🟢 | 2 | 2026-10-08 | 2026-08-09 | 2026-05-03, 2026-06-12, 2026-08-09 |
| Medium | [912. Sort an Array (Merge Sort)](https://leetcode.com/problems/sort-an-array/) | 🟢 | 1 | 2026-09-07 | 2026-08-08 | 2026-01-06, 2026-03-26, 2026-07-15, 2026-07-29, 2026-08-08 |
| Easy | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | 🟢 | 2 | 2026-10-07 | 2026-08-08 | 2026-05-19, 2026-05-21, 2026-06-30, 2026-07-09, 2026-08-08 |
| Easy | [100. Same Tree](https://leetcode.com/problems/same-tree/) | 🎓 | 3 | 2027-02-04 | 2026-08-08 | 2026-05-01, 2026-06-05, 2026-08-08 |
| Easy | [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | 🎓 | 3 | 2027-02-04 | 2026-08-08 | 2026-01-10, 2026-04-03, 2026-06-04, 2026-08-08 |
| Easy | [21. Merge Two Sorted Lists (Iterative)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🎓 | 3 | 2027-02-04 | 2026-08-08 | 2026-04-26, 2026-06-12, 2026-08-08 |
| Hard | [42. Trapping Rain Water (Array)](https://leetcode.com/problems/trapping-rain-water/) | 🟢 | 2 | 2026-10-06 | 2026-08-07 | 2026-04-15, 2026-06-29, 2026-07-08, 2026-08-07 |
| Medium | [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | 🟢 | 2 | 2026-10-06 | 2026-08-07 | 2026-06-23, 2026-07-03, 2026-08-07 |
| Medium | [130. Surrounded Regions (Union-Find)](https://leetcode.com/problems/surrounded-regions/) | 🟢 | 2 | 2026-10-06 | 2026-08-07 | 2026-06-21, 2026-06-23, 2026-07-03, 2026-08-07 |
| Easy | [110. Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | 🎓 | 3 | 2027-02-03 | 2026-08-07 | 2026-05-01, 2026-06-04, 2026-06-14, 2026-06-24, 2026-07-03, 2026-08-07 |
| Medium | [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 🟢 | 2 | 2026-10-06 | 2026-08-07 | 2026-01-28, 2026-04-17, 2026-08-07 |
| Medium | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 🟢 | 2 | 2026-10-06 | 2026-08-07 | 2026-01-31, 2026-04-14, 2026-08-07 |
| Medium | [540. Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/) | 🟢 | 1 | 2026-09-05 | 2026-08-06 | 2026-05-02, 2026-06-12, 2026-06-13, 2026-07-17, 2026-07-27, 2026-08-06 |
| Easy | [27. Remove Element](https://leetcode.com/problems/remove-element/) | 🟢 | 2 | 2026-10-05 | 2026-08-06 | 2026-01-05, 2026-03-28, 2026-05-27, 2026-06-26, 2026-07-05, 2026-08-06 |
| Easy | [1768. Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) | 🟢 | 2 | 2026-10-05 | 2026-08-06 | 2026-01-21, 2026-04-10, 2026-08-06 |
| Easy | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | 🟢 | 2 | 2026-10-05 | 2026-08-06 | 2026-01-15, 2026-04-05, 2026-08-06 |
| Easy | [344. Reverse String](https://leetcode.com/problems/reverse-string/) | 🟢 | 2 | 2026-10-05 | 2026-08-06 | 2026-01-15, 2026-04-04, 2026-08-06 |
| Medium | [323. Number of Connected Components (BFS)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 2 | 2026-10-04 | 2026-08-05 | 2026-06-16, 2026-06-22, 2026-07-06, 2026-08-05 |
| Easy | [1929. Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | 🟢 | 2 | 2026-10-04 | 2026-08-05 | 2026-01-01, 2026-03-25, 2026-08-05 |
| Easy | [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 🟢 | 2 | 2026-10-04 | 2026-08-05 | 2026-01-01, 2026-03-25, 2026-08-05 |
| Easy | [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | 🟢 | 2 | 2026-10-04 | 2026-08-05 | 2026-01-09, 2026-04-02, 2026-08-05 |
| Hard | [332. Reconstruct Itinerary (min-heap ordering)](https://leetcode.com/problems/reconstruct-itinerary/) | 🟡 | 0 | 2026-08-14 | 2026-08-04 | 2026-07-22, 2026-07-28, 2026-08-04 |
| Medium | [143. Reorder List](https://leetcode.com/problems/reorder-list/) | 🟢 | 1 | 2026-09-03 | 2026-08-04 | 2026-04-26, 2026-07-06, 2026-07-15, 2026-07-25, 2026-08-04 |
| Medium | [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | 🟢 | 2 | 2026-10-03 | 2026-08-04 | 2026-07-05, 2026-08-04 |
| Medium | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 🟢 | 2 | 2026-10-02 | 2026-08-03 | 2026-06-06, 2026-06-15, 2026-06-25, 2026-07-04, 2026-08-03 |
| Easy | [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | 🟢 | 2 | 2026-10-02 | 2026-08-03 | 2026-03-22, 2026-04-14, 2026-06-25, 2026-07-04, 2026-08-03 |
| Medium | [229. Majority Element II](https://leetcode.com/problems/majority-element-ii/) | 🟢 | 1 | 2026-09-02 | 2026-08-03 | 2026-01-30, 2026-04-14, 2026-06-27, 2026-06-29, 2026-07-12, 2026-07-24, 2026-08-03 |
| Medium | [261. Graph Valid Tree (Union-Find)](https://neetcode.io/problems/valid-tree) | 🟢 | 1 | 2026-08-31 | 2026-08-01 | 2026-06-19, 2026-06-29, 2026-07-09, 2026-07-18, 2026-08-01 |
| Easy | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | 🟢 | 1 | 2026-08-30 | 2026-07-31 | 2026-04-30, 2026-06-02, 2026-06-12, 2026-06-14, 2026-06-24, 2026-06-26, 2026-07-20, 2026-07-31 |
| Medium | [417. Pacific Atlantic Water Flow (BFS)](https://leetcode.com/problems/pacific-atlantic-water-flow/) | 🟢 | 1 | 2026-08-30 | 2026-07-31 | 2026-06-11, 2026-07-19, 2026-07-31 |
| Medium | [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 🟢 | 2 | 2026-09-27 | 2026-07-29 | 2026-01-26, 2026-04-14, 2026-06-27, 2026-06-29, 2026-07-29 |
| Easy | [733. Flood Fill (BFS)](https://leetcode.com/problems/flood-fill/) | 🎓 | 3 | 2027-01-25 | 2026-07-29 | 2026-06-12, 2026-06-19, 2026-06-28, 2026-07-29 |
| Easy | [169. Majority Element](https://leetcode.com/problems/majority-element/) | 🟢 | 2 | 2026-09-26 | 2026-07-28 | 2026-01-05, 2026-04-01, 2026-05-28, 2026-06-27, 2026-07-28 |
| Medium | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | 🟢 | 1 | 2026-08-26 | 2026-07-27 | 2026-04-19, 2026-07-02, 2026-07-10, 2026-07-17, 2026-07-27 |
| Medium | [18. Four Sum](https://leetcode.com/problems/4sum/) | 🟢 | 1 | 2026-08-26 | 2026-07-27 | 2026-01-23, 2026-07-17, 2026-07-27 |
| Easy | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢 | 2 | 2026-09-25 | 2026-07-27 | 2026-04-30, 2026-05-27, 2026-06-27, 2026-07-27 |
| Medium | [53. Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/) | 🟢 | 2 | 2026-09-24 | 2026-07-26 | 2026-01-08, 2026-04-02, 2026-06-23, 2026-06-24, 2026-07-26 |
| Medium | [189. Rotate Array](https://leetcode.com/problems/rotate-array/) | 🟢 | 2 | 2026-09-24 | 2026-07-26 | 2026-01-11, 2026-04-04, 2026-06-24, 2026-07-26 |
| Easy | [1046. Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | 🟢 | 2 | 2026-09-24 | 2026-07-26 | 2026-06-23, 2026-07-26 |
| Easy | [704. Binary Search](https://leetcode.com/problems/binary-search/) | 🎓 | 3 | 2027-01-22 | 2026-07-26 | 2026-03-09, 2026-04-13, 2026-05-27, 2026-06-27, 2026-07-26 |
| Medium | [355. Design Twitter](https://leetcode.com/problems/design-twitter/) | 🟢 | 1 | 2026-08-24 | 2026-07-25 | 2026-06-24, 2026-06-26, 2026-07-06, 2026-07-15, 2026-07-25 |
| Medium | [74. Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | 🟢 | 1 | 2026-08-24 | 2026-07-25 | 2026-04-22, 2026-07-03, 2026-07-13, 2026-07-25 |
| Medium | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 🟢 | 1 | 2026-08-24 | 2026-07-25 | 2026-01-11, 2026-04-09, 2026-05-30, 2026-07-25 |
| Medium | [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | 🟢 | 1 | 2026-08-23 | 2026-07-24 | 2026-04-20, 2026-07-02, 2026-07-12, 2026-07-24 |
| Medium | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 🟢 | 1 | 2026-08-23 | 2026-07-24 | 2026-06-09, 2026-06-13, 2026-07-24 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | 🟢 | 1 | 2026-08-23 | 2026-07-24 | 2026-01-19, 2026-04-07, 2026-05-30, 2026-07-24 |
| Hard | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | 🟢 | 1 | 2026-08-22 | 2026-07-23 | 2026-07-11, 2026-07-13, 2026-07-23 |
| Medium | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟢 | 1 | 2026-08-22 | 2026-07-23 | 2026-04-17, 2026-07-23 |
| Easy | [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | 🟢 | 2 | 2026-09-20 | 2026-07-22 | 2026-01-01, 2026-03-25, 2026-06-22, 2026-07-22 |
| Easy | [206. Reverse Linked List (Iterative)](https://leetcode.com/problems/reverse-linked-list/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-04-23, 2026-05-26, 2026-06-12, 2026-06-20, 2026-07-20 |
| Easy | [21. Merge Two Sorted Lists (Recursion)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-05-20, 2026-05-21, 2026-06-12, 2026-06-20, 2026-07-20 |
| Medium | [130. Surrounded Regions (BFS)](https://leetcode.com/problems/surrounded-regions/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-06-14, 2026-06-20, 2026-07-20 |
| Medium | [200. Number of Islands (DFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-05-31, 2026-06-02, 2026-06-16, 2026-06-26, 2026-07-20 |
| Easy | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-04-30, 2026-05-26, 2026-06-25, 2026-07-20 |
| Medium | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟢 | 2 | 2026-09-17 | 2026-07-19 | 2026-05-03, 2026-06-12, 2026-07-19 |
| Easy | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | 🟢 | 2 | 2026-09-17 | 2026-07-19 | 2026-01-10, 2026-04-02, 2026-06-02, 2026-06-12, 2026-07-19 |
| Medium | [200. Number of Islands (BFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 2 | 2026-09-16 | 2026-07-18 | 2026-05-30, 2026-06-01, 2026-06-07, 2026-07-18 |
| Medium | [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | 🟢 | 2 | 2026-09-14 | 2026-07-16 | 2026-05-02, 2026-06-12, 2026-06-13, 2026-07-16 |
| Medium | [207. Course Schedule I](https://leetcode.com/problems/course-schedule/) | 🟢 | 2 | 2026-09-14 | 2026-07-16 | 2026-06-08, 2026-06-12, 2026-06-13, 2026-07-16 |
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-01-02, 2026-03-25, 2026-07-14 |
| Medium | [199. Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-05-09, 2026-06-13, 2026-07-14 |
| Medium | [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-01-19, 2026-07-14 |
| Medium | [36. Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | 🟢 | 1 | 2026-08-08 | 2026-07-09 | 2026-01-25, 2026-05-22, 2026-06-30, 2026-07-09 |
| Medium | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 🟢 | 1 | 2026-08-03 | 2026-07-04 | 2026-04-13, 2026-05-29, 2026-06-15, 2026-06-25, 2026-07-04 |
| Medium | [684. Redundant Connection (Union-Find)](https://leetcode.com/problems/redundant-connection/) | 🟢 | 1 | 2026-07-31 | 2026-07-01 | 2026-06-18, 2026-06-22, 2026-07-01 |
| Medium | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | 🟢 | 2 | 2026-08-30 | 2026-07-01 | 2026-04-21, 2026-07-01 |
| Medium | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 🟢 | 2 | 2026-08-27 | 2026-06-28 | 2026-01-04, 2026-03-27, 2026-05-29, 2026-06-28 |
| Easy | [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 🟢 | 1 | 2026-07-15 | 2026-06-15 | 2026-01-03, 2026-03-27, 2026-06-05, 2026-06-15 |

---

## ⏳ Waiting Room — will enter rotation

**These are NOT parked.** Every entry here *will* be scheduled; it is waiting on a stated
condition. This section is **short by design and read at every weekly build** — that is the whole
anti-void mechanism. Split out of the Knowledge Expansion Queue on Jul 26, 2026 after *53 D&C*
sat three weeks past its trigger unfired: it had been filed in a bin whose name says *"don't
expect this soon,"* so nobody was wrong to skim past it. **The bin was lying.** At the split,
**14 of the queue's 21 entries turned out to belong here** — two-thirds of a "parking lot" was
actually a waiting room.

### Trigger vocabulary (keep it to these — they're all machine-checkable)

| Form | Fires when | Checked against |
|---|---|---|
| `phase:<Name>` | that roadmap phase opens | `study_guide.md` phase table + today's date |
| `graduates:<num>` | that problem's row reaches 🎓 | this tracker |
| `rated:<num>` | that problem has a rating logged | this tracker's attempt dates |
| `solved:<num>` | that problem has any 🟢 | this tracker |
| `surplus>=<n>` | measured weekly surplus | the capacity computation |

Combine with `+` (all must hold). **Never use a bare date** — a date is the one trigger that can
expire silently, which is exactly how 53 D&C was lost. Conditions survive schedule slip; dates don't.

**At every weekly build:** evaluate every row below. A fired trigger is either **slotted that week**
or **re-deferred with a written reason** — never left sitting. A fired-but-unslotted trigger with no
note is the failure mode this section exists to prevent.

| Difficulty | Problem | Trigger | Notes |
|---|---|---|---|
| Medium | [802. Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | `surplus>=1` | **Topological Sort consolidation rep (4th problem).** Requested by the learner Aug 17, 2026 **in place of a Kahn's-bookkeeping drill** — a rated interview problem over a synthetic exercise, which is the better trade. ⭐ **Why this one:** topo on the **reversed** graph, so edge direction has to be reasoned about rather than copied; and "which nodes avoid cycles" makes the **completeness check the problem statement** instead of a guard that can be forgotten. That is precisely the bug that recurred on 269 (Aug 7 → Aug 17). Number/premium verified against LeetCode GraphQL Aug 17. |
| Medium | [2115. Find All Possible Recipes from Given Supplies](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/) | `surplus>=1` | **Topological Sort consolidation rep (5th problem).** ⭐ **Why this one:** the graph is **derived from data** (ingredient lists), exactly as 269 derives edges from adjacent word pairs — the closest surface form to 269's modeling half, which is the part no other topo problem exercises. Number/premium verified Aug 17. ⚠️ **Pair with 802, not instead of it:** 802 targets the transferable bug (completeness), 2115 targets the modeling. |
| Medium | [19. Remove Nth Node From End of List (**one-pass two-pointer gap**)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | `graduates:19-iterative` + `graduates:19-postorder` | **Method variant — and the one an interviewer most likely expects on this problem.** Surfaced Aug 17, 2026 after both tracked variants went 🟢 in one sitting: 19 has three variants on the books (iterative, postorder, parked preorder) and **none is the gap method** — advance a lead pointer `n` ahead, then walk both until it falls off, so the trailing pointer lands on the predecessor. ⭐ **Why it earns a rep rather than a footnote:** both tracked variants are two-pass or O(n)-stack; the gap method is the only one that is **one pass in O(1) space**, and gap-as-invariant is the transferable part — the same device as 876 midpoint and 141 cycle detection, generalized to an arbitrary offset. **Gated by the method-variant rule** — pull only once BOTH tracked rows are 🎓 (the streak is `graduate_at_streak` in [`cse.config.yml`](../../../../cse.config.yml) — do not restate it here). Earliest possible: **Iterative** is 🟢 s2 (Oct 16 → 🎓 on a clean rep); **Postorder** is 🟢 s1 and needs two more cleans (Sept 16, then ~Nov 15). ⚠️ **So this cannot fire before mid-November 2026, and only if neither slips** — stated so the weekly build does not re-evaluate it monthly for nothing. Learner's call, Aug 17, 2026: *"let's put that in the queue for when these graduate then."* |
| Hard | [1216. Valid Palindrome III (backtracking)](https://leetcode.com/problems/valid-palindrome-iii/) | `phase:Backtracking` | **Phase-gated 🔴.** Attempted 2026-05-31 → Blank; the Backtracking foundation isn't built until **Sep 14 – Oct 11**. Premature, not forgotten. **Trigger: pull into rotation when the Backtracking phase opens (Sep 14).** |
| Hard | [1216. Valid Palindrome III (1DP)](https://leetcode.com/problems/valid-palindrome-iii/) | `phase:1D-DP` | **Phase-gated 🔴.** Attempted 2026-05-31 → Blank; the 1D DP foundation isn't built until **Oct 12 – Nov 8**. Premature, not forgotten. **Trigger: pull into rotation when the 1D DP phase opens (Oct 12).** |
| Medium | [399. Evaluate Division](https://leetcode.com/problems/evaluate-division/) | `rated:1334` | **Floyd-Warshall's 2nd problem** — approved by the learner Aug 16, 2026 from the company-wise pull (`Shortest Path` tag, 5 eligible). ⭐ **Chosen because it is a DIFFERENT SHAPE, not another distance grid**: weights are multiplicative and the query is a ratio, so it tests whether the triple loop is understood as a relation-closure pattern rather than a shortest-path recipe. Held behind 1334's Aug 25 rep by the D&C precedent — a 2nd problem run before the 1st is rated measures the teaching, not the technique. |
| Hard | [1489. Find Critical and Pseudo-Critical Edges in MST](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) | `rated:1584-kruskal` | **MST's 3rd problem** — promoted out of `backlog/competitive_style.md` Aug 16, 2026, where it had no trigger. Kruskal with include/exclude probing, so it only makes sense after the Kruskal variant rep on 1584. ⚠️ **With this, MST reaches 3 without premium**: 1584 + the Kruskal variant + this. |
| Hard | [472. Concatenated Words](https://leetcode.com/problems/concatenated-words/) | `rated:211` | **Trie's 3rd problem** — from the pull (`Trie` tag, 17 eligible; Word Break and Word Search II were both auto-flagged as already in the phase plan, which is the roadmap filter working). Trie + DFS over the dictionary itself. |
| Medium | [1472. Design Browser History](https://leetcode.com/problems/design-browser-history/) | `rated:146` | **2nd problem for HashMap + Doubly Linked List** — the technique had exactly one (146 LRU). A design problem where the DLL is the point and there is no eviction policy to hide behind. |
| Medium | [53. Maximum Subarray (Divide and Conquer)](https://leetcode.com/problems/maximum-subarray/) | `rated:912` + `surplus>=1` | **D&C consolidation rep.** ⚠️ *Original trigger "active block week of Jul 6" **expired unfired** — caught Jul 26, 2026, three weeks stale. A dead stub (`maxSubarrayDivideNConquer`, body `return`) sits in the solution file from that abandoned setup.* **Re-triggered as a condition, not a date: pull once (a) 912 Merge Sort has its RATED rep (Jul 29 — D&C was taught unrated Jul 25, so 912 measures retention first) AND (b) surplus ≥ 1.** Rationale: D&C currently has exactly **one** problem (912) where a technique wants 3–4, and this is the natural second — but running it before 912 is rated would measure the teaching, not the technique. See [[project_dandc_coding_gap]]. |
| Hard | [42. Trapping Rain Water (Two Pointer)](https://leetcode.com/problems/trapping-rain-water/) | `graduates:42` | O(1) space optimization. **Trigger: pull into rotation when 42 Array GRADUATES (🎓).** ⚠️ Wording corrected Aug 7, 2026 — it read "retires (🏆)", which predates the Jul 26 label swap; the `graduate_at_streak` tier is 🎓 Graduated, and 🏆 Retired is the terminal tier well beyond it. Gating on 🏆 would have deferred this variant by ~a year past its intended trigger. **Array method 🟢 streak 2 as of Aug 7 → the NEXT clean rep (due Oct 6) fires this trigger.** |
| Medium | [210. Course Schedule II (DFS postorder)](https://leetcode.com/problems/course-schedule-ii/) | `graduates:210` | **Method variant — the only unqueued variant gap in [`technique_coverage.md`](technique_coverage.md).** Topological sort has three problems (207, 210, 269) and **all three are Kahn's**; DFS-topo has never been written once. Gated by the method-variant rule — needs 210 itself at 🎓 (currently 🟢 streak 1, next Aug 23). **Why it earns a rep rather than a footnote:** DFS-topo requires a *three-state* visited (unvisited / in-progress / done) to detect a cycle as a back edge, plus reverse-postorder to emit forward — machinery Kahn's never makes you build, so three Kahn's reps leave it genuinely untrained. Surfaced Jul 28, 2026 by the coverage report. |
| Hard | Digit DP (technique) — e.g. [233. Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | `phase:2D-DP` | Technique: counting numbers in a range by digit constraints. Not in NC150; advanced DP. Best learned AFTER the 1D/2D DP blocks (Oct–Dec) once DP foundation is solid. |
| Medium | [300. Longest Increasing Subsequence (O(n log n))](https://leetcode.com/problems/longest-increasing-subsequence/) | `phase:1D-DP` | DP enrichment: patience-sorting / binary-search LIS. Base O(n²) LIS is NC150; this is the optimized form. Learn after the 1D DP block. |
| Hard | [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | `phase:1D-DP` | DP enrichment: multi-dimensional LIS (sort on one dim, LIS on the other). Extension of 300, NOT grid DP. Not in NC150. |
| Medium | [646. Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | `phase:1D-DP` | DP enrichment: LIS/greedy chain variant (sort + LIS). Same family as 354/Building Bridges. Not in NC150. |
| Hard | Interval DP — Matrix Chain Multiplication (classic) | `phase:2D-DP` | DP enrichment: broader interval DP beyond NC150's Burst Balloons (312). "Solve inner intervals, combine outward." Learn after 2D DP block. |
| Hard | Bitmask DP (technique) — e.g. TSP / [847. Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | `phase:2D-DP` | DP enrichment: state = bitmask of visited set. Not in NC150; common in harder interviews. Learn after 2D DP block. |
| Hard | [85. Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | `solved:84` | Matrix→row-histogram reduction (monotonic stack): per row, treat column heights as a histogram → run 84. Built on `84. Largest Rectangle in Histogram` (NC150 Stack). NOT DP space-compression. Not in NC150. |
| Medium | [1504. Count Submatrices With All Ones](https://leetcode.com/problems/count-submatrices-with-all-ones/) | `solved:84` | Same row-histogram reduction as 85, different aggregation. Anchored on 84 (NC150 Stack). Not in NC150. |
| Medium | [743. Network Delay Time (Bellman-Ford variant)](https://leetcode.com/problems/network-delay-time/) | `graduates:743` | The **direct contrast rep**: a problem already solved with Dijkstra, re-solved with Bellman-Ford on identical input, to feel the decision rule rather than recite it. **Gated by the method-variant rule** — needs 743 itself at 🏆 (currently 🟡). Different axis from a consolidation rep: this is *another technique on one problem*, not *one technique across problems*, and its gate is about rep economics rather than ROI. |

---

## 📌 Grind 75 Fill — the should-know set (added Aug 13, 2026)

**These sit ABOVE the Knowledge Expansion Queue on purpose.** They are not enrichment and not advanced —
they are problems a candidate is simply expected to have seen, which **NC150 happens not to contain.**
The learner's call: *"13/17 that are not there can be slotted in… above expansion since these are should
knows."*

**Where they came from.** Diffed [Grind 75](https://www.techinterviewhandbook.org/grind75/) against
NC150 (Aug 13, 2026): **17 of Grind 75's problems are not in NC150**, and 4 of those are already tracked
here (169 · 733 · 75 · 721 — the last two arrived as ad-hoc additions, which is itself evidence the gap
is real). **The remaining 13 are below.**

**This is a tier, not a queue with a trigger.** Every row enters normal new-problem intake; what rations
them is capacity, not a condition — so they are read at the weekly build like phase intake, **not** like
the Waiting Room. Three rules keep that from becoming a void:

1. **≤2 per week**, and **never displacing active-phase intake.** A phase is time-boxed and does not get
   done later for free; this set has no deadline. It is the *first* filler after phase intake, ahead of
   consolidation reps and ahead of the 🟢 backlog.
2. **Order is by what each closes**, not by difficulty — the ⭐ rows first.
3. **Rows with a real gate carry one** in the standard vocabulary; the rest are ungated and schedulable
   the moment there is room.

| | Difficulty | Problem | Technique / what it closes | Gate |
|---|---|---|---|---|
| ⭐ | Medium | [438. Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Sliding window + **fixed alphabet** — aimed squarely at the repo's **most repeated complexity miss** (5 occurrences across 242, 567, 424, 269×3, 621, capped once). Here the fixed-alphabet argument *is* the complexity answer | — ready |
| ⭐ | Hard | [224. Basic Calculator](https://leetcode.com/problems/basic-calculator/) | `Stack (expression evaluation)` — **no-🟢 and thin (1/2)**. Also settles the open Aug 11 objection that 150 had no value: its defence was *"it's the base rung under 224/227/772"*, which only holds if something above it is scheduled | `rated:150` *(retry Aug 21)* |
| | Medium | [236. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | The general-tree LCA. 235 (BST) is tracked at 🟡; 236 is the more commonly asked of the pair and cannot use the BST ordering shortcut | — ready |
| | Medium | [542. 01 Matrix](https://leetcode.com/problems/01-matrix/) | Multi-source BFS — consolidation against 994 (🟢) | — ready |
| | Medium | [310. Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | Leaf-peeling on an undirected graph — a genuinely different shape from the three Kahn's reps (207, 210, 269) | — ready |
| | Medium | [8. String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) | No algorithm — pure **spec-reading**, which is exactly the rep 150 turned out to deliver (all three of its bugs were spec-vs-language-default) | — ready |
| | Hard | [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Weighted interval scheduling: sort + binary search + DP. A real new shape, and the only row here that needs a foundation first | `phase:1D-DP` *(Oct 12)* |
| | Easy | [67. Add Binary](https://leetcode.com/problems/add-binary/) | Bit/string carry arithmetic | — ready |
| | Easy | [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Amortized two-stack queue — the amortization argument is the rep, not the code | — ready |
| | Easy | [278. First Bad Version](https://leetcode.com/problems/first-bad-version/) | Binary search on a predicate (🎓 Binary Search — pure application) | — ready |
| | Easy | [383. Ransom Note](https://leetcode.com/problems/ransom-note/) | Frequency counting (🟢 — pure application) | — ready |
| | Easy | [409. Longest Palindrome](https://leetcode.com/problems/longest-palindrome/) | Counting + parity | — ready |
| | Easy | [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Fast/slow pointer (🎓 — pure application) | — ready |

**The cost, stated rather than discovered later.** Intake is **33.0 units one-time** (6 Easy × 1.5 +
5 Medium × 3.0 + 2 Hard × 4.5), and **13 new rows bill roughly 0.5 slots/week forever** once mature
([[project_library_carrying_capacity]]). At ≤2/week that is ~7 weeks of the filler slot. **The SD rework
is what pays for it** — retiring the three SD lanes freed ~9 units/week, and this is a better use of them
than deeper backlog sweeps, because six of these techniques are already 🟢/🎓 here and the reps are
cheap application rather than blank-tax.

⚠️ **Six of the Easy rows are near-certain 🟢s.** That is the point (they are should-knows, and a 🟢
confirms transfer) — but it means **they buy permanent review load for little information.** If the first
three come back 🟢 with no hesitation, consider running the rest as **disposable probes with no tracker
row**, the same valve the recognition probes use.

### Not from Grind 75 — the two that prompted this, held behind a technique gate

**Minimum Knight Moves (1197)** and **Bus Routes (815)** are in **Grind 169**, not Grind 75. Both are
**BFS on implicit graph**, which `technique_coverage.md` reports as **1 problem (127), 🟡, no 🟢** — the
thinnest graph technique on the board.

**They are held, and the precedent is this repo's own:** 1631/1514 sit behind `green:Dijkstra` because
*consolidation deepens a technique, it cannot substitute for proving one.* Same shape here.

⭐ **Worth knowing beyond these two rows: HelloInterview has a full DSA section** at
`/learn/code/<category>/<slug>`, 16 categories, and the learner has premium. **That is a third mirror for
paywalled LeetCode problems**, alongside the NeetCode one — and a better-maintained one than the
hand-curated `NEETCODE_RENAMES` map in `new_problem.py`, which only grows when a link is found broken.
Reach for it whenever a premium problem's link cannot be resolved, and pass it with `--url`.

| Difficulty | Problem | Trigger | Notes |
|---|---|---|---|
| Hard | [815. Bus Routes](https://leetcode.com/problems/bus-routes/) | `solved:127` | The better of the two: its content is the **modeling call** — are the nodes stops, or routes? — which is the recognition axis nothing else on the board tests. **127 is on Thu Aug 13's board**, so this trigger has a live chance immediately |
| Medium | [1197. Minimum Knight Moves](https://www.hellointerview.com/learn/code/breadth-first-search/minimum-knight-moves) | `solved:127` | ✅ **Source resolved Aug 13: HelloInterview premium**, which the learner has — it sits under their Breadth-First Search section. The row links there, **not** to the paywalled LeetCode page, and NeetCode has no mirror. ⚠️ **Scaffold with `--url` explicitly:** `new_problem.py`'s link check only knows LeetCode GraphQL and the NeetCode rename map, so left to itself it will flag this as premium and point at a NeetCode slug that does not exist. The unbounded grid is the interesting half — BFS with no bounds means the visited set is the only thing stopping it, and symmetry folding is what keeps it finite |

---

## 🧊 Knowledge Expansion Queue — post-NC150 / below the ROI line

**Genuinely parked.** Depth and enrichment that is *deliberately* deferred — no trigger needed
beyond "after NC150," and no expectation of scheduling before then. If an entry here acquires a
real condition, it belongs in the **Waiting Room** above instead; if a Waiting Room entry turns out
to be below the ROI line, move it down here. Keeping the two separated is what stops the second
kind from burying the first.

*(Phase-gated 🔴s live in the Waiting Room, not here — a Blank on an un-taught technique is a
premature attempt with a real trigger, not enrichment. Leaving one in the review table isn't an
option either: the script recomputes `next review = latest attempt + interval`, so it snaps back
to permanently-overdue and inflates the backlog signal.)*

| Difficulty | Problem | Notes |
|---|---|---|
| Medium | [912. Sort an Array (Quick Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Radix Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Counting Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Timsort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [572. Subtree of Another Tree (serialize + KMP)](https://leetcode.com/problems/subtree-of-another-tree/) | **O(m+n)** in place of the O(m·n) nested-recursion version: preorder-serialize both trees, then substring-search. Raised by the learner Aug 15, 2026 right after 572 came back 🟡. ⚠️ **KMP goes on 28 first, not here** — the string path declared above is Trie + KMP → Z-algorithm → Aho-Corasick, and meeting the failure function inside a tree problem hides both halves. ⭐ **The serialization is the real trap, not the KMP**: values need delimiters (or `12` matches inside `123`) and null markers are what make a substring hit imply an actual subtree — that part is independent of which matcher you use. Interview value is mostly the *follow-up answer*; the O(m·n) version is what you would write under time. |
| Medium | [19. Remove Nth Node From End of List (Preorder Recursion)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Parked Jul 9 — was rotating 3 variants (iterative + postorder + preorder); kept iterative + postorder in active rotation. Preorder (count length forward, then remove on the way down) is the most contrived direction for remove-from-end; revisit for enrichment. |
| Medium | [138. Copy List with Random Pointer (one-pass O(1))](https://leetcode.com/problems/copy-list-with-random-pointer/) | Space optimization: interweave copies between originals (A→A'→B→B'…), set `.random`, then unweave — no map. Solved with two-pass hashmap Jul 5; low priority, revisit the interweaving trick later. |
| Medium | [94. Binary Tree Inorder Traversal (Morris)](https://leetcode.com/problems/binary-tree-inorder-traversal/) | Technique: Morris traversal — O(1)-space inorder via threaded trees. Niche interview follow-up; not needed for any NC150 problem. Learn after NC150. |

### Post-NC150 Core-Fill (do FIRST — NC150 coverage gaps, not advanced)

Genuine holes in NC150's coverage — medium difficulty, high interview frequency. Do these **before**
the advanced techniques below. Added Jul 25 after a curriculum spot-check. Cap intake at **≤1 new/week**
(blank tax). Also seeded in `cse-coach/curriculum/dsa/expansion_tier1.yml` (Core-fill group).

| Technique | Representative problem(s) | Notes / when |
|---|---|---|
| **Tree DP** | [337. House Robber III](https://leetcode.com/problems/house-robber-iii/), [968. Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) | DP whose recurrence runs over a tree — postorder, each node returns a small tuple of sub-answers (rob/not-rob). NC150 DP is **all** linear/grid/string — zero tree-DP. Common medium. **Trigger: pull in when the 1-D DP phase opens (trees already retired by then).** |
| **Design — O(1) structures** | [380. Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/), [460. LFU Cache](https://leetcode.com/problems/lfu-cache/) | OOD with hard per-op targets: array+hashmap-of-index for O(1) random; two-hashmap+freq-buckets for LFU. NC150 "design" is LRU+Twitter only; 380 is a top-frequency phone screen. **Trigger: pull 380 alongside the Heap/Design review cluster; 460 after 146 LRU retires.** |

### Post-NC150 Advanced Techniques

Tackle **after** NC150 is comfortable. These are genuinely advanced but still surface in *hard* interviews (Tier 1). Order within is roughly by ROI. None are needed for NC150 itself.

| Technique | Representative problem(s) | Notes / when |
|---|---|---|
| **Segment Tree** | [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/), [315. Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | Range query + update in O(log n) — what prefix sums can't do (mutable). The highest-value advanced structure. |
| **Fenwick / Binary Indexed Tree** | [307](https://leetcode.com/problems/range-sum-query-mutable/), [493. Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | Lighter segment tree for prefix-sum-with-updates. Learn alongside segment tree. |
| **KMP (failure function)** | [28. Find the Index of the First Occurrence](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/), [459. Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | O(n+m) substring search; the failure-function idea recurs across string problems. |
| **Bitwise / XOR Trie** | [421. Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | Max-XOR-pair by walking bits high→low through a binary trie. |
| **Manacher's algorithm** | [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/), [647](https://leetcode.com/problems/palindromic-substrings/) | O(n) palindrome — upgrade over the NC150 DP/expand approach. |
| **Matrix exponentiation** | fast [509. Fibonacci](https://leetcode.com/problems/fibonacci-number/), 70-at-scale | Linear recurrences in O(log n) via matrix power. |
| **Tarjan's (SCC / bridges / articulation)** | [1192. Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network/) | Strongly-connected components, critical edges. |
| **Meet in the middle** | [1755. Closest Subsequence Sum](https://leetcode.com/problems/closest-subsequence-sum/) | Halve an exponential search: 2^n → 2·2^(n/2). |
| **Reservoir sampling** | [382. Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/), [398](https://leetcode.com/problems/random-pick-index/) | Uniform random pick from a stream of unknown length. |
| **Difference array** | [1109. Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | O(1) range *updates*, materialize at end. Prefix-sum's complement. |
| **Number theory kit** | [204. Count Primes](https://leetcode.com/problems/count-primes/), [50. Pow(x,n)](https://leetcode.com/problems/powx-n/) | Sieve, modular inverse, binary exponentiation, nCr mod p. |

**=========== INTERVIEW-ROI LINE ===========**
*(Everything above serves both interviews and competitive depth. Everything below is competitive-programming growth with near-zero interview payoff — see the Mission section in `study_guide.md`. Finish NC150 + Tier 1 before crossing.)*

**Tier 2 — further horizon (competitive / rare in interviews; low interview ROI).** Only pursue when going deep into competitive programming or out of systems-depth curiosity — **not needed for interviews**. Finish NC150 + all of Tier 1 before crossing. Representative problems are given so each topic has a concrete entry point; many topics live more naturally on Codeforces than LeetCode.

| Technique | Representative problem(s) | Notes / what it unlocks |
|---|---|---|
| **Sweep line & convex hull** | [218. The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/), [587. Erect the Fence](https://leetcode.com/problems/erect-the-fence/) | Process events ordered along an axis; convex hull (Andrew's monotone chain / Graham scan) for geometry. |
| **Max-flow / min-cut & bipartite matching** | [1820. Maximum Number of Accepted Invitations](https://leetcode.com/problems/maximum-number-of-accepted-invitations/), [1349. Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/) | Hungarian / Hopcroft-Karp for matching; Dinic's for flow. Min-cut = max-flow duality. |
| **LCA (binary lifting / Euler tour + sparse table)** | [1483. Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/), [2846. Minimum Edge Weight Equilibrium Queries in a Tree](https://leetcode.com/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/) | O(log n) ancestor / path queries via 2^k jump tables or RMQ over an Euler tour. |
| **Mo's algorithm & sqrt decomposition** | [1157. Online Majority Element in Subarray](https://leetcode.com/problems/online-majority-element-in-subarray/) | Offline range queries reordered by √n blocks; sqrt decomposition as the simpler cousin of segment trees. |
| **SOS DP (sum over subsets)** | [1994. The Number of Good Subsets](https://leetcode.com/problems/the-number-of-good-subsets/) | Aggregate over all subsets of a mask in O(n·2ⁿ) instead of O(3ⁿ). |
| **Convex-hull trick / Knuth DP optimization** | [1547. Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/), [1000. Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/) | Drop interval/1D DP from O(n²)/O(n³) via monotonic hull lines or the Knuth quadrangle inequality. |
| **Suffix array / suffix automaton** | [1044. Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | Full-text indexing for substring queries; the deep end of the string path below. |
| **Aho-Corasick** | [1032. Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | Multi-pattern matching = KMP failure links layered on a trie. |
| **Z-algorithm** | [3008. Find Beautiful Indices in the Given Array II](https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-ii/) | O(n) prefix-match array; alternative to KMP for pattern search. |
| **Persistent data structures / treaps** | *(few clean LeetCode instances — practice on Codeforces)* | Versioned segment trees / balanced BSTs for historical queries and rollback. |

**String-algorithm path** (learn in this order if you cross the line for strings — each builds on the prior): **Trie** (NC150) + **KMP** (Tier 1, failure function) → **Z-algorithm** → **Aho-Corasick** (multi-pattern matching = KMP failure links layered on a trie; the deep end of Tier 2 — real-world use in multi-keyword search / IDS / `grep -F`, but you'd use a library) → **suffix array / suffix automaton**. Do not attempt Aho-Corasick before KMP is solid.

**=========== TIER 3 — competitive / research horizon ===========**

*(The deepest layer — ICPC / Codeforces territory. Essentially zero interview payoff; pursue only for serious competitive-programming or systems-research depth. Almost none have clean LeetCode instances — practice on Codeforces / AtCoder. Grouped by area; learn a group only after its Tier-1/2 prerequisites are solid. This is a menu pursued deliberately over months, not a checklist.)*

**Trees (advanced):**
- **Heavy-Light Decomposition (HLD)** — path & subtree queries by layering segment trees over chains. Prereq: segment tree + LCA.
- **Centroid Decomposition** — divide-and-conquer on trees for path-counting / distance problems.
- **DSU on tree (small-to-large)** — offline subtree queries by merging small sets into large.
- **Link-Cut Trees / Euler-Tour Trees** — online dynamic tree connectivity & path aggregates.
- **Virtual (auxiliary) trees** — compress a tree to the relevant k nodes for multi-query DP.

**Strings (deepest):**
- **Suffix Automaton (full) / Suffix Tree (Ukkonen)** — linear-time full-text index; distinct substrings, multi-string LCS.
- **Palindromic Tree (Eertree)** — all distinct palindromic substrings in O(n).
- **Suffix array + LCP (Kasai) applications** — kth substring, longest repeated, etc.

**Math / number theory (advanced):**
- **FFT / NTT** — polynomial multiplication & convolutions; **FWHT** for xor/and/or convolutions.
- **CRT, Lucas' theorem, Möbius function & inversion, totient sieve** — counting under modular / divisor constraints.
- **Discrete log (baby-step giant-step), primitive roots, Tonelli–Shanks (modular sqrt)**.
- **Combinatorics** — inclusion–exclusion, **Burnside / Pólya** counting, Catalan / Stirling numbers, generating functions.

**Flows & matching (advanced):**
- **Min-Cost Max-Flow (MCMF)** — weighted flow via SPFA / Johnson potentials.
- **Min-cut modeling** — project selection / max-weight closure; **Gomory–Hu tree** for all-pairs min-cut.
- **General matching (Blossom)**; Hungarian for assignment.

**DP optimizations (beyond CHT / Knuth):**
- **Divide & Conquer DP optimization**; **Aliens trick** (Lagrangian relaxation).
- **Broken-profile / connected-component DP**; advanced **digit DP** and **bitmask DP over subsets**.

**Advanced data structures:**
- **Segment Tree Beats** — range chmin/chmax with sum, via historic-max.
- **Li Chao tree** — CHT for arbitrary line queries; **wavelet tree** — kth element in a range.
- **Persistent segment tree** (deep); **sqrt tree**.

**Graphs (advanced):**
- **2-SAT** — implication graph + SCC (builds on Tarjan, Tier 1).
- **Dominator trees**; **offline dynamic connectivity** (DSU rollback + divide-and-conquer over time).

**Geometry (advanced):**
- **Half-plane intersection**, **rotating calipers**, **Delaunay / Voronoi**, KD-trees.

**Game theory:**
- **Sprague–Grundy / Nim** — grundy numbers for impartial games.

**Prerequisite chains within Tier 3:** segment tree → HLD / segment-tree-beats / Li Chao; LCA → HLD / virtual trees; SCC (Tarjan) → 2-SAT; modular arithmetic → NTT / discrete log; max-flow (Tier 2) → MCMF / min-cut modeling.

---

## 🏆 Retired

**The terminal tier.** Problems that cleared their 🎓 spot checks — **two** clean if they climbed the
ladder normally, **one** if they arrived by the over-learned fast-track (the coverage gate is a
standing guarantee, so it already does the second check's job).
They carry **no interval and no ongoing review cost** — this is the release valve that keeps the
library under its ~500–600 carrying capacity (see `../study_guide.md` → "Library carrying capacity").

> **You graduate, then you retire.** 🎓 Graduated is the `graduate_at_streak` tier that still comes back on the longest
> days for a spot check; 🏆 Retired is done — never called back. *(Renamed Jul 26, 2026 — the two labels
> were originally the other way round, which read backwards against the ordinary meaning of the words.)*

Deliberately a **plain list, not the 7-column table** — the tracker parser must not pick these up. It
counts entries here by matching `- <number>.` inside this section for the summary's Retired column.
Every entry must also appear in `discovery_skip` in `cse.config.yml`, or discovery will resurrect it
on the next commit.

*Format:* `- <number>. <Title> (<method>) — retired <YYYY-MM-DD>, spot checks <date>, <date>`

_None yet._ **704 Binary Search** is the first problem at 🎓 (Jul 26, 2026, via the over-learned
fast-track) and the earliest retirement: it needs **one** clean spot check, due **Jan 22, 2027** —
so it lands here that day if it holds.
