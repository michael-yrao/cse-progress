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
        mst_distances = [[math.inf, None]] * n

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