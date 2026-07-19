"""
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:

Input: root = [1]
Output: [[1]]

Example 3:

Input: root = []
Output: []

Constraints:

    The number of nodes in the tree is in the range [0, 2000].
    -1000 <= Node.val <= 1000
"""
# Definition for a binary tree node.
from collections import deque
import collections
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:

    # ── Attempt · 2026-07-19 ──────────────
    def levelOrder_20260719(self, root: Optional[TreeNode]) -> List[List[int]]:
       # BFS, returning each level as its own list
       # tree, not graph, don't neee visited set. just a queue is good enough
       if not root:
           return []
       
       queue = collections.deque()
       
       queue.append(root)
       
       result = []
       
       while queue:
           levelSize = len(queue)
           currentLevel = []
           for _ in range(levelSize):
               currentNode = queue.popleft()
               if currentNode:
                   currentLevel.append(currentNode.val)
                   if currentNode.left:
                       queue.append(currentNode.left)
                   if currentNode.right:
                       queue.append(currentNode.right)
           result.append(currentLevel)
       return result

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # this is just bfs
        # for bfs, we use a queue
        # we insert the root into the queue
        # process it and then insert its left/right children in there
        # main tricky part here is keeping track of number of nodes at each depth

        returnList = []

        queue = deque()
        queue.append(root)

        while queue:
            lenOfQueue = len(queue)
            currentList = []
            # at each step we insert children in
            # thus when we start, queue has all the nodes for the current level
            for i in range(lenOfQueue):
                currentNode = queue.popleft()

                if currentNode:
                    currentList.append(currentNode.val)
                    if currentNode.left:
                        queue.append(currentNode.left)
                    if currentNode.right:
                        queue.append(currentNode.right)
            if currentList:
                returnList.append(currentList)
        return returnList
    
    
    def levelOrder_20260611(self, root: Optional[TreeNode]) -> List[List[int]]:
        # basically just write out BFS
        # we do keep to keep track of levels it looks like
        # so we will just keep track of size of queue every time we loop around

        if not root:
            return []

        queue = collections.deque()

        queue.append(root)

        result = []

        while queue:
            sizeCurrentLevel = len(queue)
            currentLevel = []
            for _ in range(sizeCurrentLevel):
                currentNode = queue.popleft()
                currentLevel.append(currentNode.val)
                if currentNode.left:
                    queue.append(currentNode.left)
                if currentNode.right:
                    queue.append(currentNode.right)
            result.append(currentLevel)
        return result
