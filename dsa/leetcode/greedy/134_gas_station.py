"""
134. Gas Station   ·   https://leetcode.com/problems/gas-station/
Pattern: greedy

There are n gas stations along a circular route, where the amount of gas at the
i-th station is gas[i].

You have a car with an unlimited gas tank. It costs cost[i] of gas to travel from
the i-th station to its next (i+1)-th station. You begin the journey with an empty
tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's index if
you can travel around the circuit once in the clockwise direction, otherwise return
-1. If there exists a solution, it is guaranteed to be unique.

Example:
  gas = [1,2,3,4,5], cost = [3,4,5,1,2]  ->  3
  gas = [2,3,4],     cost = [3,4,3]       ->  -1

Constraints:
  n == gas.length == cost.length
  1 <= n <= 10^5
  0 <= gas[i], cost[i] <= 10^4
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-11 ──────────────
    def gasStation_20260911(self, gas: List[int], cost: List[int]) -> int:
        # we want to maximize our tank before the highest cost
        # this is a tactic, not really an algorithm cause I can't prove it always works
        # what we can do instead is just check if we can start at each index
        # netGas = gas[i] - cost[i], if we are at negative, we know we can't use this
        # essentially Kadane's algorithm

        if sum(gas) < sum(cost):
            return -1

        netGas = 0
        startingStation = 0
        for i in range(len(gas)):
            currentGas = gas[i] - cost[i]
            netGas+=currentGas
            if netGas < 0:
                netGas = 0
                startingStation = i + 1
            
        return startingStation

    # ── Attempt 1 · 2026-09-09 ────────────────────────────────────────────
    def gasStation(self, gas: List[int], cost: List[int]) -> int:
        # from example 2, we notice sum of gas must be >= sum of cost
        if sum(gas) < sum(cost):
            return -1
        
        # a few theories:
        # 1. start with as much gas as possible, but this does not always work so it's out
        # 2. start after the highest cost, meaning this allows us time to get as much gas as possible before we get there
        # so going with 2 is like doing maximum subarray basically, so variation of Kadane
        # e.g. if our net gain is less than 0, reset it
        totalGas = 0
        result = 0
        for i in range(len(gas)):
            netGas = gas[i] - cost[i]
            totalGas+=netGas
            # if we can't start here, go next
            if totalGas < 0:
                totalGas = 0
                result = i + 1
        
        return result
