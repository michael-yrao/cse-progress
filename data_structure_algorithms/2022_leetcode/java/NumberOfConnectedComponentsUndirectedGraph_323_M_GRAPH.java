package review.leetcode.leetcodeExtra;

import java.util.Arrays;

public class NumberOfConnectedComponentsUndirectedGraph_323_M_GRAPH
{
    /*
    * https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
    * */

    /*
    * 2 Methods to solve this:
    *   Method #1:
    *       1. Create an adjacency list using int n, then populate the adjacent nodes with edges
    *       2. Perform DFS and count number of components similar to how we do number of islands
    *   Method #2:
    *       1. Union Find
    *           a. This algorithm basically says we are starting with n trees
    *           b. Then using the edges array, we will connect the trees
    *           c. Keep track of the "rank" of each tree (e.g. number of nodes in the union/component)
    * */
    public int numberConnectedComponent(int n, int[][] edges)
    {
        // Initialize parent array
        int[] parent = new int[n];
        // Each node start out with themselves as their parent (e.g. 0's parent is 0, 1's parent is 1, etc.)
        for(int i=0;i<=n;i++) parent[i] = i;

        // Initialize rank array
        int[] rank = new int[n];
        // Since each node only has itself in the graph/tree, we will set each to 1
        Arrays.fill(rank,1);

        // Number of components start at n since we are saying each node is separate
        // Prior to us using edges to connect them
        // We will decrement as we go through edges
        int numberOfComponents = n;

        // Go through all the edges and perform union
        // Here we will use the return value of union to decrement or not decrement
        // Dependent on whether or not an union was performed
        for(int[] connectedNodes : edges)
        {
            numberOfComponents -= union(connectedNodes[0],connectedNodes[1],parent,rank);
        }
        return numberOfComponents;
    }

    /*
    * Responsible for combining two nodes into one union
    * Returns 0 for no unions performed
    * Returns 1 for union performed
    * */
    private int union(int firstNode, int secondNode, int[] parent, int[] rank)
    {
        int firstParent = find(firstNode, parent);
        int secondParent = find(secondNode, parent);

        // If these two are already in the same union, just return some dummy value
        if(firstParent==secondParent) return 0;

        // If they are not the same, we should connect them based on whose rank is larger
        if(rank[firstParent] > rank[secondParent])
        {
            parent[secondParent] = firstParent;
            // Update the rank of the new union with the other parent's rank
            rank[firstParent] += rank[secondParent];
        }
        else
        {
            parent[firstParent] = secondParent;
            rank[secondParent] += rank[firstParent];
        }
        return 1;
    }

    /*
    * Responsible for finding parent
    * */
    private int find(int node,int[] parent)
    {
        // Each node starts out as its own parent, so initialize result to itself
        int result = node;
        // If result is not its own parent
        // We will try to find its actual parent
        while(result!=parent[result])
        {
            // path compression
            // Set parent to result's grandparent if parent has parent
            parent[result] = parent[parent[result]];
            result = parent[result];
        }
        return result;
    }

}
