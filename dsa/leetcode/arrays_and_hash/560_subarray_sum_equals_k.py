"""
Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:

Input: nums = [1,1,1], k = 2
Output: 2

Example 2:

Input: nums = [1,2,3], k = 3
Output: 2

Constraints:

    1 <= nums.length <= 2 * 104
    -1000 <= nums[i] <= 1000
    -107 <= k <= 107
"""
from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # first thing that comes to mind for subarray sum is prefixSum
        # we are looking for # of times prefix[j] - prefix[i] = k
        # but if we go through the prefixSum looking for i and j, we will end up with O(n^2)
        # so what can we do reduce the time complexity
        # we can take an approach like two sum
        # prefix[i] = prefix[j] - k
        # prefix[i] is sum we already calculated before
        # prefix[j] is current sum
        # so if prefix[i] is in the map, we increment our solution counter
        
        # map to store number of times prefix[i] appeared
        # we do need to consider if prefix[j] = k, then prefix[i] = 0
        # so we need to store it in the map first. e.g. nums = [3], k = 3
        prefixSumMap = {}
        prefixSumMap[0] = 1
        result = 0
        runningSum = 0
        
        for j in range(len(nums)):
            runningSum += nums[j]
            prefix_i = runningSum - k
            if prefix_i in prefixSumMap:
                result+=prefixSumMap[prefix_i]
            # since we just saw runningSum, we store it in the map
            prefixSumMap[runningSum] = prefixSumMap.get(runningSum,0) + 1
        
        return result