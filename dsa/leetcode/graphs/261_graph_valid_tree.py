"""
Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes), write a function to check whether these edges make up a valid tree.

Example 1:

Input:
n = 5
edges = [[0, 1], [0, 2], [0, 3], [1, 4]]

Output:
true

Example 2:

Input:
n = 5
edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]

Output:
false

Note:

    You can assume that no duplicate edges will appear in edges. Since all edges are undirected, [0, 1] is the same as [1, 0] and thus will not appear together in edges.

Constraints:

    1 <= n <= 100
    0 <= edges.length <= n * (n - 1) / 2
"""
import collections
from typing import List

class Solution:

    # ── Attempt · 2026-08-16 ──────────────
    def validTree_20260816(self, n: int, edges: List[List[int]]) -> bool:
        # today's rep requires us to this using DFS
        # DFS = visited, adjMap
        # undirected acyclic graph with n vertices must have n - 1 edges to make a tree
        # so what we are trying to verify with DFS is that it is connected
        # connected + exactly n - 1 edges = acyclic
        if len(edges) + 1 != n:
            return False

        visited = set()
        adjMap = collections.defaultdict(list)

        for n1, n2 in edges:
            adjMap[n1].append(n2)
            adjMap[n2].append(n1)

        # we can tell a graph is a cycle if we have already visited this node before
        def dfs(node, prevNode):
            if node in visited:
                return
            
            # if we have not visited this node, add it to visited
            visited.add(node)
            # then we go through rest of the neighbors
            for neighbor in adjMap[node]:
                if neighbor != prevNode:
                    dfs(neighbor, node)

        dfs(0,-1)
        
        return len(visited) == n

# ⤵ prior attempts stashed in dsa/leetcode/.history/261_graph_valid_tree.txt — restored at session end (python scripts/restore_history.py)
