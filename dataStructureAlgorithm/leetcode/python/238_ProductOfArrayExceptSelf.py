from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Input: nums = [1,2,3,4]
        # Output: [24,12,8,6]
        # 1. We can try to keep two additional lists of size len(nums)
        #    where one keeps track of left of current value and the other keeps track of right
        # 2. Multiply the two lists and return result

        # left  = [1,1,2,6]
        # right = [24,12,4,1]

        left, right, result = [1] * len(nums), [1] * len(nums), [1] * len(nums)

        # set left

        for i in range(1,len(nums),1):
            left[i] = nums[i-1] * left[i-1]
        
        # set right

        for i in range(len(nums)-2, -1, -1):
            right[i] = nums[i+1] * right[i+1]

        # multiply for result

        for i in range(0,len(nums),1):
            result[i] = left[i] * right[i]

        return result