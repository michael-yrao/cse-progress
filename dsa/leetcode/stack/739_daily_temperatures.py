"""
739. Daily Temperatures   ·   https://leetcode.com/problems/daily-temperatures/
Pattern: stack

Given an array of integers `temperatures` representing the daily temperatures,
return an array `answer` such that `answer[i]` is the number of days you have to
wait after the i-th day to get a warmer temperature. If there is no future day
for which this is possible, keep `answer[i] == 0` instead.

Example 1:
    temperatures = [73,74,75,71,69,72,76,73]
    -> [1,1,4,2,1,1,0,0]

Example 2:
    temperatures = [30,40,50,60]   -> [1,1,1,0]

Example 3:
    temperatures = [30,60,90]      -> [1,1,0]

Constraints:
    1 <= temperatures.length <= 10^5
    30 <= temperatures[i] <= 100
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-06 ──────────────
    def dailyTemperatures_20260906(self, temperatures: List[int]) -> List[int]:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/739_daily_temperatures.txt — restored at session end (python scripts/restore_history.py)
