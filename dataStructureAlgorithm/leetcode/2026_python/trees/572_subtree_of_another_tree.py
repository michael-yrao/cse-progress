"""
Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's descendants. The tree tree could also be considered as a subtree of itself.

Example 1:

Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true

Example 2:

Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false

Constraints:

    The number of nodes in the root tree is in the range [1, 2000].
    The number of nodes in the subRoot tree is in the range [1, 1000].
    -104 <= root.val <= 104
    -104 <= subRoot.val <= 104
"""

# Definition for a binary tree node.
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # so this is like a combo problem
        # we want to find if the root of subRoot is in root
        # then we want to run isSameTree from there
        # so we can start with a bfs to find the subroot node
        # then we do preorder dfs to check isSameTree

        # bfs is queue based, so we go through the root tree
        # and populate the queue until we find the node we are looking for
        # then we run preorder dfs to find subRoot

        def dfs(p,q):
            if not p and not q:
                return True

            if p and q and p.val == q.val:
                return dfs(p.left,q.left) and dfs(p.right,q.right)
            else:
                return False

        queue = deque([root])

        while queue:
            # deque is both a queue and a stack
            # popleft is equivalent to queue.pop()
            # popright is equivalent to stack.pop()
            currentNode = queue.popleft()

            if currentNode.val == subRoot.val:
                if dfs(currentNode, subRoot):
                    return True
            if currentNode.left:
                queue.append(currentNode.left)
            if currentNode.right:
                queue.append(currentNode.right)

        return False