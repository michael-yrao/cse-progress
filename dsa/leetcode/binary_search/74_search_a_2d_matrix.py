"""
You are given an m x n integer matrix matrix with the following two properties:

    Each row is sorted in non-decreasing order.
    The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Example 2:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 100
    -104 <= matrix[i][j], target <= 104
"""
from typing import List
class Solution:

    # ── Attempt · 2026-07-13 ──────────────
    def searchMatrix_20260713(self, matrix: List[List[int]], target: int) -> bool:
        # we can find in the first column the element that is larger than target
        # that way we know the prior row is the correct row
        # then we do basic exact value binary search to get the result
        # so max boundary binary search -> exact value binary search

        l = 0
        r = len(matrix) - 1

        while l < r:
            m = (l + r + 1) // 2
            if matrix[m][0] > target:
                r = m - 1
            else:
                l = m
        
        # now l is the row
        row = l
        l = 0
        r = len(matrix[0]) - 1

        while l <= r:
            m = (l+r)//2
            if matrix[row][m] == target:
                return True
            if matrix[row][m] > target:
                r = m - 1
            else:
                l = m + 1
        return False

    # region ⚠ PRIOR ATTEMPTS — SPOILERS · fold before you start
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # we can actually just do this one dimension at a time
        # if we go down the matrix
        # we can easily tell which row should be at
        # then we do the same thing in the row
        # so binary search the column, then binary search the row
        # matrix[i][0] gets us the first element of each row
        # we want to find i where matrix[i][0] < target and matrix[i+1][0] > target
        # after which, we just want to do a normal binary search on the row

        rowCount = len(matrix)
        l, r = 0, rowCount - 1

        # we are doing a range, so not exactly sure what we are looking for
        # thus we will use l < r
        while l < r:
            # since we are looking for the maximum row, we want to bias towards right
            mid = (l + r + 1) // 2
            if matrix[mid][0] > target:
                r = mid - 1
            else:
                l = mid

        # now we have l at the row we need

        resultRow = l

        columnCount = len(matrix[0])

        l, r = 0, columnCount - 1

        while l <= r:
            mid = (l + r) // 2
            if matrix[resultRow][mid] == target:
                return True
            if matrix[resultRow][mid] > target:
                r = mid - 1
            else:
                l = mid + 1
        return False
    
    def searchMatrix_20260703(self, matrix: List[List[int]], target: int) -> bool:
        # we are looking for the maximum row this number could be in
        # so we can just look at the first column
        # we find the largest row such that the number is still smaller than target
        # then we binary search on the columns

        rows, cols = len(matrix), len(matrix[0])

        l,r=0,rows-1

        while l < r:
            m = (l+r+1)//2
            # cannot be the solution, thus we set it to l = m
            if matrix[m][0] > target:
                r = m - 1
            else:
                l = m
        
        # now l is the row so we look through the columns

        row = l

        l, r = 0, cols - 1

        while l <= r:
            m = (l+r)//2
            if matrix[row][m] == target:
                return True
            if matrix[row][m] > target:
                r = m - 1
            else:
                l = m + 1
        return False
# endregion
