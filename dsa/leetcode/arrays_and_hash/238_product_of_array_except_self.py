"""
Docstring for dsa.leetcode.arrays_and_hash.238_product_of_array_except_self
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

    # ── Attempt · 2026-08-19 ──────────────
    def productExceptSelf_20260819(self, nums: List[int]) -> List[int]:
        # pre and post
        # nums: [1,2,3,4]
        # pre:  [1,1,2,6]
        # post: [24,12,4,1]

        pre = [1] * len(nums)
        post = [1] * len(nums)

        for i in range(1, len(nums)):
            pre[i] = pre[i-1] * nums[i-1]
        
        for i in range(len(nums)-2,-1,-1):
            post[i] = post[i+1] * nums[i+1]

        result = [1] * len(nums)

        for i in range(len(nums)):
            result[i] = pre[i] * post[i]
        
        return result

    # ── Attempt · 2026-07-24 ──────────────
    def productExceptSelf_20260724(self, nums: List[int]) -> List[int]:
        # my preferred solution for this is pre and post product like prefixSum
        # input:       [1, 2, 3, 4]
        # preProduct:  [1, 1, 2, 6]
        # postProduct: [24, 12, 4, 1]
        # result:      [24, 12, 8, 6] 
        lenNums = len(nums)
        prefixProduct = [1] * lenNums
        postfixProduct = [1] * lenNums

        for i in range(1, lenNums):
            prefixProduct[i] = prefixProduct[i-1] * nums[i-1]
        
        for i in range(lenNums-2, -1, -1):
            postfixProduct[i] = postfixProduct[i+1] * nums[i+1]
        
        result = []

        for i in range(lenNums):
            product = prefixProduct[i] * postfixProduct[i]
            result.append(product)
        
        return result

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
