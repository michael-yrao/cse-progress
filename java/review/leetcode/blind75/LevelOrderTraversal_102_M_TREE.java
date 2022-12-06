package review.leetcode.blind75;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class LevelOrderTraversal_102_M_TREE
{

    /*
    * https://leetcode.com/problems/binary-tree-level-order-traversal/
    *
    * Key to BFS is using a Queue
    *
    * */

    /*
    * Level Order Traversal Algorithm:
    *   1. Create a Queue to hold each level's nodes
    *   2. Insert Root into the Queue
    *   3. Use the Queue to store current level's nodes
    *   4. While we still have levels to traverse, e.g. the Queue is not empty
    *   5. Put the current items in the Queue to a level list
    *   6. Put the children of the Queue into the Queue
    *   7. Repeat 4-6
    * */

    public List<List<Integer>> levelOrder(TreeNode root)
    {
        List<List<Integer>> result = new ArrayList<>();

        Queue<TreeNode> queue = new LinkedList<>();

        queue.offer(root);

        while(!queue.isEmpty())
        {
            int sizeOfQueue=queue.size();
            List<Integer> level = new ArrayList<>();
            for(int i=0;i<sizeOfQueue;i++)
            {
                TreeNode parent = queue.poll();
                if(parent!=null)
                {
                    if(parent.left!=null) queue.offer(parent.left);
                    if(parent.right!=null) queue.offer(parent.right);
                    level.add(parent.val);
                }
            }
            if(!level.isEmpty()) result.add(level);
        }
        return result;
    }
}

