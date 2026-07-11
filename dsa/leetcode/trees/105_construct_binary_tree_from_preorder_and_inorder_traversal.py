"""
Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

Example 1:

Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]

Constraints:

    1 <= preorder.length <= 3000
    inorder.length == preorder.length
    -3000 <= preorder[i], inorder[i] <= 3000
    preorder and inorder consist of unique values.
    Each value of inorder also appears in preorder.
    preorder is guaranteed to be the preorder traversal of the tree.
    inorder is guaranteed to be the inorder traversal of the tree.
"""
# Definition for a binary tree node.
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # preorder = root, left, right
        # inorder = left, root, right
        # preorder[0] is the root
        if not preorder:
            return None
        
        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        # left : we want inorder items before mid
        # from preorder, we want node 1 to node mid because we know there are mid number of left nodes
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        # right : we want inorder items after mid
        # from preorder, we want everythign after the mid node since those are right nodes
        root.right = self.buildTree(preorder[1+mid:], inorder[1+mid:])

        return root
    def buildTree_20260710(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # preorder -> root, left side, right side
        # inorder -> left side, root, right side
        if not preorder or not inorder:
            return None
        root = TreeNode(preorder[0])
        rootIndex = inorder.index(root.val)
        # so we know size of left is rootIndex
        # so we go 1->rootIndex+1 on preorder inclusive of rootIndex and 0 to rootIndex on inorder exclusive of rootIndex

        leftSide = self.buildTree(preorder[1:rootIndex+1],inorder[:rootIndex])
        # right side would be preorder rootIndex+1 to end
        rightSide = self.buildTree(preorder[rootIndex+1:],inorder[rootIndex+1:])
        root.left = leftSide
        root.right = rightSide

        return root