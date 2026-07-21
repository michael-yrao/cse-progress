# DSA Progress

<!--
Notes for future agents:
- The table columns are now: Difficulty, Problem, Comfort, Streak, Next Review Date, Latest Attempt Date, Attempt Dates.
- `Streak` tracks consecutive Clean results. Increments on Clean, resets to 0 on Shaky or Blank.
- `Attempt Dates` is a collapsed summary of the original Attempt 1–5 columns.
- Set `Next Review Date` as a computed value based on Comfort and Streak:
  - 🟢 Clean, **Streak 0 (provisional — first Clean directly after a 🔴 Blank): +10 days** (lock-down check; not yet trusted)
  - 🟢 Clean, Streak 1: +30 days
  - 🟢 Clean, Streak 2: +60 days
  - 🏆 Retired (Streak 3+): +180 days (spot check)
  - 🟡 Shaky (any streak): +10 days, reset Streak to 0
  - 🔴 Blank (any streak): +2 days, reset Streak to 0
- **Provisional Clean (🟢 + Streak 0):** log a 🟢 that *directly follows a 🔴* with **Streak 0**, not 1 — it
  gets a short +10 lock-down to verify the Blank→Clean actually stuck. If it survives (Clean again), log it
  Streak 1 (→ +30) and it rejoins the normal ladder; if it slips to 🟡/🔴, it resets as usual. A 🟢 after a
  🟡 (not a 🔴) is logged Streak 1 as normal — only Blank→Clean is provisional. Do NOT "fix" a 🟢/Streak-0 to
  Streak 1; that silently removes the lock-down.
- When a problem reaches Streak 3, change Comfort to 🏆 to retire it from regular rotation.
- Retired problems return for a spot check every 180 days. If still Clean, stays 🏆 (+180). If Shaky/Blank, return to active rotation.
- This Markdown file is generated from current row data by `scripts/update_review_dates.py`.
- The script also discovers LeetCode problems defined under `dsa/leetcode/*` and adds missing rows automatically.
- Problem titles in this table should include the method used, such as `(BFS)` or `(DFS)`.
- If a method is mentioned and the table already contains the same LeetCode number with a different method, a new row should be added rather than overwriting the existing entry.
- When run from git commit, the helper only scans staged source files to discover newly added or changed problems.
- The helper also auto-fills the current date for staged review rows that are missing `Latest Attempt Date`.
- The pre-commit hook now triggers when `docs/foundations/dsa/mastery/dsa_progress.md` or any `dsa/leetcode/*.py` file is staged.
- The review table is sorted by Latest Attempt Date descending whenever the script runs.
- A local git pre-commit hook has been installed to auto-run the script when `docs/foundations/dsa/mastery/dsa_progress.md` is staged.
- When a LeetCode problem is added here or a review row is updated, the file should be refreshed automatically and should not require an explicit ask.
- Run `python scripts/update_review_dates.py` or `npm run update-review-progression` if you edit the file outside of a commit flow.
- When we are doing LeetCode review, any problems mentioned should be logged in this file.
 - If any LeetCode problem is mentioned anywhere in the repo or during a review session, it should be added to this file.
-->

> **Auto-refresh note:** this table is regenerated automatically when `docs/foundations/dsa/mastery/dsa_progress.md` is staged for commit or when the helper script is run.

> **96** problems &nbsp;·&nbsp; **106** solutions &nbsp;·&nbsp; **334** attempts

| | 🏆 Retired | 🟢 Clean | 🟡 Shaky | 🔴 Blank |
|:---|:---:|:---:|:---:|:---:|
| **Solutions** | 0 | 83 | 22 | 1 |

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Medium | [1584. Min Cost to Connect All Points (Prim's MST)](https://leetcode.com/problems/min-cost-to-connect-all-points/) | 🟡 | 0 | 2026-07-30 | 2026-07-20 | 2026-07-16, 2026-07-18, 2026-07-20 |
| Medium | [1448. Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | 🟢 | 1 | 2026-08-19 | 2026-07-20 | 2026-05-15, 2026-06-18, 2026-07-10, 2026-07-20 |
| Easy | [206. Reverse Linked List (Iterative)](https://leetcode.com/problems/reverse-linked-list/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-04-23, 2026-05-26, 2026-06-12, 2026-06-20, 2026-07-20 |
| Easy | [21. Merge Two Sorted Lists (Recursion)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-05-20, 2026-05-21, 2026-06-12, 2026-06-20, 2026-07-20 |
| Medium | [130. Surrounded Regions (BFS)](https://leetcode.com/problems/surrounded-regions/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-06-14, 2026-06-20, 2026-07-20 |
| Easy | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | 🟡 | 0 | 2026-07-30 | 2026-07-20 | 2026-04-30, 2026-06-02, 2026-06-12, 2026-06-14, 2026-06-24, 2026-06-26, 2026-07-20 |
| Medium | [200. Number of Islands (DFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-05-31, 2026-06-02, 2026-06-16, 2026-06-26, 2026-07-20 |
| Easy | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 🟢 | 2 | 2026-09-18 | 2026-07-20 | 2026-04-30, 2026-05-26, 2026-06-25, 2026-07-20 |
| Medium | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟢 | 2 | 2026-09-17 | 2026-07-19 | 2026-05-03, 2026-06-12, 2026-07-19 |
| Medium | [417. Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | 🟡 | 0 | 2026-07-29 | 2026-07-19 | 2026-06-11, 2026-07-19 |
| Easy | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | 🟢 | 2 | 2026-09-17 | 2026-07-19 | 2026-01-10, 2026-04-02, 2026-06-02, 2026-06-12, 2026-07-19 |
| Medium | [235. Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 🟡 | 0 | 2026-07-29 | 2026-07-19 | 2026-05-03, 2026-06-12, 2026-07-19 |
| Medium | [261. Graph Valid Tree (Union-Find)](https://leetcode.com/problems/graph-valid-tree/) | 🟡 | 0 | 2026-07-28 | 2026-07-18 | 2026-06-19, 2026-06-29, 2026-07-09, 2026-07-18 |
| Medium | [19. Remove Nth Node From End of List (Postorder Recursion)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟡 | 0 | 2026-07-28 | 2026-07-18 | 2026-05-18, 2026-05-21, 2026-06-18, 2026-06-28, 2026-07-08, 2026-07-18 |
| Medium | [200. Number of Islands (BFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 2 | 2026-09-16 | 2026-07-18 | 2026-05-30, 2026-06-01, 2026-06-07, 2026-07-18 |
| Hard | [127. Word Ladder (BFS)](https://leetcode.com/problems/word-ladder/) | 🔴 | 0 | 2026-07-20 | 2026-07-18 | 2026-07-18 |
| Medium | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | 🟡 | 0 | 2026-07-27 | 2026-07-17 | 2026-04-19, 2026-07-02, 2026-07-10, 2026-07-17 |
| Medium | [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | 🟢 | 1 | 2026-08-16 | 2026-07-17 | 2026-07-06, 2026-07-08, 2026-07-17 |
| Medium | [75. Sort Colors (Dutch Flag)](https://leetcode.com/problems/sort-colors/) | 🟢 | 1 | 2026-08-16 | 2026-07-17 | 2026-01-08, 2026-04-01, 2026-05-26, 2026-05-28, 2026-06-28, 2026-07-08, 2026-07-17 |
| Medium | [540. Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/) | 🟡 | 0 | 2026-07-27 | 2026-07-17 | 2026-05-02, 2026-06-12, 2026-06-13, 2026-07-17 |
| Medium | [18. Four Sum](https://leetcode.com/problems/4sum/) | 🟡 | 0 | 2026-07-27 | 2026-07-17 | 2026-01-23, 2026-07-17 |
| Medium | [787. Cheapest Flights Within K Stops (Bellman-Ford)](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 🟢 | 0 | 2026-07-26 | 2026-07-16 | 2026-07-14, 2026-07-16 |
| Medium | [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | 🟢 | 1 | 2026-08-15 | 2026-07-16 | 2026-07-04, 2026-07-07, 2026-07-16 |
| Medium | [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | 🟢 | 2 | 2026-09-14 | 2026-07-16 | 2026-05-02, 2026-06-12, 2026-06-13, 2026-07-16 |
| Medium | [207. Course Schedule I](https://leetcode.com/problems/course-schedule/) | 🟢 | 2 | 2026-09-14 | 2026-07-16 | 2026-06-08, 2026-06-12, 2026-06-13, 2026-07-16 |
| Medium | [743. Network Delay Time (Dijkstra)](https://leetcode.com/problems/network-delay-time/) | 🟡 | 0 | 2026-07-25 | 2026-07-15 | 2026-07-13, 2026-07-15 |
| Medium | [355. Design Twitter](https://leetcode.com/problems/design-twitter/) | 🟡 | 0 | 2026-07-25 | 2026-07-15 | 2026-06-24, 2026-06-26, 2026-07-06, 2026-07-15 |
| Medium | [143. Reorder List](https://leetcode.com/problems/reorder-list/) | 🟡 | 0 | 2026-07-25 | 2026-07-15 | 2026-04-26, 2026-07-06, 2026-07-15 |
| Medium | [912. Sort an Array (Merge Sort)](https://leetcode.com/problems/sort-an-array/) | 🟡 | 0 | 2026-07-25 | 2026-07-15 | 2026-01-06, 2026-03-26, 2026-07-15 |
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-01-02, 2026-03-25, 2026-07-14 |
| Easy | [206. Reverse Linked List (Recursion)](https://leetcode.com/problems/reverse-linked-list/) | 🟡 | 0 | 2026-07-24 | 2026-07-14 | 2026-04-24, 2026-07-03, 2026-07-14 |
| Medium | [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | 🟢 | 1 | 2026-08-13 | 2026-07-14 | 2026-07-12, 2026-07-14 |
| Easy | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 🟢 | 1 | 2026-08-13 | 2026-07-14 | 2026-03-22, 2026-04-15, 2026-06-25, 2026-07-03, 2026-07-14 |
| Medium | [199. Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-05-09, 2026-06-13, 2026-07-14 |
| Medium | [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 🟢 | 2 | 2026-09-12 | 2026-07-14 | 2026-01-19, 2026-07-14 |
| Hard | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | 🟡 | 0 | 2026-07-23 | 2026-07-13 | 2026-07-11, 2026-07-13 |
| Medium | [271. Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) | 🟡 | 0 | 2026-07-23 | 2026-07-13 | 2026-07-01, 2026-07-03, 2026-07-13 |
| Medium | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 🟡 | 0 | 2026-07-23 | 2026-07-13 | 2026-04-22, 2026-07-03, 2026-07-13 |
| Medium | [74. Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | 🟡 | 0 | 2026-07-23 | 2026-07-13 | 2026-04-22, 2026-07-03, 2026-07-13 |
| Medium | [323. Number of Connected Components (DFS)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 1 | 2026-08-11 | 2026-07-12 | 2026-07-02, 2026-07-12 |
| Medium | [229. Majority Element II](https://leetcode.com/problems/majority-element-ii/) | 🟡 | 0 | 2026-07-22 | 2026-07-12 | 2026-01-30, 2026-04-14, 2026-06-27, 2026-06-29, 2026-07-12 |
| Medium | [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | 🟡 | 0 | 2026-07-22 | 2026-07-12 | 2026-04-20, 2026-07-02, 2026-07-12 |
| Medium | [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | 🟡 | 0 | 2026-07-21 | 2026-07-11 | 2026-07-11 |
| Medium | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 🟢 | 1 | 2026-08-10 | 2026-07-11 | 2026-05-16, 2026-05-20, 2026-06-30, 2026-07-02, 2026-07-11 |
| Medium | [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 🟡 | 0 | 2026-07-21 | 2026-07-11 | 2026-07-09, 2026-07-11 |
| Medium | [80. Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) | 🟢 | 1 | 2026-08-10 | 2026-07-11 | 2026-01-13, 2026-04-13, 2026-06-25, 2026-06-27, 2026-07-11 |
| Easy | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 🟢 | 1 | 2026-08-09 | 2026-07-10 | 2026-04-26, 2026-07-01, 2026-07-10 |
| Medium | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/) | 🟢 | 1 | 2026-08-09 | 2026-07-10 | 2026-06-30, 2026-07-01, 2026-07-10 |
| Medium | [105. Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 🟢 | 1 | 2026-08-09 | 2026-07-10 | 2026-07-08, 2026-07-10 |
| Medium | [36. Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | 🟢 | 1 | 2026-08-08 | 2026-07-09 | 2026-01-25, 2026-05-22, 2026-06-30, 2026-07-09 |
| Medium | [19. Remove Nth Node From End of List (Iterative)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟢 | 1 | 2026-08-08 | 2026-07-09 | 2026-04-29, 2026-05-18, 2026-06-30, 2026-07-09 |
| Easy | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | 🟢 | 1 | 2026-08-08 | 2026-07-09 | 2026-05-19, 2026-05-21, 2026-06-30, 2026-07-09 |
| Hard | [42. Trapping Rain Water (Array)](https://leetcode.com/problems/trapping-rain-water/) | 🟢 | 1 | 2026-08-07 | 2026-07-08 | 2026-04-15, 2026-06-29, 2026-07-08 |
| Easy | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | 🟢 | 1 | 2026-08-05 | 2026-07-06 | 2026-07-04, 2026-07-06 |
| Medium | [323. Number of Connected Components (BFS)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 1 | 2026-08-05 | 2026-07-06 | 2026-06-16, 2026-06-22, 2026-07-06 |
| Easy | [27. Remove Element](https://leetcode.com/problems/remove-element/) | 🟢 | 1 | 2026-08-04 | 2026-07-05 | 2026-01-05, 2026-03-28, 2026-05-27, 2026-06-26, 2026-07-05 |
| Medium | [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | 🟢 | 1 | 2026-08-04 | 2026-07-05 | 2026-07-03, 2026-07-05 |
| Medium | [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | 🟢 | 1 | 2026-08-04 | 2026-07-05 | 2026-07-05 |
| Medium | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 🟢 | 1 | 2026-08-03 | 2026-07-04 | 2026-04-13, 2026-05-29, 2026-06-15, 2026-06-25, 2026-07-04 |
| Easy | [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | 🟢 | 1 | 2026-08-03 | 2026-07-04 | 2026-03-22, 2026-04-14, 2026-06-25, 2026-07-04 |
| Medium | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 🟢 | 1 | 2026-08-03 | 2026-07-04 | 2026-06-06, 2026-06-15, 2026-06-25, 2026-07-04 |
| Medium | [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | 🟢 | 1 | 2026-08-02 | 2026-07-03 | 2026-06-23, 2026-07-03 |
| Medium | [130. Surrounded Regions (Union-Find)](https://leetcode.com/problems/surrounded-regions/) | 🟢 | 1 | 2026-08-02 | 2026-07-03 | 2026-06-21, 2026-06-23, 2026-07-03 |
| Easy | [110. Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | 🟢 | 1 | 2026-08-02 | 2026-07-03 | 2026-05-01, 2026-06-04, 2026-06-14, 2026-06-24, 2026-07-03 |
| Easy | [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | 🟢 | 1 | 2026-08-01 | 2026-07-02 | 2026-06-22, 2026-07-02 |
| Easy | [66. Plus One](https://leetcode.com/problems/plus-one/) | 🟢 | 1 | 2026-07-31 | 2026-07-01 | 2026-01-02, 2026-03-25, 2026-06-22, 2026-07-01 |
| Medium | [684. Redundant Connection (Union-Find)](https://leetcode.com/problems/redundant-connection/) | 🟢 | 1 | 2026-07-31 | 2026-07-01 | 2026-06-18, 2026-06-22, 2026-07-01 |
| Medium | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | 🟢 | 2 | 2026-08-30 | 2026-07-01 | 2026-04-21, 2026-07-01 |
| Medium | [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 🟢 | 1 | 2026-07-29 | 2026-06-29 | 2026-01-26, 2026-04-14, 2026-06-27, 2026-06-29 |
| Medium | [323. Number of Connected Components (Union-Find)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 1 | 2026-07-29 | 2026-06-29 | 2026-06-19, 2026-06-29 |
| Medium | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 🟢 | 1 | 2026-07-28 | 2026-06-28 | 2026-04-05, 2026-06-26, 2026-06-28 |
| Medium | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 🟢 | 2 | 2026-08-27 | 2026-06-28 | 2026-01-04, 2026-03-27, 2026-05-29, 2026-06-28 |
| Easy | [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | 🟢 | 1 | 2026-07-28 | 2026-06-28 | 2026-06-12, 2026-06-19, 2026-06-28 |
| Easy | [169. Majority Element](https://leetcode.com/problems/majority-element/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-01-05, 2026-04-01, 2026-05-28, 2026-06-27 |
| Medium | [53. Maximum Subarray (Prefix Sum)](https://leetcode.com/problems/maximum-subarray/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-01-08, 2026-04-01, 2026-06-27 |
| Easy | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-04-30, 2026-05-27, 2026-06-27 |
| Easy | [704. Binary Search](https://leetcode.com/problems/binary-search/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-03-09, 2026-04-13, 2026-05-27, 2026-06-27 |
| Medium | [53. Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-08, 2026-04-02, 2026-06-23, 2026-06-24 |
| Medium | [189. Rotate Array](https://leetcode.com/problems/rotate-array/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-11, 2026-04-04, 2026-06-24 |
| Medium | [75. Sort Colors (Bucket Sort)](https://leetcode.com/problems/sort-colors/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-07, 2026-04-01, 2026-06-24 |
| Medium | [261. Graph Valid Tree (DFS)](https://leetcode.com/problems/graph-valid-tree/) | 🟢 | 1 | 2026-07-23 | 2026-06-23 | 2026-06-15, 2026-06-17, 2026-06-21, 2026-06-23 |
| Easy | [1046. Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | 🟢 | 1 | 2026-07-23 | 2026-06-23 | 2026-06-23 |
| Easy | [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | 🟢 | 1 | 2026-07-22 | 2026-06-22 | 2026-01-01, 2026-03-25, 2026-06-22 |
| Medium | [2300. Successful Pairs of Spells and Potions](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/) | 🟢 | 1 | 2026-07-19 | 2026-06-19 | 2026-05-03, 2026-06-12, 2026-06-19 |
| Medium | [695. Max Area Of Island (DFS)](https://leetcode.com/problems/max-area-of-island/) | 🟢 | 1 | 2026-07-17 | 2026-06-17 | 2026-06-01, 2026-06-17 |
| Easy | [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 🟢 | 1 | 2026-07-15 | 2026-06-15 | 2026-01-03, 2026-03-27, 2026-06-05, 2026-06-15 |
| Medium | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-06-09, 2026-06-13 |
| Easy | [680. Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-01-19, 2026-04-05, 2026-05-28, 2026-05-30, 2026-06-12 |
| Medium | [572. Subtree Of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-02, 2026-06-12 |
| Easy | [21. Merge Two Sorted Lists (Iterative)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-04-26, 2026-06-12 |
| Medium | [1011. Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-03, 2026-06-12 |
| Medium | [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | 🟢 | 1 | 2026-07-07 | 2026-06-07 | 2026-06-04, 2026-06-05, 2026-06-07 |
| Easy | [100. Same Tree](https://leetcode.com/problems/same-tree/) | 🟢 | 1 | 2026-07-05 | 2026-06-05 | 2026-05-01, 2026-06-05 |
| Easy | [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | 🟢 | 1 | 2026-07-04 | 2026-06-04 | 2026-01-10, 2026-04-03, 2026-06-04 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | 🟢 | 1 | 2026-06-29 | 2026-05-30 | 2026-01-19, 2026-04-07, 2026-05-30 |
| Medium | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 🟢 | 1 | 2026-06-29 | 2026-05-30 | 2026-01-11, 2026-04-09, 2026-05-30 |
| Medium | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟢 | 1 | 2026-05-17 | 2026-04-17 | 2026-04-17 |
| Medium | [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 🟢 | 1 | 2026-05-17 | 2026-04-17 | 2026-01-28, 2026-04-17 |
| Medium | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 🟢 | 1 | 2026-05-14 | 2026-04-14 | 2026-01-31, 2026-04-14 |
| Medium | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 🟢 | 1 | 2026-05-13 | 2026-04-13 | 2026-01-24, 2026-04-13 |
| Easy | [1768. Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) | 🟢 | 1 | 2026-05-10 | 2026-04-10 | 2026-01-21, 2026-04-10 |
| Easy | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | 🟢 | 1 | 2026-05-05 | 2026-04-05 | 2026-01-15, 2026-04-05 |
| Easy | [344. Reverse String](https://leetcode.com/problems/reverse-string/) | 🟢 | 1 | 2026-05-04 | 2026-04-04 | 2026-01-15, 2026-04-04 |
| Easy | [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | 🟢 | 1 | 2026-05-02 | 2026-04-02 | 2026-01-09, 2026-04-02 |
| Easy | [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 🟢 | 1 | 2026-04-24 | 2026-03-25 | 2026-01-01, 2026-03-25 |
| Easy | [1929. Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | 🟢 | 1 | 2026-04-24 | 2026-03-25 | 2026-01-01, 2026-03-25 |

---

## Knowledge Expansion Queue

Problems added for algorithmic depth — not part of the spaced repetition tracker or stats. No attempt dates; these enter the schedule when the relevant topic week arrives.

**Also parked here: phase-gated 🔴s.** A Blank on a technique that hasn't been *taught yet* is a **premature attempt**, not a spaced-rep failure — the +2-day loop assumes forgetting, but there was never any encoding to forget. Churning it just re-blanks it. Park it with an explicit phase trigger instead; it re-enters rotation when its phase opens. (Leaving it in the review table isn't an option: the script recomputes `next review = latest attempt + interval`, so it snaps back to permanently-overdue and inflates the backlog signal.)

| Difficulty | Problem | Notes |
|---|---|---|
| Hard | [1216. Valid Palindrome III (backtracking)](https://leetcode.com/problems/valid-palindrome-iii/) | **Phase-gated 🔴.** Attempted 2026-05-31 → Blank; the Backtracking foundation isn't built until **Sep 14 – Oct 11**. Premature, not forgotten. **Trigger: pull into rotation when the Backtracking phase opens (Sep 14).** |
| Hard | [1216. Valid Palindrome III (1DP)](https://leetcode.com/problems/valid-palindrome-iii/) | **Phase-gated 🔴.** Attempted 2026-05-31 → Blank; the 1D DP foundation isn't built until **Oct 12 – Nov 8**. Premature, not forgotten. **Trigger: pull into rotation when the 1D DP phase opens (Oct 12).** |
| Medium | [912. Sort an Array (Quick Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Radix Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Counting Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Timsort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [53. Maximum Subarray (Divide and Conquer)](https://leetcode.com/problems/maximum-subarray/) | D&C pattern — active block week of Jul 6 |
| Medium | [19. Remove Nth Node From End of List (Preorder Recursion)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Parked Jul 9 — was rotating 3 variants (iterative + postorder + preorder); kept iterative + postorder in active rotation. Preorder (count length forward, then remove on the way down) is the most contrived direction for remove-from-end; revisit for enrichment. |
| Hard | [42. Trapping Rain Water (Two Pointer)](https://leetcode.com/problems/trapping-rain-water/) | O(1) space optimization. **Trigger: pull into rotation when 42 Array retires (🏆, streak 3).** Array method 🟢 streak 1 as of Jul 8. |
| Medium | [138. Copy List with Random Pointer (one-pass O(1))](https://leetcode.com/problems/copy-list-with-random-pointer/) | Space optimization: interweave copies between originals (A→A'→B→B'…), set `.random`, then unweave — no map. Solved with two-pass hashmap Jul 5; low priority, revisit the interweaving trick later. |
| Medium | [94. Binary Tree Inorder Traversal (Morris)](https://leetcode.com/problems/binary-tree-inorder-traversal/) | Technique: Morris traversal — O(1)-space inorder via threaded trees. Niche interview follow-up; not needed for any NC150 problem. Learn after NC150. |
| Hard | Digit DP (technique) — e.g. [233. Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | Technique: counting numbers in a range by digit constraints. Not in NC150; advanced DP. Best learned AFTER the 1D/2D DP blocks (Oct–Dec) once DP foundation is solid. |
| Medium | [300. Longest Increasing Subsequence (O(n log n))](https://leetcode.com/problems/longest-increasing-subsequence/) | DP enrichment: patience-sorting / binary-search LIS. Base O(n²) LIS is NC150; this is the optimized form. Learn after the 1D DP block. |
| Hard | [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | DP enrichment: multi-dimensional LIS (sort on one dim, LIS on the other). Extension of 300, NOT grid DP. Not in NC150. |
| Medium | [646. Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | DP enrichment: LIS/greedy chain variant (sort + LIS). Same family as 354/Building Bridges. Not in NC150. |
| Hard | Building Bridges (LintCode/classic) | DP enrichment: 2D LIS (sort by one endpoint, LIS on the other). Same "sort + LIS" cluster as 354/646. Not on LeetCode NC150. |
| Hard | Interval DP — Matrix Chain Multiplication (classic) | DP enrichment: broader interval DP beyond NC150's Burst Balloons (312). "Solve inner intervals, combine outward." Learn after 2D DP block. |
| Hard | Bitmask DP (technique) — e.g. TSP / [847. Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | DP enrichment: state = bitmask of visited set. Not in NC150; common in harder interviews. Learn after 2D DP block. |
| Hard | [85. Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Matrix→row-histogram reduction (monotonic stack): per row, treat column heights as a histogram → run 84. Built on `84. Largest Rectangle in Histogram` (NC150 Stack). NOT DP space-compression. Not in NC150. |
| Medium | [1504. Count Submatrices With All Ones](https://leetcode.com/problems/count-submatrices-with-all-ones/) | Same row-histogram reduction as 85, different aggregation. Anchored on 84 (NC150 Stack). Not in NC150. |

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
