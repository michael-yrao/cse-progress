"""

MEDIUM

You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.

 

Example 1:

Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: The answer is not 11, because the island must be connected 4-directionally.

Example 2:

Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0

 

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 50
    grid[i][j] is either 0 or 1.
"""

from typing import List

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # ok so this is pretty much identical to number of islands
        # but difference is that we need to keep track of how many nodes are part of the island
        # so let's try for a DFS approach first
        # What DFS/BFS means is that it will look at every node in this current island
        # thus what we should be returning from DFS is +1 from each traversal if it hits
        # we need a visited 

        visited = set()
        maxArea = 0

        rows, cols = len(grid), len(grid[0])

        def dfs(row,col):
            # base cases
            
            # if out of bound, 0
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return 0
        
            # if water, 0
            if grid[row][col] == 0:
                return 0

            # if visited, 0
            if (row,col) in visited:
                return 0
            
            # if not, then new node
            # we add it to visited and increment size of our current island
            visited.add((row,col))
            return 1+dfs(row+1,col)+dfs(row-1,col)+dfs(row,col+1)+dfs(row,col-1)

        for row in range(rows):
            for col in range(cols):
                # if we found land, we will get its size and compare to maxArea
                if grid[row][col] == 1 and (row,col) not in visited:
                    maxArea = max(maxArea, dfs(row,col))
        
        return maxArea