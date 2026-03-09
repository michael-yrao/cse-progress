"""
Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:

Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Constraints:

    1 <= nums.length <= 104
    -104 < nums[i], target < 104
    All the integers in nums are unique.
    nums is sorted in ascending order.
"""

from typing import List

class Solution:
    # recursion method
    def recursiveSearch(self, nums: List[int], target: int) -> int:
        def search(l,r):
            if l > r:
                return -1
            m = l + (r - l) // 2

            if nums[m] == target:
                return m
            if nums[m] > target:
                return search(l,m-1)
            return search(m+1,r)
        
        return search(0, len(nums)-1)

    # loop method
    def loopSearch(self, nums: List[int], target: int) -> int:
        # l,r,mid
        l, r = 0, len(nums)-1

        # continue until no more values to iterate through
        # covers case of nums.length == 1 e.g. [1]
        while l <= r:
            # l + (r - l) // 2 is same as (l + r) // 2
            # however, this covers case where l and r are large numbers
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] > target:
                r = mid - 1
            else:
                l = mid + 1

        return -1
    