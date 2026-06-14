package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.LinkedList;
import java.util.Queue;

public class FloodFill_733_E_GRAPH
{
    /*
    * https://leetcode.com/problems/flood-fill/
    * */

    public int[][] floodFill(int[][] image, int sr, int sc, int color)
    {
        /*
        * Essentially what we are asked to do here is a BFS starting from image[sr][sc]
        *
        * What I personally like to do when it comes to these is actually use Pair to store the x and y coordinates
        * Thus we will BFS that way
        * */

        if(image[sr][sc]==color) return image;

        int maxRow = image.length;
        int maxColumn = image[0].length;

        Pair<Integer,Integer> startingVertex = new Pair<>(sr,sc);
        int sourceColor = image[startingVertex.x][startingVertex.y];

        Queue<Pair<Integer,Integer>> queue = new LinkedList<>();

        queue.add(startingVertex);

        while(!queue.isEmpty())
        {
            int level = queue.size();
            for(int i=0;i<level;i++)
            {
                Pair<Integer,Integer> currentVertex = queue.poll();
                image[currentVertex.x][currentVertex.y] = color;
                color(image,currentVertex.x-1, currentVertex.y,sourceColor,queue,maxRow,maxColumn);
                color(image,currentVertex.x+1, currentVertex.y,sourceColor,queue,maxRow,maxColumn);
                color(image,currentVertex.x, currentVertex.y-1,sourceColor,queue,maxRow,maxColumn);
                color(image,currentVertex.x, currentVertex.y+1,sourceColor,queue,maxRow,maxColumn);
            }
        }
        return image;
    }

    private void color(int[][] image, int row, int column, int sourceColor, Queue<Pair<Integer,Integer>> queue, int maxRow, int maxColumn)
    {
        if(row<0 || column<0 || row>=maxRow || column>=maxColumn) return;
        if(image[row][column] != sourceColor) return;
        queue.offer(new Pair(row,column));
    }
}
