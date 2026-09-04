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

    # ── Attempt · 2026-09-03 ──────────────
    def networkDelayTime_20260903(self, times: List[List[int]], n: int, k: int) -> int:
        # this is literally Dijkstra's, asking for min time to travel to all nodes
        # so we do minHeap, visited set and an adjacency map
        # big diff is that we mark visited when we pop out of the heap
        
        totalTime = 0
        
        # construct and initialize our adjMap
        adjMap = collections.defaultdict(list)

        for source, target, time in times:
            adjMap[source].append((target,time))
        
        # construct and initialize our minHeap
        minHeap = []

        # start node costs 0
        heapq.heappush(minHeap,(0,k))

        visited = set()
        
        # while we have nodes to traverse, we go through it
        while minHeap:
            currentWeight, currentNode = heapq.heappop(minHeap)
            # if we have not visited yet, mark as visited and increment value
            if currentNode not in visited:
                # mark as visited
                visited.add(currentNode)
                # currentWeight needs to be cumulative
                totalTime = currentWeight
                for neighborNode, neighborWeight in adjMap[currentNode]:
                    if neighborNode not in visited:
                        heapq.heappush(minHeap, ((currentWeight + neighborWeight),neighborNode))
        
        if len(visited) == n:
            return totalTime
        return -1

    # ── Attempt · 2026-08-24 ──────────────
    def networkDelayTime_20260824(self, times: List[List[int]], n: int, k: int) -> int:
        # min time to visit all nodes where w is positive = dijkstra's
        # minHeap, visited and adjMap
        # there is a chance we can't hit all nodes, so we need to check visited size later
        
        # build adjMap
        adjMap = collections.defaultdict(list)

        for src, dst, weight in times:
            adjMap[src].append((dst, weight))

        # visited and minHeap
        visited = set()
        minHeap = []

        # start node is given to us as k
        # weight to self is zero
        heapq.heappush(minHeap, (0,k))

        cumulativeWeight = 0
        while minHeap:
            # go in waves
            lenHeap = len(minHeap)
            for _ in range(lenHeap):
                # currentWeight, currentNode
                # do note that we want the total, so we should keep currentWeight as cumulative
                # we can be greedy here and just pop if it's already visited
                # since we know we are visiting smallest first via minHeap
                currentWeight, currentNode = heapq.heappop(minHeap)
                # key diff between BFS and Dijkstra
                # Dijkstra = mark visited on popping from minHeap
                # BFS = mark visited on push into queue
                if currentNode not in visited:
                    # mark as visited
                    visited.add(currentNode)
                    # update weight
                    cumulativeWeight = currentWeight
                    # now we get neighbors 
                    for neighbor, neighborWeight in adjMap[currentNode]:
                        neighborCumulativeWeight = currentWeight + neighborWeight
                        heapq.heappush(minHeap, (neighborCumulativeWeight, neighbor))
        
        if len(visited) == n:
            return cumulativeWeight
        return -1

    # ── Attempt · 2026-08-14 ──────────────
    def networkDelayTime_20260814(self, times: List[List[int]], n: int, k: int) -> int:
        # Dijkstra's Algorithm
        # Differences between Dijkstra and BFS
        # Dijkstra: Min Heap, adjMap, add to visited set when node comes off the heap 
        # since first pop is the shortest, thus greedy shortest path algorithm
        # BFS: Queue, adjMap, add to visited set when node enters the queue
        # min time to reach all means total
        totalTime = 0

        adjMap = collections.defaultdict(list)

        for src, dst, weight in times:
            adjMap[src].append((dst,weight))
        
        # weight to starting node is zero
        minHeap = []
        heapq.heappush(minHeap, (0, k))
        visited = set()
            
        # while we are still able to visit nodes, let's visit them
        while minHeap:
            currentCumulativeWeight, currentNode = heapq.heappop(minHeap)
            if currentNode in visited:
                continue
            totalTime = currentCumulativeWeight
            visited.add(currentNode)
            # let's visit currentNode's neighbors
            for neighbor, neighborWeight in adjMap[currentNode]:
                if neighbor not in visited:
                    newCumulativeWeight = currentCumulativeWeight + neighborWeight
                    heapq.heappush(minHeap,(newCumulativeWeight, neighbor))
        
        if len(visited) == n:
            return totalTime
        return -1

    # ── Attempt · 2026-08-04 ──────────────
    def networkDelayTime_20260804(self, times: List[List[int]], n: int, k: int) -> int:
        # k is our starting node
        # edges are weighted and directed
        # we are looking for min time to all nodes, which is just dijkstra's
        # dijkstra = min heap, visited, adjmap
        # dijkstra minHeap stores total distance to node

        adjMap = collections.defaultdict(list)
        minHeap = []
        visited = set()

        for src, dst, weight in times:
            adjMap[src].append((dst, weight))

        # distance to start is zero
        heapq.heappush(minHeap, (0, k))

        totalTime = 0

        # while we can still traverse the nodes, we continue
        while minHeap:
            currentWeight, currentNode = heapq.heappop(minHeap)
            if currentNode in visited:
                continue
            totalTime = currentWeight
            visited.add(currentNode)
            for neighbor, weight in adjMap[currentNode]:
                timeToNeighbor = currentWeight + weight
                heapq.heappush(minHeap,(timeToNeighbor,neighbor))
        
        if len(visited) == n:
            return totalTime
        return -1

    # ── Attempt · 2026-07-25 ──────────────
    def networkDelayTime_20260725(self, times: List[List[int]], n: int, k: int) -> int:
        # directed graph, edges are also weighted, so not standard DFS/BFS
        # we are looking for min time to reach all edges, min time is the whole crux of Dijkstra
        # Dijkstra is essentially BFS for weighted nonnegative edges, so we use min heap as our queue
        # we still use adjacency map where it tells our immediate neighbor's cost
        # so we will do source -> list of (dest, cost)
        # we also still use a visited set to tell us when we have visited somewhere
        # and have confirmed it is the shortest
        # we should also note that since we are n 
        minTime = 0
        visited = set()
        minHeap = []
        
        adjMap = collections.defaultdict(list)
        
        for source, destination, weight in times:
            adjMap[source].append((destination, weight))
        
        # we are also given that we start at k, we we put that on the minHeap
        # weight to reach it is 0, so we add (0, k)
        # we also have to note that we are adding total weight to the minHeap
        heapq.heappush(minHeap, (minTime, k))

        while minHeap:
            currentTime, currentNode = heapq.heappop(minHeap)
            # since we add to visited on pop, we need to check if we've already calc'd shortest
            if currentNode in visited:
                continue
            # we are looking for min time but we have to visit everything
            # so we update minTime accordingly each time we visit somewhere
            # the last node should be the 'min' time
            minTime = currentTime
            visited.add(currentNode)
            # check neighbors
            for neighborDestination, neighborWeight in adjMap[currentNode]:
                neighborWeight = currentTime + neighborWeight
                if neighborDestination not in visited:
                    heapq.heappush(minHeap, (neighborWeight, neighborDestination))
        
        if len(visited) != n:
            return -1
        return minTime

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
