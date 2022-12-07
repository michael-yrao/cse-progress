package review.learning.Tree;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class PostOrderTraversal
{
    /*
     * Postorder Traversal: Left, Right, Root
     * Special Properties:
     *      Postorder traversal is used to delete the tree
     *      Postorder traversal is also useful to get the postfix expression of an expression tree
     * */

    public List<TreeNode> postorderTraversalRecursion(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        fillPostorderTraversalRecursion(root,list);
        return list;
    }

    private void fillPostorderTraversalRecursion(TreeNode root, List<TreeNode> list)
    {
        if(root!=null)
        {
            fillPostorderTraversalRecursion(root.left,list);
            fillPostorderTraversalRecursion(root.right,list);
            list.add(root);
        }
    }

    public List<TreeNode> postorderTraversalIterative(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        return list;
    }
}
