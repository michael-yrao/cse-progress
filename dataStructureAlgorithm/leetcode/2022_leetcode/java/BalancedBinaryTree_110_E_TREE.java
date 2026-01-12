package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class BalancedBinaryTree_110_E_TREE
{
    /*
    * https://leetcode.com/problems/balanced-binary-tree/
    * */

    public boolean isBalanced(TreeNode root)
    {
        if(root==null) return true;
        if(getHeight(root)==-1) return false;
        return true;
    }

    public int getHeight(TreeNode root)
    {
        if(root==null) return 0;
        int left=getHeight(root.left);
        int right=getHeight(root.right);
        if(left==-1 || right==-1) return -1;    // If at any point we got -1
        if(Math.abs(left-right) > 1) return -1; // If height of left and right side of any subtree is > 1, not balanced
        return Math.max(left,right)+1;
    }
}
