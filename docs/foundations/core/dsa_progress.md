# DSA Progress

<!--
Notes for future agents:
- The table columns are now: Difficulty, Problem, Comfort, Streak, Next Review Date, Latest Attempt Date, Attempt Dates.
- `Streak` tracks consecutive Clean results. Increments on Clean, resets to 0 on Shaky or Blank.
- `Attempt Dates` is a collapsed summary of the original Attempt 1–5 columns.
- Set `Next Review Date` as a computed value based on Comfort and Streak:
  - 🟢 Clean, Streak 1: +30 days
  - 🟢 Clean, Streak 2: +60 days
  - 🏆 Retired (Streak 3+): +180 days (spot check)
  - 🟡 Shaky (any streak): +10 days, reset Streak to 0
  - 🔴 Blank (any streak): +2 days, reset Streak to 0
- When a problem reaches Streak 3, change Comfort to 🏆 to retire it from regular rotation.
- Retired problems return for a spot check every 180 days. If still Clean, stays 🏆 (+180). If Shaky/Blank, return to active rotation.
- This Markdown file is generated from current row data by `scripts/update_review_dates.py`.
- The script also discovers LeetCode problems defined under `dsa/leetcode/*` and adds missing rows automatically.
- Problem titles in this table should include the method used, such as `(BFS)` or `(DFS)`.
- If a method is mentioned and the table already contains the same LeetCode number with a different method, a new row should be added rather than overwriting the existing entry.
- When run from git commit, the helper only scans staged source files to discover newly added or changed problems.
- The helper also auto-fills the current date for staged review rows that are missing `Latest Attempt Date`.
- The pre-commit hook now triggers when `docs/foundations/core/dsa_progress.md` or any `dsa/leetcode/*.py` file is staged.
- The review table is sorted by Latest Attempt Date descending whenever the script runs.
- A local git pre-commit hook has been installed to auto-run the script when `docs/foundations/core/dsa_progress.md` is staged.
- When a LeetCode problem is added here or a review row is updated, the file should be refreshed automatically and should not require an explicit ask.
- Run `python scripts/update_review_dates.py` or `npm run update-review-progression` if you edit the file outside of a commit flow.
- When we are doing LeetCode review, any problems mentioned should be logged in this file.
 - If any LeetCode problem is mentioned anywhere in the repo or during a review session, it should be added to this file.
-->

> **Auto-refresh note:** this table is regenerated automatically when `docs/foundations/core/dsa_progress.md` is staged for commit or when the helper script is run.

> **82** problems &nbsp;·&nbsp; **92** solutions &nbsp;·&nbsp; **237** attempts

| | 🏆 Retired | 🟢 Clean | 🟡 Shaky | 🔴 Blank |
|:---|:---:|:---:|:---:|:---:|
| **Solutions** | 0 | 60 | 22 | 10 |

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Easy | [66. Plus One](https://leetcode.com/problems/plus-one/) | 🟢 | 1 | 2026-07-31 | 2026-07-01 | 2026-01-02, 2026-03-25, 2026-06-22, 2026-07-01 |
| Easy | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 🟡 | 0 | 2026-07-11 | 2026-07-01 | 2026-04-26, 2026-07-01 |
| Medium | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/) | 🔴 | 0 | 2026-07-02 | 2026-06-30 | 2026-06-30 |
| Medium | [19. Remove Nth Node From End of List (Iterative)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟡 | 0 | 2026-07-10 | 2026-06-30 | 2026-04-29, 2026-05-18, 2026-06-30 |
| Medium | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | 🔴 | 0 | 2026-07-02 | 2026-06-30 | 2026-05-16, 2026-05-20, 2026-06-30 |
| Easy | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | 🟡 | 0 | 2026-07-10 | 2026-06-30 | 2026-05-19, 2026-05-21, 2026-06-30 |
| Medium | [36. Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | 🟡 | 0 | 2026-07-10 | 2026-06-30 | 2026-01-25, 2026-05-22, 2026-06-30 |
| Medium | [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 🟢 | 1 | 2026-07-29 | 2026-06-29 | 2026-01-26, 2026-04-14, 2026-06-27, 2026-06-29 |
| Medium | [229. Majority Element II](https://leetcode.com/problems/majority-element-ii/) | 🟡 | 0 | 2026-07-09 | 2026-06-29 | 2026-01-30, 2026-04-14, 2026-06-27, 2026-06-29 |
| Medium | [261. Graph Valid Tree (Union-Find)](https://leetcode.com/problems/graph-valid-tree/) | 🟡 | 0 | 2026-07-09 | 2026-06-29 | 2026-06-19, 2026-06-29 |
| Medium | [323. Number of Connected Components (Union-Find)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟢 | 1 | 2026-07-29 | 2026-06-29 | 2026-06-19, 2026-06-29 |
| Hard | [42. Trapping Rain Water (Array)](https://leetcode.com/problems/trapping-rain-water/) | 🟡 | 0 | 2026-07-09 | 2026-06-29 | 2026-04-15, 2026-06-29 |
| Medium | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 🟢 | 1 | 2026-07-28 | 2026-06-28 | 2026-04-05, 2026-06-26, 2026-06-28 |
| Medium | [19. Remove Nth Node From End of List (Recursion)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟡 | 0 | 2026-07-08 | 2026-06-28 | 2026-05-18, 2026-05-21, 2026-06-18, 2026-06-28 |
| Medium | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 🟢 | 2 | 2026-08-27 | 2026-06-28 | 2026-01-04, 2026-03-27, 2026-05-29, 2026-06-28 |
| Medium | [75. Sort Colors (Dutch Flag)](https://leetcode.com/problems/sort-colors/) | 🟡 | 0 | 2026-07-08 | 2026-06-28 | 2026-01-08, 2026-04-01, 2026-05-26, 2026-05-28, 2026-06-28 |
| Easy | [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | 🟢 | 1 | 2026-07-28 | 2026-06-28 | 2026-06-12, 2026-06-19, 2026-06-28 |
| Medium | [80. Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) | 🟡 | 0 | 2026-07-07 | 2026-06-27 | 2026-01-13, 2026-04-13, 2026-06-25, 2026-06-27 |
| Easy | [169. Majority Element](https://leetcode.com/problems/majority-element/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-01-05, 2026-04-01, 2026-05-28, 2026-06-27 |
| Medium | [53. Maximum Subarray (Prefix Sum)](https://leetcode.com/problems/maximum-subarray/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-01-08, 2026-04-01, 2026-06-27 |
| Easy | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-04-30, 2026-05-27, 2026-06-27 |
| Easy | [704. Binary Search](https://leetcode.com/problems/binary-search/) | 🟢 | 1 | 2026-07-27 | 2026-06-27 | 2026-03-09, 2026-04-13, 2026-05-27, 2026-06-27 |
| Medium | [355. Design Twitter](https://leetcode.com/problems/design-twitter/) | 🟡 | 0 | 2026-07-06 | 2026-06-26 | 2026-06-24, 2026-06-26 |
| Easy | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | 🟢 | 1 | 2026-07-26 | 2026-06-26 | 2026-04-30, 2026-06-02, 2026-06-12, 2026-06-14, 2026-06-24, 2026-06-26 |
| Medium | [200. Number of Islands (DFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 1 | 2026-07-26 | 2026-06-26 | 2026-05-31, 2026-06-02, 2026-06-16, 2026-06-26 |
| Easy | [27. Remove Element](https://leetcode.com/problems/remove-element/) | 🟡 | 0 | 2026-07-06 | 2026-06-26 | 2026-01-05, 2026-03-28, 2026-05-27, 2026-06-26 |
| Medium | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 🟡 | 0 | 2026-07-05 | 2026-06-25 | 2026-04-13, 2026-05-29, 2026-06-15, 2026-06-25 |
| Medium | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 🟡 | 0 | 2026-07-05 | 2026-06-25 | 2026-06-06, 2026-06-15, 2026-06-25 |
| Easy | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 🟢 | 1 | 2026-07-25 | 2026-06-25 | 2026-04-30, 2026-05-26, 2026-06-25 |
| Easy | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 🟡 | 0 | 2026-07-05 | 2026-06-25 | 2026-03-22, 2026-04-15, 2026-06-25 |
| Easy | [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | 🟡 | 0 | 2026-07-05 | 2026-06-25 | 2026-03-22, 2026-04-14, 2026-06-25 |
| Medium | [53. Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-08, 2026-04-02, 2026-06-23, 2026-06-24 |
| Easy | [110. Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | 🟡 | 0 | 2026-07-04 | 2026-06-24 | 2026-05-01, 2026-06-04, 2026-06-14, 2026-06-24 |
| Medium | [189. Rotate Array](https://leetcode.com/problems/rotate-array/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-11, 2026-04-04, 2026-06-24 |
| Medium | [75. Sort Colors (Bucket Sort)](https://leetcode.com/problems/sort-colors/) | 🟢 | 1 | 2026-07-24 | 2026-06-24 | 2026-01-07, 2026-04-01, 2026-06-24 |
| Medium | [261. Graph Valid Tree (DFS)](https://leetcode.com/problems/graph-valid-tree/) | 🟢 | 1 | 2026-07-23 | 2026-06-23 | 2026-06-15, 2026-06-17, 2026-06-21, 2026-06-23 |
| Medium | [130. Surrounded Regions (Union-Find)](https://leetcode.com/problems/surrounded-regions/) | 🟡 | 0 | 2026-07-03 | 2026-06-23 | 2026-06-21, 2026-06-23 |
| Easy | [1046. Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | 🟢 | 1 | 2026-07-23 | 2026-06-23 | 2026-06-23 |
| Medium | [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | 🟡 | 0 | 2026-07-03 | 2026-06-23 | 2026-06-23 |
| Easy | [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | 🟡 | 0 | 2026-07-02 | 2026-06-22 | 2026-06-22 |
| Easy | [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | 🟢 | 1 | 2026-07-22 | 2026-06-22 | 2026-01-01, 2026-03-25, 2026-06-22 |
| Medium | [684. Redundant Connection (Union-Find)](https://leetcode.com/problems/redundant-connection/) | 🟡 | 0 | 2026-07-02 | 2026-06-22 | 2026-06-18, 2026-06-22 |
| Medium | [323. Number of Connected Components (BFS)](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | 🟡 | 0 | 2026-07-02 | 2026-06-22 | 2026-06-16, 2026-06-22 |
| Easy | [206. Reverse Linked List (Iterative)](https://leetcode.com/problems/reverse-linked-list/) | 🟢 | 1 | 2026-07-20 | 2026-06-20 | 2026-04-23, 2026-05-26, 2026-06-12, 2026-06-20 |
| Easy | [21. Merge Two Sorted Lists (Recursion)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 | 1 | 2026-07-20 | 2026-06-20 | 2026-05-20, 2026-05-21, 2026-06-12, 2026-06-20 |
| Medium | [130. Surrounded Regions (BFS)](https://leetcode.com/problems/surrounded-regions/) | 🟢 | 1 | 2026-07-20 | 2026-06-20 | 2026-06-14, 2026-06-20 |
| Medium | [2300. Successful Pairs of Spells and Potions](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/) | 🟢 | 1 | 2026-07-19 | 2026-06-19 | 2026-05-03, 2026-06-12, 2026-06-19 |
| Medium | [1448. Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | 🟢 | 1 | 2026-07-18 | 2026-06-18 | 2026-05-15, 2026-06-18 |
| Medium | [695. Max Area Of Island (DFS)](https://leetcode.com/problems/max-area-of-island/) | 🟢 | 1 | 2026-07-17 | 2026-06-17 | 2026-06-01, 2026-06-17 |
| Easy | [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 🟢 | 1 | 2026-07-15 | 2026-06-15 | 2026-01-03, 2026-03-27, 2026-06-05, 2026-06-15 |
| Medium | [199. Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-05-09, 2026-06-13 |
| Medium | [540. Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-05-02, 2026-06-12, 2026-06-13 |
| Medium | [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-05-02, 2026-06-12, 2026-06-13 |
| Medium | [207. Course Schedule I](https://leetcode.com/problems/course-schedule/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-06-08, 2026-06-12, 2026-06-13 |
| Medium | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 🟢 | 1 | 2026-07-13 | 2026-06-13 | 2026-06-09, 2026-06-13 |
| Easy | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-01-10, 2026-04-02, 2026-06-02, 2026-06-12 |
| Easy | [680. Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-01-19, 2026-04-05, 2026-05-28, 2026-05-30, 2026-06-12 |
| Medium | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-03, 2026-06-12 |
| Medium | [235. Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-03, 2026-06-12 |
| Medium | [572. Subtree Of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-02, 2026-06-12 |
| Easy | [21. Merge Two Sorted Lists (Iterative)](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-04-26, 2026-06-12 |
| Medium | [1011. Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | 🟢 | 1 | 2026-07-12 | 2026-06-12 | 2026-05-03, 2026-06-12 |
| Medium | [417. Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | 🟢 | 1 | 2026-07-11 | 2026-06-11 | 2026-06-11 |
| Medium | [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | 🟢 | 1 | 2026-07-07 | 2026-06-07 | 2026-06-04, 2026-06-05, 2026-06-07 |
| Medium | [200. Number of Islands (BFS)](https://leetcode.com/problems/number-of-islands/) | 🟢 | 1 | 2026-07-07 | 2026-06-07 | 2026-05-30, 2026-06-01, 2026-06-07 |
| Easy | [100. Same Tree](https://leetcode.com/problems/same-tree/) | 🟢 | 1 | 2026-07-05 | 2026-06-05 | 2026-05-01, 2026-06-05 |
| Easy | [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | 🟢 | 1 | 2026-07-04 | 2026-06-04 | 2026-01-10, 2026-04-03, 2026-06-04 |
| Hard | [1216. Valid Palindrome III (backtracking)](https://leetcode.com/problems/valid-palindrome-iii/) | 🔴 | 0 | 2026-06-02 | 2026-05-31 | 2026-05-31 |
| Hard | [1216. Valid Palindrome III (1DP)](https://leetcode.com/problems/valid-palindrome-iii/) | 🔴 | 0 | 2026-06-02 | 2026-05-31 | 2026-05-31 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | 🟢 | 1 | 2026-06-29 | 2026-05-30 | 2026-01-19, 2026-04-07, 2026-05-30 |
| Medium | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 🟢 | 1 | 2026-06-29 | 2026-05-30 | 2026-01-11, 2026-04-09, 2026-05-30 |
| Medium | [143. Reorder List](https://leetcode.com/problems/reorder-list/) | 🔴 | 0 | 2026-04-28 | 2026-04-26 | 2026-04-26 |
| Easy | [206. Reverse Linked List (Recursion)](https://leetcode.com/problems/reverse-linked-list/) | 🔴 | 0 | 2026-04-26 | 2026-04-24 | 2026-04-24 |
| Medium | [74. Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | 🔴 | 0 | 2026-04-24 | 2026-04-22 | 2026-04-22 |
| Medium | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 🔴 | 0 | 2026-04-24 | 2026-04-22 | 2026-04-22 |
| Medium | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | 🟢 | 1 | 2026-05-21 | 2026-04-21 | 2026-04-21 |
| Medium | [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | 🟢 | 1 | 2026-05-20 | 2026-04-20 | 2026-04-20 |
| Medium | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | 🔴 | 0 | 2026-04-21 | 2026-04-19 | 2026-04-19 |
| Medium | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟢 | 1 | 2026-05-17 | 2026-04-17 | 2026-04-17 |
| Medium | [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 🟢 | 1 | 2026-05-17 | 2026-04-17 | 2026-01-28, 2026-04-17 |
| Medium | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 🟢 | 1 | 2026-05-14 | 2026-04-14 | 2026-01-31, 2026-04-14 |
| Medium | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 🟢 | 1 | 2026-05-13 | 2026-04-13 | 2026-01-24, 2026-04-13 |
| Easy | [1768. Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) | 🟢 | 1 | 2026-05-10 | 2026-04-10 | 2026-01-21, 2026-04-10 |
| Easy | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | 🟢 | 1 | 2026-05-05 | 2026-04-05 | 2026-01-15, 2026-04-05 |
| Easy | [344. Reverse String](https://leetcode.com/problems/reverse-string/) | 🟢 | 1 | 2026-05-04 | 2026-04-04 | 2026-01-15, 2026-04-04 |
| Easy | [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | 🟢 | 1 | 2026-05-02 | 2026-04-02 | 2026-01-09, 2026-04-02 |
| Medium | [912. Sort an Array (Merge Sort)](https://leetcode.com/problems/sort-an-array/) | 🔴 | 0 | 2026-03-28 | 2026-03-26 | 2026-01-06, 2026-03-26 |
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🟢 | 1 | 2026-04-24 | 2026-03-25 | 2026-01-02, 2026-03-25 |
| Easy | [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 🟢 | 1 | 2026-04-24 | 2026-03-25 | 2026-01-01, 2026-03-25 |
| Easy | [1929. Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | 🟢 | 1 | 2026-04-24 | 2026-03-25 | 2026-01-01, 2026-03-25 |
| Medium | [18. Four Sum](https://leetcode.com/problems/4sum/) | 🟢 | 1 | 2026-02-22 | 2026-01-23 | 2026-01-23 |
| Medium | [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 🟢 | 1 | 2026-02-18 | 2026-01-19 | 2026-01-19 |

---

## Knowledge Expansion Queue

Problems added for algorithmic depth — not part of the spaced repetition tracker or stats. No attempt dates; these enter the schedule when the relevant topic week arrives.

| Difficulty | Problem | Notes |
|---|---|---|
| Medium | [912. Sort an Array (Quick Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Radix Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Counting Sort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [912. Sort an Array (Timsort)](https://leetcode.com/problems/sort-an-array/) | Sorting algorithms deep-dive |
| Medium | [53. Maximum Subarray (Divide and Conquer)](https://leetcode.com/problems/maximum-subarray/) | D&C pattern — active block week of Jul 6 |
| Hard | [42. Trapping Rain Water (Two Pointer)](https://leetcode.com/problems/trapping-rain-water/) | O(1) space optimization — solved with O(n) array approach Jun 29; revisit two-pointer derivation later |
