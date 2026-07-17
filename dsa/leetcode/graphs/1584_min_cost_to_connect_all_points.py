"""
1584. Min Cost to Connect All Points   ·   https://leetcode.com/problems/min-cost-to-connect-all-points/
Pattern: graphs

You are given an array `points` of integer coordinates on a 2D plane, where
points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the Manhattan distance
between them: |xi - xj| + |yi - yj|.

Return the minimum cost to make all points connected. All points are connected if
there is exactly one simple path between any two points.

Example 1:
    Input:  points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20

Example 2:
    Input:  points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Constraints:
    1 <= points.length <= 1000
    -10^6 <= xi, yi <= 10^6
    All pairs (xi, yi) are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import heapq
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-07-16 ────────────────────────────────────────────
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # so we are the ones to draw the edges here
        # from the example, we can see [2,2] connected to two nodes
        # so idea is that we just do this greedily
        # And this is basically building a minimum spanning tree
        # so working off of another greedy algorithm in Dijkstra's
        # we need a minHeap to help us keep track of of shortest path so (distance, node)
        # technically everything can be connected, so maybe no adj map
        # since to construct the adjMap, it would be very costly
        # visited for marking nodes we've visited


        numberOfNodes = len(points)
        totalCost = 0
        visited = set()

        def manhattanDistance(node1, node2):
            return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

        minHeap = []
        
        heapq.heappush(minHeap,(0,0))

        # while we haven't visited everyone yet
        while len(visited) < numberOfNodes:
            cost, node = heapq.heappop(minHeap)
            # if we already visited the node, we can move on
            if node in visited:
                continue
            # otherwise, add cost to total cost
            totalCost+=cost
            visited.add(node)
            for neighbor in range(numberOfNodes):
                if neighbor not in visited:
                    distance = manhattanDistance(points[node], points[neighbor])
                    heapq.heappush(minHeap, (distance, neighbor))
        return totalCost
