package review.leetcode.blind75;

import DataModel.TreeNode;

public class DeleteLeavesWithAGivenValue_1325_M_TREE
{
    /*
    * https://leetcode.com/problems/delete-leaves-with-a-given-value/
    * */

    public TreeNode removeLeafNodesBFS(TreeNode root, int target)
    {
        /*
        * For this, I believe we can do either BFS or DFS and just delete
        * Seems like the most difficult part here is that once the leaf is deleted,
        * if the parent becomes a leaf with the target, it must also be deleted
        *
        * As such, we will use DFS
        *
        * */

        if(root!=null && isLeaf(root,target)) return null;
        dfs(null,root,target);
        if(isLeaf(root,target)) return null;
        return root;
    }

    private boolean isLeaf(TreeNode node)
    {
        return node.left==null && node.right==null;
    }

    private boolean isLeaf(TreeNode node, int target)
    {
        return node.left==null && node.right==null && node.val == target;
    }

    private void dfs(TreeNode parent, TreeNode node, int target)
    {
        // If the current node is a leaf
        // Delete its reference from its parent
        if(isLeaf(node))
        {
            if(isLeaf(node,target))
            {
                if(parent!=null)
                {
                    if(parent.left==node) parent.left=null;
                    else parent.right = null;
                }
            }
        }
        else
        {
            // If we are here, that means this node is not a leaf node

            if(node.left != null) dfs(node,node.left,target);
            if(node.right != null) dfs(node,node.right,target);

            // Check to see if the node has become a leaf node after the recursion's call stack comes here

            if(isLeaf(node,target))
            {
                if(parent != null)
                {
                    if(parent.left==node) parent.left=null;
                    else parent.right = null;
                }
            }
        }
    }
}
