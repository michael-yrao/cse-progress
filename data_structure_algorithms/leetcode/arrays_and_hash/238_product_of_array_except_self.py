"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.238_product_of_array_except_self
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:

    2 <= nums.length <= 105
    -30 <= nums[i] <= 30
    The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

"""

from typing import List

class Solution:
    def productExceptSelfDivisionSolution(self, nums: List[int]) -> List[int]:
        total = 1
        result = []
        for num in nums:
            total*=num
        
        for i in range(len(nums)):
            result[i] = total / nums[i]

        return result

    def productExceptSelfPrefixSum(self, nums: List[int]) -> List[int]:
        numSize = len(nums)
        result, prefix, suffix = [1] * numSize, [1] * numSize, [1] * numSize

        # result[i] = prefix[i] * suffix[i]

        for i in range(1, numSize):
            prefix[i] = prefix[i-1] * nums[i-1]
        
        for i in range(numSize - 2, -1, -1):
            suffix[i] = suffix[i+1] * nums[i+1]

        for i in range(numSize):
            result[i] = prefix[i] * suffix[i]
        
        return result

    def productExceptSelfPrefixSumEfficient(self, nums: List[int]) -> List[int]:
        # take advantage of the fact that result does not count towards space complexity
        # store prefix in result, using a variable to help
        # then loop through again multiplying by suffix, using another variable to help

        result = [1] * len(nums)

        prefix = suffix = 1

        for i in range(len(nums)):
            result[i] = prefix
            prefix *= nums[i]

        for i in range(len(nums)-1,-1,-1):
            result[i] *= suffix
            suffix *= nums[i]
        
        return result