"""
Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

 

Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 300
    grid[i][j] is '0' or '1'.
"""

import collections
from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # so this is clearly a bfs question
        # So how do we determine we have an island
        # And how do we know when to continue looking
        # how do know the 1s are part of the same island
        
        if not grid:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        islandCount = 0

        def bfs(row,col):
            queue = collections.deque()
            currentCoordinate = (row,col)
            visited.add(currentCoordinate)
            queue.append(currentCoordinate)

            while queue:
                r, c = queue.popleft()
                # check the 4 neighbors of this coordinate
                # east, west, north, south
                directions = [[1,0], [-1,0], [0,1], [0,-1]]

                for dr, dc in directions:
                    # if neighbor is a valid unvisited land
                    # mark it as visited
                    neighourCoordinate = (r+dr, c+dc)
                    if (r + dr in range(rows) 
                        and c + dc in range(cols)
                        and grid[r+dr][c+dc] == '1'
                        and neighourCoordinate not in visited):
                        queue.append(neighourCoordinate)
                        visited.add(neighourCoordinate) 

        for r in range(rows):
            for c in range(cols):
                # when we see an unvisited island
                # we perform bfs on it to mark all land connected to it 
                if grid[r][c] == '1' and (r,c) not in visited:
                    bfs(r,c)
                    islandCount+=1

        return islandCount