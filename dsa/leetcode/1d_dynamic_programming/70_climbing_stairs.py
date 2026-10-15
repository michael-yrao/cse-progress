"""
70. Climbing Stairs   ·   https://leetcode.com/problems/climbing-stairs/
Pattern: 1d_dynamic_programming

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways
can you climb to the top?

Example 1:
    Input:  n = 2
    Output: 2
    Explanation: There are two ways to climb to the top.
    1. 1 step + 1 step
    2. 2 steps

Example 2:
    Input:  n = 3
    Output: 3
    Explanation: There are three ways to climb to the top.
    1. 1 step + 1 step + 1 step
    2. 1 step + 2 steps
    3. 2 steps + 1 step

Constraints:
    1 <= n <= 45
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-10-14 ────────────────────────────────────────────
    def climbStairs(self, n: int) -> int:
        # we will try memo
        memo = {}

        def ways(i):
            # from the two examples, we are looking to get to exactly n
            # so when we get to n, that is one completion
            if i == n:
                return 1
            
            if i > n:
                return 0
            
            # if we have already calculated this before, return it
            if i in memo:
                return memo[i]

            # if we've never calculated i before, put current steps in there
            memo[i] = ways(i + 1) + ways(i + 2)
            # otherwise, go 1 step or 2 steps
            return memo[i]
        
        return ways(0)
