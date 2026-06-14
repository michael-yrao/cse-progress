package review.miscProblems;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class ConnectAdjacentNodes
{

    /*
    * Given a Binary Tree
    * Connect the adjacent nodes
    * Return a list of linked list
    * */

    public List<LinkedList<TreeNode>> connectAdjacentNodes(TreeNode node)
    {
        // Trick to this is level order traversal aka BFS
        // BFS is done using a Queue
        // Push parent to queue
        // Push children of parent to queue
        // Pop out the parents as its own level

        List<LinkedList<TreeNode>> solution = new ArrayList<>();

        Queue<TreeNode> queue = new LinkedList<>();

        queue.offer(node);

        while(!queue.isEmpty())
        {
            int levelSize = queue.size(); // Need size of each level to loop through
            LinkedList<TreeNode> linkedList = new LinkedList<>();
            TreeNode parent = null;

            for(int i=0;i<levelSize;i++)
            {
                parent = queue.poll();
                if(parent!=null) linkedList.offer(parent);
                if(parent!=null && parent.left != null) linkedList.offer(parent.left);
                if(parent!=null && parent.right != null) linkedList.offer(parent.right);
            }
            if(parent!=null) parent.next = null;
            solution.add(linkedList);
        }
        return solution;
    }
}
