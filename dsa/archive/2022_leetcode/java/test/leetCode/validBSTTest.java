package review.test.leetCode;

import DataModel.TreeNode;
import org.junit.jupiter.api.Test;
import review.leetcode.blind75.ValidBST_98_E_TREE;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class validBSTTest
{
    private ValidBST_98_E_TREE validBST = new ValidBST_98_E_TREE();

    @Test
    public void validBSTTest1()
    {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(4);
        root.right = new TreeNode(6);
        root.right.left = new TreeNode(3);
        root.right.right = new TreeNode(7);
        assertEquals(false,validBST.isValidBST(root));
    }

}
