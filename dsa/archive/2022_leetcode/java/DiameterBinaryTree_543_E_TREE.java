package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class DiameterBinaryTree_543_E_TREE
{
    /*
    * https://leetcode.com/problems/diameter-of-binary-tree/
    * */

    /*
    * Diameter is one of the below:
    *   1. Max Depth of left subtree + Max Depth of right subtree
    *   2. diameter of left subtree
    *   3. diameter of right subtree
    *
    * max depth only gives max depth of the whole tree
    * We want maxDepth of left + maxDepth of right
    * So what we should do is store left and right in their own variables
    * But we also should note that we are looking for edge count and not vertex count
    * Therefore, we can't just do 1+Math.max(left,right), which is the true max depth of vertices
    * We are instead looking for just Math.max(left,right), which would be the max depth of edges
    * So let's store this in some other variable while we have Max Depth DFS do its thing
    *
    * */

    int maxDiameter = Integer.MIN_VALUE;
    public int diameterOfBinaryTree(TreeNode root)
    {
        if(root==null) return 0;
        maxDepthDFS(root);
        return maxDiameter;
    }

    private int maxDepthDFS(TreeNode root)
    {
        if(root==null) return 0;
        int left = maxDepthDFS(root.left);
        int right = maxDepthDFS(root.right);
        maxDiameter = Math.max(maxDiameter,left+right); // Max Diameter is # of edges, so it's l+r, not l+r+1
        return Math.max(left,right) + 1;                // This is to make the max depth DFS work
    }
}
