"""
974. Subarray Sums Divisible by K   ·   https://leetcode.com/problems/subarray-sums-divisible-by-k/
Pattern: arrays_and_hash

Given an integer array nums and an integer k, return the number of NON-EMPTY subarrays
that have a sum divisible by k.

A subarray is a contiguous part of an array.

  Input:  nums = [4,5,0,-2,-3,1], k = 5
  Output: 7
  Explanation: the 7 subarrays with a sum divisible by 5 are
    [4,5,0,-2,-3,1], [5], [5,0], [5,0,-2,-3], [0], [0,-2,-3], [-2,-3]

  Input:  nums = [5], k = 9
  Output: 0

Constraints: 1 <= nums.length <= 3*10^4; -10^4 <= nums[i] <= 10^4; 2 <= k <= 10^4.
⚠️ nums may contain negatives and zeros.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-18 ────────────────────────────────────────────
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        pass
