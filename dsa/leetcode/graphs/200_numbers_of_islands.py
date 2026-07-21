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

    # ── Attempt · 2026-07-20 ──────────────
    def numIslands_20260720(self, grid: List[List[str]]) -> int:
        # DFS solution
        # visited set to keep track of visited land

        rows, cols = len(grid), len(grid[0])

        visited = set()
        numOfIslands = 0

        def dfs(row,col):
            # if out of bound, return 0
            # if not land, return 0
            # if visited, return 0

            if row < 0 or row >= rows or col < 0 or col >= cols:
                return 0
            
            if grid[row][col] != '1':
                return 0
            
            if (row,col) in visited:
                return 0

            # mark as visited if not visited and visit neighbors
            visited.add((row,col))

            dfs(row-1,col)
            dfs(row+1,col)
            dfs(row,col+1)
            dfs(row,col-1)

            return 1

        for row in range(rows):
            for col in range(cols):
                if (row,col) not in visited and grid[row][col] == '1':
                    numOfIslands+=dfs(row,col)
        
        return numOfIslands

    # ── Attempt · 2026-07-18 ──────────────
    def numIslands_20260718(self, grid: List[List[str]]) -> int:
        # BFS method, so we should go through each node and mark them as visited
        # every time we see a land node, we should be hitting new land since BFS would mark everything as visited otherwise

        rows, cols = len(grid), len(grid[0])

        visited = set()

        queue = collections.deque()

        numberOfIslands = 0

        def bfs():            
            while queue:
                currentRow, currentCol = queue.popleft()
                neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
                for ir,ic in neighbors:
                    nr = currentRow + ir
                    nc = currentCol + ic
                    # visit unvisited land neighbors
                    if nr >= 0 and nr < rows and nc >= 0 and nc < cols and grid[nr][nc] == '1' and (nr,nc) not in visited:
                        visited.add((nr,nc))
                        queue.append((nr,nc))
                    

        for row in range(rows):
            for col in range(cols):
                # we found new island, let's mark all of it as visited
                if grid[row][col] == '1' and (row, col) not in visited:
                    numberOfIslands+=1
                    # mark node as visited
                    visited.add((row,col))
                    # mark node to visit
                    queue.append((row,col))
                    # mark all connected nodes as visited
                    bfs()
        
        return numberOfIslands

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


    def numIslandsDFS(self, grid: List[List[str]]) -> int:
        # so we can do DFS as well to traverse the island
        # we will traverse if node is land
        # check all neighbors and mark all land neighbors as visited
        # when we return, we will add 1 to island count

        visited = set()
        result = 0

        rows, cols = len(grid), len(grid[0])

        def dfs(row, col):
            # base case to stop is if we find water
            # if we are out of bounds, return 0
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return 0

            # if we find water, return 0
            if grid[row][col] == '0':
                return 0

            # if we already visited, return 0
            if (row, col) in visited:
                return 0
            
            # mark current node as visited
            visited.add((row, col))
            # now we go as deep as possible in all 4 directions
            dfs(row+1,col)
            dfs(row-1,col)
            dfs(row,col+1)
            dfs(row,col-1)

            return 1

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1' and (row,col) not in visited:
                    result+=dfs(row,col)
        return result

    def numIslands_20260616(self, grid: List[List[str]]) -> int:
        # DFS
        # we need to find the first piece of land
        # DFS on it, mark each node we visit as visited
        # when we get out of the DFS, we know we've marked all parts of this island

        visited = set()

        islandCounter = 0

        rows, cols = len(grid), len(grid[0])

        def dfs(row,col):
            # exit if in bound
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            # exit if visited
            if (row, col) in visited:
                return
            # exit if not land
            if grid[row][col] != '1':
                return 
            
            # knowing this node is valid, mark it as visited
            visited.add((row,col))

            # visit neighbors
            dfs(row+1,col)
            dfs(row-1,col)
            dfs(row,col+1)
            dfs(row,col-1)

        for row in range(rows):
            for col in range(cols):
                # if we haven't visited this node
                # and it is a land, it is an unvisited island
                if (row,col) not in visited and grid[row][col] == '1':
                    islandCounter+=1
                    # dfs to mark all nodes connected to this land as visited
                    dfs(row,col)
        
        return islandCounter
    def numIslands_20260626(self, grid: List[List[str]]) -> int:
        # DFS method
        # we perform DFS whenever we find land
        # when we find land, we mark land as visited and increment # of islands

        numOfIslands = 0
        visited = set()

        rows, cols = len(grid), len(grid[0])

        def dfs(row, col):
            # we return if not land, visited or out of bound
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if (row,col) in visited:
                return
            if grid[row][col] == '1':
                visited.add((row,col))
                dfs(row-1,col)
                dfs(row+1,col)
                dfs(row,col+1)
                dfs(row,col-1)

        for row in range(rows):
            for col in range(cols):
                # found an unvisited land
                if grid[row][col] == '1' and (row, col) not in visited:
                    numOfIslands+=1
                    dfs(row,col)
        
        return numOfIslands
