package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class PathSum_112_E_TREE
{
    /*
    * https://leetcode.com/problems/path-sum/
    * */

    public boolean hasPathSumDFS(TreeNode root, int targetSum)
    {
        /*
        * DFS and subtract current node's value from targetSum each time
        * */

        if(root==null) return false;
        if(root.val == targetSum && root.left == null && root.right == null) return true;
        return hasPathSumDFS(root.left,targetSum-root.val) || hasPathSumDFS(root.right, targetSum - root.val);
    }
}
