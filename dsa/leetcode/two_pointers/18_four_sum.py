"""

MEDIUM

Docstring for dsa.leetcode.two_pointers.18_four_sum
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

    # ── Attempt · 2026-07-17 ──────────────
    def fourSum_20260717(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        # a + b + c + d = target
        # a + b + c = target - d

        result = set()

        def twoSumSorted(i,j,newTarget):
            results = []
            while i < j:
                if nums[i] + nums[j] == newTarget:
                    results.append([i,j])
                    i+=1
                    j-=1
                elif nums[i] + nums[j] > newTarget:
                    j-=1
                else:
                    i+=1
            return results

        for a in range(len(nums)-3):
            for b in range(a+1,len(nums)-2):
                c = b+1
                d = len(nums)-1
                newTarget = target - nums[a] - nums[b]
                resultArray = twoSumSorted(c,d,newTarget)
                for c, d in resultArray:
                    result.add((nums[a],nums[b],nums[c],nums[d]))
        
        resultList = []

        for a,b,c,d in result:
            resultList.append([a,b,c,d])

        return list(resultList)

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
