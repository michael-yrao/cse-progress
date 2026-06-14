package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

public class WallsAndGates_286_M_GRAPH
{
    /*
    * https://leetcode.com/problems/walls-and-gates/
    * */

    /*
    * Gate = 0
    * Wall/Obstacle = -1
    * Empty Spot = Integer.MAX_VALUE
    *
    * Fill Empty Spots with distance to closest Gate
    *
    * */

    /*
    * Perform BFS from every gate simultaneously
    * */

    public void wallsAndGates(int[][] rooms)
    {
        Queue<Pair<Integer,Integer>> queue = new LinkedList<>();

        Set<Pair<Integer,Integer>> visited = new HashSet<>();

        int maxRow=rooms.length;
        int maxColumn=rooms[0].length;

        for(int cr=0;cr<maxRow;cr++)
        {
            for(int cc=0;cc<maxColumn;cc++)
            {
                if(rooms[cr][cc] == 0)
                {
                    Pair<Integer,Integer> pair = new Pair(cr,cc);
                    queue.offer(pair);
                    visited.add(pair);
                }
            }
        }

        int distance = 0;
        while(!queue.isEmpty())
        {
            int levelSize = queue.size();
            // We want to update our closest vertices with distance+1
            for(int i=0;i<levelSize;i++)
            {
                Pair<Integer,Integer> gateVertex = queue.poll();

                rooms[gateVertex.x][gateVertex.y] = distance;

                // Visit all 4 neighbors of this gate

                visitNeighbor(gateVertex.x+1,gateVertex.y,maxRow,maxColumn,rooms,queue,visited);
                visitNeighbor(gateVertex.x-1,gateVertex.y,maxRow,maxColumn,rooms,queue,visited);
                visitNeighbor(gateVertex.x,gateVertex.y+1,maxRow,maxColumn,rooms,queue,visited);
                visitNeighbor(gateVertex.x,gateVertex.y-1,maxRow,maxColumn,rooms,queue,visited);
            }

            distance++;
        }
    }

    private void visitNeighbor(int currentRow, int currentColumn, int maxRow, int maxColumn, int[][] rooms,
                               Queue<Pair<Integer,Integer>> queue, Set<Pair<Integer,Integer>> visited)
    {
        Pair<Integer,Integer> vertex = new Pair(currentRow,currentColumn);
        if(currentRow<0 || currentColumn<0 || currentRow>=maxRow || currentColumn>=maxColumn
                || rooms[currentRow][currentColumn] == -1
                || visited.contains(vertex)) return;

        queue.offer(vertex);
        visited.add(vertex);
    }
}
