package review.leetcode.leetcodeExtra;

public class SurroundedRegions_130_M_GRAPH
{
    /*
    * https://leetcode.com/problems/surrounded-regions/
    * */

    /*
     * Find everything that is not surrounded
     * Go through borders
     * */

    /*
    * Knowing that the vertices on the edge of the grid will never be surrounded
    * We can run DFS on those vertices to make sure those vertices don't get marked off by turning them into a temporary value
    *       1. Go through the sides of the grid, dfs through the board, change unsurrounded vertex to a temporary value
    *       2. Go through entire grid with nested for loop, change Os to Xs
    *       3. Go through entire grid again, change Ts to Os
    * */

    public void solve(char[][] board)
    {
        int row = board.length;
        int column = board[0].length;

        // Capture "unsurrounded" regions
        // [0][n]; [row-1][n]; [n][0]; [n][column-1]

        for(int i=0;i<row;i++)
        {
            if(board[i][0] == 'O') capture(board,i,0);
            if(board[i][column-1] == 'O') capture(board,i,column-1);
        }

        for(int i=0;i<column;i++)
        {
            if(board[0][i] == 'O') capture(board,0,i);
            if(board[row-1][i] == 'O') capture(board,row-1,i);
        }

        // Capture "surrounded" regions

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                if(board[i][j]=='O') board[i][j]='X';
            }
        }

        // Uncapture "unsurrounded" regions

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                if(board[i][j]=='T') board[i][j]='O';
            }
        }
    }

    // capture is to be used to capture "unsurrounded", so we just look for only Os

    private void capture(char[][] board, int currentRow, int currentColumn)
    {
        if(currentRow<0 || currentRow>=board.length || currentColumn<0 || currentColumn>=board[0].length
                || board[currentRow][currentColumn] != 'O')
            return;

        board[currentRow][currentColumn] = 'T';

        capture(board,currentRow-1,currentColumn);
        capture(board,currentRow+1,currentColumn);
        capture(board,currentRow,currentColumn-1);
        capture(board,currentRow,currentColumn+1);
    }

}
