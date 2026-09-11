"""
1584. Min Cost to Connect All Points   ·   https://leetcode.com/problems/min-cost-to-connect-all-points/
Pattern: graphs

You are given an array `points` of integer coordinates on a 2D plane, where
points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the Manhattan distance
between them: |xi - xj| + |yi - yj|.

Return the minimum cost to make all points connected. All points are connected if
there is exactly one simple path between any two points.

Example 1:
    Input:  points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20

Example 2:
    Input:  points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Constraints:
    1 <= points.length <= 1000
    -10^6 <= xi, yi <= 10^6
    All pairs (xi, yi) are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import heapq
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-10 ──────────────
    def minCostConnectPoints_20260910(self, points: List[List[int]]) -> int:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/1584_min_cost_to_connect_all_points.txt — restored at session end (python scripts/restore_history.py)
