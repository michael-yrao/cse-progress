package review.learning.Tree;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class InOrderTraversal
{
    /*
    * Inorder Traversal: Left, Root, Right
    * Special Properties:
    *    Inorder Traversal on a Binary Search Tree always produces a sorted list ascending
    * */

    public List<TreeNode> inorderTraversalRecursion(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        fillInorderRecursion(root,list);
        return list;
    }

    private void fillInorderRecursion(TreeNode root, List<TreeNode> list)
    {
        if(root!=null)
        {
            fillInorderRecursion(root.left,list);
            list.add(root);
            fillInorderRecursion(root.right,list);
        }
    }

    public List<TreeNode> inorderTraversalIterative(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        return list;
    }

}
