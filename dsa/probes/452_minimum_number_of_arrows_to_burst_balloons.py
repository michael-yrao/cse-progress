"""
452. Minimum Number of Arrows to Burst Balloons   ·   https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

There are some spherical balloons taped onto a flat wall that represents the XY-plane.
The balloons are represented as a 2D integer array points where
points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches
between xstart and xend. You do not know the exact y-coordinates of the balloons.

Arrows can be shot up directly vertically (in the positive y-direction) from different
points along the x-axis. A balloon with xstart and xend is burst by an arrow shot at x
if xstart <= x <= xend. There is no limit to the number of arrows that can be shot. A
shot arrow keeps traveling up infinitely, bursting any balloons in its path.

Given the array points, return the minimum number of arrows that must be shot to burst
all balloons.

Example 1:
    Input:  points = [[10,16],[2,8],[1,6],[7,12]]
    Output: 2
    Explanation: Shoot an arrow at x = 6, bursting [2,8] and [1,6].
                 Shoot an arrow at x = 11, bursting [10,16] and [7,12].

Example 2:
    Input:  points = [[1,2],[3,4],[5,6],[7,8]]
    Output: 4
    Explanation: One arrow per balloon.

Example 3:
    Input:  points = [[1,2],[2,3],[3,4],[4,5]]
    Output: 2
    Explanation: Shoot an arrow at x = 2, bursting [1,2] and [2,3].
                 Shoot an arrow at x = 4, bursting [3,4] and [4,5].

Constraints:
    1 <= points.length <= 10^5
    points[i].length == 2
    -2^31 <= xstart < xend <= 2^31 - 1

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        pass
