"""

MEDIUM

Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

 

Test case format:

For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.

An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.

 

Example 1:

Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation: There are 4 nodes in the graph.
1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).

Example 2:

Input: adjList = [[]]
Output: [[]]
Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.

Example 3:

Input: adjList = []
Output: []
Explanation: This an empty graph, it does not have any nodes.

 

Constraints:

    The number of nodes in the graph is in the range [0, 100].
    1 <= Node.val <= 100
    Node.val is unique for each node.
    There are no repeated edges and no self-loops in the graph.
    The Graph is connected and all nodes can be visited starting from the given node.

"""

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

import collections
from typing import Optional
class Solution:

    # ── Attempt · 2026-08-09 ──────────────
    def cloneGraph_20260809(self, node: Optional['Node']) -> Optional['Node']:
        # we know this is connected, so we can do one node at a time
        # use either BFS or DFS and create one node at a time where we have an old to new map

        if not node:
            return None

        oldToNewMap = {}
        queue = collections.deque()
        queue.append(node)
        newNode = Node(node.val)
        oldToNewMap[node] = newNode

        while queue:
            oldNode = queue.popleft()
            for neighbor in oldNode.neighbors:
                if neighbor not in oldToNewMap:
                    newNeighborNode = Node(neighbor.val)
                    oldToNewMap[neighbor] = newNeighborNode
                    queue.append(neighbor)
                oldToNewMap[oldNode].neighbors.append(oldToNewMap[neighbor])

        return newNode

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # ok so to do a deep copy, we need to do completely new nodes of each
        # and then after we do copy with newNode = Node(old.val, old.neighbors)
        # we need to be able to traverse through old.neighbors and give them to the newNode
        # so we have to a visited set?
        # or we have a map of old -> new node so that we can track neighbors
        # so what is our dfs going to accomplish
        # 

        oldToNew = {}

        def dfs(oldNode):
            # if we already visited and created a copy of this node, exit
            if oldNode in oldToNew:
                return oldToNew[oldNode]

            # now that we know we are visiting a new node
            # we need to create a copy
            newNode = Node(oldNode.val)

            # map oldNode to newNode
            oldToNew[oldNode] = newNode

            # create copies of oldNode's neighbors and put them as newNode's neighbors
            for neighbor in oldNode.neighbors:
                newNode.neighbors.append(dfs(neighbor))

            return newNode
    
        return dfs(node)
