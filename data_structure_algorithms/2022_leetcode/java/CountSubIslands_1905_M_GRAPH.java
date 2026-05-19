package review.leetcode.blind75;

import DataStructure.Pair;

import java.util.HashSet;
import java.util.Set;

public class CountSubIslands_1905_M_GRAPH
{
    /*
    * https://leetcode.com/problems/count-sub-islands/
    * */

    public int countSubIslands(int[][] grid1, int[][] grid2)
    {
        /*
        *
        * Idea is to DFS on both islands at the same time
        *
        * */

        int subIslandCount=0;

        int row = grid1.length;
        int column = grid1[0].length;

        Set<Pair<Integer,Integer>> visitedSet = new HashSet<>();

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                Pair<Integer,Integer> vertex = new Pair(i,j);
                if(grid2[i][j] == 1 && !visitedSet.contains(vertex) && dfs(grid1,grid2,visitedSet,i,j,row,column))
                    subIslandCount++;
            }
        }
        return subIslandCount;
    }

    private boolean dfs(int[][] firstGrid, int[][] secondGrid, Set<Pair<Integer,Integer>> visitedSet, int currentRow, int currentColumn, int maxRow, int maxColumn)
    {
        Pair<Integer,Integer> vertex = new Pair<>(currentRow, currentColumn);
        // If we step out of bounds or if we have already visited,
        // we will return true since this means we have just visited and/or we have reached the end of the grid
        if(secondGrid[currentRow][currentColumn] == 0
                || visitedSet.contains(vertex)
                || currentRow < 0 || currentRow >= maxRow
                || currentColumn < 0 || currentColumn >= maxColumn)
            return true;

        // Confused here, re-visit

        boolean resultBoolean = firstGrid[currentRow][currentColumn] != 0;

        // Mark that we have visited this vertex
        visitedSet.add(vertex);

        resultBoolean = resultBoolean && dfs(firstGrid,secondGrid,visitedSet,currentRow-1,currentColumn,maxRow,maxColumn);
        resultBoolean = resultBoolean && dfs(firstGrid,secondGrid,visitedSet,currentRow+1,currentColumn,maxRow,maxColumn);
        resultBoolean = resultBoolean && dfs(firstGrid,secondGrid,visitedSet,currentRow,currentColumn-1,maxRow,maxColumn);
        resultBoolean = resultBoolean && dfs(firstGrid,secondGrid,visitedSet,currentRow,currentColumn+1,maxRow,maxColumn);

        return resultBoolean;
    }
}
