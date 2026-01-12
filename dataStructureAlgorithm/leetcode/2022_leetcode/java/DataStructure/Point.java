package DataStructure;

import java.util.ArrayList;
import java.util.List;

public class Point
{
    public int x,y;

    public Point(int x, int y)
    {
        this.x = x;
        this.y = y;
    }

    public List<Point> createPointArray(int[][] inputMatrix)
    {
        int row=inputMatrix.length;
        int column=inputMatrix[0].length;

        List<Point> list = new ArrayList<>();

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                list.add(new Point(i,j));
            }
        }
        return list;
    }
}
