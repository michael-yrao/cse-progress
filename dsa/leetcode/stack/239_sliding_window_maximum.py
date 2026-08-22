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
import collections
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-22 ──────────────
    # ── RECOGNITION — fill BEFORE coding, before the coach says anything ──
    #   shape cues seen →
    #   technique →
    #   discriminator (why this, not the nearest neighbour) →
    def maxSlidingWindow_20260822(self, nums: List[int], k: int) -> List[int]:
        # one natural way to do this problem is sliding window with maxHeap of tuple (value, index)
        # that will give us a O(nlogn) solution
        # we can do better by doing a monotonic deque so that we can simulate the sliding window
        # by being able to remove from both ends
        # the monotonic deque will need to be decreasing, that way when we see a larger value
        # we pop from the stack side until we are smaller
        # if the front index is no longer in the window, we pop from the queue side

        result = []

        # store indices
        monotonicDeque = collections.deque()

        for i in range(len(nums)):
            # check values and pop until we can insert
            while monotonicDeque and nums[i] > nums[monotonicDeque[-1]]:
                monotonicDeque.pop()
            # nothing else is bigger, let's insert the value
            monotonicDeque.append(i)
            # now we remove from the queue side if we are bigger than window
            # since our monotonic deque don't always hold the whole window size
            # we need to check if i - monotonicDeque[0] is bigger than k
            while i - monotonicDeque[0] + 1 > k:
                monotonicDeque.popleft()
            # now we are good to add to the result
            # notice the result is of size len(nums) - k so we don't add until we get to k - 1
            # decreasing deque so the front has the biggest
            if i >= k - 1:
                result.append(nums[monotonicDeque[0]])
        return result

    # ── Attempt 1 · 2026-08-20 ────────────────────────────────────────────
    # ── RECOGNITION — fill BEFORE coding, before the coach says anything ──
    #   shape cues seen →
    #   technique →
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # using a deque, we can move things in and out of it from both sides
        # so this acts like our sliding window
        # we will use monotonically decreasing deque
        # when size of the deque is greater than k, we remove from the queue side
        # when we see an element that is greater than peek, we remove from stack side

        result = []

        decreasingDeque = collections.deque()

        # go through the array
        for i in range(len(nums)):
            # if new value coming in is greater and not decreasing, pop from stack side
            while decreasingDeque and nums[i] > nums[decreasingDeque[-1]]:
                decreasingDeque.pop()
            # insert index in deque
            decreasingDeque.append(i)

            # now that we know decreasingDeque holds the maximum
            # let's check if this is within the boundary
            # at index i, the window starts at i - k + 1
            # so the queue side index should be no smaller than that
            while decreasingDeque[0] < i - k + 1:
                decreasingDeque.popleft()
            
            # now that we know we have a valid window
            # we put the peak value into the result if we are past kth element
            # so index k - 1 is when we start adding to result
            if i >= k - 1:
                result.append(nums[decreasingDeque[0]])
        
        return result
