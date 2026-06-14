package review.learning.Tree;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class BreadthFirstTraversal
{
    public List<Integer> bfs(TreeNode node)
    {
        List<Integer> list = new ArrayList<>();
        bfsTraversal(node,list);
        return list;
    }

    public void bfsTraversal(TreeNode node, List<Integer> list)
    {
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(node);
        while(!queue.isEmpty())
        {
            int sizeOfQueue = queue.size();
            for(int i=0;i<sizeOfQueue;i++)
            {
                TreeNode parent = queue.poll();
                if(parent!=null) list.add(parent.val);
                if(parent!=null && parent.left!=null) queue.offer(parent.left);
                if(parent!=null && parent.right!=null) queue.offer(parent.right);
            }
        }
    }
}
