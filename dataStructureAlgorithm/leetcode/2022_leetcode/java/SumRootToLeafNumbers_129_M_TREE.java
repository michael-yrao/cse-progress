package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class SumRootToLeafNumbers_129_M_TREE
{
    public int sumNumbers(TreeNode root)
    {
        /*
        * Idea is that we need to do DFS through the tree and parent need to have a 10x multiplier each time
        *
        * If we think about a Tree of only the root, we just return root's value
        * If we think about a Tree of root + leaf children
        *    We need to do (root.right + root * 10) + ( root.left + root * 10 )
        *
        * From here, we will notice that we need to be able to pass the root's value to each iteration of dfs
        * Thus we will use a helper DFS function that takes in 2 params, the currentNode and its parent value
        *
        * * */

        // Base case

        if(root==null) return 0;

        return sumNumbersDFS(root,0);
    }

    private int sumNumbersDFS(TreeNode currentNode, int parentValue)
    {
        if(currentNode==null) return 0;
        int currentSum = currentNode.val + parentValue * 10;

        // If currentNode is a leaf, we should just return from here

        if(currentNode.left==null && currentNode.right==null) return currentSum;

        // Do the same for rest of the tree

        return sumNumbersDFS(currentNode.left, currentSum) + sumNumbersDFS(currentNode.right, currentSum);

    }
}
