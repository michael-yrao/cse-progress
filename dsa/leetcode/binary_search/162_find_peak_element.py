"""
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in O(log n) time.

Example 1:

Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.

Example 2:

Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.

Constraints:

    1 <= nums.length <= 1000
    -231 <= nums[i] <= 231 - 1
    nums[i] != nums[i + 1] for all valid i.
"""
from typing import List

class Solution:

    # ── Attempt · 2026-07-16 ──────────────
    def findPeakElement_20260716(self, nums: List[int]) -> int:
        # it's honestly a very strange problem
        # but we can use binary search here
        # so looking at example 2, at m = 3, m + 1 can be a peak because it is bigger, so we go that side
        # so this is a min boundary binary search

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            if m+1 < len(nums) and nums[m] < nums[m+1]:
                # we take m out of the convo for being a possible result
                l = m + 1
            else:
                r = m
        
        return l

    def findPeakElement(self, nums: List[int]) -> int:
        # key is that a peak must exist
        # and a peak is only applicable to its immediate neighbors
        # so knowing peaks exist, we can be greedy and assume that if nums[mid] < nums[mid + 1], then there is a peak on the right
        # this is a boundary type search where we find the first position where the condition holds
        
        l, r = 0, len(nums) - 1
        # min boundary binary search (find first true position)
        # is_valid(mid) = nums[mid] >= nums[mid + 1] (peak at or left of mid)
        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] < nums[mid + 1]:
                l = mid + 1  # peak on right
            else:
                r = mid  # peak on left or at mid
        
        return l
    
    def findPeakElement_20260610(self, nums: List[int]) -> int:
        # key is that a peak must exist
        # and a peak is only applicable to its immediate neighbors
        # logn time also means binary search
        # so we are looking for the first number that sits in between two smaller numbers
        # looking at example 2
        # [1,2,1,3,5,6,4]
        #          l m r
        # so 3 is smaller than 5 but bigger than 1
        # so we should go right since 5 is potentially an answer
        # so if nums[m] < nums[m+1], we move l = m + 1 since this is min boundary
        # otherwise, we move r = m
        # peak element means I have to check m-1 and m+1

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            if nums[m] < nums[m+1]:
                l = m + 1
            else:
                r = m
        
        return l
    
    def findPeakElement_20260613(self, nums: List[int]) -> int:
        # key is that a peak must exist
        # given peak element index is p
        # nums[p] > nums[p-1] and nums[p] > nums[p+1]
        # if nums[i] < nums[i+1], we know nums[i+1] can be a candidate
        # so we greedily just move to the side that is bigger
        # since we don't know what we are searching for, this is another boundary style binary search
        # i guess we are trying to find the first number that fits the criteria
        # so we'll just default to min boundary

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            if m+1 < len(nums) and nums[m] < nums[m+1]:
                l = m + 1
            else:
                r = m
        return l
