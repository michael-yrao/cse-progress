"""
55. Jump Game   ·   https://leetcode.com/problems/jump-game/
Pattern: greedy

You are given an integer array nums. You start at the first index (nums[0]).
Each nums[i] is the MAXIMUM jump length from position i (you may jump anywhere
from 0..nums[i] steps forward).

Return True if you can reach the last index, else False.

Example:  [2,3,1,1,4] -> True   (0->1->4, or 0->2->3->4)
          [3,2,1,0,4] -> False  (every path stalls at the 0 at index 3)

Constraints: 1 <= len(nums) <= 10^4 ; 0 <= nums[i] <= 10^5.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-05 ────────────────────────────────────────────
    def jumpGame(self, nums: List[int]) -> bool:
        # first instinct is to jump to the highest value index we can jump to
        # but 3 at index 1 and 3 at index 10 are vastly different values
        # and we don't care for the path that we are taking to finish and only whether we can reach or not
        # so key is to check how far we can reach via i + nums[i]
        # we are asked whether or not we can get to the end
        # so what we need to check if how far can we reach from each index
        # we know i + nums[i] is the furthest we can reach, so if we are not within that, we know we hit a wall
        # otherwise, just continue checking and see if we are able to reach the end

        # starting at first index, this is how far we can reach
        maxReach = 0

        for i in range(len(nums)):
            # we are saying maxReach is the furthest we can go
            # so if we are overstepping it, it means we cannot move forward
            if i > maxReach:
                return False
            maxReach = max(maxReach, i + nums[i])
        return maxReach >= len(nums) - 1
