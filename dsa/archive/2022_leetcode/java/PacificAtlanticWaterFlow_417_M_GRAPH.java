package review.leetcode.blind75;

import DataStructure.Pair;

import java.util.*;

public class PacificAtlanticWaterFlow_417_M_GRAPH
{
    /*
    * https://leetcode.com/problems/pacific-atlantic-water-flow/
    * */

    public List<List<Integer>> pacificAtlantic(int[][] heights)
    {
        int row=heights.length;
        int column=heights[0].length;

        Set<Pair<Integer,Integer>> atlanticVisitSet = new HashSet<>();
        Set<Pair<Integer,Integer>> pacificVisitSet  = new HashSet<>();

        /*
        * [0][n] all touch pacific ocean
        * [n][0] all touch pacific ocean
        * [height.length][n] all touch atlantic ocean
        * [n][height.length] all touch atlantic ocean
        * */

        // Trying to visit first row of the matrix, which is all touching the pacific ocean

        for(int currentColumn=0;currentColumn<column;currentColumn++)
        {
            // [0][n]
            dfs(heights,0,currentColumn,row,column,pacificVisitSet,heights[0][currentColumn]);
            // [height.length][n]
            dfs(heights,row-1,currentColumn,row,column,atlanticVisitSet,heights[row-1][currentColumn]);
        }

        for(int currentRow=0;currentRow<row;currentRow++)
        {
            // [n][0]
            dfs(heights,currentRow,0,row,column,pacificVisitSet,heights[currentRow][0]);
            // [n][height[0].length]
            dfs(heights,currentRow,column-1,row,column,atlanticVisitSet,heights[currentRow][column-1]);
        }

        // Now that we traversed through the entire matrix for both atlantic and pacific
        // Let's go through the grid again to find the ones that intersect for the result

        List<List<Integer>> resultList = new ArrayList<>();

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                Pair<Integer,Integer> vertex = new Pair(i,j);
                if(atlanticVisitSet.contains(vertex) && pacificVisitSet.contains(vertex))
                {
                    resultList.add(Arrays.asList(i,j));
                }
            }
        }
        return resultList;

    }

    private void dfs(int[][] heights, int currentRow, int currentColumn, int maxRow, int maxColumn, Set<Pair<Integer,Integer>> visitSet, int prevHeight)
    {
        /*
        * We are trying to reach from the ocean inwards, therefore we should fail on the below conditions
        *   1. Row/Column go out of bounds
        *   2. We have already visited this vertex
        *   3. We are unable to reach (e.g. previous height is bigger) <- note that we are going from ocean upwards, so previous height must be smaller
        * */
        if(currentRow < 0 || currentRow >= maxRow || currentColumn < 0 || currentColumn >= maxColumn) return;

        if(visitSet.contains(new Pair(currentRow,currentColumn)) || heights[currentRow][currentColumn] < prevHeight) return;

        // If we can reach this vertex from the ocean, mark it as visitable in the Set
        visitSet.add(new Pair(currentRow,currentColumn));

        // Since we know this vertex is visitable, check all neighbors of it using DFS

        dfs(heights,currentRow-1,currentColumn,maxRow,maxColumn,visitSet,heights[currentRow][currentColumn]);
        dfs(heights,currentRow+1,currentColumn,maxRow,maxColumn,visitSet,heights[currentRow][currentColumn]);
        dfs(heights,currentRow,currentColumn-1,maxRow,maxColumn,visitSet,heights[currentRow][currentColumn]);
        dfs(heights,currentRow,currentColumn+1,maxRow,maxColumn,visitSet,heights[currentRow][currentColumn]);
    }
}
