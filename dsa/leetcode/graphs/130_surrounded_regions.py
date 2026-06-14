"""
You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:

    Connect: A cell is connected to adjacent cells horizontally or vertically.
    Region: To form a region connect every 'O' cell.
    Surround: A region is surrounded if none of the 'O' cells in that region are on the edge of the board. Such regions are completely enclosed by 'X' cells.

To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.

Example 1:

Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

Explanation:

In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.

Example 2:

Input: board = [["X"]]

Output: [["X"]]

Constraints:

    m == board.length
    n == board[i].length
    1 <= m, n <= 200
    board[i][j] is 'X' or 'O'.
"""
import collections
from typing import List

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # so the idea is that if an O is connected to the edge
        # any of its neighbors with an O is considered safe
        # so it is the same idea as pacific/atlantic water flow
        # we want to start at the 4 sides
        # do BFS and mark those nodes as safe
        # so let's get all the Os on the edges and put them into a queue

        rows, cols = len(board), len(board[0])

        safeQueue = collections.deque()

        # left and right side
        for row in range(rows):
            # if O, add to safeQueue
            if board[row][0] == 'O':
                safeQueue.append((row,0))
            if board[row][cols-1] == 'O':
                safeQueue.append((row,cols-1))

        # top and bottom
        for col in range(cols):
            # if O, add to safeQueue
            if board[0][col] == 'O':
                safeQueue.append((0,col))
            if board[rows-1][col] == 'O':
                safeQueue.append((rows-1,col))

        # now that we have our safe nodes to start
        # we want to BFS and mark them as 'Safe'
        # then anything not marked after that, we'll just change to 'X'

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        while safeQueue:
            currentRow, currentCol = safeQueue.popleft()
            # we'll set it to S temporarily to mark as visited and safe
            board[currentRow][currentCol] = 'S'

            # now we check the neighbors of this node
            for neighbor in neighbors:
                rowInc = neighbor[0]
                colInc = neighbor[1]
                neighborRow = currentRow + rowInc
                neighborCol = currentCol + colInc
                # if not out of bound and value is O, add to queue
                if neighborRow >= 0 and neighborRow < rows and neighborCol >= 0 and neighborCol < cols and board[neighborRow][neighborCol] == 'O':
                    safeQueue.append((neighborRow,neighborCol))
        
        # now that we marked all safe nodes as safe
        # we want to go through the board once again and put all Os to Xs and then S to Os

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == 'O':
                    board[row][col] = 'X'
                elif board[row][col] == 'S':
                    board[row][col] = 'O'
        