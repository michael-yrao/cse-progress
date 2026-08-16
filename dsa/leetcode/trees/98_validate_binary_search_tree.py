"""
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

    The left of a node contains only nodes with keys strictly less than the node's key.
    The right subtree of a node contains only nodes with keys strictly greater than the node's key.
    Both the left and right subtrees must also be binary search trees.

Example 1:

Input: root = [2,1,3]
Output: true

Example 2:

Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.

Constraints:

    The number of nodes in the tree is in the range [1, 104].
    -231 <= Node.val <= 231 - 1
"""
# Definition for a binary tree node.
from collections import deque
import math
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:

    # ── Attempt · 2026-08-16 ──────────────
    def isValidBST_iterativeDFS_20260816(self, root: Optional[TreeNode]) -> bool:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/98_validate_binary_search_tree.txt — restored at session end (python scripts/restore_history.py)
