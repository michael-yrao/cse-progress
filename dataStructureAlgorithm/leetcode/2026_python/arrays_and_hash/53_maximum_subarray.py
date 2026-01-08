"""
Given an integer array nums, find the

with the largest sum, and return its sum.

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Constraints:

    1 <= nums.length <= 105
    -104 <= nums[i] <= 104

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.

"""

import math
from typing import List

class Solution:
    def maxSubArrayKadane(self, nums: List[int]) -> int:
        # Kadane's Algorithm
        maxSum, currentSum = nums[0]
        for n in nums:
            if currentSum < 0:
                currentSum = 0
            currentSum += n
            maxSum = max(maxSum, currentSum)
        return maxSum
    
    def maxSubarrayKadaneV2(self, nums: List[int]) -> int:
        # Kadane's Algorithm
        maxSum = currentSum = nums[0]
        for n in nums[1:]:
            # if currentSum + n is smaller than n
            # that means currentSum is negative
            # thus we start a new subarray with n only
            currentSum = max(n, currentSum + n)
            maxSum = max(maxSum, currentSum)
        return maxSum
    
    def maxSubarrayPrefixSum(self, nums: List[int]) -> int:
        # prefix sum solution
        # we can build a prefix sum list
        # sum of subarray = pre[j] - pre[i]
        # keep track of a maxSum
        # and also a min pre since we need to do pre[j] - pre[i] to get sum

        maxSum = -math.inf
        preMin = 0

        pre = []
        pre.append(nums[0])

        for i in range(1,len(nums)):
            pre.append(pre[i-1]+nums[i])

        for prefixSum in pre:
            maxSum = max(maxSum, prefixSum - preMin)
            preMin = min(preMin, prefixSum)

        return maxSum