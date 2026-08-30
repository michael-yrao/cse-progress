"""
332. Reconstruct Itinerary   ·   https://leetcode.com/problems/reconstruct-itinerary/
Pattern: graphs

tickets[i] = [from_i, to_i] = one flight. Reconstruct the itinerary in order,
using ALL tickets exactly once, starting from "JFK".
If multiple valid itineraries → return the lexicographically smallest one
(compare the whole itinerary as a list of strings).
A valid itinerary is guaranteed to exist (may reuse an airport, not a ticket).

  Input:  [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
  Output: ["JFK","MUC","LHR","SFO","SJC"]

Constraints: 1 <= tickets.length <= 300; airport codes are 3 uppercase letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
import heapq
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-29 · ROW 1 — pre-sorted adjacency ──────────────
    def findItinerary_20260829(self, tickets: List[List[str]]) -> List[str]:
        pass

    # ── Attempt · 2026-08-29 · ROW 2 — min-heap ordering ──────────────
    def findItinerary_20260829_minheap(self, tickets: List[List[str]]) -> List[str]:
        # Eulerian Path since we are not guaranteed to finish at our starting vertex
        # we know we traverse starting with JFK
        # Eulerian Path, we want to visit every edge once, so that is our visited set
        # visited set = (startVertex, endVertex) but we are not given that those are unique
        # so maybe just a visited list instead
        # lexicalgraphical order, minHeap to hold the vertices will sort that for us automatically
        # we then need adjacency map so we can push those onto the minHeap
        # actually we just might not need visited if we are popping off the minHeap
        # it basically tells us it is visited, TBD

        adjMap = collections.defaultdict(list)

        for src, dst in tickets:
            heapq.heappush(adjMap[src],dst)

        result = []
        # now that we have an adjMap with the neighbors in lexicographical order
        # go through the edges
        # notice that we end when we hit the final node without any edges
        # DFS until we hit the end
        def dfs(node):
            # we have neighbors for this node, so we push them onto our recursion stack
            while adjMap[node]:
                dfs(heapq.heappop(adjMap[node]))

            # add each node to the result
            result.append(node)

        dfs("JFK")
        result.reverse()
        return result

    # ── Attempt · 2026-08-18 ──────────────
    def findItinerary_20260818(self, tickets: List[List[str]]) -> List[str]:
        # Eulerian 
        # we use a stack to trace current path of the vertices and find dead ends
        # we pop off the stack when this node gets stuck, aka all neighbors visited
        stack = []

        # we have to do lexicographical order, so since we are not doing minHeap method
        # we need to sort the input before mapping so we go by lexicographical order
        tickets.sort(reverse=True)
        
        adjMap = collections.defaultdict(list)

        for src, tgt in tickets:
            adjMap[src].append(tgt)
        
        # we know we start with JFK so we put JFK onto the stack
        
        stack.append("JFK")

        result = []
        # while we still have nodes in the stack to visit, we keep going
        while stack:
            currentNode = stack[-1]
            # if no neighbors left for current node
            # it means we hit a dead end and this node is elligible
            # to go onto the result
            if not adjMap[currentNode]:
                result.append(stack.pop())
            else:
                # otherwise, add its neighbor to the stack
                neighbor = adjMap[currentNode].pop()
                stack.append(neighbor)

        result.reverse()

        return result

    # ── Attempt · 2026-08-14 ──────────────
    def findItinerary_20260814(self, tickets: List[List[str]]) -> List[str]:
        # this is not Dijkstra's, we don't have a destination nor edge weight
        # notice that we do try to do lexicographical order
        # we start with JFK and the ending node must have nowhere else to go
        # this looks like DFS, get to end node first then take care of call stack
        # adjacency map, visited holds edges not nodes and needs to be a minHeap
        # the minHeap takes care of our lexicographical issue

        adjMap = collections.defaultdict(list)
        result = []
        
        for src, dst in tickets:
            heapq.heappush(adjMap[src], dst)

        def dfs(node):
            # we are trying to find our end node
            # so if no more neighbors, that is the end
            if not adjMap[node]: 
                result.append(node)
                return
            
            # while we have neighbors we visited
            while adjMap[node]:
                neighbor = heapq.heappop(adjMap[node])
                dfs(neighbor)
            result.append(node)
        
        dfs("JFK")
        result.reverse()
        return result

    # ── Attempt · 2026-08-04 ──────────────
    def findItinerary_20260804(self, tickets: List[List[str]]) -> List[str]:
        # the most important thing to note here is that the final node has nowhere else to go
        # so what we can do is get to the end and construct backwards to the start
        # so this reads like variation of DFS
        # we have a starting node, we need to build an adj map
        # and we also need visited
        # this also looks like we are storing edges in visited, not nodes
        # missed the lexical order completely, we need a minheap for it
        # so our adjacency map will be a minHeap

        adjMap = collections.defaultdict(list)

        for src, dst in tickets:
            heapq.heappush(adjMap[src], dst)

        result = []

        def dfs(node):
            nonlocal result
            # we go back when we have nowhere else to go
            if not adjMap[node]:
                result.append(node)
                return

            while adjMap[node]:
                closestNeighbor = heapq.heappop(adjMap[node])
                dfs(closestNeighbor)
            
            # this is our postorder traversal here
            result.append(node)
        
        dfs("JFK")
        result.reverse()
        return result

    # ── Attempt · 2026-07-28 ──────────────
    def findItinerary_20260728(self, tickets: List[List[str]]) -> List[str]:
        # Eulerian Path = visit all edges once - Hierholzer's
        # Hamiltonian Path = visit all nodes once
        # we are marking edges as visited not nodes, so this is Eulerian
        # We know the starting location of JFK
        # for adjMap, do string -> minHeap to get smallest lexical ordering
        # DFS since we don't want to push all neighbors of JFK (e.g. example 2)
        # One very important detail to note is that what happens when there is nowhere to go
        # Since we know we must form a valid itinerary, this node must be the end
        # so we should append backwards on the DFS
        # [["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]
        result = []

        adjMap = collections.defaultdict(list)

        # construct the adjacency map
        for source, destination in tickets:
            heapq.heappush(adjMap[source], destination)
        
        def dfs(node):
            # exhaust every ticket out of a node, then append the node itself
            # first node to run out = last stop, so the list builds end-to-front
            # on the way back up the stack, push leftover tickets into the result
            while adjMap[node]:
                currentChild = heapq.heappop(adjMap[node])
                # go as deep as we can here
                dfs(currentChild)
            # now when we are back here, we are the last node of this DFS
            # so we add ourselves to the result
            result.append(node)

        dfs("JFK")
        result.reverse()
        return result

    # ── Attempt 1 · 2026-07-22 ────────────────────────────────────────────
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # using only once means we should keep track of edges and not nodes
        # so maybe set of tuple, (from, to)
        # since we should also go in smaller lexical order, I'm also considering using a minHeap
        # so adjMap -> minHeap
        # popping off the heap is kinda us telling us we visited already, so don't need visited set
        # problem tells us our starting node is JFK, so we can work off that as well
        # so is this a DFS or BFS or does it not matter since we cannot revisit edges
        # I will try DFS since I cannot use a queue since I don't know my destination node instantly so I can't initialize my starting node
        
        # string -> minheap
        adjMap = collections.defaultdict(list)
        # construct our minHeap
        for source, destination in tickets:
            heapq.heappush(adjMap[source], destination)
        
        # add JFK to result
        result = []

        # go to the first destination possible from current node
        def dfs(node):
            nonlocal result
            # if node is null or node has no more neighbors
            if not node:
                return
            
            # one important thing to note that the destination with nowhere else to go
            # must be our end
            while adjMap[node]:
                closestNeighbor = heapq.heappop(adjMap[node])
                
                # go to neighbor
                dfs(closestNeighbor)
            # we are popping back from the end, so we need to remember to reverse when we return
            if not adjMap[node]:
                result.append(node)

        dfs("JFK")

        result.reverse()

        return result
