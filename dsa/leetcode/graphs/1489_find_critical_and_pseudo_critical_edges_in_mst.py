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

# ── Attempt · 2026-10-03 ──────────────
class UF_20261003:
    def __init__(self, n):
        self.numComponents = n
        self.rankMap = {}
        self.parentMap = {}
        for i in range(self.numComponents):
            self.rankMap[i] = 0
            self.parentMap[i] = i
        
    def find(self, node):
        if self.parentMap[node] != node:
            self.parentMap[node] = self.find(self.parentMap[node])
        return self.parentMap[node]
    
    def union(self, n1, n2):
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


# ── Attempt · 2026-09-23 ──────────────
class UF_20260923:
    def __init__(self, n):
        self.numComponents = n
        self.parentMap = {}
        self.rankMap = {}
        for i in range(n):
            self.parentMap[i] = i
            self.rankMap[i] = 0
        
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
    def findCriticalAndPseudoCriticalEdges_20261003(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        # there are already edges here so we are just trying to find MSTs based on pre-existing edges so this means Kruskal's
        # critical edges mean that they must be in the MST otherwise the span goes up, so we try to do MST creation without each edge and any edge that is not in that makes the MST go up is critical
        # pseudo-critical means it is in some MSTs but not all
        # opposite of critical is not pseudo-critical, it can mean either pseudo-critical or not in any MST
        # if we force an edge to be part of the MST and it makes it goes up, it means it is not part of any MST, so we are looking for edges such that if we include them, they don't change
        # kruskal's require us to sort by the weight of the edges but answer is based on the original index of the edges so we need to make a new array with original index
        # we also need to make sure excluding/including an edge allows us to even create a MST
        # if we can create, it means numComponents is 1, otherwise it is impossible

        for i in range(len(edges)):
            edges[i].append(i)
        
        # sort by edge[2] which is the weight
        edges.sort(key=lambda edge:edge[2])

        # helper function for excluding a node
        def get_mst_without(node_index):
            uf = UF_20261003(n)
            total_span = 0
            for i in range(len(edges)):
                src = edges[i][0]
                dst = edges[i][1]
                weight = edges[i][2]
                if i == node_index:
                    continue
                if uf.union(src,dst):
                    total_span+=weight
            if uf.numComponents == 1:
                return total_span
            return math.inf
        
        # helper function for including a node
        def get_mst_with(node_index):
            uf = UF_20261003(n)
            # start total span at forced node
            total_span = edges[node_index][2]
            uf.union(edges[node_index][0],edges[node_index][1])
            for i in range(len(edges)):
                src = edges[i][0]
                dst = edges[i][1]
                weight = edges[i][2]
                if i == node_index:
                    continue
                if uf.union(src,dst):
                    total_span+=weight
            if uf.numComponents == 1:
                return total_span
            return math.inf
        
        # get the smallest MST we possibly can
        base_mst = get_mst_without(-1)

        critical_edges = set()

        # let's get the critical edges
        for edge_index in range(len(edges)):
            critical_mst = get_mst_without(edge_index)
            if critical_mst > base_mst:
                critical_edges.add(edges[edge_index][3])
        
        pseudo_critical_edges = []

        # now let's do the pseudo-critical edges
        # critical edges are also pseudo-critical, so make sure to exclude those
        for edge_index in range(len(edges)):
            pseudo_critical_mst = get_mst_with(edge_index)
            if pseudo_critical_mst == base_mst and edges[edge_index][3] not in critical_edges:
                pseudo_critical_edges.append(edges[edge_index][3])
        
        result = []
        result.append(list(critical_edges))
        result.append(pseudo_critical_edges)

        return result

    def findCriticalAndPseudoCriticalEdges_20260923(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        # critical = this edge must exist in every MST possible
        # pseudo-critical = this edge exist in some MST
        # MST with the smallest weight is our base case
        # if we exclude an edge and the weight goes up, it is critical
        # we can find the edge using the index, the index actually is important by this, so we need to keep the index when we sort, create new edges array with it in there
        # Kruskal's algorithm for MST

        # add original index into edges
        for i, sublist in enumerate(edges):
            sublist.append(i)

        # sort the edges by the smallest weight
        edges.sort(key=lambda edge:edge[2])

        # 1. Build method to exclude an edge and give the weight of the MST without this edge

        def build_mst_exclude_edge(edge_index):
            overallWeight = 0
            uf = UF_20260923(n)
            for i in range(len(edges)):
                src = edges[i][0]
                dst = edges[i][1]
                weight = edges[i][2]
                # skip this index
                if i == edge_index:
                    continue
                if uf.union(src,dst):
                    overallWeight+=weight
            if uf.numComponents == 1:
                return overallWeight
            return math.inf

        # 2. Build method to must include an edge and give the weight of the MST that must include this edge

        def build_mst_include_edge(edge_index):
            uf = UF_20260923(n)
            # include this index by starting the weight with it
            overallWeight = edges[edge_index][2]
            # union the nodes of this index immediately
            uf.union(edges[edge_index][0], edges[edge_index][1])
            # now we go through rest of edges
            for i in range(len(edges)):
                src = edges[i][0]
                dst = edges[i][1]
                weight = edges[i][2]
                # skip this index
                if i == edge_index:
                    continue
                if uf.union(src,dst):
                    overallWeight+=weight
            if uf.numComponents == 1:
                return overallWeight
            return math.inf

        # 3. Build our base MST

        base_mst_weight = build_mst_exclude_edge(-1)

        # 4. compare all other possible MST to base MST if we were to exclude each, this helps us generate our critical edges
        # criticalEdges need to a set so that when we check for pseudo critical, it's constant time
        
        critical_edges = set()

        for i in range(len(edges)):
            mst_weight_without_i = build_mst_exclude_edge(i)
            if mst_weight_without_i > base_mst_weight:
                critical_edges.add(edges[i][3])

        # 5. pseudo-critical edges
        # we can note that some edges might never appear in MST
        # if i include an edge that is never part of a MST, 
        # the value would be too big, so we don't care for those, 
        # we only want the edges that give us value equal to base_mst_weight
        # but this also includes critical edges, so make sure to exclude those

        pseudo_critical_edges = set()

        for i in range(len(edges)):
            mst_weight_with_i = build_mst_include_edge(i)
            if mst_weight_with_i == base_mst_weight and edges[i][3] not in critical_edges:
                pseudo_critical_edges.add(edges[i][3])

        result = []

        result.append(list(critical_edges))
        result.append(list(pseudo_critical_edges))
        return result                

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
