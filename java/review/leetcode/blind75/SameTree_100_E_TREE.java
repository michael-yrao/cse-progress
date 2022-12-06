package review.leetcode.blind75;

import DataModel.TreeNode;

public class SameTree_100_E_TREE
{
    /*
    * https://leetcode.com/problems/same-tree/
    * */

    public boolean isSameTree(TreeNode p, TreeNode q)
    {
        if(p==null && q==null) return true;  // Both are null
        if(p==null || q==null) return false; // Only one is null
        if(p.val!=q.val) return false;
        return isSameTree(p.left,q.left) && isSameTree(p.right,q.right);
    }
}
