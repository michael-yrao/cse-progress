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
    def isValidBST_iterativeDFS(self, root: Optional[TreeNode]) -> bool:
        # valid BST means we need to compare current node's value to it's children or vice versa
        # let's do this with iterative DFS
        # we should keep track of what is allowed in current node
        # from the root, we allow everything, so lower bound of -inf and upper bound of inf
        # when we go left, the upper bound changes to root
        # when we go right, the lower bound changes to root

        stack = deque()
        stack.append([root,-math.inf, math.inf])

        while stack:
            currentNode, low, high = stack.pop()
            if not currentNode:
                continue

            # if current node not within bounds, return false
            # currentNode.val must be greater than low
            # currentNode.val must be less than high
            if currentNode.val <= low or currentNode.val >= high:
                return False

            # current node is valid, update boundaries to children and add to stack
            if currentNode.left:
                stack.append([currentNode.left, low, currentNode.val])
            if currentNode.right:
                stack.append([currentNode.right, currentNode.val, high])
        return True


    def isValidBST_inorderDFS(self, root: Optional[TreeNode]) -> bool:
        # for BST, inorder DFS looks at the values in ascending order (left -> root -> right)
        # thus we can just use that as our premise
        
        prevValue = -math.inf

        def dfs(root):
            nonlocal prevValue
            if not root:
                return True
            
            # left tree, if breaks BST rule, return false
            if not dfs(root.left):
                return False
            
            # current node
            # inorder traversal, so our return caller should be smaller than us
            # if it is bigger, then we just return false
            # we actually need to store the child value somewhere
            # going to right side, this wouldn't be child anymore, so we'll just call this prevValue
            if prevValue >= root.val:
                return False
            prevValue = root.val
            
            # right tree
            return dfs(root.right)
        
        return dfs(root)
    def isValidBST_20260630(self, root: Optional[TreeNode]) -> bool:
        # inorder traversal == BST
        # but we need to create the list, check if data is unique,
        # and check if sorted == unsorted, which makes this an O(nlogn) approach
        # we can do better, thinking about the property of BST
        # going from root, left is always smaller, right is always bigger
        # we can still do an inorder traversal but we can check while we traverse
        # so if we go left, caller must be bigger
        # if we go right, caller must be smaller
        # starting at root, any number goes, so we just put -math.inf

        callerValue = -math.inf

        def inorderDFS(node):
            nonlocal callerValue
            if not node:
                return True
            
            # inorder, left, operation, right

            # if false, we need to return immediately, otherwise continue
            if not inorderDFS(node.left):
                return False
            
            # when we are here, it means we returned from left side, so we should be bigger than callerValue
            if node.val <= callerValue:
                return False
            # otherwise, we are good and we update callerValue
            callerValue = node.val

            if not inorderDFS(node.right):
                return False

            return True

        return inorderDFS(root)