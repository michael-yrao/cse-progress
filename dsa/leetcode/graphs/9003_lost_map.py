"""
9003. Lost Map   ·   https://progressiveoverflow.com/practice/9003
Pattern: graphs
Difficulty: Medium

There are `n` villages numbered 0 to n-1, joined by exactly n-1 roads, so there is
exactly one route between any two villages. Every road has a positive length.

You are given `distances`, an n x n matrix. `distances[i][j]` is the length of the
route between village `i` and village `j`.

Return the roads. Write each road as `[u, v]`, the two villages it joins. The roads
may be in any order, and a road may list its two villages in either order.

Example 1:
    Input:  distances = [[0,1,1,2],[1,0,2,3],
                        [1,2,0,3],[2,3,3,0]]
    Output: [[0,1],[0,2],[0,3]]

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
    # ── Attempt 1 · 2026-10-04 ────────────────────────────────────────────
    def lostMap(self, distances: List[List[int]]) -> List[List[int]]:
        pass
