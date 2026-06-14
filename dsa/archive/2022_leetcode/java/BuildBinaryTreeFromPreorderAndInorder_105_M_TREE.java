package review.leetcode.blind75;

import DataModel.TreeNode;

import java.util.Arrays;

public class BuildBinaryTreeFromPreorderAndInorder_105_M_TREE
{
    /*
    * https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
    * */

    /*
    * Example #1:
    *       preorder: 1 2 4 5 3, Root -> Left SubTree -> Right SubTree
    *       inorder:  4 2 5 1 3, Left SubTree -> Root -> Right SubTree
    *
    * Expected Output: 1, 2, 3, 4, 5, null, null
    *
    * Example #2:
    *       preorder: 3, 9, 20, 15, 7
    *       inorder : 9, 3, 15, 20, 7
    *
    * Expected Output: 3, 9, 20, null, null, 15, 7
    * */

    public TreeNode buildTree(int[] preorder, int[] inorder)
    {
        if(preorder.length==0 || inorder.length==0) return null;

        TreeNode root = new TreeNode(preorder[0]);

        // Knowing Inorder Trees, we know that everything to the left of root is the left subtree
        // While everything to the right of the root is the right subtree

        // int middleTest = Arrays.asList(inorder).indexOf(preorder[0]); //<- THIS FUNCTION DOESN'T WORK

        int middle = 0;

        for (int i = 0; i < inorder.length; i++) {
            if (preorder[0] == inorder[i]) middle = i;
        }

        // Build the left side of the tree from 1-middle (the copyOfRange method is not inclusive for last element)

        root.left = buildTree(Arrays.copyOfRange(preorder,1,middle+1), Arrays.copyOfRange(inorder,0,middle));

        // Build the right side of the tree from middle to end

        root.right = buildTree(Arrays.copyOfRange(preorder,middle+1,preorder.length), Arrays.copyOfRange(inorder,middle+1,inorder.length));

        return root;

    }



}
