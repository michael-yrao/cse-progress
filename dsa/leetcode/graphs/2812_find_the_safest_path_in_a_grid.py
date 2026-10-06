"""
2812. Find the Safest Path in a Grid   ·   https://leetcode.com/problems/find-the-safest-path-in-a-grid/
Pattern: graphs

You are given a 0-indexed 2D matrix grid of size n x n, where (r, c) represents:
  - A cell containing a thief if grid[r][c] = 1
  - An empty cell if grid[r][c] = 0

You are initially positioned at cell (0, 0). In one move, you can move to any adjacent
cell in the grid, including cells containing thieves.

The safeness factor of a path on the grid is defined as the minimum manhattan distance
from any cell in the path to any thief in the grid.

Return the maximum safeness factor of all paths leading to cell (n - 1, n - 1).

An adjacent cell of cell (r, c) is one of (r, c + 1), (r, c - 1), (r + 1, c), (r - 1, c)
if it exists. Manhattan distance between (a, b) and (x, y) is |a - x| + |b - y|.

Example 1: grid = [[1,0,0],[0,0,0],[0,0,1]]                  -> 0
  All paths from (0, 0) to (n - 1, n - 1) go through the thieves at (0, 0) and (n - 1, n - 1).
Example 2: grid = [[0,0,1],[0,0,0],[0,0,0]]                  -> 2
  Closest path cell to the thief at (0, 2) is (0, 0): |0 - 0| + |0 - 2| = 2.
Example 3: grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]  -> 2
  Thief (0, 3) is closest to path cell (1, 2): distance 2.
  Thief (3, 0) is closest to path cell (3, 2): distance 2.

Constraints:
  1 <= grid.length == n <= 400
  grid[i].length == n
  grid[i][j] is either 0 or 1.
  There is at least one thief in the grid.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
import heapq
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-05 ──────────────
    def maximumSafenessFactor_20261005(self, grid: List[List[int]]) -> int:
        # shallow dijkstra with rows/cols being 400 max each side and 4 neighbors each node
        # what we do here is to maximize distance from thieves at each point
        # so what we can do is initialize a 2D grid stating closest each node to a thief
        # then use this as our validation to go or not go to this node via minHeap
        # for dijkstra's, since we are already in a 2D grid, we can do 2D distance and visited grid as well to help with the minHeap

        rows, cols = len(grid), len(grid[0])

        closest_thief = []

        distance = []

        visited = []

        for i in range(rows):
            distance_row = [-1] * cols
            visited_row = [False] * cols
            thief_row = [math.inf] * cols 
            distance.append(distance_row)
            visited.append(visited_row)
            closest_thief.append(thief_row)

        # now let's populate the closest thief for all nodes
        # we can actually do this with multi-source BFS
        thief_visited = set()
        thief_queue = collections.deque()
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    thief_queue.append((row,col))
                    closest_thief[row][col] = 0
                    thief_visited.add((row,col))
        
        # now we do BFS, set row,col's value to its source + 1

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        while thief_queue:
            lenQueue = len(thief_queue)
            for _ in range(lenQueue):
                cr, cc = thief_queue.popleft()
                for ir, ic in neighbors:
                    nr, nc = cr + ir, cc + ic
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in thief_visited:
                        closest_thief[nr][nc] = 1 + closest_thief[cr][cc]
                        thief_queue.append((nr,nc))
                        thief_visited.add((nr,nc))
        
        # now with the thief distance set, let's start our dijkstra
        # we are trying to maximize our distance from thieves, so we should be doing a max heap
        max_heap = []

        heapq.heappush(max_heap, (-closest_thief[0][0], 0, 0))

        # update distance of [0][0], this will never change
        distance[0][0] = closest_thief[0][0]

        while max_heap:
            current_max_distance, current_row, current_col = heapq.heappop(max_heap)
            # if already visited, continue
            if visited[current_row][current_col]:
                continue
            # otherwise, changed to visited
            visited[current_row][current_col] = True
            # now check neighbors
            for ir, ic in neighbors:
                nr, nc = current_row + ir, current_col + ic
                # if this grid is valid and we have not visited
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols and not visited[nr][nc]:
                    new_min = min(-current_max_distance, closest_thief[nr][nc])
                    # if new min does not help, skip it
                    if new_min <= distance[nr][nc]:
                        continue
                    distance[nr][nc] = new_min
                    heapq.heappush(max_heap, (-distance[nr][nc], nr, nc))
        
        return distance[rows-1][cols-1]

    # ── Attempt 1 · 2026-09-27 ────────────────────────────────────────────
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        # so we want to find a path from 0,0 to rows-1,cols-1 and maximize the distance to a cell with 1
        # this is clearly dijkstra's and being a grid means we only have four neighbors each node so shallow graph so min heap method will dominate here but let's see the thought process first before moving that direction
        # what we need to do is have a set of thieves and we need to relax a node against that set of thieves each time
        # when we say relax though, it is slightly different, we are picking the higher values so maxHeap dominate if we use heap method
        # so that means we start all nodes with -math.inf so that we can pick the furthest from all thieves
        # relax at each step, but relaxing at each step is really expensive
        # we can actually just find the distance to all thieves at the start for all nodes

        rows, cols = len(grid), len(grid[0])

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        distance = []

        for row in range(rows):
            new_row = [math.inf] * cols
            distance.append(new_row)

        # get our thief nodes

        thief_visited = set()
        thief_queue = collections.deque()

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    thief_visited.add((row,col))
                    distance[row][col] = 0
                    thief_queue.append((row,col))
        
        # let's calc every single node's distance to a thief node
        # instead of going nodes to thief, we do multi source BFS
        # we can then spread manhattan distance by just adding 1 each time

        while thief_queue:
            lenQueue = len(thief_queue)
            for _ in range(lenQueue):
                current_row, current_col = thief_queue.popleft()
                for ir, ic in neighbors:
                    nr, nc = current_row + ir, current_col + ic
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in thief_visited:
                        # we take the closest so min here
                        distance[nr][nc] = distance[current_row][current_col] + 1
                        # mark as visited
                        thief_visited.add((nr,nc))
                        # add to the queue
                        thief_queue.append((nr,nc))

        # now we start at 0,0 and try to maximize our distance from a thief
        # we also need a visited array to help us make sure we don't overwrite our already solidified value

        visited = []

        for _ in range(rows):
            new_row = [False] * cols
            visited.append(new_row)

        max_heap = []
        
        heapq.heappush(max_heap, (-distance[0][0], 0, 0))

        while max_heap:
            current_distance, current_row, current_col = heapq.heappop(max_heap)
            # multiply by -1 to get actual max
            current_distance = current_distance * -1
            # if we have been here already, we can just continue
            if visited[current_row][current_col]:
                continue
            visited[current_row][current_col] = True

            for ir, ic in neighbors:
                nr, nc = current_row + ir, current_col + ic
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols and not visited[nr][nc]:
                    # to get to nr, nc, we needed to go through current_row
                    # so we set to min of these two
                    distance[nr][nc] = min(current_distance, distance[nr][nc])
                    # now we add it to the heap
                    heapq.heappush(max_heap, (distance[nr][nc] * -1, nr, nc))
        
        return distance[rows-1][cols-1]
