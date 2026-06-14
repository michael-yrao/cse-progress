package review.learning.DynamicProgramming.Tabulation;

public class GridTraveler
{
    /*
    * Table iteration is O(xy)
    * Time: O(xy)
    * Space: O(xy)
    * */

    public long gridTraveler(int x, int y)
    {
        long[][] table = new long[x+1][y+1];

        table[0][0] = 0;
        table[1][1] = 1;

        for(int i=0;i<=x;i++)
        {
            for(int j=0;j<=y;j++)
            {
                long currentElement = table[i][j];
                if(i<x) table[i+1][j] += currentElement;
                if(j<y) table[i][j+1] += currentElement;
            }
        }
        return table[x][y];
    }
}
