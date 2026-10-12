"""
9003. Lost Map   ·   https://progressiveoverflow.com/practice/9003
Pattern: graphs
Difficulty: Medium

There are `n` villages, numbered 0 to n-1. Some pairs of villages are joined by a direct
road, and every road has a positive length. There are exactly n-1 roads, and they connect
every village, so there is exactly one way to travel between any two villages.

The map of the roads is lost. All you have is `distances`, an n x n matrix.
`distances[i][j]` is the total length of the roads you travel along to get from village `i`
to village `j`. Most pairs of villages have no direct road, so most entries are a sum of
several road lengths.

Return the n-1 roads. Write each road as `[u, v]`, the two villages it joins. The roads
may be in any order, and a road may list its two villages in either order.

Example 1:
    Input:  distances = [[0,1,1,2],[1,0,2,3],
                        [1,2,0,3],[2,3,3,0]]
    Output: [[0,1],[0,2],[0,3]]
    Explanation: the roads are 0-1 with length 1, 0-2 with
    length 1, and 0-3 with length 2. distances[1][2] is 2
    because the trip from 1 to 2 goes 1 -> 0 -> 2, using two
    roads.

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
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-11 ──────────────
    def lostMap_20261011(self, distances: List[List[int]]) -> List[List[int]]:
        # distances is the full constructed distance map
        # we need to essentially work backwards to get the original roads
        # n nodes and n - 1 roads where every village is connected means the original roads form a MST
        # prim's algorithm or kruskal's algorithm to find the MST
        # we will do prim's today
        # we will construct from nothing and use distance as a validator
        # we need distances array, whether or not we've connected these nodes or not and also relaxing the un-visited nodes
        n = len(distances)

        # we actually need the node that gave us the mst
        # so let's do [distance, from_edge]
        mst_dist = []

        for i in range(n):
            mst_dist.append([math.inf, None])

        mst_dist[0][0] = 0

        visited = [False] * n

        result = []

        def get_smallest_unvisited_node():
            smallest_value = math.inf
            smallest_node = math.inf
            for node in range(n):
                if mst_dist[node][0] < smallest_value and not visited[node]:
                    smallest_value = mst_dist[node][0]
                    smallest_node = node

            return smallest_node

        def relax_relative_to(node):
            # check what is the cheapest from this node to other un-visited and update their smallest so far
            for neighbor in range(n):
                if not visited[neighbor] and distances[node][neighbor] < mst_dist[neighbor][0]:
                    mst_dist[neighbor][0] = distances[node][neighbor]
                    mst_dist[neighbor][1] = node
        
        for _ in range(n):
            next_node = get_smallest_unvisited_node()
            # mark node as visited
            visited[next_node] = True # type: ignore
            # since we connected it, let's add it to MST as well
            if mst_dist[next_node][1] != None: # type: ignore
                result.append([next_node,mst_dist[next_node][1]]) # type: ignore
            relax_relative_to(next_node)

        return result

    # ── Attempt 1 · 2026-10-09 ────────────────────────────────────────────
    def lostMap(self, distances: List[List[int]]) -> List[List[int]]:
        # so we are given the distances array and we are working our way backwards to find the original n - 1 edges
        # looking at n, 2500 is a bit too high for me to try anything with floyd warshall
        # let's see where this distances gets used by dijkstra
        # we typically relax until we get to this point
        # so how do we work backwards. Actually looking at the result, the answer is literally just a MST, so we work out a MST from the distances
        # so we are going to try to build a MST based on what we have
        # distances is a Prim's thing, so we can try to work it out from there
        
        n = len(distances)

        # tells us whether or not we visited this node to the MST yet
        visited = [False] * n

        # tells us the cheapest edge value to the node
        # we also need to keep track of the node getting us to to it for the result
        mst_distances = []

        for _ in range(n):
            mst_distances.append([math.inf, None])

        mst_edges = []
        # our own distances array
        mst_distances[0][0] = 0

        def get_cheapest_unvisited_node():
            return_value = math.inf
            return_index = math.inf
            for i in range(n):
                if not visited[i]:
                    if mst_distances[i][0] < return_value:
                        return_index = i
                        return_value = mst_distances[i][0]
            return return_index

        def relax(node):
            # for all nodes that we haven't visited, relax to node
            for i in range(n):
                if not visited[i]:
                    # if smaller than what we currently have, modify who gave us this edge
                    if distances[node][i] < mst_distances[i][0]:
                    # if we haven't visited yet, update mst_distances if applicable
                        mst_distances[i][0] = min(mst_distances[i][0], distances[node][i])
                        mst_distances[i][1] = node

        for _ in range(n):
            # get the cheapest unvisited node
            cheapest_unvisited_node = get_cheapest_unvisited_node()
            # mark as visited
            visited[cheapest_unvisited_node] = True # type: ignore
            # if not None, we have an optimal edge, add to result
            if mst_distances[cheapest_unvisited_node][1] != None: # type: ignore
                mst_edges.append([cheapest_unvisited_node, mst_distances[cheapest_unvisited_node][1]]) # type: ignore
            # relax everyone in cheapest to this
            relax(cheapest_unvisited_node)

        return mst_edges
