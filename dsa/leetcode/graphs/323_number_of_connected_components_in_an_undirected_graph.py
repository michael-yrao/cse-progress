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
    
    def countComponents_20260622(self, n: int, edges: List[List[int]]) -> int:
        # with BFS method, we would loop through the n nodes
        # we would increment counter each time we enter the BFS
        # mark each node as visited as we go through there
        # we also need an adjMap to indicate the neighbors of these nodes

        componentCounter = 0
        visited = set()
        adjMap = collections.defaultdict(list)

        for node1, node2 in edges:
            adjMap[node1].append(node2)
            adjMap[node2].append(node1)

        queue = collections.deque()

        for i in range(n):
            # if never visited
            # add i to our visited list
            if i not in visited:
                visited.add(i)
                queue.append(i)

                while queue:
                    currentNode = queue.popleft()
                    for neighbor in adjMap[currentNode]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                componentCounter+=1
        
        return componentCounter
    
    def countComponents_20260629(self, n: int, edges: List[List[int]]) -> int:
        # for this problem using the union find approach
        # we want to keep track of number of components
        # to start, we have n and as we successfully union, we subtract

        numberOfComponents = n

        rankMap, parentMap = {}, {}

        for i in range(n):
            rankMap[i] = i
            parentMap[i] = i
        
        def find(node):
            if parentMap[node] != node:
                parentMap[node] = find(parentMap[node])
            return parentMap[node]
        
        def union(node1, node2):
            n1r = find(node1)
            n2r = find(node2)
            if n1r == n2r:
                return False
            if rankMap[n1r] > rankMap[n2r]:
                parentMap[n2r] = n1r
            elif rankMap[n1r] < rankMap[n2r]:
                parentMap[n1r] = n2r
            else:
                parentMap[n2r] = n1r
                rankMap[n1r]+=1
            return True
        
        for n1, n2 in edges:
            if union(n1,n2):
                numberOfComponents-=1
        
        return numberOfComponents

    def countComponents_20260702_DFS(self, n: int, edges: List[List[int]]) -> int:
        # DFS solution
        # we basically want to go through the n nodes and run DFS/BFS with adjacency map
        # we increment counter when we finish a DFS/BFS
        # the purpose of the DFS is to mark the component as visited

        visited = set()
        adjMap = collections.defaultdict(list)
        counter = 0

        for n1, n2 in edges:
            adjMap[n1].append(n2)
            adjMap[n2].append(n1)
        
        def dfs(node):
            # return if null or visited
            if node in visited:
                return 0
            # not empty, so we want to mark as visited
            visited.add(node)
            # visit neighbors of this guy
            for neighbor in adjMap[node]:
                if neighbor not in visited:
                    dfs(neighbor)
            return 1
            
        for i in range(n):
            if i not in visited:
                counter+=dfs(i)

        return counter