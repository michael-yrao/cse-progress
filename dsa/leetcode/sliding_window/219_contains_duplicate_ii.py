"""
219. Contains Duplicate II   ·   https://leetcode.com/problems/contains-duplicate-ii/
Pattern: sliding_window

Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.

Example 1:

Input: nums = [1,2,3,1], k = 3
Output: true

Example 2:

Input: nums = [1,0,1,1], k = 1
Output: true

Example 3:

Input: nums = [1,2,3,1,2,3], k = 2
Output: false

Constraints:

    1 <= nums.length <= 105
    -109 <= nums[i] <= 109
    0 <= k <= 105

"""

from typing import List

class Solution:

    # ── Attempt · 2026-08-03 ──────────────
    def containsNearbyDuplicate_20260803(self, nums: List[int], k: int) -> bool:
        # so k is the window size
        # we will add from r and remove from l and compare
        l, r = 0, 0
        windowSet = set()
        while r < len(nums):
            windowSet.add(nums[r])
            while r - l + 1 > k:
                windowSet.remove(nums[l])
                l+=1
            # now that we know the window size is valid
            # let's check if window set is size of window, if it is not, we have a duplicate
            if len(windowSet) != r - l + 1:
                return True
            r+=1
        return False

    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # create a set that keeps track of values inside the window size of k
        windowSet = set()

        # loop through the array with l = r = 0
        l = r = 0
        while r < len(nums):
            # ensure our set is valid by removing nums[l] if r - l > k
            if abs(r - l) > k:
                windowSet.remove(nums[l])
                l+=1
            if l != r and abs(r - l) <= k:
                # knowing our set is valid, if nums[r] in set, return True
                if nums[r] in windowSet:
                    return True
            windowSet.add(nums[r])
            r+=1
        
        return False
    def containsNearbyDuplicate_20260625(self, nums: List[int], k: int) -> bool:
        # we can use a set
        # l and r to traverse

        l = r = 0

        windowSet = set()

        while r < len(nums):
            while (r - l) > k:
                windowSet.remove(nums[l])
                l+=1
            if l != r and abs(r - l) <= k:
                if nums[r] in windowSet:
                    return True
            windowSet.add(nums[r])
            r+=1
        
        return False
    def containsNearbyDuplicate_20260704(self, nums: List[int], k: int) -> bool:
        # sliding window, use a set

        l = r = 0

        windowSet = set()

        while r < len(nums):
            # check if r - l > k, if greater, we need to shrink l
            while r - l > k:
                windowSet.remove(nums[l])
                l+=1
            # now that we know we have a valid window
            # check if nums[r] already exists in window
            # if so, we return True
            if nums[r] in windowSet:
                return True
            # if not, we add nums[r] to the window
            windowSet.add(nums[r])
            r+=1
        return False
