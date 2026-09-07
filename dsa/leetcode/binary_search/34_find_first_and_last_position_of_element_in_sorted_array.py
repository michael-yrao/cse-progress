"""
34. Find First and Last Position of Element in Sorted Array   ·   https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
Pattern: binary_search

Given an array of integers `nums` sorted in non-decreasing order, find the starting
and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
  Input:  nums = [5,7,7,8,8,10], target = 8
  Output: [3, 4]

Example 2:
  Input:  nums = [5,7,7,8,8,10], target = 6
  Output: [-1, -1]

Example 3:
  Input:  nums = [], target = 0
  Output: [-1, -1]

Constraints:
  0 <= nums.length <= 10^5
  -10^9 <= nums[i] <= 10^9
  nums is a non-decreasing array.
  -10^9 <= target <= 10^9
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-06 ────────────────────────────────────────────
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # we have to find this number twice
        # so let's do one min boundary and one max boundary
        # this is sorted, so we just shrink like normal binary search

        result = []

        # min boundary
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r)//2
            # if too small, this can't be the start
            # so move l up
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        
        if l >= 0 and l < len(nums) and nums[l] == target:
            result.append(l)
        else:
            result.append(-1)

        l, r = 0, len(nums) - 1

        # [5,7,7,8,8,10]
        #          l r
        while l < r:
            m = (l + r + 1)//2
            # if too big, this can't be the end
            # so move r down
            if nums[m] > target:
                r = m - 1
            else:
                l = m
        
        if l >= 0 and l < len(nums) and nums[l] == target:
            result.append(l)
        else:
            result.append(-1)
        
        return result