"""
Given a binary tree, determine if it is .

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: true

Example 2:

Input: root = [1,2,2,3,3,null,null,4,4]
Output: false

Example 3:

Input: root = []
Output: true

Constraints:

    The number of nodes in the tree is in the range [0, 5000].
    -104 <= Node.val <= 104

"""
# Definition for a binary tree node.
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # another dfs question since we want to check difference in depth
        # how do we know if a tree is height balanced?
        # it is height balanced if absolute depth of left - right > 1
        # we are checking after we return from both left and right side, so postorder dfs
        # I want to just do depth comparison, so basically just do max depth and check the formula above for if it is balanced
        # but maxdepth returns integer, so we need to keep track of the boolean somehow
        # so we will have a global boolean that we can set
        
        isBalanced = True

        def dfs(root):
            nonlocal isBalanced
            if not root:
                return 0
            
            left=dfs(root.left)
            right=dfs(root.right)

            if abs(left - right) > 1:
                isBalanced = False

            # left and right are max depth of each side
            return 1 + max(left,right)
        
        dfs(root)
        return isBalanced
    
    def isBalanced_20260614(self, root: Optional[TreeNode]) -> bool:
        # so this is height diff, we check if max depth of left and max depth of right differ by more than 1
        
        if not root:
            return True
        
        def dfs(node):
            if not node:
                return 0
            
            # get left and right depth
            leftDepth = dfs(node.left)
            rightDepth = dfs(node.right)

            # if we already know either is bad, just return -1
            if leftDepth == -1 or rightDepth == -1:
                return -1

            if abs(leftDepth-rightDepth) > 1:
                return -1

            return 1 + max(leftDepth, rightDepth)
        
        return dfs(root) != -1