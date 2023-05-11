from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # Not very obvious to figure out for in-place
        # 1. Reverse the array
        # 2. Reverse first k elements
        # 3. Reverse the last len - k elements

        # If k is greater than len, we just want the modular
        k = k % len(nums)

        # Reverse the array
        def reverse(l: int, r: int):
            while l < r:
                nums[l],nums[r] = nums[r],nums[l]
                l,r=l+1,r-1

        reverse(0,len(nums)-1)
        reverse(0,k-1)
        reverse(k,len(nums)-1)

    def rotateLinearMemory(self, nums: List[int], k: int) -> None:
        # If we can solve this problem with linear memory, all we need to do is create a temporary array
        # Loop through the original array and put values in i+k % len(nums) index and copy back to the original

        length = len(nums)
        temp = [] * length

        for i,v in enumerate(nums):
            temp[(i+k)%length] = nums[i]

        # Shallow copy
        nums = temp.copy()