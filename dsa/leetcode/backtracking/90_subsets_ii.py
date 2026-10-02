"""
90. Subsets II   ·   https://leetcode.com/problems/subsets-ii/
Pattern: backtracking

Given an integer array `nums` that may contain duplicates, return all possible
subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Example 1:
    Input:  nums = [1,2,2]
    Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]

Example 2:
    Input:  nums = [0]
    Output: [[],[0]]

Constraints:
    1 <= nums.length <= 10
    -10 <= nums[i] <= 10
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-10-01 ────────────────────────────────────────────
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # we are getting all subsets but this time we have duplicates in here
        # path: current subset
        # state: index of the value that we are deciding whether to add or not
        # validity: whether or not the state is >= len(nums)
        # choice: pick or not pick current state 
        # base case: if current state index >= len(nums), add result
        # to account for duplicates, sort and check value

        nums.sort()

        result = []

        def backtrack(path, index):
            # base case
            if index == len(nums):
                result.append(path.copy())
                return
            
            # decision 1: include
            path.append(nums[index])
            backtrack(path, index + 1)
            path.pop()

            # decision 2: exclude
            # if we are excluding, we should also exclude any value that is the same as what is already picked
            while index + 1 < len(nums) and nums[index] == nums[index + 1]:
                index+=1
            backtrack(path, index + 1)
        
        backtrack([], 0)
        return result