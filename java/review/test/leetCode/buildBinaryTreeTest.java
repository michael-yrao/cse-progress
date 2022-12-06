package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.blind75.BuildBinaryTreeFromPreorderAndInorder_105_M_TREE;

public class buildBinaryTreeTest
{
    private BuildBinaryTreeFromPreorderAndInorder_105_M_TREE build = new BuildBinaryTreeFromPreorderAndInorder_105_M_TREE();

    @Test
    public void buildTest1()
    {
        int[] preorder = new int[]{1, 2, 4, 5, 3};
        int[] inorder  = new int[]{4, 2, 5, 1, 3};
        build.buildTree(preorder,inorder);
    }
}
