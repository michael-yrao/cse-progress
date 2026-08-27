"""
435. Non-overlapping Intervals   ·   https://leetcode.com/problems/non-overlapping-intervals/
Pattern: greedy

Given `intervals` where intervals[i] = [start, end], return the minimum number
of intervals you must remove so that the rest are non-overlapping. Intervals
touching at an endpoint ([1,2],[2,3]) do NOT overlap.

Example: [[1,2],[2,3],[3,4],[1,3]]  ->  1   (remove [1,3])
Example: [[1,2],[1,2],[1,2]]        ->  2
Example: [[1,2],[2,3]]              ->  0

Constraints: 1 <= n <= 10^5; -5*10^4 <= start < end <= 5*10^4.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-26 ────────────────────────────────────────────
    def nonOverlappingIntervals(self, intervals: List[List[int]]) -> int:
        # we are being asked to remove as little as possible, so keep as many intervals as possible
        # greedy approach, we'll need to sort by end
        # now what do we replace
        # [[1,2],[1,3],[2,3],[3,4]]
        # removing [1,3] = keeping the one that ends earlier
        # so how do we check overlaps
        # how do we know [1,2] and [1,3] overlaps
        # when we are at [1,3], we can compare whether or not 2 < 1
        # since we know this is sorted, we know this always works
        # so keep track of the last known good of end

        lkgEnd = -math.inf

        # sort by end
        intervals.sort(key=lambda x: x[1])
        # how many intervals to remove
        removalCount = 0
        
        index = 0
        while index < len(intervals):
            start, end = intervals[index]
            # if start >= lkgEnd, we set lkgEnd to end and continue
            # we can add = due to example 3
            if start >= lkgEnd:
                lkgEnd = end
            # if overlapping, we need to remove the current and increment removal count
            else:
                removalCount+=1
            index+=1
        return removalCount
