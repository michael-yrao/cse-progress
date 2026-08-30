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

    # ── Attempt · 2026-08-29 · ROW 1 — pre-sorted adjacency ──────────────
    def findItinerary_20260829(self, tickets: List[List[str]]) -> List[str]:
        pass

    # ── Attempt · 2026-08-29 · ROW 2 — min-heap ordering ──────────────
    def findItinerary_20260829_minheap(self, tickets: List[List[str]]) -> List[str]:
        # Eulerian Path since we are not guaranteed to finish at our starting vertex
        # we know we traverse starting with JFK
        # Eulerian Path, we want to visit every edge once, so that is our visited set
        # visited set = (startVertex, endVertex) but we are not given that those are unique
        # so maybe just a visited list instead
        # lexicalgraphical order, minHeap to hold the vertices will sort that for us automatically
        # we then need adjacency map so we can push those onto the minHeap
        # actually we just might not need visited if we are popping off the minHeap
        # it basically tells us it is visited, TBD

        adjMap = collections.defaultdict(list)

        for src, dst in tickets:
            heapq.heappush(adjMap[src],dst)

        result = []
        # now that we have an adjMap with the neighbors in lexicographical order
        # go through the edges
        # notice that we end when we hit the final node without any edges
        # DFS until we hit the end
        def dfs(node):
            # we have neighbors for this node, so we push them onto our recursion stack
            while adjMap[node]:
                dfs(heapq.heappop(adjMap[node]))

            # add each node to the result
            result.append(node)

        dfs("JFK")
        result.reverse()
        return result

# ⤵ prior attempts stashed in dsa/leetcode/.history/332_reconstruct_itinerary.txt — restored at session end (python scripts/restore_history.py)
