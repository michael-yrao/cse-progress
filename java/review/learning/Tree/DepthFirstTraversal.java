package review.learning.Tree;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class DepthFirstTraversal
{
    public List<Integer> dfs(TreeNode node)
    {
        List<Integer> list = new ArrayList<>();
        dfsTraversal(node,list);
        return list;
    }

    public void dfsTraversal(TreeNode node, List<Integer> list)
    {
        if(node==null) return;
        if(node.left == null && node.right == null) list.add(node.val);
        dfsTraversal(node.left,list);
        dfsTraversal(node.right,list);
    }
}