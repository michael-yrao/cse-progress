"""
332. Reconstruct Itinerary   ·   https://leetcode.com/problems/reconstruct-itinerary/
Pattern: graphs

tickets[i] = [from_i, to_i] = one flight. Reconstruct the itinerary in order,
using ALL tickets exactly once, starting from "JFK".
If multiple valid itineraries → return the lexicographically smallest one
(compare the whole itinerary as a list of strings).
A valid itinerary is guaranteed to exist (may reuse an airport, not a ticket).

  Input:  [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
  Output: ["JFK","MUC","LHR","SFO","SJC"]

Constraints: 1 <= tickets.length <= 300; airport codes are 3 uppercase letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
import heapq
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-28 · ROW 1 — pre-sorted adjacency ──────────────
    def findItinerary_20260828(self, tickets: List[List[str]]) -> List[str]:
        pass

    # ── Attempt · 2026-08-28 · ROW 2 — min-heap ordering ──────────────
    def findItinerary_20260828_minheap(self, tickets: List[List[str]]) -> List[str]:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/332_reconstruct_itinerary.txt — restored at session end (python scripts/restore_history.py)
