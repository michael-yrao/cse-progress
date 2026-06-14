package review.leetcode.leetcodeExtra;

import java.util.Arrays;

public class NumberOfProvinces_547_M_GRAPH
{
    /*
    * https://leetcode.com/problems/number-of-provinces/
    * */

    /*
    * Problem is slightly confusing but it is basically saying i connects to j if isConnected[i][j] == 1
    * From here, we know this is a square and thus the starting number of nodes is always isConnected.length
    *
    * 1. Using Union Find, we can assume we start at number of provinces at isConnected.length
    * 2. We can also always assume at the start that the node's parent is itself
    * 3.
    * */
    public int findCircleNum(int[][] isConnected)
    {
        int numberOfProvinces = isConnected.length;

        // Initialize parent of each node to be itself
        int[] parent = new int[numberOfProvinces];
        for(int i=0;i<parent.length;i++) parent[i] = i;

        int[] rank = new int[numberOfProvinces];
        Arrays.fill(rank,1);

        // Annoying thing with this problem is isConnected is a matrix so I have to traverse through regardless to get neighbors

        int maxDimension = isConnected.length;

        for(int i=0;i<maxDimension;i++)
        {
            for(int j=0;j<maxDimension;j++)
            {
                if(i==j) continue;
                if(isConnected[i][j] == 1)
                {
                    numberOfProvinces -= union(i,j,parent,rank);
                }
            }
        }
        return numberOfProvinces;
    }

    public int union(int firstNode, int secondNode, int[] parent, int[] rank)
    {
        int firstParent = find(firstNode, parent);
        int secondParent = find(secondNode, parent);

        if(firstParent == secondParent) return 0;

        if(rank[firstParent] > rank[secondParent])
        {
            parent[secondParent] = firstParent;
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
    * Find parent of node
    * */
    public int find(int node, int[] parent)
    {
        int result = node;
        while(result != parent[result])
        {
            parent[result] = parent[parent[result]];
            result = parent[result];
        }
        return result;
    }
}
