"""
57. Insert Interval   ·   https://leetcode.com/problems/insert-interval/
Pattern: greedy

Given `intervals`, a list of non-overlapping intervals sorted by start, and a
new interval `newInterval`, insert it into the list so the result is still sorted
and non-overlapping (merge where needed). Return the resulting list.

Example: intervals = [[1,3],[6,9]], newInterval = [2,5]  ->  [[1,5],[6,9]]
Example: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
         ->  [[1,2],[3,10],[12,16]]

Constraints: intervals sorted by start, non-overlapping; 0 <= n <= 10^4.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-26 ────────────────────────────────────────────
    def insertInterval(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # intervals = [[1,3],[6,9]], newInterval = [2,5] -> merge with [1,3]
        # intervals = [2,4], newInterval = [1,6] -> absorbs [2,4]
        # compare end of each interval with newInterval's start
        # if intervalEnd >= newStart, we merge these
        # if intervalEnd < newStart, this interval is not in scope, so we go next
        # but this doesn't work because 9 < 2 is false
        # so we need to do if intervalEnd < newStart which means interval is before newInterval
        # OR intervalStart > newEnd which means interval is AFTER newInterval

        # we will split this into phases
        # 1. insert intervals newInterval
        # 2. combine intervals that overlap with newInterval
        # 3. insert merged interval
        # 4. insert intervals after merged interval

        result = []
        newStart, newEnd = newInterval
        index = 0
        
        # insert intervals smaller than newInterval into result
        while index < len(intervals) and intervals[index][1] < newStart:        
            result.append(intervals[index])
            index+=1
        
        # index is now overlapping with newInterval, so go until we no longer overlap
        # so while intervalStart <= newEnd
        while index < len(intervals) and intervals[index][0] <= newEnd: 
            # update newStart and newEnd accordingly each time
            # marking these as 'merging'
            newStart = min(newStart, intervals[index][0])
            newEnd = max(newEnd, intervals[index][1])
            index+=1
        
        # insert merged interval into result
        result.append([newStart, newEnd])
        
        # now insert everything that comes after
        while index < len(intervals) and intervals[index][0] > newEnd:
            result.append(intervals[index])
            index+=1
        
        return result