"""
547. Number of Provinces   ·   https://leetcode.com/problems/number-of-provinces/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

There are n cities. Some of them are connected, while some are not. If city a is
connected directly with city b, and city b is connected directly with city c, then
city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other
cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the i-th
city and the j-th city are directly connected, and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.

Example:
  isConnected = [[1,1,0],[1,1,0],[0,0,1]]  ->  2
  isConnected = [[1,0,0],[0,1,0],[0,0,1]]  ->  3

Constraints:
    1 <= n <= 200
    n == isConnected.length == isConnected[i].length
    isConnected[i][j] is 1 or 0
    isConnected[i][i] == 1
    isConnected[i][j] == isConnected[j][i]

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        # First statement of the problem led me to believe it is a Floyd Warshall problem
        # Problem name tells me it is UF, let's do UF

        numNodes = len(isConnected)

        rankMap = {}
        parentMap = {}

        for i in range(numNodes):
            rankMap[i] = 0
            parentMap[i] = i
        
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
                parentMap[n2r] = n1r
                rankMap[n1r]+=1
            return True
        
        numProvinces = numNodes
        # go through each row, see who this guy is connected to and connect them
        for i in range(numNodes):
            for j in range(1,numNodes):
                # if i and j are connected and we can merge them
                # that means we decrement numProvinces
                if isConnected[i][j] and union(i,j):
                    numProvinces-=1
        
        return numProvinces
