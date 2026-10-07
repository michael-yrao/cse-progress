"""
452. Minimum Number of Arrows to Burst Balloons   ·   https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/
Pattern: intervals

Spherical balloons are taped to a flat wall (the XY-plane). Each balloon is given as
points[i] = [xstart, xend]: its horizontal diameter spans xstart..xend. You don't know
the exact y-coordinates.

Arrows are shot straight up (positive y) from points on the x-axis. An arrow shot at x
bursts every balloon with xstart <= x <= xend. There is no limit on arrows; a shot arrow
keeps travelling up forever, bursting every balloon in its path.

Return the minimum number of arrows that must be shot to burst all balloons.

Example 1: points = [[10,16],[2,8],[1,6],[7,12]]          -> 2
  (x = 6 bursts [2,8] and [1,6]; x = 11 bursts [10,16] and [7,12])
Example 2: points = [[1,2],[3,4],[5,6],[7,8]]             -> 4
Example 3: points = [[1,2],[2,3],[3,4],[4,5]]             -> 2
  (x = 2 bursts [1,2] and [2,3]; x = 4 bursts [3,4] and [4,5])

Constraints:
  1 <= points.length <= 10^5
  points[i].length == 2
  -2^31 <= xstart < xend <= 2^31 - 1
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # this is an interval question
        # we are seeing how many overlaps happen
        # sort by start of interval
        # we then check for overlapping
        # so [1,6] and [2,8] has [2,6] overlapping, we have arrow count at 1
        # and we get [7,12] which is not within [2,6] so we increment arrow and change current overlap, which is [7,12] since we are saying it doesn't need to be overlapped
        # then come 10, 16, it overlaps so we update current overlap to [10,12] and does not increment arrow

        # sort by start since this is merge intervals
        points.sort()

        arrow_counter = 0

        current_overlap = [-math.inf,-math.inf]

        for start, end in points:
            current_overlap_start = current_overlap[0]
            current_overlap_end = current_overlap[1]
            # if we are part of a merge, we just updating current_overlap
            if start <= current_overlap_end:
                current_overlap[0] = max(start, current_overlap_start)
                current_overlap[1] = min(end, current_overlap_end)
            # if we are not part of the merge, increment arrow counter
            # and update overlap to start and end of new interval
            else:
                current_overlap[0] = start
                current_overlap[1] = end
                arrow_counter+=1
        
        return arrow_counter
