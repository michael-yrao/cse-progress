package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class MaximumDifferenceBetweenNodeAndAncestor_1026_M_TREE
{
    /*
    * https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/
    * */

    public int maxAncestorRecursiveDFS(TreeNode root)
    {
        return maxAncestorRecursive(root,root.val,root.val);
    }

    public int maxAncestorRecursive(TreeNode root, int max, int min)
    {
        /*
        * Idea is to go through an entire ancestry and see if that largest difference is bigger than diff
        * We pass the minimum and maximum values to the children,
        * At the leaf node, we return max - min through the path from the root to the leaf.
        * */

        if(root==null) return max-min;
        max = Math.max(max,root.val);
        min = Math.min(min,root.val);
        return Math.max(maxAncestorRecursive(root.left,max,min),maxAncestorRecursive(root.right,max,min));
    }
}
