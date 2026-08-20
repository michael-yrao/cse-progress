"""
1584. Min Cost to Connect All Points   ·   https://leetcode.com/problems/min-cost-to-connect-all-points/
Pattern: graphs

You are given an array `points` of integer coordinates on a 2D plane, where
points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the Manhattan distance
between them: |xi - xj| + |yi - yj|.

Return the minimum cost to make all points connected. All points are connected if
there is exactly one simple path between any two points.

Example 1:
    Input:  points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20

Example 2:
    Input:  points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Constraints:
    1 <= points.length <= 1000
    -10^6 <= xi, yi <= 10^6
    All pairs (xi, yi) are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import heapq
import math
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-19 ──────────────
    def minCostConnectPointsKruskal_20260819(self, points: List[List[int]]) -> int:
        # Kruskal's Algorithm - Sort edges, Union Find
        # points only give us the vertices, so we need to calculate 
        # the manhattan distance of every node to every other node
        # this is an O(E) operation
        # we then need to take advantage of graph theory here
        # we are building a MST, so we will have one component at the end
        # what that means given n nodes where n = len(points)
        # we will have n - 1 edges
        # since we are greedily going through the edges using shortest edges
        # we stop when we have connected n - 1 edges
        
        edgeWithWeight = []

        
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                manhattanDistance = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                # [0] = index of source, [1] = index of target, [2] = weight
                edgeWithWeight.append((i, j, manhattanDistance))

        # sort by weight ascending
        edgeWithWeight.sort(key=lambda edge: edge[2])

        # union find based on indices of points

        rankMap = {}
        parentMap = {}

        for i in range(len(points)):
            rankMap[i] = 0
            parentMap[i] = i

        def find(node):
            if parentMap[node] != node:
                parentMap[node] = find(parentMap[node])
            return parentMap[node]
        
        def union(n1,n2):
            n1r = find(n1)
            n2r = find(n2)
            # unioning these two forms a cycle, return false
            if n1r == n2r:
                return False
            if rankMap[n1r] > rankMap[n2r]:
                parentMap[n2r] = n1r
            elif rankMap[n1r] < rankMap[n2r]:
                parentMap[n1r] = n2r
            else:
                rankMap[n1r]+=1
                parentMap[n2r] = n1r
            return True

        # result cost
        cost = 0
        # keep track of number of edges
        edgesUsed = 0

        for srcIndex, tgtIndex, weight in edgeWithWeight:
            # if we have not connected this node yet, connect it
            if find(srcIndex) != find(tgtIndex):
                union(srcIndex, tgtIndex)
                cost+=weight
                edgesUsed+=1
                # if we have n - 1 edges, we have finished our component
                if edgesUsed == len(points) - 1:
                    break

        return cost

    # ── Attempt · 2026-08-11 ──────────────
    def minCostConnectPoints_20260811(self, points: List[List[int]]) -> int:
        # Minimum Spanning Tree, built via Prim's Algorithm
        # Idea is that we are expanding our component to the nearest node that is not yet part of the component
        # So we start with a distance array and relax against the our candidate to be absorbed
        # Visited set will hold nodes that are already part of the component
        # we will use the index as our key here

        distance = [math.inf] * len(points)
        # set our starting point to have distance of 0
        distance[0] = 0

        visited = set()

        def getCandidate():
            candidate = math.inf
            candidateValue = math.inf
            for i in range(len(distance)):
                if i not in visited:
                    if distance[i] < candidateValue:
                        candidate = i
                        candidateValue = distance[i]
            return candidate

        # relax all unvisited nodes relative to candidate
        def relax(candidate):
            for i in range(len(distance)):
                if i not in visited:
                    # calculate distance from i to candidate
                    manhattanDistance = abs(points[candidate][0] - points[i][0]) + abs(points[candidate][1] - points[i][1])
                    distance[i] = min(distance[i], manhattanDistance)

        # while we have not connected all nodes yet
        while len(visited) != len(points):
            # get our candidate to insert into the component
            candidate = getCandidate()
            # add candidate to the visited
            visited.add(candidate)
            # relax distance of all nodes in relation to visited
            relax(candidate)

        # return sum of distance
        return sum(distance) # type: ignore

    # ── Attempt · 2026-08-01 ──────────────
    def minCostConnectPoints_20260801(self, points: List[List[int]]) -> int:
        # connecting all points with minimum cost, min spanning tree
        # Prim's Algorithm
        # we start with the first node, which is the start of our component
        # from here, we want to be greedy and find the closest node to our component
        # add it to our component, then update all unvisited edges if it is smaller than the existing potential edge to attach
        # repeat until we do it for all nodes
        # we will start with distance of infinity to all nodes except our starting node
        # distance[i] represents shortest edge to attach i to the component, so min(distance[i], currentManhattanDistance)
        
        size = len(points)

        distance = [math.inf] * size
        # our starting value will have distance of 0 to itself
        distance[0] = 0

        # i think we still need visited to say what is in the component so far
        visited = set()

        def findNext():
            minValue = math.inf
            minIndex = math.inf
            for i in range(size):
                # we only care for smallest that is not visited
                if i not in visited:
                    if distance[i] < minValue:
                        minValue = distance[i]
                        minIndex = i
            return minIndex
        
        def updateDistance(nodeIndex):
            cx, cy = points[nodeIndex][0], points[nodeIndex][1]
            
            # go through the points that are not yet in visited
            # update distance compared to cx, cy
            for i in range(size):
                if i not in visited:
                    nx, ny = points[i][0], points[i][1]
                    manhattanDistance = abs(cx-nx) + abs(cy-ny)
                    distance[i] = min(distance[i],manhattanDistance)

        # while we have not connected all nodes to the component
        while len(visited) != size:
            # find the smallest distance that is not in visited
            nextNodeIndex = findNext()
            # mark it as visited
            visited.add(nextNodeIndex)
            # update distance of all unvisited nodes relative to nextNodeIndex
            updateDistance(nextNodeIndex)
        
        return sum(distance) # type: ignore

    # ── Attempt · 2026-07-20 ──────────────
    def minCostConnectPoints_20260720(self, points: List[List[int]]) -> int:
        # prim's algorithm to build a MST greedily
        # we will find the closest unvisited node to our visited node set
        # compare all unvisited's distance relative to it, continue until we did this for all nodes
        # we will use indices to help us navigate
        # have a math.inf array and starting node will have 0
        # visited will contain nodes that we have finalized the distance in
        visited = set()
        distance = [math.inf] * len(points)
        distance[0] = 0

        def getClosestNode():
            closestDistance = math.inf
            closestNode = -1
            for i in range(len(points)):
                if i not in visited:
                    if distance[i] < closestDistance:
                        closestDistance = distance[i]
                        closestNode = i
            return closestNode
        
        def relax(index):
            for i in range(len(points)):
                if i not in visited and i != index:
                    x1, y1 = points[i][0], points[i][1]
                    x2, y2 = points[index][0], points[index][1]
                    manhattanDistance = abs(x1-x2) + abs(y1-y2)
                    distance[i] = min(distance[i],manhattanDistance)

        # while we have not found the shortest distance to all nodes
        # relax distance to all unvisited nodes relative to current node
        # current node is closest node to our already visited component
        while len(visited) < len(points):
            nextNode = getClosestNode()
            # if we don't have a next node to visit while we haven't filled visited
            # we return -1
            if nextNode == -1:
                return -1
            # now that we found the next node, relax everyone relative to it
            relax(nextNode)
            # mark nextNode as visited
            visited.add(nextNode)
        
        return sum(distance) # type: ignore

    # ── Attempt · 2026-07-18 ──────────────
    def minCostConnectPoints_20260718(self, points: List[List[int]]) -> int:
        # min spanning tree is the perfect candidate for greedy algorithm
        # we will use an array like we did for bellman ford to indicate all nodes are infinite distance away
        # then we update it as we go through them
        # we need a visited set that tells us whether or not this is the absolute min we can get for this node
        visited = set()

        distance = [math.inf] * len(points)

        # starting at first node, the distance is 0, so we will set it as such
        distance[0] = 0

        def findClosestNode():
            minCost = math.inf
            minNode = -1
            for i in range(len(points)):
                if i in visited:
                    continue
                if distance[i] < minCost:
                    minCost = distance[i]
                    minNode = i
            return minNode
        
        def relax(node):
            for i in range(len(points)):
                # skip finalized nodes
                if i in visited:
                    continue
                x1, y1 = points[node][0], points[node][1]
                x2, y2 = points[i][0], points[i][1]
                manhattanDistance = abs(x1-x2) + abs(y1-y2)
                distance[i] = min(distance[i], manhattanDistance)

        # while we have not finalized all nodes' min
        while len(visited) < len(points):
            # get the closest node that we have not visited yet
            nextNode = findClosestNode()
            # if visited is not len(points) AND we can't find a next node to visit, we can't build a MST
            if nextNode == -1:
                break
            # if we can find a nextNode, add to visited
            visited.add(nextNode)
            # then we relax every other node relative to it
            relax(nextNode)
        
        return sum(distance) # type: ignore

    # ── Attempt 1 · 2026-07-16 ────────────────────────────────────────────
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # so we are the ones to draw the edges here
        # from the example, we can see [2,2] connected to two nodes
        # so idea is that we just do this greedily
        # And this is basically building a minimum spanning tree
        # so working off of another greedy algorithm in Dijkstra's
        # we need a minHeap to help us keep track of of shortest path so (distance, node)
        # technically everything can be connected, so maybe no adj map
        # since to construct the adjMap, it would be very costly
        # visited for marking nodes we've visited


        numberOfNodes = len(points)
        totalCost = 0
        visited = set()

        def manhattanDistance(node1, node2):
            return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

        minHeap = []
        
        heapq.heappush(minHeap,(0,0))

        # while we haven't visited everyone yet
        while len(visited) < numberOfNodes:
            cost, node = heapq.heappop(minHeap)
            # if we already visited the node, we can move on
            if node in visited:
                continue
            # otherwise, add cost to total cost
            totalCost+=cost
            visited.add(node)
            for neighbor in range(numberOfNodes):
                if neighbor not in visited:
                    distance = manhattanDistance(points[node], points[neighbor])
                    heapq.heappush(minHeap, (distance, neighbor))
        return totalCost
