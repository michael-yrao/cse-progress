"""
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:

Input: root = [1,null,2]
Output: 2

Constraints:

    The number of nodes in the tree is in the range [0, 104].
    -100 <= Node.val <= 100
"""

# Definition for a binary tree node.
import collections
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # max depth = dfs
        # how do we think about this? is this postorder/preorder/inorder
        # we can go as deep as possible and when we get to null children, we return 0
        # then go backwards, so this would mean postorder
        # since we want max depth, we would return max of either directions

        if not root:
            return 0
        
        # these 2 returns are the same
        # return max(1+self.maxDepth(root.left),1+self.maxDepth(root.right))
        return 1+max(self.maxDepth(root.left),self.maxDepth(root.right))

    def maxDepthIterativePreorderDFS(self, root: Optional[TreeNode]) -> int:
        stack = collections.deque()
        stack.append([root,1])
        # keep track of max depth
        depth = 0
        while stack:
            currentNode, curDepth = stack.pop()
            if currentNode:
                depth = max(curDepth, depth)
                stack.append([currentNode.left, curDepth + 1])
                stack.append([currentNode.right, curDepth + 1])
        return depth

    def maxDepthBFS(self, root: Optional[TreeNode]) -> int:
        # BFS max depth
        depth = 0

        queue = collections.deque()
        if root:
            queue.append(root)

        while queue:
            lenQueue = len(queue)
            for i in range(lenQueue):
                currentNode = queue.popleft()
                if currentNode:
                    if currentNode.left:
                        queue.append(currentNode.left)
                    if currentNode.right:
                        queue.append(currentNode.right)
            depth+=1
        
        return depth