"""
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [aᵢ, bᵢ] indicates that there is an edge between aᵢ and bᵢ in the graph.

Return the number of connected components in the graph.

Example 1:

Input:
n = 5, edges = [[0,1],[1,2],[3,4]]

Output: 2

Example 2:

Input:
n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]

Output: 1

Constraints:

    1 <= n <= 2000
    1 <= edges.length <= 5000
    edges[i].length == 2
    0 <= aᵢ <= bᵢ < n
    aᵢ != bᵢ
    There are no repeated edges.
"""
import collections
from typing import List

class Solution:
    def countComponents_BFS_20260616(self, n: int, edges: List[List[int]]) -> int:
        # first thought is that we iterate through n
        # bfs on each node and mark them as visited as we visit them
        # each time bfs comes back, we basically have a component
        # we should also have an adjMap

        componentCounter = 0

        visited = set()

        adjMap = collections.defaultdict(list)

        for node1, node2 in edges:
            adjMap[node1].append(node2)
            adjMap[node2].append(node1)

        def bfs(node):
            queue = collections.deque()

            queue.append(node)
            
            visited.add(node)

            while queue:
                # pop node from queue
                currentNode = queue.popleft()
                # mark node as visited
                visited.add(currentNode)
                # add neighbors to the queue
                for neighbor in adjMap[currentNode]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        for i in range(n):
            if i not in visited:
                bfs(i)
                componentCounter+=1
        
        return componentCounter
    def countComponents_20260619_UnionFind(self, n: int, edges: List[List[int]]) -> int:
        # union find solution
        # since we are given n nodes, we can say that we started out with n components
        # then we try to merge as many as we can and when we cannot anymore, we decrement component counter
        # then we return the end component counter

        parentMap, rankMap = {}, {}
        componentCounter = n

        # initialize parent and rank maps
        for i in range(n):
            parentMap[i] = i
            rankMap[i] = 0
        
        # path compression
        def findParent(node):
            if node == parentMap[node]:
                return parentMap[node]
            parentMap[node] = findParent(parentMap[node])
            return parentMap[node]
        
        # union by rank
        def unionByRank(node1, node2):
            node1Root = findParent(node1)
            node2Root = findParent(node2)
            if node1Root == node2Root:
                return False
            
            if rankMap[node1Root] > rankMap[node2Root]:
                parentMap[node2Root] = node1Root
            elif rankMap[node2Root] > rankMap[node1Root]:
                parentMap[node1Root] = node2Root
            else:
                # if equal, pick a random one to rank up
                parentMap[node2Root] = node1Root
                rankMap[node1Root] += 1
            return True
        
        for node1, node2 in edges:
            # if we can connect, subtract 1 from component counter
            if unionByRank(node1, node2):
                componentCounter-=1
        
        return componentCounter