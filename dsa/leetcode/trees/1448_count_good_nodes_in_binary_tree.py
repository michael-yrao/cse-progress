"""
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:

Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: Nodes in blue are good.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.

Example 2:

Input: root = [3,3,null,4,2]
Output: 3
Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.

Example 3:

Input: root = [1]
Output: 1
Explanation: Root is considered as good.

Constraints:

    The number of nodes in the binary tree is in the range [1, 10^5].
    Each node's value is between [-10^4, 10^4].
"""
# Definition for a binary tree node.
from collections import deque
import math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        # first thing that comes to mind is monotonic stack since we want all non-decreasing nodes
        # so we can do an iterative postorder dfs
        # then we can just use the stack and specifically just use that as a monotonic stack
        # However, monotonic stack is used normally for next biggest/smallest element
        # This also overcomplicates things. What we can do instead is use a tuple like in iterative max depth
        # this would keep track of node.val, currentMax
        # we need to keep track of currentMax to ensure we are still non-decreasing
        
        currentMax = root.val
        result = 0
        stack = deque()
        stack.append([root, currentMax])

        while stack:
            # if currentNode is not null, check if it is non-decreasing compared to the currentMax
            currentNode, currentMax = stack.pop()
            if currentNode:
                if currentNode.val >= currentMax:
                    result+=1
                    currentMax = max(currentMax, currentNode.val)
                # if smaller, we just don't include it and move on to the children
                stack.append([currentNode.left,currentMax])
                stack.append([currentNode.right,currentMax])
        
        return result
    def goodNodes_20260618(self, root: TreeNode) -> int:
        # so we clearly need to know the previous node and know if it is good or not
        # we actually seem to need to know current largest so we will pass that going down the tree
        # basically we check if currentNode is good by comparing it against current largest
        # keep passing current largest down, so we are doing preorder DFS

        largestValue = -math.inf
        
        goodNodeCounter = 0

        def dfs(currentNode, largestNodeValue):
            nonlocal goodNodeCounter
            if not currentNode:
                return
            
            if currentNode.val >= largestNodeValue:
                goodNodeCounter+=1
                largestNodeValue = currentNode.val
            
            dfs(currentNode.left, largestNodeValue)
            dfs(currentNode.right, largestNodeValue)
        
        dfs(root, largestValue)

        return goodNodeCounter