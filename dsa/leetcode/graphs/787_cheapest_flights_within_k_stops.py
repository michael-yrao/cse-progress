"""
787. Cheapest Flights Within K Stops   ·   https://leetcode.com/problems/cheapest-flights-within-k-stops/
Pattern: graphs

There are n cities connected by some number of flights. You are given an array
`flights` where flights[i] = [from_i, to_i, price_i] indicates that there is a
flight from city from_i to city to_i with cost price_i.

You are also given three integers src, dst, and k. Return the cheapest price
from src to dst with at most k stops. If there is no such route, return -1.

Example:
  n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
  src = 0, dst = 3, k = 1  ->  700
  (0 -> 1 -> 3 costs 700; 0 -> 1 -> 2 -> 3 costs 400 but uses 2 stops)

Constraints:
  1 <= n <= 100
  0 <= flights.length <= (n * (n - 1) / 2)
  flights[i].length == 3
  0 <= from_i, to_i < n,  from_i != to_i
  1 <= price_i <= 10^4
  There will not be any multiple flights between two cities.
  0 <= src, dst, k < n
  src != dst
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-07-14 ────────────────────────────────────────────
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        pass
