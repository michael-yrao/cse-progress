package review.leetcode.blind75;

import DataModel.TreeNode;

public class ValidBST_98_E_TREE
{
    /*
    * https://leetcode.com/problems/validate-binary-search-tree/
    * */

    public boolean isValidBST(TreeNode root)
    {
        return dfsBST(root,null, null);
    }

    // We need to do a modified DFS using a minimum value and maximum value
    // e.g. the left side of the tree should have a min of Integer.MIN_VALUE and a max of the root
    // Similarly the right side of the tree should have a min of root and a max of Integer.MAX_VALUE

    private boolean dfsBST(TreeNode root, Integer min, Integer max)
    {
        if(root==null) return true;
        if((min!=null && root.val <= min) || (max!=null && root.val >= max)) return false;
        return dfsBST(root.left,min,root.val) && dfsBST(root.right,root.val,max);
    }
}
