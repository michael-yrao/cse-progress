"""
78. Subsets   ·   https://leetcode.com/problems/subsets/
Pattern: backtracking

Given an integer array `nums` of UNIQUE elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets; return in any order.

Example: nums=[1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]  (8 = 2^3 subsets).
Example: nums=[0] -> [[],[0]].

Constraints: 1 <= len(nums) <= 10, -10 <= nums[i] <= 10, all elements unique.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-20 ────────────────────────────────────────────
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # returning all possible subsets is backtracking
        # so let's define a few things here
        # path = the array that we are building. since array is mutable, we need a copy of it
        # state = which index we are performing the choice on
        # choice = choose or not choose number
        # validity = not applicable?
        # base case = state == len(nums)

        result = []

        def backtrack(path, indexState):
            # base case
            if indexState == len(nums):
                result.append(path)
                return
            
            # choice #1, choose to use this current character at indexState
            option1 = path.copy()
            option1.append(nums[indexState])
            backtrack(option1, indexState+1)

            # choice #2, do not use this
            option2 = path.copy()
            backtrack(option2, indexState+1)

        backtrack([], 0)
        return result
