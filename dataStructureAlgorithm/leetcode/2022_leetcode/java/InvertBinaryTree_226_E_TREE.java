package review.leetcode.blind75;

import DataModel.TreeNode;

public class InvertBinaryTree_226_E_TREE
{
    /*
    * https://leetcode.com/problems/invert-binary-tree/
    * */

    // If tree has no children, return root

    public TreeNode invertTree(TreeNode root)
    {
        if (root == null) return root;
        TreeNode temp = root.left;
        root.left=root.right;
        root.right=temp;
        invertTree(root.left);
        invertTree(root.right);
        return root;
    }
}
