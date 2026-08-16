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
import collections
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-15 ──────────────
    def findCheapestPrice_20260815(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # this is bellman ford since we are looking for the shortest path 
        # and we are limiting number of steps
        # we do not use a visited set as we want to check if we can go faster each time
        # neither do we need an adjacency map here since flights is our adjacency map
        # bellman ford's algorithm, especially if we are limiting steps is that we need a copy
        # of the solution

        # we start with a price array and use a working copy for current step's work
        prices = [math.inf] * n
        # starting point costs nothing
        prices[src] = 0

        # k means number of nodes in between, but we are traversing edges
        # so we need to go to k + 1
        for _ in range(k+1):
            # make copy of current iteration
            workingPrices = prices.copy()
            for source, destination, price in flights:
                # if starting point has not been reached, no point in trying to iterate
                if prices[source] == math.inf:
                    continue
                # otherwise, let's see if we can get to workingPrices[dst] faster
                # we use workingPrices in case there are multiple paths to it this iteration
                if prices[source] + price < workingPrices[destination]:
                    workingPrices[destination] = prices[source] + price
            # update prices to workingPrices
            prices = workingPrices
        if prices[dst] == math.inf:
            return -1
        return prices[dst] # type: ignore

    # ── Attempt · 2026-08-05 ──────────────
    def findCheapestPrice_20260805(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # looking for cheapest within k means we need to limit the amount of iterations
        # which also means we need a working copy and a primary copy of the distance
        # this way, we can make sure we get the cheapest at each iteration
        # this is the premise of Bellman Ford's shortest path algorithm
        # we will create a distance array to indicate distance to all nodes
        # Bellman Ford is not a greedy algorithm, we need to consider all edges and nodes
        # so we do not use a minHeap here and will just use a queue
        # bellman ford's algorithm just relax every node if possible
        
        prices = [math.inf] * n

        # we set the distance at src to zero
        prices[src] = 0

        # k is number of nodes we can go through but we are iteration through edges, so we need to do k + 1
        for _ in range(k+1):
            workingPrices = prices.copy()
            # now for each iteration, let's take a look and see if we can relax the node
            for source, destination, price in flights:
                # if we can't start from source, we just continue
                if prices[source] == math.inf:
                    continue
                # if not, then let's update working copy to lowest price
                # we need to update working prices and check working prices in case multiple routes go to the same destination
                # we use the canonical prices to not do multiple steps in 1 iteration
                if prices[source] + price < workingPrices[destination]:
                    workingPrices[destination] = prices[source] + price
            # now that we relaxed what we could have this iteration, update prices to the working prices
            prices = workingPrices
        
        # now if the distance is still math.inf, we can't reach the destination
        # otherwise, return shortest distance we found

        if prices[dst] == math.inf:
            return -1
        return prices[dst] # type: ignore

    # ── Attempt · 2026-07-26 ──────────────
    def findCheapestPrice_20260726(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # we are trying to travel from src to dst
        # what we can do is use a distance map where we set everyone's distance to infinite
        # except for starting node and update as we go through the graph
        # adjacency map is given to us in flights, so no need to create one
        # we don't need a visited because we can use distance
        # one very important thing to note is that we can only make k stops, so we need to make sure
        # we don't go two cities in one iteration, so this is a BFS with a traversal restriction
        # so keep a global copy and a local copy so we can see where we've travelled so far to prevent multi-traversal
        # we also need to have a counter for k, we will use k to track our level instead of a queue

        distance = [math.inf] * n
        distance[src] = 0
        iteration = 0

        # k = 1 means 1 node in between, that is 2 edges allowed, so k + 1
        while iteration < k + 1:
            workingDistance = distance.copy()
            for source, destination, weight in flights:
                if distance[source] == math.inf:
                    continue
                if distance[source] + weight < workingDistance[destination]:
                    workingDistance[destination] = distance[source] + weight
            distance = workingDistance
            iteration+=1

        if distance[dst] == math.inf:
            return -1
        return distance[dst] # type: ignore

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
