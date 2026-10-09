"""
9003. Lost Map   ·   https://progressiveoverflow.com/practice/9003
Pattern: graphs
Difficulty: Medium

There are `n` villages, numbered 0 to n-1. Some pairs of villages are joined by a direct
road, and every road has a positive length. There are exactly n-1 roads, and they connect
every village, so there is exactly one way to travel between any two villages.

The map of the roads is lost. All you have is `distances`, an n x n matrix.
`distances[i][j]` is the total length of the roads you travel along to get from village `i`
to village `j`. Most pairs of villages have no direct road, so most entries are a sum of
several road lengths.

Return the n-1 roads. Write each road as `[u, v]`, the two villages it joins. The roads
may be in any order, and a road may list its two villages in either order.

Example 1:
    Input:  distances = [[0,1,1,2],[1,0,2,3],
                        [1,2,0,3],[2,3,3,0]]
    Output: [[0,1],[0,2],[0,3]]
    Explanation: the roads are 0-1 with length 1, 0-2 with
    length 1, and 0-3 with length 2. distances[1][2] is 2
    because the trip from 1 to 2 goes 1 -> 0 -> 2, using two
    roads.

Example 2:
    Input:  distances = [[0,4,9],[4,0,5],[9,5,0]]
    Output: [[0,1],[1,2]]

Example 3:
    Input:  distances = [[0,7],[7,0]]
    Output: [[0,1]]

Constraints:
    2 <= n <= 2500
    distances[i][i] == 0
    distances[i][j] == distances[j][i]
    1 <= distances[i][j] < 10^7 for i != j
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-10-08 ────────────────────────────────────────────
    def lostMap(self, distances: List[List[int]]) -> List[List[int]]:
        pass
