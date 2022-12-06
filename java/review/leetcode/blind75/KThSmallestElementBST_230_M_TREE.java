package review.leetcode.blind75;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class KThSmallestElementBST_230_M_TREE
{
    /*
    * https://leetcode.com/problems/kth-smallest-element-in-a-bst/
    * */

    public int kthSmallest(TreeNode root, int k)
    {
        List<TreeNode> list = new ArrayList<>();
        convertTreeToInorderList(root,list);
        return list.get(k-1).val;
    }

    /*
    * In order traversal puts a BST into an ordered list from smallest to largest
    * */

    public void convertTreeToInorderList(TreeNode root, List<TreeNode> list)
    {
        if(root!=null) convertTreeToInorderList(root.left, list);
        if(root!=null) list.add(root);
        if(root!=null) convertTreeToInorderList(root.right,list);
    }
}
