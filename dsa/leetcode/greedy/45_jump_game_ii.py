"""
45. Jump Game II   ·   https://leetcode.com/problems/jump-game-ii/
Pattern: greedy

MEDIUM

You are given a 0-indexed array `nums` of length n. You start at nums[0].

Each nums[i] is the maximum jump length forward from index i: from i you can
reach any index in [i+1, i+nums[i]].

Return the MINIMUM number of jumps to reach index n-1. The test cases guarantee
that you can always reach n-1.

Example 1:
  Input:  nums = [2,3,1,1,4]
  Output: 2        (jump 1 step 0->1, then 3 steps 1->4)

Example 2:
  Input:  nums = [2,3,0,1,4]
  Output: 2

Constraints:
  1 <= n <= 1e4 ;  0 <= nums[i] <= 1000 ;  reaching n-1 is guaranteed.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-08 ────────────────────────────────────────────
    def jump(self, nums: List[int]) -> int:
        # in order to jump the minimum amount of times
        # the logical thing to do is jump to the node with i + nums[i] being the highest possible
        
        jump = 0
        # let's do this with a 'two pointer', this is the window we need to check for the first
        # repeat until right is len(nums) - 1 or more which means we can reach now
        left = 0
        right = nums[0]

        # if we don't need to jump return 0
        if len(nums) == 1:
            return 0
        
        # right is here to tell us whether or not we are able to reach a certain point
        while right < len(nums) - 1:
            # if at any point, if nums at left is zero, we are just doomed
            if nums[left] == 0:
                return 0
            nextJumpPoint = left
            # go through the window of left and right
            for i in range(left,right+1):
                currentJumpPotential = i + nums[i]
                if currentJumpPotential >= nextJumpPoint + nums[nextJumpPoint]:
                    nextJumpPoint = i
            # found the next jump point, increment jump and right
            jump+=1
            left = nextJumpPoint
            right = nextJumpPoint + nums[nextJumpPoint]
        
        return jump+1