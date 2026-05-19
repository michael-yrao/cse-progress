"""
There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:

Input: nums = [1], target = 0
Output: -1

Constraints:

    1 <= nums.length <= 5000
    -104 <= nums[i] <= 104
    All values of nums are unique.
    nums is an ascending array that is possibly rotated.
    -104 <= target <= 104
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # if we are looking for logn time, we can't go through the array to find k
        # we should binary search to find k
        # then binary search on the 2 halves
        # k is smallest value, thus we do binary search on smallest value
        # Want exact target index? l <= r
        # Want first/last occurrence or smallest pivot? l < r
        # If looking for a boundary and not a single target, prefer l < r

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        
        k = l

        # binary search on both halves

        def binarySearch(l,r) -> int:
            while l<=r:
                mid = (l+r)//2
                if nums[mid] == target:
                    return mid
                elif nums[mid] > target:
                    r = mid - 1
                else:
                    l = mid + 1
            return -1
        
        result = binarySearch(0,k-1)
        if result == -1:
            result = binarySearch(k,len(nums)-1)
        
        return result