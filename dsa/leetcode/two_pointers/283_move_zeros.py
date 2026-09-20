"""
Docstring for dsa.leetcode.two_pointers.283_move_zeros

Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:

Input: nums = [0]
Output: [0]

Constraints:

    1 <= nums.length <= 104
    -231 <= nums[i] <= 231 - 1

Follow up: Could you minimize the total number of operations done?

"""

from typing import List
import unittest

class Solution:

    # ── Attempt · 2026-09-19 ──────────────
    def moveZeroes_20260919(self, nums: List[int]) -> None:
        # two pointers, we can use left as a pointer to define where to put the next 0
        # we will use right to traverse the array
        # time complexity is O(n) since we have to go through the whole array
        # space complexity is O(1) with no extra space other than the two pointers
        
        left = right = 0
        
        while right < len(nums):
            # if we see a nonzero number, swap with left
            if nums[right] != 0:
                tmp = nums[left]
                nums[left] = nums[right]
                nums[right] = tmp
                left+=1
            right+=1

if __name__ == "__main__":
    inputArray = [0,1,0,3,12]
    expectedArray = [1,3,12,0,0]
    print(f"Before: {inputArray}")
    Solution().moveZeroes_20260919(inputArray)
    print(f"After: {inputArray}")

    # ── Attempt · 2026-07-19 ──────────────
    def moveZeroes_20260719(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # two pointers, we just want to move nonzeros to the front
        # so we use l to keep track of where to put the next nonzero value
        l = r = 0

        while r < len(nums):
            if nums[r] != 0:
                tmp = nums[l]
                nums[l] = nums[r]
                nums[r] = tmp
                l+=1
            r+=1

    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        
        def swap(l,r):
            tmp = nums[l]
            nums[l] = nums[r]
            nums[r] = tmp
        
        l = r = 0

        while r < len(nums):
            if nums[r] != 0:
                swap(l,r)
                l+=1
            r+=1
