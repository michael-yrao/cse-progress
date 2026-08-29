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
import collections
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        # nice little BFS
        if not root:
            return []
        
        result = []

        queue = collections.deque()
        queue.append(root)

        while queue:
            lenQueue = len(queue)
            total = 0
            for _ in range(lenQueue):
                currentNode = queue.popleft()
                total+=currentNode.val
                if currentNode.left:
                    queue.append(currentNode.left)
                if currentNode.right:
                    queue.append(currentNode.right)
            result.append(total/lenQueue)

        return result
