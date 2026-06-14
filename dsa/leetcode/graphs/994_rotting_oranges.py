"""

MEDIUM

You are given an m x n grid where each cell can have one of three values:

    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

 

Example 1:

Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

Example 2:

Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Example 3:

Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 10
    grid[i][j] is 0, 1, or 2.
"""

import collections
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # so this is clearly a bfs problem
        # what happens is when we hit a rotten orange, we perform a bfs on it to mark its neighbors as rotten
        # The above is wrong, we need to do a pre-scan to find all rotten oranges
        # because otherwise we will not be able to scan in real time
        # but one thing we have to keep notice is what if the orange there is already rotten
        # then we need to do a bfs on that so we should have a bfs helper function
        # we also need to check at the end if there are leftovers non-rotten oranges
        # The above here is also wrong, we should instead keep track of a starting count of fresh oranges
        # and decrement every time we mark one as rotten and if the number is not 0 at the end, we return false
        # we don't actually need a visited set like usual since when we rot the oranges, we mark the node as 2
        # which is equivalent of rotten here

        minute = 0

        neighbors = [[1,0], [-1,0], [0,1], [0,-1]]

        rottenQueue = collections.deque()
        freshOrangeCounter = 0

        rows, cols = len(grid), len(grid[0])

        # initial scan for rotten oranges and fresh oranges
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    freshOrangeCounter+=1
                elif grid[row][col] == 2:
                    rottenQueue.append((row,col))

        # now we spread the rot to neighbors
        # we also need to make sure there are fresh oranges to spread to
        while rottenQueue and freshOrangeCounter > 0:
            # we actually need to keep track of how many rotten oranges we have to start
            # this way we accurately depict how much time has passed
            numberOfRottenOranges = len(rottenQueue)
            for _ in range(numberOfRottenOranges):
                currentRow, currentCol = rottenQueue.popleft()
                for rowIncrement, colIncrement in neighbors:
                    # if 0, we don't do anything
                    # if 1, we rotten them by adding them to visited and rottenQueue
                    neighborRow = currentRow + rowIncrement
                    neighborCol = currentCol + colIncrement
                    if neighborRow >= 0 and neighborRow < rows and neighborCol >= 0 and neighborCol < cols and grid[neighborRow][neighborCol] == 1:
                        # change it to rotten
                        grid[neighborRow][neighborCol] = 2
                        # add to queue
                        rottenQueue.append((neighborRow, neighborCol))
                        # decrement fresh counter
                        freshOrangeCounter-=1
                # with this breadth over, we will increment time
            minute+=1

        if freshOrangeCounter > 0: 
            return -1
        else:
            return minute