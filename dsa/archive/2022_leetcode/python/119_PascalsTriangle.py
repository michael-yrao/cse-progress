from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        # We should assume each level that we are calculating from
        # has a zero at the beginning and a zero at the end,
        # which will make it easy to use a two pointer technique to get the next row

        # We'll start with the first row in our result
        # since input for numRows is between 1 to 30
        result = [[1]]

        # Do 1 less loop since we already created 1 row in our declaration
        for i in range(numRows - 1):
            paddingRow = [0] + result[-1] + [0]
            nextRow = []
            # Build the next row by getting latest row from result but 1 index bigger
            for j in range(len(result[-1]) + 1):
                l,r=j,j+1
                nextRow.append(paddingRow[l] + paddingRow[r])
            result.append(nextRow)
        
        return result