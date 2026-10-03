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

    # ── Attempt · 2026-10-02 ──────────────
    def combinationSum2_20261002(self, candidates: List[int], target: int) -> List[List[int]]:
        # example 1 output are all sorted, we sort first
        # path: current combination
        # state: current target and current index and whether or not we pick it
        # validity: if adding, must be less than target, if not adding, ignore other values that are equal
        # decision: pick or not pick value at current index
        # base case: if current target == 0 is success, if index >= len, exit

        candidates.sort()
        result = []

        def backtrack(path, current_target, current_index):
            # base case
            if current_target == 0:
                result.append(path.copy())
                return
            if current_index >= len(candidates):
                return
            
            # validity
            # decision 1: add number at current index
            if candidates[current_index] <= current_target:
                path.append(candidates[current_index])
                backtrack(path, current_target - candidates[current_index], current_index + 1)
                path.pop()

            # validity
            # decision 2: do not add number at current index
            # need to skip duplicates here
            while current_index + 1 < len(candidates) and candidates[current_index] == candidates[current_index+1]:
                current_index+=1
            
            backtrack(path, current_target, current_index + 1)
        
        backtrack([], target, 0)
        return result

    # ── Attempt · 2026-09-30 ──────────────
    def combinationSum2_20260930(self, candidates: List[int], target: int) -> List[List[int]]:
        # all unique combinations = backtracking
        # no duplicates combinations so will need to consider that in validity
        # sort and then go through each node in a loop
        # path: current array for solution
        # state: index state, first index this path can pick from
        # validity: if candidates[i] != candidates[i-1] and sum(path) + candidates[index] <= target
        # choice: choose next index to include
        # base case: sum is equal to target

        result = []

        candidates.sort()

        def backtrack(path, indexState):
            if sum(path) == target:
                result.append(path)
                return
            
            # for loop is our breadth and tells us to do recursion on each of current node's children based on validity
            for i in range(indexState, len(candidates)):
                if i > indexState and candidates[i] == candidates[i-1]:
                    continue
                if sum(path) + candidates[i] <= target:
                    # recursion call is our depth
                    # pick i and then pick i + 1 onwards in our recursion calls
                    backtrack(path + [candidates[i]], i + 1)
                
        backtrack([], 0)
        return result

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
