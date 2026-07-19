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

class Solution:

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
