"""
9001. Single Source Shortest Path, Negative Weights   ·   https://progressiveoverflow.com/practice/9001
Pattern: graphs
Difficulty: Medium

You are given a directed graph with `n` nodes numbered 0 to n-1. `edges[i] = [u, v, w]`
is an edge from `u` to `v` with weight `w`. Weights may be negative.

For each node in `queries`, report the minimum distance from the start node `s` to
that node. Return one number per query, in the same order:

    the distance    e.g. 2, when a minimum distance exists
    math.inf        when there is no path from s to that node
    -math.inf       when there are arbitrarily short paths from s to that node

Example 1:
    Input:  n = 5, s = 0
            edges = [[0,1,999],[1,2,-2],[2,1,1],[0,3,2]]
            queries = [1,3,4]
    Output: [-math.inf, 2, math.inf]

Example 2:
    Input:  n = 2, s = 0
            edges = [[0,1,-100]]
            queries = [1]
    Output: [-100]

Constraints:
    1 <= n <= 1000
    0 <= edges.length <= 5000
    1 <= queries.length <= 100
    0 <= s < n
    -2000 <= w <= 2000
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-03 ──────────────
    def singleSourceShortestPathNegativeWeights_20261003(self, n: int, edges: List[List[int]], s: int, queries: List[int]) -> List[int]:
        # shortest path with negative weights with 1000 nodes and edges of 5000 means this should be bellman ford
        # with bellman ford, we go through the edges n - 1 times. This should give us the best possible route to all nodes
        # with example 1, we can see there is a cycle, so what we can do is run n - 1 more times to see if the min changed. if it did, that means there is a cycle and any nodes involved in the cycle will always be infinitely decreasing
        
        distance = [math.inf] * n
        # distance from src to src is zero
        distance[s] = 0

        # n - 1 and not n because no cycle means n - 1 edges
        for _ in range(n - 1):
            working_distance = distance.copy()
            for src,dst,weight in edges:
                if distance[src] == math.inf:
                    continue
                if distance[src] + weight < working_distance[dst]:
                    working_distance[dst] = distance[src] + weight
            distance = working_distance

        # now that we have the smallest for all assuming no cycles
        # let's check for cycles

        # if there are cycles, we could go around all n nodes, so let's do n cycles
        for _ in range(n):
            working_distance = distance.copy()
            for src,dst,weight in edges:
                # if still decreasing, cycle
                if distance[src] + weight < working_distance[dst]:
                    working_distance[src] = -math.inf
                    working_distance[dst] = -math.inf
            distance = working_distance

        result = []

        for query_dst in queries:
            result.append(distance[query_dst])

        return result

    # ── Attempt 1 · 2026-10-01 ────────────────────────────────────────────
    def singleSourceShortestPathNegativeWeights(self, n: int, edges: List[List[int]], s: int, queries: List[int]) -> List[int]:
        # we have negative edges so I want to use bellman ford here
        # so for bellman ford, what we are doing is have a distance array where we have a working copy
        # we then try to make one move on working copy and set distance to working copy each round
        # we are given s as our starting node so distance to s is 0
        # since we are not given a constraint on how many trips we can take, we do standard n - 1
        # standard n - 1 is derived from the fact that the shortest path, if it exists, takes at most n - 1 edges
        # one thing we need to notice here is the cycle in example 1. we need to do cycle detection

        query_results = []

        distance = [math.inf] * n
        distance[s] = 0

        for _ in range(n - 1):
            working_distance = distance.copy()
            # go through edges and try to relax relative to these edges
            for src, dst, weight in edges:
                if distance[src] == math.inf:
                    continue
                if distance[src] + weight < working_distance[dst]:
                    working_distance[dst] = distance[src] + weight
            distance = working_distance

        # now that we have gone through all the edges, all the distance should be finalized
        # if they still change, that means there is a cycle and all nodes involved in that is marked as such

        working_distance = distance.copy()

        for _ in range(n):
            working_distance = distance.copy()
            for src, dst, weight in edges:
                # this shouldn't happen, if it does, we mark both as cycles
                if distance[src] + weight < working_distance[dst]:
                    working_distance[dst] = -math.inf
                    working_distance[src] = -math.inf
            distance = working_distance

        for query_dst in queries:
            query_results.append(distance[query_dst])

        return query_results
