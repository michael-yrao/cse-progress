package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class EvaluationDivision_399_M_GRAPH
{
    /*
    * https://leetcode.com/problems/evaluate-division/
    * */

    /*
    * Input: equations = [["a","b"],["b","c"]]
    *        values    = [2.0,3.0]
    *        queries   = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
    *
    * Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
    *
    * Explanation: a/b = 2, b/c = 3 and we want to find the results of all equations in queries
    *
    * One way to think about this is left side of division is starting node and right side is ending node
    * a -> b = 2,   b -> c = 3
    * b -> a = 1/2, c -> b = 1/3
    *
    * Queries is given to us the same way as equation, so we just need to travel down our graph to get to the solution
    *
    * Two ways to solve this problem:
    *   1. DFS/Backtracking
    *       a. Using same logic as below, create an adjacency list of all the nodes
    *       b. We will map them as Node -> Node, Distance
    *   2. Union Find
    * */

    public double[] calcEquationDFS(List<List<String>> equations, double[] values, List<List<String>> queries)
    {
        Map<String, Map<String,Double>> adjacencyList = new HashMap<>();
        for(int i=0;i<values.length;i++)
        {
            // Put both sides of the division into the Hashmap
            adjacencyList.putIfAbsent(equations.get(i).get(0), new HashMap<>());
            adjacencyList.putIfAbsent(equations.get(i).get(1), new HashMap<>());
            // Populate their distance to each other based on values
            adjacencyList.get(equations.get(i).get(0)).put(equations.get(i).get(1), values[i]);
            adjacencyList.get(equations.get(i).get(1)).put(equations.get(i).get(0), 1 / values[i]);
        }

        double[] queryResults = new double[queries.size()];

        // DFS through our adjacency list to get to result
        for(int i=0;i<queryResults.length;i++)
        {
            queryResults[i] = backtrack(queries.get(i).get(0), queries.get(i).get(1), 1, adjacencyList, new HashSet<>());
        }
        return queryResults;
    }

    // "a" - > "c"
    private double backtrack(String leftDivision, String rightDivision, double result, Map<String, Map<String,Double>> adjacencyList, Set<String> visited)
    {
        if(!adjacencyList.containsKey(leftDivision) || visited.contains(leftDivision)) return -1;
        if(leftDivision.equals(rightDivision)) return result;

        // Mark current node as seen
        visited.add(leftDivision);

        // Get neighbors of leftDivision
        // e.g. in our example of a -> c, we will get b in this list
        Map<String,Double> neighbors = adjacencyList.get(leftDivision);
        // For each neighbor in between leftDivision and rightDivision, we want to multiply by the distance
        for(String neighbor : neighbors.keySet())
        {
            double distance = backtrack(neighbor,rightDivision, result * neighbors.get(neighbor), adjacencyList, visited);
            if(distance != -1) return distance;
        }

        visited.remove(leftDivision);
        return -1;
    }
}
