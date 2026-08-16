"""
69. Sqrt(x)   ·   https://leetcode.com/problems/sqrtx/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

Given a non-negative integer `x`, return the square root of `x` rounded down to the
nearest integer. The returned integer should be non-negative as well.

You must NOT use any built-in exponent function or operator — no `pow(x, 0.5)` and
no `x ** 0.5`.

    x = 4    ->  2
    x = 8    ->  2      (2.828... rounded down)

Constraints:
    0 <= x <= 2^31 - 1
"""
# Write everything yourself from here.
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-08-16 ────────────────────────────────────────────
    def mySqrt(self, x: int) -> int:
        # what is square root
        # it is just y^2 = x where we are solving for y
        # what if we do binary search on the result
        # sqrt(x) is at most x for x = 1
        # x can also be 0, so we have l, r = 0, x
        # we are looking for the largest number that does not equal to x
        l, r = 0, x
        
        while l < r:
            # upper boundary bias
            m = (l + r + 1) // 2
            # check if m multiplied by itself is smaller or equal than x
            # if it is, it is a potential result and we want to see if we can go bigger
            if m * m <= x:
                l = m
            # otherwise, go up
            else:
                r = m - 1
        
        return l