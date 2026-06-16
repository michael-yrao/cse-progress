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
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # so we basically need to return whether or not this has a cycle
        # [[0,1],[1,2],[2,0]] would be invalid because 2 leads back to 0
        # so we can have a visited set and do adjacency map based on the input
        # we also need to verify all nodes are traversed since a disconnected node also means not a tree

        # visited means we have already gone this route 
        # so we need to dfs on currentNode, parentNode
        # this way we know which direction we went
        visited = set()
        
        adjMap = collections.defaultdict(list)
        
        # notice that this is bidirectional
        # so we have to do adjMap both ways
        for firstNode, secondNode in edges:
            adjMap[firstNode].append(secondNode)
            adjMap[secondNode].append(firstNode)
        
        def dfs(currentNode, parentNode):
            # if we have seen this node, we are in a cycle thus return False
            if currentNode in visited:
                return False

            # if we haven't seen this node yet
            # let's add it to visited
            visited.add(currentNode)

            # now let's take a look at its neighbors
            for neighbor in adjMap[currentNode]:
                # neighbor will always have the same pair the opposite way
                # so we need to ignore that one
                if neighbor == parentNode:
                    continue
                if not dfs(neighbor, currentNode):
                    return False
            return True
                    
        return dfs(0,-1) and len(visited) == n