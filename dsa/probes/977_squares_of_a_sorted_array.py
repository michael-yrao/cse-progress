"""
977. Squares of a Sorted Array   ·   https://leetcode.com/problems/squares-of-a-sorted-array/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

Given an integer array `nums` sorted in NON-DECREASING order, return an array of
the squares of each number, also sorted in non-decreasing order.

    nums = [-4,-1,0,3,10]   ->  [0,1,9,16,100]
    nums = [-7,-3,2,3,11]   ->  [4,9,9,49,121]

Constraints:
    1 <= len(nums) <= 10^4
    -10^4 <= nums[i] <= 10^4
    nums is sorted in non-decreasing order.

Follow-up: an O(n) solution exists. Find it.

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-10 ────────────────────────────────────────────
    def sortedSquares(self, nums: List[int]) -> List[int]:
        # squaring and sort is trivial
        # let's go for the O(n) time solution
        # one thing we can notice is that if we use two pointers
        # one at left and one at right, we can easily tell what is the next biggest number
        l, r = 0, len(nums) - 1

        result = []
        while l <= r:
            if abs(nums[l]) > abs(nums[r]):
                result.append(nums[l]**2)
                l+=1
            else:
                result.append(nums[r]**2)
                r-=1
        
        result.reverse()
        return result
