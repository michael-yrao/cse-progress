package review.test.leetCode;

import DataModel.TreeNode;
import org.junit.jupiter.api.Test;
import review.leetcode.blind75.KThSmallestElementBST_230_M_TREE;

public class kthSmallestElementBSTTest
{
    private KThSmallestElementBST_230_M_TREE kThSmallestElementBST = new KThSmallestElementBST_230_M_TREE();

    @Test
    public void kThSmallestElementBSTTest1()
    {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(1);
        root.left.right = new TreeNode(2);
        root.right = new TreeNode(4);
        kThSmallestElementBST.kthSmallest(root,2);
    }

    @Test
    public void kThSmallestElementBSTTest2()
    {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(6);
        root.left.right = new TreeNode(4);
        root.left.left = new TreeNode(2);
        root.left.left.left = new TreeNode(1);
        kThSmallestElementBST.kthSmallest(root,2);
    }
}
