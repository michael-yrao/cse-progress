"""
46. Permutations   ·   https://leetcode.com/problems/permutations/
Pattern: backtracking

Given an array nums of DISTINCT integers, return all possible permutations. Any order.

Example 1: nums = [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
Example 2: nums = [0,1]   -> [[0,1],[1,0]]
Example 3: nums = [1]     -> [[1]]

Constraints: 1 <= len(nums) <= 6, -10 <= nums[i] <= 10, all values unique.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-05 ──────────────
    def permute_20261005(self, nums: List[int]) -> List[List[int]]:
        # all possible permutations mean each permutation is of len(nums)
        # path: current permutation path
        # state: set of indices we have so far in this path (don't really need to use a set)
        # choice: next element to put in the permutation
        # validity: if choosing: have we already used this index. 
        # base case: if len(path) == len(nums), add to result

        result = []

        def backtrack(path):
            if len(path) == len(nums):
                result.append(path.copy())
                return

            for num in nums:
                if num not in path:
                    path.append(num)
                    backtrack(path)
                    path.pop()

        backtrack([])
        return result

    # ── Attempt 1 · 2026-09-25 ────────────────────────────────────────────
    def permute(self, nums: List[int]) -> List[List[int]]:
        # all possible permutations, backtracking
        # each index literally always has two options, pick or not pick it
        # path -> current array
        # state -> current set of values in the path
        # choice -> which number goes into the next slot in path
        # validity -> if current number is not in set path
        # base case -> len(path) == len(nums)

        result = []

        def backtrack(path, setState):
            if len(path) == len(nums):
                result.append(path)
                return

            for num in nums:
                if num not in setState:
                    newSet = setState.copy()
                    newSet.add(num)
                    backtrack(path + [num], newSet)
        
        backtrack([], set())

        return result
