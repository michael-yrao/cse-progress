package review.leetcode.blind75;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class BinaryTreeRightSideView_199_M_TREE
{
    /*
    * https://leetcode.com/problems/binary-tree-right-side-view/
    * */

    public List<Integer> rightSideView(TreeNode root)
    {
        /*
        Idea is to get the last element in each level when we perform BFS/Level Order Traversal
        Level Order Traversal = Queue

        1. Have Queue
        2. Add root
        3. While queue is not empty (e.g. still values to traverse through in the tree), keep going and keep track of parent
        4. We want the last parent of each level, so we need a variable to keep track of the parent at each level

        */

        List<Integer> resultList = new ArrayList<>();
        Queue<TreeNode> queue = new LinkedList<>();

        TreeNode parent = root;

        queue.offer(parent);

        while(!queue.isEmpty())
        {
            int size = queue.size();

            // For each node currently in the queue, get all their children

            for(int i=0;i<size;i++)
            {
                parent = queue.poll();
                if(parent!=null)
                {
                    if(parent.left!=null) queue.offer(parent.left);
                    if(parent.right!=null) queue.offer(parent.right);
                }
            }

            if(parent!=null) resultList.add(parent.val);
        }
        return resultList;
    }
}
