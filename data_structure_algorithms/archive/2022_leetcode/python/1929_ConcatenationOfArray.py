from typing import List

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        numLength = len(nums)
        arr = [0] * (numLength * 2)

        for i in range(len(arr)):
            arr[i] = nums[i%numLength]
        
        return arr
    
    # python magic
    def getConcatenationAlternative(self, nums: List[int]) -> List[int]:
        return nums*2 # Can also do nums + nums