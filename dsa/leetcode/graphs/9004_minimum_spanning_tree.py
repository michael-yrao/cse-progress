"""
9004. Minimum Spanning Tree   ·   https://progressiveoverflow.com/practice/9004
Pattern: graphs
Difficulty: Medium

You are given an undirected graph with `n` nodes numbered 0 to n-1. `edges[i] = [u, v, w]`
is an edge between `u` and `v` with weight `w`. Weights may be negative.

Find a minimum spanning tree of the graph. Return `[cost, tree_edges]`:

    cost         the total weight of the tree
    tree_edges   the tree's edges, each written `[x, y]`
                 with x < y, listed in ascending order
                 (by x, then by y)

If the graph has no spanning tree, return `None`.

Example 1:
    Input:  n = 4
            edges = [[0,1,1],[1,2,2],[1,3,3],[2,3,0]]
    Output: [3, [[0,1],[1,2],[2,3]]]

Example 2:
    Input:  n = 2
            edges = [[0,1,100]]
    Output: [100, [[0,1]]]

Example 3:
    Input:  n = 3
            edges = []
    Output: None

Constraints:
    1 <= n <= 20000
    0 <= edges.length <= 30000
    -20000 <= w <= 20000

Every stored case here has distinct edge weights, so its answer is unique.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).

from typing import List, Optional

# ── Attempt 1 · 2026-10-02 ────────────────────────────────────────────
class UF:
    def __init__(self, n):
        self.numComponents = n
        self.parentMap = {}
        self.rankMap = {}

        for i in range(n):
            self.parentMap[i] = i
            self.rankMap[i] = 0

    def find(self,node):
        if self.parentMap[node] != node:
            self.parentMap[node] = self.find(self.parentMap[node])
        return self.parentMap[node]

    def union(self,n1,n2):
        n1r, n2r = self.find(n1), self.find(n2)
        # forms cycle
        if n1r == n2r:
            return False
        if self.rankMap[n1r] > self.rankMap[n2r]:
            self.parentMap[n2r] = n1r
        elif self.rankMap[n1r] < self.rankMap[n2r]:
            self.parentMap[n1r] = n2r
        else:
            self.rankMap[n1r]+=1
            self.parentMap[n2r] = n1r
        self.numComponents-=1
        return True

class Solution:
    def minimumSpanningTree(self, n: int, edges: List[List[int]]) -> Optional[List]:
        # since we already have edges here, this is Kruskal's MST
        # so we sort and do UF
        # the scenario where we cannot do a MST is when not all nodes are connected
        
        edges.sort(key=lambda edge:edge[2])

        uf = UF(n)
        
        result_edges = []
        total_weight = 0
        
        for n1, n2, weight in edges:
            if uf.union(n1,n2):
                total_weight+=weight
                if n1 < n2:
                    result_edges.append([n1,n2])
                else:
                    result_edges.append([n2,n1])

        if uf.numComponents == 1:
            result = []
            result_edges.sort()
            result.append(total_weight)
            result.append(result_edges)
            return result
        return None
