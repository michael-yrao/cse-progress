"""
1462. Course Schedule IV   ·   https://leetcode.com/problems/course-schedule-iv/
Pattern: graphs

numCourses courses labeled 0..numCourses-1. prerequisites[i]=[a,b] => a must be
taken before b (a is prereq of b). Prereqs are transitive.

queries[j]=[u,v] => is u a prerequisite (direct OR indirect) of v?
Return List[bool], one answer per query.

Constraints: n<=100, no cycles (DAG). queries can be many.
Goal: answer all "is u ancestor of v" reachability queries.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-04 ──────────────
    def courseScheduleIv_20260904(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # build a 2D array of prereqs so we always know answers to queries immediately
        # this is just floyd warshall, especially given numCourses <= 100
        # so floyd warshall is on the premise of edges
        # initialize the 2D array first, then update based on prereq
        # we will say 0 in [i][j] means i is not prereq of j and 1 is pre-req

        prereqMap = []

        for i in range(numCourses):
            prereqMap.append([0] * numCourses)

        # now we initialize the ones that have immediate prereqs
        for pre, course in prerequisites:
            prereqMap[pre][course] = 1
        
        # now do the middle thing
        for middle in range(numCourses):
            for left in range(numCourses):
                for right in range(numCourses):
                    # if we need left to take middle and middle to take right
                    # then left to right is definitely 1
                    if prereqMap[left][middle] == 1 and prereqMap[middle][right]:
                        prereqMap[left][right] = 1
        
        # now we can just query for our results
        result = []

        for pre, course in queries:
            if prereqMap[pre][course] == 0:
                result.append(False)
            else:
                result.append(True)
        
        return result

    # ── Attempt 1 · 2026-08-25 ────────────────────────────────────────────
    def courseScheduleIv(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # this actually looks like union find but it is directed so we can rule UF out
        # one basic way to look at this is literally go through all queries and see if we can reach from source -> destination
        # from example 3, we'll notice we will have done duplicated work
        # so we should utilize Floyd Warshall
        # canReach[i][j] initialized to False and we ask ourselves if we can reach j from i via k

        canReach = []

        for i in range(numCourses):
            array = [False] * numCourses
            canReach.append(array)
            canReach[i][i] = True
        
        # populate canReach with prerequisites

        for src, dst in prerequisites:
            canReach[src][dst] = True
        
        # now we can do Floyd Warshall

        for midPoint in range(numCourses):
            for start in range(numCourses):
                for end in range(numCourses):
                    if canReach[start][midPoint] == True and canReach[midPoint][end]:
                        canReach[start][end] = True
        
        result = []
        for start, end in queries:
            result.append(canReach[start][end])
        
        return result
