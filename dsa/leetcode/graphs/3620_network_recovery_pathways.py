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
import collections
import heapq
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-06 ──────────────
    def findMaxPathScore_20261006(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        # we need maximum possible edge on the path from 0 -> n - 1 under k
        # strangely worded question but essentially we need to find a path that finishes in k
        # keep track of the smallest edge on it and return the maximum of all the runs
        # what this means is we need to do max boundary binary search on the answer
        # lower bound for cost is 0, so our lower bound for answer is also zero
        # we want edge cost to not exceed k, so k is our upper bound
        # then we see if we can achieve with minimum edge weight of m
        # we will do lazy dijkstra with a min heap here
        # so that is min heap, adj map and visited
        
        # we need to do adj_map based on the online first for Dijkstra
        adj_map = collections.defaultdict(list)

        for n1,n2,weight in edges:
            if online[n1] and online[n2]:
                adj_map[n1].append((n2, weight))

        # so we must not use edges smaller than min weight here
        def can_finish_with_edge_weight(min_weight):
            min_heap = []
            distance = [math.inf] * len(online)
            visited = set()
            heapq.heappush(min_heap, (0, 0))
            distance[0] = 0

            # now we go through min_heap and see if we can achieve <= k with min_weight
            while min_heap:
                current_weight, current_node = heapq.heappop(min_heap)
                # if we already populated 
                if current_node in visited:
                    continue
                # we mark as visited
                visited.add(current_node)
                # let's go through the neighbors and update distances as we go
                for neighbor, neighbor_weight in adj_map[current_node]:
                    new_weight = current_weight + neighbor_weight
                    if neighbor in visited or neighbor_weight < min_weight:
                        continue
                    distance[neighbor] = min(distance[neighbor], new_weight)
                    heapq.heappush(min_heap, (new_weight, neighbor))
            
            return distance[len(online) - 1] <= k

        # check if we can even reach with no constraints
        if not can_finish_with_edge_weight(-math.inf):
            return -1

        l, r = 0, k

        while l < r:
            # m is the smallest edge we will allow on this
            m = (l + r + 1) // 2
            if can_finish_with_edge_weight(m):
                l = m
            else:
                r = m - 1
        
        return l

    # ── Attempt 1 · 2026-10-04 ────────────────────────────────────────────
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        # this is just dijkstra's where we find are finding a path from 0 to n - 1 under k
        # only difference here is that we need to check if a node is online before we use it
        # n goes up to 5 * 10^4 so a distance and visited grid would be way too massive
        # this means a min heap dijkstra, specifically a min heap dijkstra without arrays
        # so the bfs-esque dijkstra
        # min heap over a queue, visited set, adj map
        # now issue here is that we need to maximize the weight given multiple paths
        # the way we do this is actually a max boundary binary search on the answer
        # so we need a min and a max for edge weight

        n = len(online)

        max_edge_weight = -math.inf

        adj_map = collections.defaultdict(list)

        # this instantly takes care of the offline issue
        # now all edges going in or out of that node is just not accounted for
        for src,dst,weight in edges:
            if online[src] and online[dst]:
                adj_map[src].append((dst, weight))
                max_edge_weight = max(max_edge_weight, weight)
        
        # now our dijkstra is here to help check if we can reach with this edge cost
        def can_reach_with_edge_weight(min_edge_cost):
            visited = set()
            min_heap = []
            # add in the 0th node with 0 weight. (weight, node)
            heapq.heappush(min_heap,(0,0))
            
            distance = [math.inf] * n
            distance[0] = 0

            while min_heap:
                weight, node = heapq.heappop(min_heap)
                if node in visited:
                    continue
                # mark as visited if not visited
                visited.add(node)

                for neighbor, neighbor_weight in adj_map[node]:
                    # we need min_edge_cost to get to k, if smaller, skip
                    if neighbor_weight < min_edge_cost:
                        continue
                    weight_to_neighbor = weight + neighbor_weight
                    # if new total is more than k, also skip
                    if weight_to_neighbor > k:
                        continue
                    if neighbor not in visited:
                        distance[neighbor] = weight_to_neighbor
                        heapq.heappush(min_heap, (weight_to_neighbor, neighbor))
            
            return distance[n-1] <= k

        # before we even run the check for highest weighted route from 0 to n - 1
        # see if we can even reach n - 1
        
        if not can_reach_with_edge_weight(0):
            return -1

        l, r = 0, max_edge_weight

        while l < r:
            m = (l + r + 1) // 2
            if can_reach_with_edge_weight(m):
                l = m
            else:
                r = m - 1
        
        return l # type: ignore
