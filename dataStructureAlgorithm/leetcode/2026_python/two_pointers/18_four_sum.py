"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.18_four_sum
Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:

    0 <= a, b, c, d < n
    a, b, c, and d are distinct.
    nums[a] + nums[b] + nums[c] + nums[d] == target

You may return the answer in any order.

Example 1:

Input: nums = [1,0,-1,0,-2,2], target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]

Example 2:

Input: nums = [2,2,2,2,2], target = 8
Output: [[2,2,2,2]]

Constraints:

    1 <= nums.length <= 200
    -109 <= nums[i] <= 109
    -109 <= target <= 109
"""
from typing import List

class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        resultSet = set()
        nums.sort()
        for a in range(len(nums)):
            # skip a index to avoid duplicates
            currentTarget = target - nums[a]
            for b in range(a+1,len(nums),1):
                twoSumTarget = currentTarget - nums[b]
                c, d = b+1, len(nums) - 1
                while c < d:
                    if nums[c] + nums[d] == twoSumTarget:
                        result = (nums[a], nums[b], nums[c], nums[d])
                        resultSet.add(result)
                        c+=1
                        d-=1
                    elif nums[c] + nums[d] < twoSumTarget:
                        c+=1
                    else:
                        d-=1
        return list(resultSet)