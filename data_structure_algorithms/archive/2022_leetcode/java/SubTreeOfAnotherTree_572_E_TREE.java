package review.leetcode.blind75;

import DataModel.TreeNode;

public class SubTreeOfAnotherTree_572_E_TREE
{
    /*
    * https://leetcode.com/problems/subtree-of-another-tree/
    * */

    private SameTree_100_E_TREE sameTree = new SameTree_100_E_TREE();

    // Take advantage of Same Tree. A SubTree must be the Same Tree of the bigger tree's children or itself

    public boolean isSubtree(TreeNode root, TreeNode subRoot)
    {
        if(root==null) return subRoot==null;
        return sameTree.isSameTree(root,subRoot) || isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }
}
