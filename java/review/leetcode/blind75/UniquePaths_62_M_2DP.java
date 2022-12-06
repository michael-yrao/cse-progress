package review.leetcode.blind75;

import DataStructure.Pair;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class UniquePaths_62_M_2DP
{
    /*
    * https://leetcode.com/problems/unique-paths/
    * */

    /*
    * First thing we can do is probably do a decision tree
    * and do the backtracking solution and see if we can optimize it
    * The complexity of this would be 2^n
    * */

    public int uniquePathsBacktrack(int row, int column)
    {
        return dfs(0,0,row,column);
    }

    private int dfs(int currentRow, int currentColumn, int maxRow, int maxColumn)
    {
        // Base case, we've reached the end
        if(currentRow==maxRow-1 && currentColumn==maxColumn-1) return 1;
        // Base case, out of bounds, return 0
        if(currentRow < 0 || currentRow >= maxRow || currentColumn < 0 || currentColumn >= maxColumn) return 0;

        return dfs(currentRow+1,currentColumn,maxRow,maxColumn) + dfs(currentRow,currentColumn+1,maxRow,maxColumn);
    }

    /*
    * Solution at the top exceeds the time limit set by LeetCode since it does do a lot of repeated work
    * We can optimize this by caching each value we go to
    * We can say that we have 1 way to reaching our starting point since we start there
    * */

    public int uniquePaths(int row, int column)
    {
        Map<Pair<Integer,Integer>, Integer> cache = new HashMap<>();

        cache.put(new Pair(0,0),1);

        for(int currentRow=0;currentRow<row;currentRow++)
        {
            for(int currentColumn=0;currentColumn<column;currentColumn++)
            {
                Pair<Integer,Integer> currentVertex = new Pair(currentRow,currentColumn);
                // If we already visited here before, continue
                if(cache.containsKey(currentVertex)) continue;
                // Otherwise sum up the left and up of this current vertex

                Pair<Integer,Integer> leftVertex = new Pair<>(currentVertex.x, currentVertex.y - 1);
                Pair<Integer,Integer> upperVertex = new Pair<>(currentVertex.x-1, currentVertex.y);
                cache.put(currentVertex, cache.getOrDefault(leftVertex,0) + cache.getOrDefault(upperVertex,0));
            }
        }
        return cache.get(new Pair(row-1,column-1));
    }
}
