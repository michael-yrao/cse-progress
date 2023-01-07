from typing import List

class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        # [17,18,5,4,6,1]
        # [18,6,6,6,6,-1] <- construct this array from right side
        # curMax = -1
        
        rightList = [-1] * len(arr)
        rightMax = -1

        # range(start,stop,step)
        for index in range(len(arr) - 1, -1, -1):
            currentMax = max(rightMax,arr[index])
            rightList[index] = rightMax
            rightMax = currentMax
        
        return rightList

    def replaceElementsSingleArray(self, arr: List[int]) -> List[int]:
        # [17,18,5,4,6,1]
        # [18,6,6,6,6,-1] <- construct this array from right side
        # curMax = -1
        
        rightMax = -1

        # range(start,stop,step)
        for index in range(len(arr) - 1, -1, -1):
            currentMax = max(rightMax,arr[index])
            arr[index] = rightMax
            rightMax = currentMax
        
        return arr