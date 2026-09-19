"""
84. Largest Rectangle in Histogram   ·   https://leetcode.com/problems/largest-rectangle-in-histogram/
Pattern: increasingStack

Given `heights`, where heights[i] is the height of bar i (each width 1), return the
area of the largest rectangle that fits entirely within the histogram.

Example: heights = [2,1,5,6,2,3] -> 10  (bars at index 2,3 → height 5 × width 2).

Constraints: 1 <= len(heights) <= 1e5, 0 <= heights[i] <= 1e4.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-18 ──────────────
    def largestRectangleArea_20260918(self, heights: List[int]) -> int:
        # we should do an increasing monotonic stack
        # that means we add a -math.inf at the end to make sure we calc in case of permanently increasing
        # calculate the current boundary area when we break that pattern
        # so keep track of a maxArea
        # so when we reach 2 (index 5), we have 6x1, how do we get 5 * 2 in the next pop
        # stack[-1] holds the left boundary of the window, so i - stack[-1] - 1

        maxArea = 0

        heights.append(-math.inf) # type: ignore

        increasingStack = []

        for i in range(len(heights)):
            # while we are decreasing, 
            while increasingStack and heights[i] < heights[increasingStack[-1]]:
                # current height
                currentHeightIndex = increasingStack.pop()
                # width is left boundary (i), right boundary (stack[-1]) now that we popped, then - 1
                if not increasingStack:
                    width = i
                else:
                    width = i - increasingStack[-1] - 1
                maxArea = max(maxArea, heights[currentHeightIndex] * width)
            increasingStack.append(i)
        
        return maxArea

    # ── Attempt 1 · 2026-09-04 ────────────────────────────────────────────
    def largestRectangleArea(self, heights: List[int]) -> int:
        # in our two pointer method for max area, we didn't have to consider
        # if the height is constrained in between
        # so how do we know 1 is the constraint for 2
        # 1 is the next smallest value after 2
        # so this leads to a monotonically increasing stack
        # so when we see an element that is smaller
        # we should calculate the prior area before we started descending
        # however, there is a flaw here, we are calculating when the rightWall is the constraint
        # but what if we never fall off, so let's add a 0 to the end

        increasingStack=[]
        maxArea=0

        # append so we calculate when we go up continuously
        heights.append(0)

        for i in range(len(heights)):
            # we found a smaller element
            # now calculate the maxArea based on the prior height
            # repeat this until we cannot go any further
            # we can do this because we are monotonically non-decreasing
            while increasingStack and heights[i]<heights[increasingStack[-1]]:
                height=heights[increasingStack.pop()]
                if increasingStack:
                    width=i-increasingStack[-1]-1
                else:
                    width=i
                area=width*height
                maxArea=max(maxArea,area)
            increasingStack.append(i)

        return maxArea
