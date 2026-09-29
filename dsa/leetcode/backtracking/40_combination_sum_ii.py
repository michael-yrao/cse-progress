"""
40. Combination Sum II   ·   https://leetcode.com/problems/combination-sum-ii/
Pattern: backtracking

Given a collection of candidate numbers `candidates` and a target number `target`,
find all unique combinations in `candidates` where the candidate numbers sum to `target`.

Each number in `candidates` may only be used once in the combination.

Note: the solution set must not contain duplicate combinations.

Example 1:
    Input:  candidates = [10,1,2,7,6,1,5], target = 8
    Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

Example 2:
    Input:  candidates = [2,5,2,1,2], target = 5
    Output: [[1,2,2],[5]]

Constraints:
    1 <= candidates.length <= 100
    1 <= candidates[i] <= 50
    1 <= target <= 30
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-28 ────────────────────────────────────────────
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # path: current array
        # state: current index
        # validity: if index is not used and adding it is <= target
        # choice: use or not use this candidate and whether or not we already have this
        # base case: if == target, add to result

        result = []
        candidates.sort()

        def backtrack(path, indexState):
            if sum(path) == target:
                result.append(path)
                return
            if indexState >= len(candidates):
                return

            # use this candidate
            if sum(path) + candidates[indexState] <= target:
                backtrack(path + [candidates[indexState]], indexState + 1)
            
            # index needs to be different value than what we already have in path
            # since we didn't pick current value, check prior values
            while indexState + 1 < len(candidates) and candidates[indexState] == candidates[indexState + 1]:
                indexState+=1
            backtrack(path, indexState + 1)
        
        backtrack([], 0)
        return result