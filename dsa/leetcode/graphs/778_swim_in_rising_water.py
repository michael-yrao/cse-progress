"""
778. Swim in Rising Water   ·   https://leetcode.com/problems/swim-in-rising-water/
Pattern: graphs

You are given an n x n integer matrix grid where each grid[i][j] represents the
elevation at that point (i, j).

It starts raining. At time t, the depth of the water everywhere is t. You can swim
from a square to another 4-directionally adjacent square if and only if the elevation
of both squares individually are at most t. You can swim infinite distances in zero
time. Of course, you must stay within the boundaries of the grid during your swim.

Return the least time until you can reach the bottom right square (n - 1, n - 1) if
you start at the top left square (0, 0).

Example 1:
  Input:  grid = [[0,2],[1,3]]
  Output: 3
  Explanation: At time 0 you are at (0,0). You cannot move since the four adjacent
  cells all have higher elevation than t=0. You cannot reach (1,1) until t=3, when the
  path (0,0)->(0,1)->(1,1) (elevations 0,2,3) all have elevation <= 3.

Example 2:
  Input:  grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
  Output: 16

Constraints:
  n == grid.length == grid[i].length
  1 <= n <= 50
  0 <= grid[i][j] < n^2
  Each value grid[i][j] is unique.

"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import heapq
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-02 ──────────────
    def swimInWater_20260802(self, grid: List[List[int]]) -> int:
        # from our starting point, it seems like we go in the direction that has the min
        # but this fails if the min goes to a dead end so we need to add nodes from neighbors
        # into a minHeap, so either Dijkstra or Prims but Prims doesn't have a source/destination
        # so this is a Dijkstra style BFS 
        # the result is also the biggest node traversed along the way instead of summing
        # 

        rows, cols = len(grid), len(grid[0])
        # holds (value, row, col)
        minHeap = []
        # holds nodes we already traversed
        visited = set()
        # need time to count how far we can go
        time = 0

        # add starting node
        heapq.heappush(minHeap, (grid[0][0],0,0))

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        while minHeap:
            # if current time allows us to continue running through the minHeap, we use the node
            while minHeap and time >= minHeap[0][0]:
                currentValue, cr, cc = heapq.heappop(minHeap)
                # add node to visited
                visited.add((cr,cc))
                # add neighbors to minHeap
                for ir, ic in neighbors:
                    nr = cr + ir
                    nc = cc + ic
                    # add neighbors to minHeap
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in visited:
                        # if we are reaching the end on this neighbor
                        # return the max
                        if nr == rows - 1 and nc == cols - 1:
                            return max(time, grid[nr][nc])
                        heapq.heappush(minHeap,(grid[nr][nc],nr,nc))
            time+=1
        
        return 0

    # ── Attempt 1 · 2026-07-23 ────────────────────────────────────────────
    def swimInWater(self, grid: List[List[int]]) -> int:
        # in example 2, we see that we will wait 11 iterations to go to the closest one
        # so that means we want to use a minheap
        # we also need to keep track of depth, which is actually just level in the BFS
        # e.g. if closest to us is bigger than depth, we don't go anywhere
        # but if it is not bigger than us, we go as far as we possibly can
        # minHeap will be our adjacency map since we will add to it as we go
        # we also need a visited set
        rows, cols = len(grid), len(grid[0])
        minHeap = []
        heapq.heappush(minHeap,(grid[0][0],0,0))
        level = 0
        visited = set()
        # we want to traverse until there is no more 
        while minHeap:
            # traverse the nodes we are able to traverse
            while minHeap and minHeap[0][0] <= level:
                currentNode, row, col = heapq.heappop(minHeap)
                visited.add((row,col))
                if (rows-1,cols-1) in visited:
                    return level
                neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
                for ir, ic in neighbors:
                    nr = row + ir
                    nc = col + ic
                    # if we are in bound, add it to the heap
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in visited:
                        heapq.heappush(minHeap,(grid[nr][nc],nr,nc))
            # increment level
            level+=1
        return level

    def swimInWater_v2(self, grid: List[List[int]]) -> int:
        # in example 2, we see that we will wait 11 iterations to go to the closest one
        # so that means we want to use a minheap
        # we also need to keep track of depth, which is actually just level in the BFS
        # e.g. if closest to us is bigger than depth, we don't go anywhere
        # but if it is not bigger than us, we go as far as we possibly can
        # minHeap will be our adjacency map since we will add to it as we go
        # we also need a visited set
        rows, cols = len(grid), len(grid[0])
        minHeap = []
        heapq.heappush(minHeap,(grid[0][0],0,0))
        level = 0
        visited = set()
        visited.add((0,0))
        # we want to traverse until there is no more 
        while minHeap:
            # traverse the nodes we are able to traverse
            while minHeap and minHeap[0][0] <= level:
                currentNode, row, col = heapq.heappop(minHeap)
                if row == rows - 1 and col == cols - 1:
                    return level
                neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
                for ir, ic in neighbors:
                    nr = row + ir
                    nc = col + ic
                    # if we are in bound, add it to the heap
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and (nr,nc) not in visited:
                        heapq.heappush(minHeap,(grid[nr][nc],nr,nc))
                        visited.add((nr,nc))
            # increment level
            level+=1
        return level
