"""
Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

Example 1:

Input: root = [1,2,3,4,5]
Output: 3
Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

Example 2:

Input: root = [1,2]
Output: 1

Constraints:

    The number of nodes in the tree is in the range [1, 104].
    -100 <= Node.val <= 100

"""
# Definition for a binary tree node.
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # so what it looks like if we have to get max of both sides of the subtree and add it
        # in the example, we get depth of 2 on left and depth of 1 and the right
        # thus we return 3
        # thus this is postorder dfs
        # issue is we need to keep track of the max diameter as well as max of left and right
        # so we need to have a helper function

        maxDiameter = 0

        def dfs(root):
            nonlocal maxDiameter
            
            if not root:
                return 0

            left = dfs(root.left)
            right = dfs(root.right)
            maxDiameter = max(maxDiameter, left + right)

            # return the max depth to caller
            return 1 + max(left, right)
        
        dfs(root)
        return maxDiameter
    
    def diameterOfBinaryTree_20260614(self, root: Optional[TreeNode]) -> int:
        # we are basically just adding max of left and max of right depth
        # if we are just 3 nodes, we want to go as far down as possible
        # return length after we get back up, so that is postorder DFS

        maxDiameter = 0

        def dfs(node):
            nonlocal maxDiameter
            if not node:
                return 0
            
            leftSize = dfs(node.left)
            rightSize = dfs(node.right)

            # with both left and right side returning
            # we need to check size of diameter
            maxDiameter = max(maxDiameter, leftSize + rightSize)

            # keep moving back up, so we add 1 to the size
            return 1 + max(leftSize, rightSize)

        dfs(root)
        return maxDiameter
    
    def diameterOfBinaryTree_20260624(self, root: Optional[TreeNode]) -> int:
        # postorder dfs
        maxDiameter = 0

        def dfs(node):
            nonlocal maxDiameter

            if not node:
                return 0
            
            left = dfs(node.left)
            right = dfs(node.right)
            # check current largest diameter
            maxDiameter = max(maxDiameter, left + right)
            
            # 1 + max(left,right) is just height
            return 1 + max(left, right)
        
        dfs(root)
        return maxDiameter