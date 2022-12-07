package review.leetcode.leetcodeExtra;

public class MaxAreaOfIsland_695_M_GRAPH
{
    /*
    * https://leetcode.com/problems/max-area-of-island/
    * */

    /*
    * Max Area = # of 1s in an island
    *
    * We can try to treat this problem similarly to number of islands
    * But instead of just marking the island as visited as we go through them
    * We should also keep a maxArea variable that we update as we go through each vertex
    *
    * */

    public int maxAreaOfIsland(int[][] grid)
    {
        int maxArea=0;
        if(grid==null) return maxArea;

        int row=grid.length;
        int column=grid[0].length;

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                maxArea = Math.max(maxArea,islandDFS(grid,i,j,row,column));
            }
        }
        return maxArea;
    }

    private int islandDFS(int[][] grid, int currentRow, int currentColumn, int maxRow, int maxColumn)
    {
        // If we hit water, return 0

        if(currentRow<0 || currentRow>=maxRow
                || currentColumn<0 || currentColumn>=maxColumn
                || grid[currentRow][currentColumn] == 0) return 0;

        // Mark current spot as visited

        grid[currentRow][currentColumn] = 0;

        return 1 + islandDFS(grid,currentRow-1,currentColumn,maxRow,maxColumn)
                 + islandDFS(grid,currentRow+1,currentColumn,maxRow,maxColumn)
                + islandDFS(grid,currentRow,currentColumn-1,maxRow,maxColumn)
                + islandDFS(grid,currentRow,currentColumn+1,maxRow,maxColumn);
    }
}
