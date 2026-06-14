package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class BinaryTreeInorderTraversal_94_E_TREE
{
    /*
    * https://leetcode.com/problems/binary-tree-inorder-traversal/
    * */

    public List<Integer> inorderTraversal(TreeNode root)
    {
        // Inorder = Left, Root, Right
        List<Integer> list = new ArrayList<>();
        fillInorderList(root,list);
        return list;
    }

    public void fillInorderList(TreeNode root, List<Integer> list)
    {
        if(root!=null)
        {
            fillInorderList(root.left,list);
            list.add(root.val);
            fillInorderList(root.right,list);
        }
    }
}
