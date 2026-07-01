"""
In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.

Example 1:

Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]

Example 2:

Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]

Constraints:

    n == edges.length
    3 <= n <= 1000
    edges[i].length == 2
    1 <= ai < bi <= edges.length
    ai != bi
    There are no repeated edges.
    The given graph is connected.
"""
from typing import List

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # trees are connected and have no cycles
        # so we are trying to find an edge to remove that makes this graph a tree
        # if multiple are found, we found the latest in the list
        # we are basically just doing cycle finding and then remove last edge that causes the cycle
        # disjoint sets / union find to find cycles in a graph
        # since we know we started with a tree with n edges, we know we started with n - 1 nodes
        # we added one edge to make a cycle, so we know this problem has n edges and n nodes
        # union find: for all the nodes, we connect the nodes to the root parent 
        # (union by rank and path compression) - Time complexity of O(α(n)), inverse Ackerman function
        # Union by Rank and Path Compression both aim to compress the linked list from naive union find
        # Union by Rank - pre-emptively attacks the linked list problem
        # Path Compression - reacts to the linked list problem after the fact
        
        numberOfNodes = len(edges)
        
        # node -> parent mapping
        # start by setting the current node's parent to itself
        # base case for union find before we go through each edge
        # the node is its own isolated component
        parentMap = {}
        rankMap = {}
        
        # 1 -> numberOfNodes + 1 since the problem starts with node 1 and not node 0
        for i in range(1,numberOfNodes+1):
            parentMap[i] = i
        
        # union by rank, start with a rank of 0 for everything
        # node -> rank mapping
        for i in range(1,numberOfNodes+1):
            rankMap[i] = 0
        
        # find the root of node
        def find(node):
            # if node is its own parent
            # we return parent node, this is base case of union find
            if node == parentMap[node]:
                return parentMap[node]
            # otherwise, we find the root of this node until we get to the starting root
            parentMap[node] = find(parentMap[node])
            return parentMap[node]
            
        # merges two nodes together
        # returns True for successful merge
        # returns False for bad merge, e.g. cycle found
        def union(node1, node2):
            node1Root = find(node1)
            node2Root = find(node2)
            if node1Root == node2Root:
                return False
            
            # if either ranks higher, we will compress by 
            # setting the parent of the lower rank to the higher rank
            if rankMap[node1Root] < rankMap[node2Root]:
                parentMap[node1Root] = node2Root
            elif rankMap[node2Root] < rankMap[node1Root]:
                parentMap[node2Root] = node1Root
            else:
                # same level, we'll just preemptively set one higher rank
                parentMap[node2Root] = node1Root
                rankMap[node1Root] += 1
            return True
        
        for node1, node2 in edges:
            # if union was unsuccessful
            if not union(node1, node2):
                return [node1, node2]
        
        return []

    def findRedundantConnection_20260622(self, edges: List[List[int]]) -> List[int]:
        # trees are connected and have no cycles
        # we also already know this has a redundant connection, so we don't really need to check if n nodes have n - 1 edges
        # so we will just straight up do union find and return the first set we see that gives the merge issue, which should be the last edge as indicated in the description
        # we are also given n == edges.length
        # node starts at 1 and not 0, so small thing there

        parentMap, rankMap = {}, {}

        # set parent to self
        # set rank to 0
        for i in range(1,len(edges)+1):
            parentMap[i] = i
            rankMap[i] = 0
        
        # find root parent of input node
        def findParent(node):
            if node == parentMap[node]:
                return parentMap[node]
            parentMap[node] = findParent(parentMap[node])
            return parentMap[node]
        
        # see if we are able to connect the nodes without creating a cycle
        def union(node1, node2):
            node1Root = findParent(node1)
            node2Root = findParent(node2)
            # if same parent, we will have a cycle by connecting
            if node1Root == node2Root:
                return False
            # otherwise, we connect the nodes by rank
            if rankMap[node1Root] > rankMap[node2Root]:
                parentMap[node2Root] = node1Root
            elif rankMap[node1Root] < rankMap[node2Root]:
                parentMap[node1Root] = node2Root
            else:
                # pick at random and promote at random
                parentMap[node2Root] = node1Root
                rankMap[node1Root]+=1
            return True
        
        for node1, node2 in edges:
            if not union(node1, node2):
                return [node1, node2]
        
        return []
    def findRedundantConnection_20260701_UF(self, edges: List[List[int]]) -> List[int]:
        # so we know this is a tree with one extra edge
        # so len(edges) = n
        # we also look to start our edges from 1
        n = len(edges)
        parentMap, rankMap = {}, {}
        # start from 1
        for i in range(1,n+1):
            parentMap[i] = i
            rankMap[i] = 0
        
        def find(node):
            if parentMap[node] != node:
                parentMap[node] = find(parentMap[node])
            return parentMap[node]

        def union(n1,n2):
            n1r = find(n1)
            n2r = find(n2)
            if n1r == n2r:
                return False
            if rankMap[n1r] > rankMap[n2r]:
                parentMap[n2r] = n1r
            elif rankMap[n1r] < rankMap[n2r]:
                parentMap[n1r] = n2r
            else:
                # pick at random
                parentMap[n2r] = n1r
                rankMap[n1r]+=1
            return True
        
        # now we go through each node and find which one unsuccessfully unions without giving us a cycle
        for n1, n2 in edges:
            if not union(n1,n2):
                return [n1,n2]
        
        return None # type: ignore