"""
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

Example 1:

Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
Explanation: The LCA of nodes 2 and 8 is 6.

Example 2:

Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.

Example 3:

Input: root = [2,1], p = 2, q = 1
Output: 2

Constraints:

    The number of nodes in the tree is in the range [2, 105].
    -109 <= Node.val <= 109
    All Node.val are unique.
    p != q
    p and q will exist in the BST.
"""
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:

    # ── Attempt · 2026-07-19 ──────────────
    def lowestCommonAncestor_20260719(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        # this is a BST so we can decide direction to go based on values
        # if root is smaller than both p and q, we go left
        # if root is bigger than both p and q, we go right
        # if root is in between, this is the smallest LCA
        if not root or not p or not q:
            return root
        
        # if root is in between p and q, we found the answer
        if root.val <= p.val and root.val >= q.val:
            return root
        if root.val <= q.val and root.val >= p.val:
            return root

        if root.val <= p.val and root.val <= q.val:
            return self.lowestCommonAncestor_20260719(root.right, p, q) # type: ignore
        else:
            return self.lowestCommonAncestor_20260719(root.left, p, q) # type: ignore

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode: # type: ignore
        # While we can generate the BST with inorder DFS
        # it isn't the right way to find the answer
        # this is preorder DFS since the direction we go depends on the currentNode.val
        # since we are making a decision based on currentNode to go left or right, this is preorder
        currentNode = root

        while currentNode:
            # if both are smaller, we go left
            if p.val < currentNode.val and q.val < currentNode.val:
                currentNode = currentNode.left
            # if both are bigger, we go right
            elif p.val > currentNode.val and q.val > currentNode.val:
                currentNode = currentNode.right
            # if in separate sub-trees, it's currentNode
            else:
                return currentNode
    
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode: # type: ignore
        # kind of difficult for me to understand the concept of LCA
        # but essentially we are just trying to find the nodes p and q
        # so we do preorder since we need to compare value of current node to value of p and q

        currentNode = root

        while currentNode:
            # if bigger than both, we go left
            if currentNode.val > p.val and currentNode.val > q.val:
                currentNode = currentNode.left
            # if smaller than both, we go right
            elif currentNode.val < p.val and currentNode.val < q.val:
                currentNode = currentNode.right
            # if in between, we found answer already
            else:
                return currentNode
