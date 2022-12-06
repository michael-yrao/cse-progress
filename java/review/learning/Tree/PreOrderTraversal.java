package review.learning.Tree;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class PreOrderTraversal
{

    /*
     * Preorder Traversal: Root, Left, Right
     * Special Properties:
     *      Preorder traversal is used to create a copy of the tree
     *      Preorder traversal is also used to get prefix expression on an expression tree
     * */

    public List<TreeNode> preorderTraversalRecursion(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        fillPreorderTraversalRecursion(root,list);
        return list;
    }

    private void fillPreorderTraversalRecursion(TreeNode root, List<TreeNode> list)
    {
        if(root!=null)
        {
            list.add(root);
            fillPreorderTraversalRecursion(root.left,list);
            fillPreorderTraversalRecursion(root.right,list);
        }
    }

    public List<TreeNode> preorderTraversalIterative(TreeNode root)
    {
        List<TreeNode> list = new ArrayList<>();
        return list;
    }

}
