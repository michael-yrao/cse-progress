"""
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

Example 1:

Input: root = [1,2,3,null,5,null,4]

Output: [1,3,4]

Explanation:

Example 2:

Input: root = [1,2,3,4,null,null,null,5]

Output: [1,3,4,5]

Explanation:

Example 3:

Input: root = [1,null,3]

Output: [1,3]

Example 4:

Input: root = []

Output: []

 

Constraints:

    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100
"""


# Definition for a binary tree node.
import collections
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # if we do bfs, it's just the last element we see each time
        # so we'll just do that
        if not root:
            return []

        result = []

        queue = collections.deque()

        queue.append(root)

        while queue:
            # we want to put the last element of each level in the result
            # so we want to keep track of number of elements in each level
            numElementInLevel = len(queue)

            for i in range(numElementInLevel):
                currentNode = queue.popleft()
                # at last element, add to result
                if i == numElementInLevel - 1:
                    result.append(currentNode.val)
                if currentNode.left:
                    queue.append(currentNode.left)
                if currentNode.right:
                    queue.append(currentNode.right)
        
        return result