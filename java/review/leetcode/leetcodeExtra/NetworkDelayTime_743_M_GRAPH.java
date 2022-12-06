package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class NetworkDelayTime_743_M_GRAPH
{
    /*
    * https://leetcode.com/problems/network-delay-time/
    * */

    /*
    * First Dijkstra Algorithm problem
    * Things to note for Dijkstra's Algorithm:
    *   1. Greedy Algorithm
    *   2. Perform BFS on Graph using an adjacency map (In this case, we use a Map of Integer -> List of Pair)
    *   3. Insert nodes visited by BFS into Min-Heap sorted by length of the edges (e.g. smallest edge, hence greedy)
    *   4. We also want another Map that holds a mapping of Vertex to Distance,
    *      where Distance = min distance from start vertex k to Vertex
    *
    * */

    /*
    * each int[] in times is given to us as (source vertex, destination vertex, edge value)
    * O(E*logV)
    * */

    public int networkDelayTime(int[][] times, int n, int k)
    {
        // We want a hashmap of Source Node to Destination Node and how much it takes to get there
        // So we need a HashMap of Integer, Pair where Pair will contain Destination Node, Weight
        // This just makes it easier for us to access this information later down the line instead
        Map<Integer, List<Pair<Integer, Integer>>> adjacencyList = new HashMap<>();

        // Get all immediate neighbors of connection[0]
        for(int[] connection : times)
        {
            // Fancy way of adding a new value into a map
            adjacencyList.computeIfAbsent(connection[0], key -> new ArrayList<>()).add(new Pair(connection[1],connection[2]));
        }

        PriorityQueue<Pair<Integer,Integer>> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a.y));

        Map<Integer,Integer> distanceMap = new HashMap<>();

        // Let's put Vertex K into this minHeap since we start there
        // and we know we don't need to spend any time getting there

        minHeap.offer(new Pair(k,0));

        while(!minHeap.isEmpty())
        {
            Pair<Integer,Integer> vertex = minHeap.poll();
            // If we have already visited this node, go to next node instead
            if(distanceMap.containsKey(vertex.x)) continue;
            // Otherwise, add to visited list with the weight
            distanceMap.put(vertex.x, vertex.y);

            // Visit adjacent vertices by performing BFS
            if(adjacencyList.containsKey(vertex.x))
            {
                for(Pair<Integer,Integer> edge : adjacencyList.get(vertex.x))
                {
                    minHeap.offer(new Pair(edge.x, vertex.y + edge.y));
                }
            }
        }
        if(distanceMap.size() != n) return -1;
        int returnValue = Integer.MIN_VALUE;
        for(int vertex : distanceMap.keySet())
        {
            returnValue = Math.max(returnValue, distanceMap.get(vertex));
        }
        return returnValue;
    }
}
