package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;
import DataStructure.Pair;

import java.util.LinkedList;
import java.util.Queue;

public class MinDepthOfBinaryTree_111_E_TREE
{
    /*
    * https://leetcode.com/problems/minimum-depth-of-binary-tree/
    * */

    /*
    *
    * Postorder Traversal
    *
    * */

    public int minDepthPostorder(TreeNode root)
    {
        if(root==null) return 0;
        int left = minDepthPostorder(root.left);
        int right = minDepthPostorder(root.right);

        if(root.left == null) return 1 + right;
        if(root.right == null) return 1 + left;
        return Math.min(left,right) + 1;
    }

    /*
    * BFS Solution
    * BFS makes the most sense for this problem as we would want to return as soon as we find a leaf
    * Each time we traverse through a node, we will store a Pair of TreeNode and its depth
    * */

    public int minDepthBFS(TreeNode root)
    {
        if(root==null) return 0;

        Queue<Pair<TreeNode,Integer>> queue = new LinkedList<>();

        queue.add(new Pair<>(root,1));

        while(!queue.isEmpty())
        {
            TreeNode node = queue.peek().x;
            int depth = queue.peek().y;

            queue.poll();

            if(isLeaf(node)) return depth;

            if(node.left != null) queue.add(new Pair<>(node.left, depth + 1));
            if(node.right != null) queue.add(new Pair<>(node.right, depth + 1));
        }
        return 0;
    }

    private boolean isLeaf(TreeNode node)
    {
        return node.left==null&&node.right==null;
    }

}
