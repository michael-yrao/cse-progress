"""
239. Sliding Window Maximum   ·   https://leetcode.com/problems/sliding-window-maximum/
Pattern: stack

You are given an array `nums` and a window of size `k` that slides from the far left
to the far right, one position at a time. At each position you can only see the `k`
numbers inside the window.

Return a list of the maximum value in the window at each position, in order.

Example: nums = [1,3,-1,-3,5,3,6,7], k = 3  ->  [3,3,5,5,6,7]

Constraints: 1 <= nums.length <= 1e5 · -1e4 <= nums[i] <= 1e4 · 1 <= k <= nums.length
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-20 ────────────────────────────────────────────
    # ── RECOGNITION — fill BEFORE coding, before the coach says anything ──
    #   shape cues seen →
    #   technique →
    #   discriminator (why this, not the nearest neighbour) →
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        pass
