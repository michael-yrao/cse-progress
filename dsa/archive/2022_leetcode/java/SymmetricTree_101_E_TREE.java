package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class SymmetricTree_101_E_TREE
{
    /*
    * https://leetcode.com/problems/symmetric-tree/
    * */

    public boolean isSymmetric(TreeNode root)
    {
        /*
        * symmetric if:
        *   a. left != null && right != null
        *   b. left.val==right.val
        *
        * Let's do a helper function to simplify the problem a bit
        *
        * */

        if(root==null) return true;
        return isSymmetricHelper(root.left, root.right);
    }

    private boolean isSymmetricHelper(TreeNode left, TreeNode right)
    {
        // Base cases
        if(left==null && right==null) return true;
        if(left == null || right == null) return false;

        // Now that we know both sides exist, check to see if both sides have same value

        return  (left.val==right.val)
                && isSymmetricHelper(left.left, right.right)
                && isSymmetricHelper(left.right, right.left);
    }
}
