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
import math
from typing import List, Optional


class Solution:
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