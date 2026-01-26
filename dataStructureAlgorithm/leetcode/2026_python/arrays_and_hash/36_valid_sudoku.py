"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.36_valid_sudoku
Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

    Each row must contain the digits 1-9 without repetition.
    Each column must contain the digits 1-9 without repetition.
    Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

Note:

    A Sudoku board (partially filled) could be valid but is not necessarily solvable.
    Only the filled cells need to be validated according to the mentioned rules.
Input: board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true

Example 2:

Input: board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
"""
from collections import defaultdict
from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # 3 validations
        # 1. check row
        # 2. check column
        # 3. check 3x3
        # #1 and #2 can be solved by a set + double for loop
        # #3 we need to use (i/3, j/3) as key and a set as value where we then do a double for loop

        for row in range(9):
            columnSet = set()
            for column in range(9):
                if board[row][column] == '.':
                    # wildcard, skip
                    continue
                elif board[row][column] in columnSet:
                    return False
                else:
                    columnSet.add(board[row][column])
        
        for column in range(9):
            rowSet = set()
            for row in range(9):
                if board[row][column] == '.':
                    # wildcard, skip
                    continue
                elif board[row][column] in rowSet:
                    return False
                else:
                    rowSet.add(board[row][column])

        seenMap = defaultdict(set)

        for row in range(9):
            for column in range(9):
                if board[row][column] == '.':
                    # wildcard, skip
                    continue
                elif board[row][column] in seenMap[(row//3), (column//3)]:
                    return False
                else:
                    seenMap[(row//3), (column//3)].add(board[row][column])
        
        return True
    
    
    def isValidSudokuSingleLoop(self, board: List[List[str]]) -> bool:
        # Can do this in single loop by using 3 maps
        # each map keeping track of one criteria we are checking for
        rowMap = defaultdict(set)
        columnMap = defaultdict(set)
        squareMap = defaultdict(set)
        for row in range(9):
            for column in range(9):
                if board[row][column] == '.':
                    # wildcard, skip
                    continue
                if ( board[row][column] in rowMap[row]
                    or board[row][column] in columnMap[column]
                    or board[row][column] in squareMap[(row//3),(column//3)]
                    ):
                    return False
                else:
                    rowMap[row].add(board[row][column])
                    columnMap[column].add(board[row][column])
                    squareMap[(row//3),(column//3)].add(board[row][column])
        return True