package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class InorderSuccessorInBST_285_M_TREE
{

    /*
    * This problem is Premium:
     * https://leetcode.com/problems/inorder-successor-in-bst/
    *
    * You can find the same problem on LintCode:
    * https://www.lintcode.com/problem/448/
    * */

    // In Binary Tree, Inorder successor of a node is the next node in Inorder traversal of the Binary Tree
    // Inorder: Left SubTree -> Root -> Right SubTree
    // In BST, inorder = sorted list, thus we want the value bigger than p
    public TreeNode inorderSuccessor(TreeNode root, TreeNode p)
    {
        List<TreeNode> list = new ArrayList<>();

        convertToList(root,list);

        for(int i=0;i<list.size();i++)
        {
            if(list.get(i) == p)
            {
                if(i+1 < list.size()) return list.get(i+1);
            }
        }
        return null;
    }

    private void convertToList(TreeNode root, List<TreeNode> list)
    {
        convertToList(root.left,list);
        if(root!=null) list.add(root);
        convertToList(root.right,list);
    }
}
