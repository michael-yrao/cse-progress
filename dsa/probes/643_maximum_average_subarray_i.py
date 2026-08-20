"""
643. Maximum Average Subarray I   ·   https://leetcode.com/problems/maximum-average-subarray-i/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

You are given an integer array `nums` consisting of `n` elements, and an integer `k`.

Find a contiguous subarray whose length is equal to `k` that has the maximum average value
and return this value. Any answer with a calculation error less than `10^-5` will be
accepted.

    nums = [1,12,-5,-6,50,3], k = 4   ->  12.75000
        (12-5-6+50)/4 = 51/4 = 12.75

    nums = [5], k = 1                ->  5.00000

Constraints:
    n == nums.length
    1 <= k <= n <= 10^5
    -10^4 <= nums[i] <= 10^4

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # so we are just looking for the max sum in a window of size k

        maxSum = -math.inf
        l = r = 0
        currentSum = 0
        while r < len(nums):
            currentSum+=nums[r]
            if r - l + 1 > k:
                currentSum-=nums[l]
                l+=1
            if r - l + 1 == k:
                maxSum = max(maxSum, currentSum)
            r+=1
        
        return maxSum/k
