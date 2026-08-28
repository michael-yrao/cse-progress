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

    # ── Attempt · 2026-08-27 ──────────────
    def dailyTemperatures_20260827(self, temperatures: List[int]) -> List[int]:
        # go from this backwards
        # if we do this from the front, it feels like an O(n^2)
        # going from the end, the last element always has zero
        # when we see 76, 73 is useless because it will never be ith day warmer temperature
        # so we can pop it, so decreasing stack
        # we also care for how many days, which is how many indices between i and j
        # such that value at j is greater than value at i

        decreasingStack = []

        # initialize decreasing stack with last item and also the output with all 0s
        result = [0] * len(temperatures)

        decreasingStack.append(len(temperatures) - 1)

        for i in range(len(temperatures)-2,-1,-1):
            # if top element of stack is smaller or equal to current element, pop it
            while decreasingStack and temperatures[decreasingStack[-1]] <= temperatures[i]:
                decreasingStack.pop()
            # when we are here, there is either nothing in stack or stack[-1] is greater
            # set result[i] to stack[-1] - i
            if decreasingStack:
                result[i] = decreasingStack[-1] - i
            # insert i into the stack
            decreasingStack.append(i)
        
        return result

    # ── Attempt 1 · 2026-08-14 ────────────────────────────────────────────
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # we need to go from end to beginning
        # definitely a monotonic stack problem
        # stack should be monotonically decreasing
        # so we are incrementing when the number goes down
        length = len(temperatures)
        answer = [0] * length
        decreasingStack = []

        # we are given length of temperatures is always 1 or more
        # we care about number of days so our decreasing stack should hold index
        decreasingStack.append(length - 1)

        for i in range(length - 2, -1, -1):
            # if current index is equal or bigger, we keep going until we find a higher number 
            while decreasingStack and temperatures[i] >= temperatures[decreasingStack[-1]]:
                priorTemperatureIndex = decreasingStack.pop()
            # now that we are here, we know the current item on the stack is bigger
            # or there is nothing on the stack
            if decreasingStack and temperatures[i] < temperatures[decreasingStack[-1]]:
                answer[i] = decreasingStack[-1] - i
            # push current index onto the stack
            decreasingStack.append(i)
        
        return answer
