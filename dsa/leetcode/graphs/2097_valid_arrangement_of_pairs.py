"""
2097. Valid Arrangement of Pairs   ·   https://leetcode.com/problems/valid-arrangement-of-pairs/
Pattern: graphs

You are given a 0-indexed 2D array pairs where pairs[i] = [start_i, end_i].
An arrangement of pairs is VALID if for every i (1-indexed, i >= 1) the end of
the previous pair equals the start of the current pair:
    end_of(arrangement[i-1]) == start_of(arrangement[i]).

Return ANY valid arrangement of pairs. A valid arrangement is guaranteed to exist.
(You may reorder the pairs; you must use every pair exactly once.)

Example:  pairs = [[5,1],[4,5],[11,9],[9,4]]
          -> [[11,9],[9,4],[4,5],[5,1]]   (9==9, 4==4, 5==5)

Constraints: 1 <= pairs.length <= 10^5 ; a valid arrangement exists ; no duplicate pairs.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-07 ──────────────
    def validArrangementOfPairs_20260907(self, pairs: List[List[int]]) -> List[List[int]]:
        # since we just did this two days ago, I still remember the numbers are nodes
        # and that the edges are the results
        # so example 1, we have nodes as below
        # 11, 9, 4, 5, 1
        # this example is an Eulerian Path
        # looking at example 2 with nodes of 1, 3, 2 where path ends back at 1
        # we have an Eulerian Circuit
        # so key thing for this problem is to figure out what the starting and end nodes are
        # all nodes in an Eulerian circuit have an in and out edge with its degree evening out
        # if we have an Eulerian path, start node has an edge exiting and end node has an edge entering
        # so let's say leaving = -1 and entering is +1
        # so we will construct a degreeMap to help us find our start and end node
        # Hierholzer, so we need a stack and adjMap for the nodes
        # we also need to realize our output needs to be created after Hierholzer finishes
        # since Hierholzer will help us generate line 6 but not the actual result

        resultNodes = []

        adjMap = collections.defaultdict(list)

        # defaultdict of int initializes these nodes' be of 0 degree, therefore nothing going to it or even amount of edges going in and out
        degreeMap = collections.defaultdict(int)

        # adjMap is pretty straightforward, it's just the pairs
        # entering = +1, exiting = -1 so src-=1 and dst+=1
        for src, dst in pairs:
            degreeMap[src]-=1
            degreeMap[dst]+=1
            adjMap[src].append(dst)

        # initialize our startingNode to first node in case of Eulerian Circuit        
        startingNode = pairs[0][0]

        # if it is not, let's set startingNode to the one with -1 degree
        for node in degreeMap:
            if degreeMap[node] == -1:
                startingNode = node
                break

        # Starting Hierholzer
        # now that we have our starting node, let's add it to our stack
        stack = []

        stack.append(startingNode)

        # while we have nodes in the stack to go through
        while stack:
            # check if current node has neighbors we have yet to add to the stack
            # if it does not have anything else, this is the first node we put into result
            # we also don't pop off the stack unless it fits this criteria
            currentNode = stack[-1]
            if not adjMap[currentNode]:
                stack.pop()
                resultNodes.append(currentNode)
            else:
            # if this is not true, then we add its neighbors
                stack.append(adjMap[currentNode].pop())
        
        # when this is done, since we pushed the nodes in in reverse order, we need to reverse it
        resultNodes.reverse()

        # now we go through the resultNodes to generate the actual result
        result = []
        
        for i in range(1,len(resultNodes)):
            startNode = resultNodes[i-1]
            endNode = resultNodes[i]
            result.append([startNode, endNode])
        
        return result

    # ── Attempt 1 · 2026-09-05 ────────────────────────────────────────────
    def validArrangementOfPairs(self, pairs: List[List[int]]) -> List[List[int]]:
        # drawing this makes it really easy to notice it is a graph problem
        # more specifically an Eulerian Path problem
        # so this means Hierholzer's
        # but it is the numbers that are nodes and the pairs are the edges
        # adjacency is stated in the problem, by matching y -> x
        # the issue becomes how do we find the starting node?
        # if an end node has nothing connecting to it, it is obvly not the start
        # in order to visit all the nodes, these has to be true
        # 1. starting node must have an edge leaving it so must have one y -> x
        # 2. middle nodes must have edges entering and edges leaving it
        # 3. end node must have an edge entering it, which means y -> None is possible
        # so this tells us we need to count degrees on each node
        # positive means nodes going in
        # negative means nodes going out
        # 0 means even or no nodes going in/out

        degreeCounter = collections.defaultdict(int)
        
        # since we are going through to count degrees, might as well use the same loop to build our adjMap
        adjMap = collections.defaultdict(list)
        
        for src, dst in pairs:
            degreeCounter[src]-=1
            degreeCounter[dst]+=1
            adjMap[src].append(dst)
        
        # now startingNode is the one that has one thing leaving it only so that is -1
        
        startingNode = -1
        
        for node in degreeCounter:
            if degreeCounter[node] == -1:
                startingNode = node
        
        # if startingNode is still -1, that means we have an Eulerian Circuit
        # which means every single node is zero, so we just start with any node
        if startingNode == -1:
            startingNode = pairs[0][0]
        
        # now we can just do our classic stack DFS Hierholzer
        
        stack = []
        stack.append(startingNode)
        
        resultNodes = []
        
        while stack:
            # check if current node has edges to visit
            currentNode = stack[-1]
            # if no more edges to visit left, we can safely add this
            if not adjMap[currentNode]:
                resultNodes.append(stack.pop())
            # if there are edges left for this node, let's add them in
            else:    
                stack.append(adjMap[currentNode].pop())
            
        resultNodes.reverse()
        
        result = []
        # construct the edges for the result
        for i in range(1, len(resultNodes)):
            result.append([resultNodes[i-1],resultNodes[i]])
        
        return result
