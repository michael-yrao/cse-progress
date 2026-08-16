"""
1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance   ·   https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/
Pattern: graphs

There are `n` cities numbered from `0` to `n - 1`. You are given an array `edges` where
`edges[i] = [from_i, to_i, weight_i]` represents a **bidirectional and weighted** edge between
cities `from_i` and `to_i`, and given the integer `distanceThreshold`.

Return the city with the **smallest number** of cities that are reachable through some path and
whose distance is **at most** `distanceThreshold`. If there are multiple such cities, return the
city with the **greatest** number.

Notice that the distance of a path connecting cities `i` and `j` is equal to the sum of the edges'
weights along that path.

Example 1:
    Input:  n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
    Output: 3
    Explanation: The neighboring cities at a distanceThreshold = 4 for each city are:
        City 0 -> [City 1, City 2]
        City 1 -> [City 0, City 2, City 3]
        City 2 -> [City 0, City 1, City 3]
        City 3 -> [City 1, City 2]
    Cities 0 and 3 have 2 neighboring cities at a distanceThreshold = 4, but we have to
    return city 3 since it has the greatest number.

Example 2:
    Input:  n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
    Output: 0
    Explanation: The neighboring cities at a distanceThreshold = 2 for each city are:
        City 0 -> [City 1]
        City 1 -> [City 0, City 4]
        City 2 -> [City 3, City 4]
        City 3 -> [City 2, City 4]
        City 4 -> [City 1, City 2, City 3]

Constraints:
    2 <= n <= 100
    1 <= edges.length <= n * (n - 1) / 2
    edges[i].length == 3
    0 <= from_i < to_i < n
    1 <= weight_i, distanceThreshold <= 10^4
    All pairs (from_i, to_i) are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-15 ──────────────
    def findTheCity_20260815(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # smallest number of cities and distanceThreshold tells me we should use shortest path
        # we can have at max 100 nodes for n so this opens up the O(n^3) algorithm of Floyd Warshall
        # Floyd Warshall says to get from A to B, can we go through C to get to B faster
        
        # we need to have a 2D distance array that tells us from A to B, this is the shortest path so far
        distances = []
        # initialize the distance to infinity
        for i in range(n):
            distances.append([math.inf] * n)
            distances[i][i] = 0
        
        # set the distance based on edges
        for n1, n2, weight in edges:
            distances[n1][n2] = weight
            distances[n2][n1] = weight
        
        for middle in range(n):
            for source in range(n):
                for destination in range(n):
                    # get source to middle distance
                    sourceToMiddle = distances[source][middle]
                    middleToDestination = distances[middle][destination]
                    # compare if source -> middle + middle -> dst < source - > dst
                    if sourceToMiddle + middleToDestination < distances[source][destination]:
                        distances[source][destination] = sourceToMiddle + middleToDestination
        
        minCity = -1
        minCityCounter = math.inf
        for i in range(n):
            currentCityCounter = 0
            for j in range(n):
                # count how many cities we've reached with distanceThreshold
                if distances[i][j] <= distanceThreshold:
                    currentCityCounter+=1
            if currentCityCounter <= minCityCounter:
                minCityCounter = currentCityCounter
                minCity = i
        
        return minCity

    # ── Attempt · 2026-08-05 ──────────────
    def findTheCity_20260805(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # from all cities, we want the one with the smallest amount of connections under the distance threshold
        # we also want the highest numbered node that fits that criteria
        # we need to know what every single node can reach within distanceThreshold
        # Since we need to look at all pairs of nodes, this is Floyd Warshall algorithm
        # the premise of Floyd Warshall is that given i -> j takes x, can we get there faster via a midpoint
        # for Floyd Warshall, we create a 2D array of distances, so distance[i][j] tells me shortest path from i to j

        distance = []

        for _ in range(n):
            row = [math.inf] * n
            distance.append(row)

        # populate this distance map with the edges provided

        for n1, n2, weight in edges:
            distance[n1][n2] = weight
            distance[n2][n1] = weight
        
        # set distance to self to 0

        for i in range(n):
            for j in range(n):
                if i == j:
                    distance[i][j] = 0

        # now we go through the premise of the problem

        for midway in range(n):
            for src in range(n):
                for dst in range(n):
                    if distance[src][midway] + distance[midway][dst] < distance[src][dst]:
                        distance[src][dst] = distance[src][midway] + distance[midway][dst]
        
        # now that we relaxed all the nodes, go through each row and grab smallest count under distanceThreshold

        minCounter = math.inf
        minCity = -1
        for city in range(n):
            cityCounter = 0
            for neighbor in range(n):
                if distance[city][neighbor] <= distanceThreshold:
                    cityCounter+=1
            if cityCounter <= minCounter:
                minCounter = cityCounter
                minCity = city
        
        return minCity

    # ── Attempt 1 · 2026-07-31 ────────────────────────────────────────────
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # We need to use every node as the source here and then find the smallest number of nodes
        # we can reach with distanceThreshold as total edge length
        # Dijkstra = from one node, distance to everything
        # Floyd Warhsall = from all nodes, distance to everything else

        distance = []

        # start by initializing the distance to all other nodes as infinity
        for _ in range(n):
            row = [math.inf] * n
            distance.append(row)

        # set distance to self as zero
        for i in range(n):
            distance[i][i] = 0

        # set edges currently existing
        for source, destination, weight in edges:
            distance[source][destination] = weight
            distance[destination][source] = weight

        # now we find min between current path from city i to city j vs going through city k
        # 
        for mid in range(n):
            for start in range(n):
                for end in range(n):
                    if distance[start][mid] + distance[mid][end] < distance[start][end]:
                        distance[start][end] = distance[start][mid] + distance[mid][end]

        minPath = math.inf
        minPathCity = -1
        for i in range(n):
            currentPath = 0
            for j in range(n):
                if distance[i][j] <= distanceThreshold:
                    currentPath+=1
            # we want to return the largest number if same, so use <=
            if currentPath <= minPath:
                minPath = currentPath
                minPathCity = i

        return minPathCity
