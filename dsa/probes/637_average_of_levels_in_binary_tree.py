"""
637. Average of Levels in Binary Tree   ·   https://leetcode.com/problems/average-of-levels-in-binary-tree/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

Given the `root` of a binary tree, return the average value of the nodes on each
level, as an array. Answers within `10^-5` of the actual answer are accepted.

    root = [3,9,20,null,null,15,7]  ->  [3.00000, 14.50000, 11.00000]
        level 0: 3            -> 3
        level 1: 9, 20        -> 14.5
        level 2: 15, 7        -> 11

    root = [3,9,20,15,7]      ->  [3.00000, 14.50000, 11.00000]

Constraints:
    number of nodes is in [1, 10^4]
    -2^31 <= Node.val <= 2^31 - 1

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── RECOGNITION — fill BEFORE coding ──────────────────────────────────
    # shape:
    # technique:
    # picks it over:
    def averageOfLevels(self, root: Optional["TreeNode"]) -> List[float]:
        pass
