package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class CheapestFlightsWithinKStops_787_M_GRAPH
{
    /*
    * https://leetcode.com/problems/cheapest-flights-within-k-stops/
    * */

    /*
    * Bellman-Ford Algorithm
    * */

    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k)
    {
        // Create an array where the index is the flight vertices
        int[] prices = new int[n];

        // Fill every index with infinity meaning not reachable
        Arrays.fill(prices, Integer.MAX_VALUE);

        // We don't need any money to reach the source vertex, so we can initialize that as zero
        prices[src] = 0;

        // We want to go through the graph k times since k is the number of stops we can make
        for(int i=0;i<=k;i++)
        {
            int[] tempPrices = Arrays.copyOf(prices, prices.length);

            for(int j=0;j<flights.length;j++)
            {
                int sourceVertex = flights[j][0];
                int destinationVertex = flights[j][1];
                int price = flights[j][2];

                // If source vertex is not reachable, we can move on to the next vertex
                if(prices[sourceVertex] == Integer.MAX_VALUE) continue;

                // If source vertex + price is smaller than our current method of getting to destination
                // Update the destination vertex's price
                // Note that we are also updating the temporary price array in case the price gets updated multiple times here
                if(prices[sourceVertex] + price < tempPrices[destinationVertex])
                    tempPrices[destinationVertex] = prices[sourceVertex] + price;
            }
            prices = tempPrices;
        }
        return prices[dst]==Integer.MAX_VALUE?-1:prices[dst];
    }
}
