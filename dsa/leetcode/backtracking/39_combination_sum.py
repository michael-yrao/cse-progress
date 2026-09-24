"""
39. Combination Sum   ·   https://leetcode.com/problems/combination-sum/
Pattern: backtracking

Given an array of distinct integers candidates and a target integer target, return a
list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two
combinations are unique if the frequency of at least one of the chosen numbers is
different.

The test cases are generated such that the number of unique combinations that sum up to
target is less than 150 combinations for the given input.

Example 1:
  Input: candidates = [2,3,6,7], target = 7
  Output: [[2,2,3],[7]]
  Explanation: 2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used
  multiple times. 7 is a candidate, and 7 = 7. These are the only two combinations.

Example 2:
  Input: candidates = [2,3,5], target = 8
  Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
  Input: candidates = [2], target = 1
  Output: []

Constraints:
  1 <= candidates.length <= 30
  2 <= candidates[i] <= 40
  All elements of candidates are distinct.
  1 <= target <= 40
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-23 ────────────────────────────────────────────
    def combinationSum_v1(self, candidates: List[int], target: int) -> List[List[int]]:
        # all combinations where chosen numbers sum to target
        # we can also choose a number infinite amount of times
        # path = current array
        # state = current index of candidates
        # choice = choose or not use this candidate at index state
        # validity = sum(path) + index state <= target
        # base case = sum(path) == target and if index is out of range

        candidates.sort()
        
        result = []

        def backtrack(path, indexState):
            if indexState >= len(candidates):
                return
            if sum(path) == target:
                result.append(path)
                return
            # if we are able to pick this candidate, pick it
            if sum(path) + candidates[indexState] <= target:
                backtrack(path + [candidates[indexState]], indexState)

            # regardless of whether we can pick it or not, go next
            backtrack(path.copy(), indexState + 1)
            
        backtrack([], 0)

        return result
    
    def combinationSum_v2(self, candidates: List[int], target: int) -> List[List[int]]:
        # all combinations where chosen numbers sum to target
        # we can also choose a number infinite amount of times
        # path = current array
        # state = smallest value allowed
        # choice = which number goes next
        # validity = number >= smallestState sum(path) + choice <= target
        # base case = sum(path) == target

        candidates.sort()
        
        result = []

        def backtrack(path, smallestState):
            if sum(path) == target:
                result.append(path)
                return
            
            for number in candidates:
                # if valid, do both choices
                if number >= smallestState and sum(path) + number <= target:
                    # path + [number] creates a new array so no need for copy
                    backtrack(path + [number], number)
        
        backtrack([], candidates[0])

        return result