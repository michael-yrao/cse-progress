"""
3620. Network Recovery Pathways   ·   https://leetcode.com/problems/network-recovery-pathways/
Pattern: graphs

You are given a directed acyclic graph of n nodes numbered 0..n-1, as a 2D array edges of
length m, where edges[i] = [ui, vi, costi] is a one-way communication from ui to vi with a
recovery cost of costi.

Some nodes may be offline. online[i] = true means node i is online. Nodes 0 and n-1 are
always online.

A path from 0 to n-1 is VALID if:
  - all intermediate nodes on the path are online, and
  - the total recovery cost of all edges on the path does not exceed k.

For each valid path, its SCORE is the minimum edge cost along that path.
Return the maximum path score (the largest minimum edge cost) among all valid paths.
If no valid path exists, return -1.

Example 1:
  edges = [[0,1,5],[1,3,10],[0,2,3],[2,3,4]], online = [true,true,true,true], k = 10
  -> 3
  0->1->3: total 5+10 = 15 > 10, invalid.
  0->2->3: total 3+4 = 7 <= 10, valid; score min(3,4) = 3.

Example 2:
  edges = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]],
  online = [true,true,true,false,true], k = 12
  -> 6
  0->1->4: total 12 <= 12, valid; score 5.
  0->2->3->4: node 3 offline, invalid.
  0->2->4: total 12 <= 12, valid; score 6.

Constraints:
  n == online.length
  2 <= n <= 5 * 10^4
  0 <= m == edges.length <= min(10^5, n*(n-1)/2)
  edges[i] = [ui, vi, costi]
  0 <= ui, vi < n
  ui != vi
  0 <= costi <= 10^9
  0 <= k <= 5 * 10^13
  online[0] and online[n-1] are true.
  The graph is a directed acyclic graph.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-10-03 ────────────────────────────────────────────
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        pass
