package review.miscProblems;

import DataModel.TreeNode;
import DataStructure.Pair;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class BinaryTreeLeftSideView
{
    public List<Integer> leftSideView(TreeNode root)
    {
        /*
        * Same idea as right side view of Binary Tree but this time we want the left side
        *
        * So this means we want to preserve the first parent in each level
        *
        *   1. Use a Queue for BFS
        *   2. Add queue.peek to result list before we start going down the full level
        *
        * */

        Queue<TreeNode> queue = new LinkedList<>();

        List<Integer> result = new ArrayList<>();

        TreeNode parent = root;

        queue.offer(parent);

        while(!queue.isEmpty())
        {
            int size = queue.size();
            if(queue.peek() != null) result.add(queue.peek().val);
            for(int i=0;i<size;i++)
            {
                parent = queue.poll();
                if(parent!=null)
                {
                    if(parent.left != null) queue.offer(parent.left);
                    if(parent.right != null) queue.offer(parent.right);
                }
            }
        }
        return result;
    }
}
