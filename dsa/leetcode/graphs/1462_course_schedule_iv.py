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

    # ── Attempt · 2026-10-04 ──────────────
    def courseScheduleIv_20261004(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/1462_course_schedule_iv.txt — restored at session end (python scripts/restore_history.py)
