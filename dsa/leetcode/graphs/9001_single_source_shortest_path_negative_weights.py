"""
9001. Single Source Shortest Path, Negative Weights   ·   https://open.kattis.com/problems/shortestpath3
Pattern: graphs

You are given a directed graph with `n` nodes numbered 0 to n-1. `edges[i] = [u, v, w]`
is an edge from `u` to `v` with weight `w`. Weights may be negative.

For each node in `queries`, report the minimum distance from the start node `s` to
that node. Return one string per query, in the same order:

    the distance    e.g. "2", when a minimum distance exists
    "Impossible"    when there is no path from s to that node
    "-Infinity"     when there are arbitrarily short paths from s to that node

Example 1:
    Input:  n = 5, s = 0
            edges = [[0,1,999],[1,2,-2],[2,1,1],[0,3,2]]
            queries = [1,3,4]
    Output: ["-Infinity","2","Impossible"]

Example 2:
    Input:  n = 2, s = 0
            edges = [[0,1,-100]]
            queries = [1]
    Output: ["-100"]

Constraints:
    1 <= n <= 1000
    0 <= edges.length <= 5000
    1 <= queries.length <= 100
    0 <= s < n
    -2000 <= w <= 2000

────────────────────────────────────────────────────────────────────────────
Submitting on Kattis (only needed once the method works)

The judge sends several test cases on stdin, one after another. You write the loop
that reads them, calls the method once per test case, and prints the answers.

    One test case:
        line 1          n m q s      (m = number of edges, q = number of queries)
        next m lines    u v w
        next q lines    one queried node per line
    End of input:       a line "0 0 0 0", which is not a test case

    Print one answer per line. The page says: "For clarity, the sample output has a
    blank line between the output for different cases."

    Sample input        Sample output
        5 4 3 0             -Infinity
        0 1 999             2
        1 2 -2              Impossible
        2 1 1
        0 3 2               -100
        1
        3
        4
        2 1 1 0
        0 1 -100
        1
        0 0 0 0

    Limits: CPU time 3 seconds, memory 1024 MB.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:
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