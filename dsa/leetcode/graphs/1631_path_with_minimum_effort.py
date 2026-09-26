"""
1631. Path With Minimum Effort   ·   https://leetcode.com/problems/path-with-minimum-effort/
Pattern: graphs

You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of
size rows x columns, where heights[row][col] represents the height of cell (row, col).
You are situated in the top-left cell, (0, 0), and you hope to travel to the
bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left,
or right, and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two
consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the
bottom-right cell.

Example 1:
  heights = [[1,2,2],[3,8,2],[5,3,5]]
  ->  2
  The route [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
  This is better than the route [1,2,2,2,5], where the maximum difference is 3.

Example 2:
  heights = [[1,2,3],[3,8,4],[5,3,5]]
  ->  1
  The route [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells,
  which is better than route [1,3,5,3,5].

Example 3:
  heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
  ->  0
  This route does not require any effort.

Constraints:
    rows == heights.length
    columns == heights[i].length
    1 <= rows, columns <= 100
    1 <= heights[i][j] <= 10^6
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import heapq
import math
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-26 ────────────────────────────────────────────
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        # since this is a grid with a maximum of four neighbors per node, this feels like a minHeap based Dijkstra
        # minHeap Dijkstra is similar to a BFS
        # we use minHeap instead of a queue
        # we use a visited set
        # we don't really need adjacency map since it is a grid
        # distance array so we don't need to add every node's weight to the heap
        # we add to visited on pop, not on looking at the neighbors
        # the effort to get to starting point is 0, so we put (0,0,0) in heap to start. (weight, row, col)

        rows, cols = len(heights), len(heights[0])

        distance = []

        for _ in range(rows):
            row = [math.inf] * cols
            distance.append(row)

        distance[0][0] = 0

        minHeap = []
        
        heapq.heappush(minHeap, (0,0,0))

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        # while we are able to travel still, continue travelling
        while minHeap:
            currentEffort, currentRow, currentCol = heapq.heappop(minHeap)
            if currentEffort > distance[currentRow][currentCol]:
                continue
            # go through the neighbors
            for ir, ic in neighbors:
                nr, nc = currentRow + ir, currentCol + ic
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols:
                    effort = abs(heights[nr][nc] - heights[currentRow][currentCol])
                    # keep track of the max effort we needed to get here
                    candidate = max(currentEffort, effort)
                    if candidate < distance[nr][nc]:
                        distance[nr][nc] = candidate
                        heapq.heappush(minHeap, (candidate,nr,nc))

        return distance[rows-1][cols-1]

    # v2 — the original rated attempt (2026-09-26): visited set + running max, pushes single-step costs
    def minimumEffortPathV2(self, heights: List[List[int]]) -> int:
        # since this is a grid with a maximum of four neighbors per node, this feels like a minHeap based Dijkstra
        # minHeap Dijkstra is similar to a BFS
        # we use minHeap instead of a queue
        # we use a visited set
        # we don't really need adjacency map since it is a grid
        # we add to visited on pop, not on looking at the neighbors
        # the effort to get to starting point is 0, so we put (0,0,0) in heap to start. (weight, row, col)

        rows, cols = len(heights), len(heights[0])

        minEffort = -math.inf

        visited = set()

        minHeap = []

        heapq.heappush(minHeap, (0,0,0))

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        # while we are able to travel still, continue travelling
        while minHeap:
            currentEffort, currentRow, currentCol = heapq.heappop(minHeap)
            # don't care for nodes we already visited since minHeap greedily lets us visit lower effort first
            if (currentRow, currentCol) in visited:
                continue
            # add node to visited
            visited.add((currentRow, currentCol))
            # update effort if applicable
            minEffort = max(minEffort, currentEffort)
            # check if we have already visited the end node
            if (rows-1, cols-1) in visited:
                return minEffort # type: ignore
            # go through the neighbors
            for ir, ic in neighbors:
                nr, nc = currentRow + ir, currentCol + ic
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in visited:
                    effort = abs(heights[nr][nc] - heights[currentRow][currentCol])
                    heapq.heappush(minHeap, (effort,nr,nc))

        return minEffort # type: ignore