"""
787. Cheapest Flights Within K Stops   ·   https://leetcode.com/problems/cheapest-flights-within-k-stops/
Pattern: graphs

There are n cities connected by some number of flights. You are given an array
`flights` where flights[i] = [from_i, to_i, price_i] indicates that there is a
flight from city from_i to city to_i with cost price_i.

You are also given three integers src, dst, and k. Return the cheapest price
from src to dst with at most k stops. If there is no such route, return -1.

Example:
  n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
  src = 0, dst = 3, k = 1  ->  700
  (0 -> 1 -> 3 costs 700; 0 -> 1 -> 2 -> 3 costs 400 but uses 2 stops)

Constraints:
  1 <= n <= 100
  0 <= flights.length <= (n * (n - 1) / 2)
  flights[i].length == 3
  0 <= from_i, to_i < n,  from_i != to_i
  1 <= price_i <= 10^4
  There will not be any multiple flights between two cities.
  0 <= src, dst, k < n
  src != dst
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-07-16 ──────────────
    def findCheapestPrice_20260716(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # we can initialize an array of max price and set src to 0
        prices = [math.inf] * n
        prices[src] = 0

        # cool thing about bellman ford is that we don't need adjacency map, we just use flights
        # we want to lockdown prices as our prices from the prior iteration since we are limited to number of stops
        # k stops means we can have k + 1 edges, so that is our main constraint

        stopCounter = 0

        while stopCounter < k + 1: 
            # we will perform all modification on unsettledPrices
            # we can do one stop only here
            unsettledPrices = prices.copy()
            for source, destination, price in flights:
                # if source is infinite, just skip this
                if prices[source] == math.inf:
                    continue
                # now check if we can do better than our prior iteration
                if prices[source] + price < unsettledPrices[destination]:
                    unsettledPrices[destination] = prices[source] + price
                # if not, we just continue to the next
            stopCounter+=1
            prices = unsettledPrices
        
        if prices[dst] == math.inf:
            return -1
        return prices[dst] # type: ignore

    # ── Attempt 1 · 2026-07-14 ────────────────────────────────────────────
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # weighted directed graph
        # so like any other graph problem, we create an adj map which keeps track of immediate neighbors only
        # we also need a visited set
        # we can initialize an array of size n with all nodes with math.inf except src
        # so with the adjMap, we can check if distance[target] > distance[source] + price, if it is set distance[target] to distance[source] + price

        prices = [math.inf] * n
        prices[src] = 0

        # we are limiting at k + 1 edges, so we will do k + 1 traversals only
        for _ in range(k+1):
            unsettledPrices = prices.copy()
            for source, target, price in flights:
                # if source is not reachable, continue. not necessary but saves us useless operations
                # since math.inf + anything = math.inf
                if prices[source] == math.inf:
                    continue
                # prices[source] = price as of last round
                # if we use unsettledPrices[source], it means current round's prices, which would introduce chaining and more than k + 1 edges
                if unsettledPrices[target] > prices[source] + price:
                    unsettledPrices[target] = prices[source] + price
            prices = unsettledPrices
        
        if prices[dst] == math.inf:
            return -1
        return prices[dst]   # type: ignore
