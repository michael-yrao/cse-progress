"""
1489. Find Critical and Pseudo-Critical Edges in MST   ·   https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/
Pattern: graphs

Given a weighted undirected connected graph with n vertices numbered 0..n-1, and an array
edges where edges[i] = [ai, bi, weighti] is a bidirectional weighted edge between ai and bi.
An MST is a subset of edges connecting all vertices, no cycles, minimum total weight.

Find all critical and pseudo-critical edges of the MST:
  - a CRITICAL edge is one whose deletion from the graph would INCREASE the MST weight;
  - a PSEUDO-CRITICAL edge is one that can appear in SOME MSTs but not all.
Return [critical_indices, pseudo_critical_indices], indices in any order.

Example 1:
  n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
  -> [[0,1],[2,3,4,5]]   (edges 0,1 in every MST; 2,3,4,5 in some but not all)

Example 2:
  n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]
  -> [[],[0,1,2,3]]      (all equal weight; any 3 of 4 form an MST -> all pseudo-critical)

Constraints:
  2 <= n <= 100
  1 <= edges.length <= min(200, n*(n-1)/2)
  edges[i].length == 3
  0 <= ai < bi < n
  1 <= weighti <= 1000
  All pairs (ai, bi) are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional

class UF:
# we will use a UF helper class
# we need the typical UF objects but we also need a numComponents so we know if we are fully connected

    def __init__(self, n):
        self.rankMap = {}
        self.parentMap = {}
        self.numComponents = n

        for i in range(n):
            self.rankMap[i] = 0
            self.parentMap[i] = i
    
    def find(self,node):
        if self.parentMap[node] != node:
            self.parentMap[node] = self.find(self.parentMap[node])
        return self.parentMap[node]
    
    def union(self,n1,n2):
        n1r = self.find(n1)
        n2r = self.find(n2)
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
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # MST, so Prim's or Kruskal but we are specifically saying some edges are pseudo-critical
        # so we need to be able to ban specific edges, thus it has to be UF and Kruskal
        # We need to do Kruskal's if an edge did not exist and see if that edge's removal caused a weight increase. If it did, we add that to critical edge list
        # not sure I understand what a pseudo-critical edge is
        # Edges are one of three categories:
        # 1. critical
        # 2. pseudo-critical
        # 3. useless
        # using edge removal kruskal, we can find #1
        # forcing edge usage kruskal while maintaining same weight as base MST weight, we can find #2
        
        # 1. Setup the sorted array for the base MST

        # sort edge by edge[2] which is the weight
        # we do need to keep the original for the result for when we figure out what to ban for each MST
        # but if we create a new one and we don't know the original index immediately, we have to compare each time
        # cleanest way is actually to add index to the end
        sortedEdgesWithOriginalIndex = []
        
        for i in range(len(edges)):
            row = edges[i] + [i]
            sortedEdgesWithOriginalIndex.append(row)
        
        # 0 = n1, 1 = n2, 2 = weight, 3 = og index
        sortedEdgesWithOriginalIndex.sort(key=lambda edge:edge[2])
        
        # 2. Helper method that does Kruskal's without a certain edge
        # returns the totalWeight with this edge removed

        def findMSTWithEdgeRemoved(removeEdgeIndex):
            totalWeight = 0
            uf = UF(n)
            for i in range(len(sortedEdgesWithOriginalIndex)):
                node1 = sortedEdgesWithOriginalIndex[i][0]
                node2 = sortedEdgesWithOriginalIndex[i][1]
                weight = sortedEdgesWithOriginalIndex[i][2]
                if i == removeEdgeIndex:
                    continue
                if uf.union(node1,node2):
                    totalWeight += weight
            # check if everyone is connected
            # if not, then it is not possible to do MST without this edge
            if uf.numComponents == 1:
                return totalWeight
            return math.inf
        
        # 3. Helper to find weight if we have to use a certain edge
        # this helps us find pseudo-critical edges
        
        def findMSTWithMandatoryEdge(mandatoryEdgeIndex):
            uf = UF(n)
            mandatoryNode1, mandatoryNode2, mandatoryWeight, _ = sortedEdgesWithOriginalIndex[mandatoryEdgeIndex]
            totalWeight = mandatoryWeight
            # connect the two nodes first from the mandatory edge
            uf.union(mandatoryNode1, mandatoryNode2)
            # now we can skip this edge
            for i in range(len(sortedEdgesWithOriginalIndex)):
                if i == mandatoryEdgeIndex:
                    continue
                node1 = sortedEdgesWithOriginalIndex[i][0]
                node2 = sortedEdgesWithOriginalIndex[i][1]
                weight = sortedEdgesWithOriginalIndex[i][2]
                if uf.union(node1,node2):
                    totalWeight += weight
            # check if everyone is connected
            # if not, then it is not possible to do MST without this edge
            if uf.numComponents == 1:
                return totalWeight
            return math.inf
        
        # 4. Find the weight of the most efficient MST

        baseMSTWeight = findMSTWithEdgeRemoved(-1)
        
        # 5. go through all edges and find critical and pseudo-critical edges
        
        critical = set()
        pseudoCritical = set()
        unionFind = UF(n)
        for i in range(len(sortedEdgesWithOriginalIndex)):
            removedWeight = findMSTWithEdgeRemoved(i)
            mandatoryWeight = findMSTWithMandatoryEdge(i)
            # if removing edge makes it bigger than base, it is critical
            if removedWeight > baseMSTWeight:
                # need to append the original index
                critical.add(sortedEdgesWithOriginalIndex[i][3])
            # if it does not increase, it means it is either unnecessary or pseudo-critical
            # if we have to use this edge, if our weight still doesn't change, this is pseudo-critical
            else:
                if mandatoryWeight == baseMSTWeight:
                    pseudoCritical.add(sortedEdgesWithOriginalIndex[i][3])
        
        return [list(critical), list(pseudoCritical)]