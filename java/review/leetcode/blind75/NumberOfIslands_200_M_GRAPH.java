package review.leetcode.blind75;

public class NumberOfIslands_200_M_GRAPH
{
    /*
    * https://leetcode.com/problems/number-of-islands/
    * */

    // Island must be connected vertically and horizontally, NOT diagonally
    // Entire grid is surrounded by water by default
    // 0 is water otherwise, 1 is land
    //
    // Idea here is to find the first 1 by traversing through the graph
    // Perform either DFS/BFS to find all the 1s connected to it and that counts as 1 island
    // Repeat

    public int numIslands(char[][] grid)
    {
        /*
        So given that we know the entire grid is surrounded by water
        What we want to do effectively is just find the first 1 that we traverse through
        and count every 1 that is connected to it as 1 island. We can do this by either BFS or DFS, I will do DFS here
        Once that is completed, we can just repeat the process.

        Normally we would want to tag which vertex we have already visited, but since we don't care about 0s
        What we should do is just mark the visited vertices as 0
        */

        /*
        1. Have a variable for max row and another for max column of grid
        2. Have a counter for number of islands
        3. Loop through the entire matrix, when we see a 1, increment counter and call DFS
        4. return counter
        */

        int row=grid.length;
        int column=grid[0].length;
        int numberOfIslands=0;

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                if(grid[i][j] == '1')
                {
                    numberOfIslands++;
                    dfs(grid,i,j,row,column);
                }
            }
        }
        return numberOfIslands;
    }

    private void dfs(char[][] grid, int currentRow, int currentColumn, int maxRow, int maxColumn)
    {
        if(currentRow < 0 || currentRow >= maxRow || currentColumn < 0 || currentColumn >= maxColumn || grid[currentRow][currentColumn] == '0')
            return;

        // Mark as visited if we haven't exitted out of DFS

        grid[currentRow][currentColumn] = '0';

        /*
        Visit all neighbors of current vertex
        left: -1,0
        right: 1,0
        up     0,1
        down   0,-1
        */

        dfs(grid,currentRow-1,currentColumn,maxRow,maxColumn);
        dfs(grid,currentRow+1,currentColumn,maxRow,maxColumn);
        dfs(grid,currentRow,currentColumn-1,maxRow,maxColumn);
        dfs(grid,currentRow,currentColumn+1,maxRow,maxColumn);
    }
}
