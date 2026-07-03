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
                    
    def solve_20260620(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # so this is pretty much just pacific atlantic water flow
        # we know the land on the edges are safe, so we are going to mark all nodes connected to the lands on the edges as safe
        # then go through and mark all the non-safe lands as water
        # then change the safe land back to land

        rows, cols = len(board), len(board[0])

        safeLand = collections.deque()

        for row in range(rows):
            if board[row][0] == 'O':
                safeLand.append((row,0))
            if board[row][cols-1] == 'O':
                safeLand.append((row,cols-1))
        
        for col in range(cols):
            if board[0][col] == 'O':
                safeLand.append((0,col))
            if board[rows-1][col] == 'O':
                safeLand.append((rows-1,col))

        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]

        # now that we have our starting point, we will do multipoint traversal
        while safeLand:
            safeLandSize = len(safeLand)
            for _ in range(safeLandSize):
                safeRow, safeCol = safeLand.popleft()
                # temporary value as a way for us to say safe and visited
                board[safeRow][safeCol] = 'S'
                for nr, nc in neighbors:
                    neighborRow = safeRow + nr
                    neighborCol = safeCol + nc
                    if neighborRow >= 0 and neighborRow < rows and neighborCol >= 0 and neighborCol < cols and board[neighborRow][neighborCol] == 'O':
                        safeLand.append((neighborRow, neighborCol))
        
        # now that all safe land are marked, we just go through the board, mark everything O to water
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == 'O':
                    board[row][col] = 'X'
                if board[row][col] == 'S':
                    board[row][col] = 'O'
    
    def solve_20260621_UnionFind(self, board: List[List[str]]) -> None:
        # Union Find version of 130
        # so the general idea behind union find method is that we are grouping them into components and any component not connected to the virtual node is gone
        # we want to create an extra node outside to help us mark the edge lands as safe
        # this node will be our base root parent for union find
        # but we are not creating a new node per say, we are creating a virtual node
        # which means it will have a rank and a parent but never exist in the board
        # we also want to flatten the 2D array structure to 1D
        # 2D -> 1D : (row, col) -> row * cols + col (index)
        # 1D -> 2D: row = index // cols, col = index % cols
        # nodes in 1D would go up to rows * cols, excluding rows * cols
        # so we will assign the extra node with rows * cols
        
        rows = len(board)
        cols = len(board[0])
        
        rankMap = {}
        parentMap = {}
        
        # 1D map representation for parent and rank map
        for i in range(rows * cols + 1):
            parentMap[i] = i
            rankMap[i] = 0
            
        
        def findParent(node):
            if node == parentMap[node]:
                return parentMap[node]
            parentMap[node] = findParent(parentMap[node])
            return parentMap[node]
        
        # union two nodes
        def union(node1,node2):
            node1Root = findParent(node1)
            node2Root = findParent(node2)
            if node1Root == node2Root:
                return False
            if rankMap[node1Root] > rankMap[node2Root]:
                parentMap[node2Root] = node1Root
            elif rankMap[node1Root] < rankMap[node2Root]:
                parentMap[node1Root] = node2Root
            else:
                # random assignment
                parentMap[node2Root] = node1Root
                rankMap[node1Root] += 1
            return True
        
        neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
        
        # Connect the nodes that are on the edge
        # to the virtual node
        for row in range(rows):
            for col in range(cols):
                current1DNode = row * cols + col
                virtual1DNode = rows * cols
                if board[row][col] == 'O':
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        union(current1DNode, virtual1DNode)
                    # union the neighbors as well
                    for ir, ic in neighbors:
                        nr, nc = row+ir, col+ic 
                        if nr >= 0 and nr < rows and nc >= 0 and nc < cols and board[nr][nc] == 'O':
                            neighbor1DNode = nr * cols + nc
                            union(current1DNode, neighbor1DNode)
        
        # now that we have unioned all the safe nodes
        # we mark all the Os that have not been saved as water
        for row in range(rows):
            for col in range(cols):
                current1DNode = row * cols + col
                virtual1DNode = rows * cols
                if board[row][col] == 'O' and findParent(current1DNode) != findParent(virtual1DNode):
                    board[row][col] = 'X'
        
    def solve_20260623(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # Union Find method
        # so we can pretend all nodes are its own component at the start
        # we will create a dummy component that will encapsulate all nodes touching the edges
        # we'll do union on the neighbor of those
        # then anything that is not connected to the dummy component is gone
        # the way to do this is to convert the 2D array to a 1D array
        # formula for 2D -> 1D for board[row][col] = row * cols + col
        # going backwards, row = index // cols ; col = index % cols
        # since we have rows * cols - 1 nodes, we can do dummy component at rows * cols

        rows, cols = len(board), len(board[0])

        dummyComponentIndex = rows * cols

        parentMap, rankMap = {}, {}

        # rows * cols + 1 to account for the dummy component
        for i in range(rows * cols + 1):
            parentMap[i] = i
            rankMap[i] = 0
        
        def findParent(node):
            if node == parentMap[node]:
                return parentMap[node]
            parentMap[node] = findParent(parentMap[node])
            return parentMap[node]

        def union(node1, node2):
            node1Root = findParent(node1)
            node2Root = findParent(node2)
            if node1Root == node2Root:
                return False
            if rankMap[node1Root] > rankMap[node2Root]:
                parentMap[node2Root] = node1Root
            elif rankMap[node1Root] < rankMap[node2Root]:
                parentMap[node1Root] = node2Root
            else:
                # equal, pick at random
                parentMap[node2Root] = node1Root
                rankMap[node1Root]+=1
            return True

        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                # union land nodes with its neighbors
                # and union edge nodes with the virtual node
                if board[row][col] == 'O':
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        union(index, dummyComponentIndex)
                    neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
                    for ir, ic in neighbors:
                        nr, nc = row + ir, col + ic
                        if nr >= 0 and nr < rows and nc >= 0 and nc < cols and board[nr][nc] == 'O':
                            neighborIndex = nr * cols + nc
                            union(index, neighborIndex)
        
        # now that all the nodes are connected
        # we change all nodes not connected to edge nodes/virtual nodes to water
        
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                # if index is not connectable to virtual node, mark as water
                if board[row][col] == 'O' and findParent(index) != findParent(dummyComponentIndex):
                    board[row][col] = 'X'
    def solve_20260703(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # Today's goal is to use union find here
        # so we want to use a dummy node outside of the grid
        # and connect all nodes on the border to it
        # since we are having an external node, we need 1D representation of the board
        # formula is row * cols + col to convert from 2D -> 1D
        # this way, our external node will be rows * cols
        rankMap = {}
        parentMap = {}
        rows, cols = len(board), len(board[0])
        for i in range(rows*cols+1):
            rankMap[i]=0
            parentMap[i] = i
        
        def find(node):
            if node == parentMap[node]:
                return parentMap[node]
            parentMap[node] = find(parentMap[node])
            return parentMap[node]
        
        def union(n1,n2):
            n1r = find(n1)
            n2r = find(n2)
            if n1r == n2r:
                return False
            if rankMap[n1r] > rankMap[n2r]:
                parentMap[n2r] = n1r
            elif rankMap[n1r] < rankMap[n2r]:
                parentMap[n1r] = n2r
            else:
                # pick at random
                parentMap[n2r] = n1r
                rankMap[n1r]+=1

        externalNode = rows * cols
        for row in range(rows):
            for col in range(cols):
                # if land, we want to try to connect them with their neighbors
                neighbors = [[1,0],[-1,0],[0,1],[0,-1]]
                if board[row][col] == 'O':
                    node = row * cols + col
                    # we also want to connect edges to the extra node
                    if row == 0 or col == 0 or row == rows - 1 or col == cols - 1:
                        union(node, externalNode)
                    # now we connect with all neighbors
                    for ir,ic in neighbors:
                        nr = row + ir
                        nc = col + ic
                        if nr >= 0 and nr < rows and nc >= 0 and nc < cols and board[nr][nc] == 'O':
                            neighborNode = nr * cols + nc
                            union(node, neighborNode)
        
        # now that everyone is connected
        # let's turn all land that does not have the same parent as external node into water
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == 'O':
                    node = row * cols + col
                    if find(node) != find(externalNode):
                        board[row][col] = 'X'
        