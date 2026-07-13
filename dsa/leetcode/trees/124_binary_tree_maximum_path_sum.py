"""
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

Example 1:

Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

Example 2:

Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

Constraints:

    The number of nodes in the tree is in the range [1, 3 * 104].
    -1000 <= Node.val <= 1000
"""
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
import math
from typing import Optional


class Solution:

    # ── Attempt · 2026-07-13 ──────────────
    def maxPathSum_20260713(self, root: Optional[TreeNode]) -> int:
        maxPath = -math.inf

        def postorderDFS(node):
            nonlocal maxPath
            # DFS problem
            # need to keep track of max I believe so we can just pass that through the recursion

            if not node:
                return 0
            
            leftSum = max(postorderDFS(node.left),0)
            rightSum = max(postorderDFS(node.right),0)

            maxPath = max(maxPath, node.val + leftSum + rightSum)

            return node.val + max(leftSum, rightSum)
        
        postorderDFS(root)
        return maxPath # type: ignore

    # region ⚠ PRIOR ATTEMPTS — SPOILERS · fold before you start
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # so this is definitely DFS since we can only go down a path and not repeat
        # and we basically wanna do max(leftPath, rightPath) to pass to the root
        # so postorder DFS

        maxPath = -math.inf

        def dfs(node):
            nonlocal maxPath
            if not node:
                return 0

            # add max to remove any negative sums
            leftPath = max(dfs(node.left),0)
            rightPath = max(dfs(node.right),0)

            maxPath = max(maxPath, node.val + leftPath + rightPath)

            return node.val + max(leftPath, rightPath)
        
        dfs(root)
        return maxPath # type: ignore
# endregion