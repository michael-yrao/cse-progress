"""

MEDIUM

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.

Example 1:

Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
Explanation: The following cells can flow to the Pacific and Atlantic oceans, as shown below:
[0,4]: [0,4] -> Pacific Ocean 
       [0,4] -> Atlantic Ocean
[1,3]: [1,3] -> [0,3] -> Pacific Ocean 
       [1,3] -> [1,4] -> Atlantic Ocean
[1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
       [1,4] -> Atlantic Ocean
[2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
       [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
[3,0]: [3,0] -> Pacific Ocean 
       [3,0] -> [4,0] -> Atlantic Ocean
[3,1]: [3,1] -> [3,0] -> Pacific Ocean 
       [3,1] -> [4,1] -> Atlantic Ocean
[4,0]: [4,0] -> Pacific Ocean 
       [4,0] -> Atlantic Ocean
Note that there are other possible paths for these cells to flow to the Pacific and Atlantic oceans.

Example 2:

Input: heights = [[1]]
Output: [[0,0]]
Explanation: The water can flow from the only cell to the Pacific and Atlantic oceans.

Constraints:

    m == heights.length
    n == heights[r].length
    1 <= m, n <= 200
    0 <= heights[r][c] <= 105
"""

import collections
from typing import List

class Solution:

    # ── Attempt · 2026-07-19 ──────────────
    def pacificAtlantic_20260719(self, heights: List[List[int]]) -> List[List[int]]:
        # we start from all the sides
        # since each side already touches one side of the ocean
        # from there, we can see if other nodes can reach the nodes that are already reach the ocean. BFS using the same logic
        # so two sets. canReachPacific and canReachAtlantic
        # canReachPacific starts with all values in column 0 and row 0
        # canReachAtlantic starts with all values in last column and last row
        
        rows = len(heights)
        cols = len(heights[0])
        canReachPacific = set()
        canReachAtlantic = set()
        pacificQueue = collections.deque()
        atlanticQueue = collections.deque()
        

        for row in range(rows):
            canReachPacific.add((row,0))
            canReachAtlantic.add((row,cols-1))
            pacificQueue.append((row,0))
            atlanticQueue.append((row,cols-1))
        
        for col in range(cols):
            canReachPacific.add((0,col))
            canReachAtlantic.add((rows-1,col))
            pacificQueue.append((0,col))
            atlanticQueue.append((rows-1,col))
        
        # now that we have our starting nodes, we will go through and populate both sets with appropriate nodes that can reach either
        # once we finish that, we just return the nodes that are in both set
        
        while pacificQueue:
            cr, cc = pacificQueue.popleft() 
            neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
            for ir,ic in neighbors:
                nr = cr + ir
                nc = cc + ic
                # if this is a valid node that can reach pacific and we have not visited it yet, add it to the set and the queue
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols and heights[nr][nc] >= heights[cr][cc] and (nr,nc) not in canReachPacific:
                    canReachPacific.add((nr,nc))
                    pacificQueue.append((nr,nc))
        
        while atlanticQueue:
            cr, cc = atlanticQueue.popleft()
            neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
            for ir,ic in neighbors:
                nr = cr + ir
                nc = cc + ic
                # if this is a valid node that can reach pacific and we have not visited it yet, add it to the set and the queue
                if nr >= 0 and nr < rows and nc >= 0 and nc < cols and heights[nr][nc] >= heights[cr][cc] and (nr,nc) not in canReachAtlantic:
                    canReachAtlantic.add((nr,nc))
                    atlanticQueue.append((nr,nc))    
        
        # now that we have both sets populated, take nodes that are in both
        
        result = []
        
        for pr, pc in canReachPacific:
            if (pr,pc) in canReachAtlantic:
                result.append([pr,pc])
        
        return result

    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        # the question is really confusing
        # it is just asking to return a list of cells that can flow to both oceans
        # basically then we are doing DFS on every single cell and seeing if it can reach two of the 4 surfaces
        # preorder DFS as well since we need to make decision on current node
        # what we should do is start from each ocean instead and mark nodes as (canReachPacific, canReachAtlantic)
        # so we have a list of pacific nodes and a list of atlantic nodes
        # DFS on neighbors that are bigger, since we are starting from the end and then mark those nodes with (canReachPacific, canReachAtlantic)
        # we can't use a tuple because tuples are immutable, so we'll just do two sets

        canReachPacific = set()
        canReachAtlantic = set()

        rows = len(heights)
        cols = len(heights[0])

        # remember we are coming from outside
        # so previousHeight should be smaller than height we are going to
        def dfs(row, col, visitedSet, previousHeight):
            # this dfs is responsible for adding node to visited

            # typical base case first of going out of bounds or is already visited
            if (row,col) in visitedSet or row < 0 or row >= rows or col < 0 or col >= cols:
                return

            # if height is smaller than previousHeight, we don't continue as well
            if heights[row][col] < previousHeight:
                return

            # if valid, we will start with adding to visited
            visitedSet.add((row,col))

            # now let's go to the neighbors that have more height
            dfs(row+1, col, visitedSet, heights[row][col])
            dfs(row-1, col, visitedSet, heights[row][col])
            dfs(row, col+1, visitedSet, heights[row][col])
            dfs(row, col-1, visitedSet, heights[row][col])

        for row in range(rows):
            # we actually need to pass the set since we have two sets here
            # we actually also need to pass the previous height otherwise we can't tell if it can flow down or not
            # dfs starting from the left most column, which is pacific
            dfs(row, 0, canReachPacific, heights[row][0])
            # dfs starting from the top row, which is the atlantic
            dfs(row, cols - 1, canReachAtlantic, heights[row][cols-1])
        
        for col in range(cols):
            # first row, which is pacific ocean
            dfs(0, col, canReachPacific, heights[0][col])
            # last row, which is the atlantic ocean
            dfs(rows - 1, col, canReachAtlantic, heights[rows-1][col])
        
        result = []

        # now we go through and get everything that is in both sets
        for row in range(rows):
            for col in range(cols):
                if (row,col) in canReachAtlantic and (row,col) in canReachPacific:
                    result.append([row,col])
        
        return result


    def pacificAtlantic_20260611(self, heights: List[List[int]]) -> List[List[int]]:
        # so all this question is asking is to return all nodes that can get to both oceans
        # which is just DFS. Thinking normally, higher number is mountains which is normally from the middle
        # however, it's hard to traverse from the middle
        # what we should instead do is traverse from each side since we know each side reaches one of the oceans for sure
        # then whether or not its neighbors are bigger
        # if it is bigger, that means it can also reach this ocean
        # so we should have two sets, one for pacific, one for atlantic

        rows, cols = len(heights), len(heights[0])

        canVisitPacific = set()
        canVisitAtlantic = set()

        def dfs(row, col, visitedSet, priorHeight):
            # base cases
            # - if out of bounds
            # - if already visited
            # - if current height is lower than prior height

            if row < 0 or row >= rows or col < 0 or col >= cols:
                return

            if (row,col) in visitedSet:
                return
            
            if heights[row][col] < priorHeight:
                return
            
            # knowing we have a valid node, we add it to visitedSet saying we can reach such ocean from here
            visitedSet.add((row,col))

            # now we check its neighbors
            dfs(row+1,col,visitedSet,heights[row][col])
            dfs(row-1,col,visitedSet,heights[row][col])
            dfs(row,col+1,visitedSet,heights[row][col])
            dfs(row,col-1,visitedSet,heights[row][col])

        for row in range(rows):
            # first column, which is pacific
            dfs(row, 0, canVisitPacific, heights[row][0])
            # last column, which is atlantic
            dfs(row, cols-1, canVisitAtlantic, heights[row][cols-1])

        for col in range(cols):
            # first row, which is pacific
            dfs(0, col, canVisitPacific,heights[0][col])
            # last row, which is atlantic
            dfs(rows-1, col, canVisitAtlantic,heights[rows-1][col])

        result = []

        for row in range(rows):
            for col in range(cols):
                if (row,col) in canVisitAtlantic and (row,col) in canVisitPacific:
                    result.append([row,col])
        
        return result
