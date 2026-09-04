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

    # ── Attempt · 2026-09-03 ──────────────
    def merge_20260903(self, intervals: List[List[int]]) -> List[List[int]]:
        # sort first on startTime, then merge
        # I know it is sort, but what is the intuition to sort here and by what
        # with it sorted, now let's look at the criterias to merge
        # [2,6] is merging with [1,3] because priorEnd >= currentStart
        # [2,6] is not merging with [8,10] because of the same
        # now what about [1,8] and [2,6], we know to merge because of the same reason
        # now consider [[1,10],[2,3],[5,6]]
        # this tells us we need to sort by start so our start time is settled in place
        # and we only need to update our end time if we need to merge

        intervals.sort(key = lambda interval:interval[0])

        result = []
        result.append(intervals[0])
        # we are given intervals is at least size 1, so start our index at 1
        # everything before index - 1, we consider to be sacred and complete
        for i in range(1, len(intervals)):
            currentStart = intervals[i][0]
            currentEnd = intervals[i][1]
            priorIntervalEnd = result[-1][1]
            # this means we need to merge
            if priorIntervalEnd >= currentStart:
                result[-1][1] = max(priorIntervalEnd, currentEnd)
            # if we do not need to merge, we just insert
            else:
                result.append(intervals[i])
        return result

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
