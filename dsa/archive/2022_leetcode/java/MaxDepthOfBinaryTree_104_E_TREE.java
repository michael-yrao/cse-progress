package review.leetcode.blind75;

import DataModel.TreeNode;

public class MaxDepthOfBinaryTree_104_E_TREE
{
    /*
    * https://leetcode.com/problems/maximum-depth-of-binary-tree/
    * */

    public int maxDepth(TreeNode root)
    {
        if(root==null) return 0;
        return 1+Math.max(maxDepth(root.left),maxDepth(root.right));
    }
}
