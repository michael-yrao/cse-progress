package review.leetcode.blind75;

public class RotateImage_48_M_GEOMETRY
{
    /*
    * https://leetcode.com/problems/rotate-image/
    * */

    /*
    * Best way to really do this problem is probably using some geometric manipulations
    *   1. Transpose the matrix (e.g. swap row and column)
    *   2. Reverse each row to get our final result
    * */

    public void rotate(int[][] matrix)
    {
        int size = matrix.length;
        transpose(matrix);
        reverse(matrix);
    }

    // transpose means to swap row and column
    // so we'll just do something like matrix[cr][cc] = matrix[cc][cr] while making sure to save the original value

    // [[1,2,3],[4,5,6],[7,8,9]] -> [[1,4,7],[2,5,8],[3,6,9]]
    private void transpose(int[][] matrix)
    {
        for(int cr=0;cr<matrix.length;cr++)
        {
            for(int cc=cr+1;cc<matrix.length;cc++)
            {
                int temp = matrix[cr][cc];
                matrix[cr][cc] = matrix[cc][cr];
                matrix[cc][cr] = temp;
            }
        }
    }

    // Generic reversal for a integer array
    // Swap first and last value and continue until done
    // [[1,4,7],[2,5,8],[3,6,9]] -> [[7,4,1],[8,5,2],[9,6,3]]
    private void reverse(int[][] matrix)
    {
        for(int[] array : matrix)
        {
            int left=0;
            int right=array.length-1;
            while(right>left)
            {
                int temp = array[left];
                array[left] = array[right];
                array[right] = temp;
                left++;
                right--;
            }
        }
    }
}
