package review.test.leetCode;

import DataModel.TreeNode;
import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.DiameterBinaryTree_543_E_TREE;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class diameterOfBinaryTreeTest
{
    private DiameterBinaryTree_543_E_TREE diameterBinaryTree = new DiameterBinaryTree_543_E_TREE();

    @Test
    public void diameterTest1()
    {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right = new TreeNode(3);
        assertEquals(3,diameterBinaryTree.diameterOfBinaryTree(root));
    }
}
