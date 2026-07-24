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
from typing import List, Optional


class Solution:
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