"""
56. Merge Intervals   ·   https://leetcode.com/problems/merge-intervals/
Pattern: greedy

Given an array `intervals` where intervals[i] = [start_i, end_i], merge all
overlapping intervals and return an array of the non-overlapping intervals that
cover all the intervals in the input.

Example:
  [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]   ([1,3] & [2,6] overlap)
  [[1,4],[4,5]]                -> [[1,5]]                    (touching counts as overlap)

Constraints: 1 <= intervals.length <= 10^4 ; 0 <= start_i <= end_i <= 10^4.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-24 ────────────────────────────────────────────
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # sort by start time so that any overlapping intervals are next to each other
        # then just check against latest interval in the list

        intervals.sort()

        result = []

        for start, end in intervals:
            # prevStart = 1, prevEnd = 3
            # start = 2, end = 6
            # if there is something in result and overlapping
            # pop what is in result and add the merged interval in
            if result and start <= result[-1][1]:
                prevStart, prevEnd = result.pop()
                newEnd = max(prevEnd, end)
                result.append([prevStart, newEnd])
            else:
                result.append([start,end])
        return result
