package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

import java.util.*;

public class BinaryTreeLevelOrderTraversalII_107_M_TREE
{
    /*
    * https://leetcode.com/problems/binary-tree-level-order-traversal-ii/
    * */

    public List<List<Integer>> levelOrderBottom(TreeNode root)
    {
        if(root==null) return new ArrayList<>();
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        Stack<List<Integer>> resultStack = new Stack<>();
        List<List<Integer>> result = new ArrayList<>();

        while(!queue.isEmpty())
        {
            int level = queue.size();
            List<Integer> levelList = new ArrayList<>();
            for(int i=0;i<level;i++)
            {
                TreeNode parent = queue.poll();
                if(parent!=null)
                {
                    levelList.add(parent.val);
                    if(parent.left!=null) queue.offer(parent.left);
                    if(parent.right!=null) queue.offer(parent.right);
                }
            }
            resultStack.push(levelList);
        }
        while(!resultStack.isEmpty())
        {
            result.add(resultStack.pop());
        }
        return result;
    }
}
