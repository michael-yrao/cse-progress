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
    # ── Attempt 1 · 2026-07-22 ────────────────────────────────────────────
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # using only once means we should keep track of edges and not nodes
        # so maybe set of tuple, (from, to)
        # since we should also go in smaller lexical order, I'm also considering using a minHeap
        # so adjMap -> minHeap
        # popping off the heap is kinda us telling us we visited already, so don't need visited set
        # problem tells us our starting node is JFK, so we can work off that as well
        # so is this a DFS or BFS or does it not matter since we cannot revisit edges
        # I will try DFS since I cannot use a queue since I don't know my destination node instantly so I can't initialize my starting node
        
        # string -> minheap
        adjMap = collections.defaultdict(list)
        # construct our minHeap
        for source, destination in tickets:
            heapq.heappush(adjMap[source], destination)
        
        # add JFK to result
        result = []

        # go to the first destination possible from current node
        def dfs(node):
            nonlocal result
            # if node is null or node has no more neighbors
            if not node:
                return
            
            # one important thing to note that the destination with nowhere else to go
            # must be our end
            while adjMap[node]:
                closestNeighbor = heapq.heappop(adjMap[node])
                
                # go to neighbor
                dfs(closestNeighbor)
            # we are popping back from the end, so we need to remember to reverse when we return
            if not adjMap[node]:
                result.append(node)

        dfs("JFK")

        result.reverse()

        return result