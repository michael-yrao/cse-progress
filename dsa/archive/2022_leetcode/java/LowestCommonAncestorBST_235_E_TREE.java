package review.leetcode.blind75;

import DataModel.TreeNode;

public class LowestCommonAncestorBST_235_E_TREE
{
    /*
    * https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
    * */

    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q)
    {
        if(root.left==p && root.right==q) return root;
        if(root == p || root == q) return root;
        if(p.val < root.val && q.val < root.val) return lowestCommonAncestor(root.left,p,q);
        if(p.val > root.val && q.val > root.val) return lowestCommonAncestor(root.right,p,q);
        return root;
    }

}
