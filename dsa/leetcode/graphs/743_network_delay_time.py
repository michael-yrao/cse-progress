"""
743. Network Delay Time   ·   https://leetcode.com/problems/network-delay-time/
Pattern: graphs

You are given a network of n nodes, labeled from 1 to n. You are also given
times, a list of travel times as directed edges times[i] = (ui, vi, wi), where
ui is the source node, vi is the target node, and wi is the time it takes for a
signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for
all the n nodes to receive the signal. If it is impossible for all the n nodes
to receive the signal, return -1.

Example 1:
    Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2

Example 2:
    Input:  times = [[1,2,1]], n = 2, k = 1
    Output: 1

Example 3:
    Input:  times = [[1,2,1]], n = 2, k = 2
    Output: -1

Constraints:
    1 <= k <= n <= 100
    1 <= times.length <= 6000
    times[i].length == 3
    1 <= ui, vi <= n
    ui != vi
    0 <= wi <= 100
    All the pairs (ui, vi) are unique. (i.e., no multiple edges.)
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
import heapq
from typing import List, Optional


class Solution:

    def networkDelayTime_20260715(self, times: List[List[int]], n: int, k: int) -> int:
        # Dijkstra's algorithm is a modified BFS
        # BFS uses visited set, queue and adjacency map
        # Dijkstra uses visited set, min heap and adjacency map
        # queue is good when we know all edges are the same
        # but min heap shines when we have edges of varying positive values
        # our min heap will have (cumulative weight to get to node, node)
        # adjacency map will tell us the immediate weight to get from src -> dst based on input times, it just helps us grab all children of src in O(1) time
        # visited set tells us whether or not we already have the shortest way here
        # since all edges are positive, cumulative distance will always be increasing

        visited = set()
        adjMap = collections.defaultdict(list)
        
        for source, target, time in times:
            adjMap[source].append((target,time))
        
        minHeap = []
        # takes 0 cumulative time to get to starting node so we add it to minHeap to start
        heapq.heappush(minHeap,(0,k))
        # since we know value is always increasing, we can keep track of largest value by just setting it each time. Problem says minimum but it will be the highest value in our heap
        minTime = 0

        while minHeap:
            currentCumulativeTime, currentNode = heapq.heappop(minHeap)
            # if already visited / calculated smallest, we can skip it
            if currentNode in visited:
                continue
            visited.add(currentNode)
            minTime = max(minTime, currentCumulativeTime)
            # since we know currentCumulativeTime is the shortest possible
            # since we are doing 'BFS' and edges are never negative
            # we can add neighbor values to currentCumulativeTime
            for neighborNode, neighborTime in adjMap[currentNode]:
                # if we have not calculated shortest distance here yet
                # calculate it
                if neighborNode not in visited:
                    neighborCumulativeTime = currentCumulativeTime + neighborTime
                    heapq.heappush(minHeap, (neighborCumulativeTime, neighborNode))
        
        if len(visited) != n:
            return -1
        return minTime

    # ── Attempt 1 · 2026-07-13 ────────────────────────────────────────────
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # we can do an adjacency map using times
        # the adjMap can have a -> (b, weight)
        # we use a heap instead of a queue since this is weighted graph
        # hasShortest set to mark the node as visited and already have the shortest possible here

        adjMap = collections.defaultdict(list)
        hasShortest = set()
        minTime = 0

        for source, target, weight in times:
            adjMap[source].append((target,weight))

        minHeap = []
        # k is our starting point so takes 0 weight to get there
        heapq.heappush(minHeap,(0,k))

        while minHeap:
            cumulativeWeightToNode, node = heapq.heappop(minHeap)
            # if we already have shortest path for this node, we can skip it
            if node in hasShortest:
                continue
            # if we have not, add it to visited
            hasShortest.add(node)
            
            # since weight is always accumulating, we can just set minTime to weight
            # because the cumulative weight will always be the latest largest we've seen
            minTime = cumulativeWeightToNode

            # push neighbors into the heap
            for neighborNode, neighborWeight in adjMap[node]:
                if neighborNode not in hasShortest:
                    heapq.heappush(minHeap,(neighborWeight + cumulativeWeightToNode, neighborNode))
        
        # if we have shortest distance to all nodes, return minTime
        if len(hasShortest) == n:
            return minTime
        return -1
