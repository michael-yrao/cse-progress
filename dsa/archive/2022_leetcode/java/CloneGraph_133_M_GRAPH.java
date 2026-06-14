package review.leetcode.blind75;

import DataModel.GraphNode;

import java.util.HashMap;
import java.util.Map;

public class CloneGraph_133_M_GRAPH
{
    /*
    * https://leetcode.com/problems/clone-graph/
    * */

    // Need to create a deep copy
    // What that means is a new GraphNode for each GraphNode in the old one (e.g. with a new memory address but with same values)

    public GraphNode cloneGraph(GraphNode node)
    {
        Map<GraphNode, GraphNode> oldToNew = new HashMap<>();
        return cloneGraphDFS(node,oldToNew);
    }

    // This code looks like a memoization Dynamic Programming solution but without the base cases
    // We are recursively going through this Graph and creating an exact copy of it
    // Where the only base case is to check whether the map already has this node created

    public GraphNode cloneGraphDFS(GraphNode node, Map<GraphNode,GraphNode> oldToNew)
    {
        if(oldToNew.containsKey(node)) return oldToNew.get(node);

        GraphNode deepCopyNode = new GraphNode(node.val);
        oldToNew.put(node,deepCopyNode);

        for(GraphNode neighbor : node.neighbors)
        {
            deepCopyNode.neighbors.add(cloneGraphDFS(neighbor,oldToNew));
        }
        return deepCopyNode;
    }
}
