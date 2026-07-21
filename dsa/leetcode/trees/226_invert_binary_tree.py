"""
Given the root of a binary tree, invert the tree, and return its root.

Example 1:

Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Example 2:

Input: root = [2,1,3]
Output: [2,3,1]

Example 3:

Input: root = []
Output: []

Constraints:

    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100
"""
from typing import Optional

# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:

    # ── Attempt · 2026-07-20 ──────────────
    def invertTree_20260720(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        leftNode = self.invertTree_20260720(root.left)
        rightNode = self.invertTree_20260720(root.right)

        root.right = leftNode
        root.left = rightNode
        return root

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # processing children first
        # thus postorder dfs

        # when root is null, return
        if not root:
            return root
        
        self.invertTree(root.left)
        self.invertTree(root.right)
        temp = root.left
        root.left = root.right
        root.right = temp

        # return the root
        return root
    
    def invertTree_20260625(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        leftNode = self.invertTree(root.left)
        rightNode = self.invertTree(root.right)

        root.left = rightNode
        root.right = leftNode

        return root
