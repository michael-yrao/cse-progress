package review.leetcode.leetcodeExtra;

public class SetMatrixZeroes_73_M_GRAPH
{
    /*
    * https://leetcode.com/problems/set-matrix-zeroes/
    * */

    /*
    * Since it is possible we need to set the entire grid to zero, the best time complexity is O(m*n) regardless
    * Notice that we cannot just run DFS since if we do that, we will pretty much set the entire grid to 0
    * What we can do is:
    *   #1 create a copy of the matrix
    *   #2 create an array for column replacement and another for row replacement
    *
    * There is also a way to do this with O(1) space but 2 arrays make the most sense to me
    *
    * */

    /*
    * O(m*n) time
    * O(m+n) space
    * */

    public void setZeroes(int[][] matrix)
    {
        int maxRow = matrix.length;
        int maxColumn = matrix[0].length;

        // For row replacement, we are saying we want to go through each row
        // And mark all the rows that need to be replaced
        // Similarly for the column replacement
        boolean[] rowReplacement = new boolean[maxRow];
        boolean[] columnReplacement = new boolean[maxColumn];

        // Mark the rows and columns that need to be marked as zeroes

        for(int currentRow=0;currentRow<maxRow;currentRow++)
        {
            for(int currentColumn=0;currentColumn<maxColumn;currentColumn++)
            {
                if(matrix[currentRow][currentColumn] == 0)
                {
                    rowReplacement[currentRow] = true;
                    columnReplacement[currentColumn] = true;
                }
            }
        }

        // Make the changes on row replacements

        for(int currentRow=0;currentRow<maxRow;currentRow++)
        {
            for(int currentColumn=0;currentColumn<maxColumn;currentColumn++)
            {
                if(rowReplacement[currentRow]) matrix[currentRow][currentColumn] = 0;
            }
        }

        // Make the changes on column replacements

        for(int currentColumn=0;currentColumn<maxColumn;currentColumn++)
        {
            for(int currentRow=0;currentRow<maxRow;currentRow++)
            {
                if(columnReplacement[currentColumn]) matrix[currentRow][currentColumn] = 0;
            }
        }
    }
}
