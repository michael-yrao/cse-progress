package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

public class RottingOranges_994_M_GRAPH
{
    /*
    * https://leetcode.com/problems/rotting-oranges/
    * */

    /*
    * Seems to be BFS and we want to keep track of how many iterations we go through to mark every fresh orange
    * 1. From a fresh orange (grid[i][j] == 2), we want to do BFS <- Actually not true since we can have multiple
    *    rotten oranges to start with
    *
    * 1. Go through entire grid, find every single rotten orange that exists, add them into the Queue
    * 2. Since we also care if all fresh oranges get rotten or not, we should create a Set that keeps track of our fresh oranges
    * 2. Afterwards, we want to go from there and
    * */
    public int orangesRotting(int[][] grid)
    {
        int row = grid.length;
        int column = grid[0].length;

        Set<Pair<Integer,Integer>> freshOranges = new HashSet<>();

        Queue<Pair<Integer,Integer>> queue = new LinkedList<>();

        // Initialize both Set and Queue

        for(int currentRow=0;currentRow<row;currentRow++)
        {
            for(int currentColumn=0;currentColumn<column;currentColumn++)
            {
                if(grid[currentRow][currentColumn]==1) freshOranges.add(new Pair(currentRow,currentColumn));
                if(grid[currentRow][currentColumn]==2) queue.offer(new Pair(currentRow,currentColumn));
            }
        }

        int currentTime = 0;

        while(!queue.isEmpty() && freshOranges.size() > 0)
        {

            int currentQueueSize = queue.size();

            for(int i=0;i<currentQueueSize;i++)
            {
                // Check if the 4 vertices around the rotten orange is a 1
                // If it is, mark it as 2 and remove it from freshOranges
                Pair<Integer,Integer> currentVertex = queue.poll();
                markRotten(grid,currentVertex.x-1, currentVertex.y, row, column,freshOranges,queue);
                markRotten(grid,currentVertex.x+1, currentVertex.y, row, column,freshOranges,queue);
                markRotten(grid,currentVertex.x, currentVertex.y+1, row, column,freshOranges,queue);
                markRotten(grid,currentVertex.x, currentVertex.y-1, row, column,freshOranges,queue);
            }
            // Increment time at the end

            currentTime++;
        }

        return (freshOranges.size()==0)?currentTime:-1;
    }

    private void markRotten(int[][] grid, int currentRow, int currentColumn, int rowLimit, int columnLimit, Set<Pair<Integer,Integer>> freshOranges,Queue<Pair<Integer,Integer>> queue)
    {
        if(currentRow < 0 || currentRow >= rowLimit || currentColumn < 0 || currentColumn >= columnLimit
            || grid[currentRow][currentColumn]!=1) return;
        Pair<Integer,Integer> currentVertex = new Pair<>(currentRow,currentColumn);
        if(grid[currentRow][currentColumn]==1)
        {
            if(freshOranges.contains(currentVertex)) freshOranges.remove(currentVertex);
            grid[currentRow][currentColumn] = 2;
            queue.add(currentVertex);
        }
    }
}
