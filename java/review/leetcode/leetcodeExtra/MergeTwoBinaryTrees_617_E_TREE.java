package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class MergeTwoBinaryTrees_617_E_TREE
{
    /*
    * https://leetcode.com/problems/merge-two-binary-trees/
    * */

    /*
    * There's 3 scenarios:
    *   1. Node at current position exist in both trees
    *   2. Node at current position only exists in root1
    *   3. Node at current position only exists in root2
    * */

    public TreeNode mergeTrees(TreeNode root1, TreeNode root2)
    {
        // Base cases
        if(root1==null && root2==null) return null;

        if(root1==null) return root2;
        if(root2==null) return root1;

        // If here, then both exists
        root1.val+=root2.val;

        // Call on left and right sides of the trees
        // Assign root1.left and root1.right to the results
        root1.left=mergeTrees(root1.left, root2.left);
        root1.right=mergeTrees(root1.right, root2.right);

        // Since we are pushing adding to root1 side, return root1 as return node

        return root1;
    }

}
