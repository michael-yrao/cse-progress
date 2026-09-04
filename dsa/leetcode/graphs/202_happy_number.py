"""
202. Happy Number   ·   https://leetcode.com/problems/happy-number/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

Write an algorithm to determine if a number `n` is "happy".

A happy number is defined by the following process:
  - Starting with any positive integer, replace the number by the sum of the
    squares of its digits.
  - Repeat the process until the number equals 1 (where it will stay), or it
    loops endlessly in a cycle which does not include 1.
  - Those numbers for which this process ends in 1 are happy.

Return True if n is a happy number, and False if not.

    n = 19  ->  True
        1^2 + 9^2  = 82
        8^2 + 2^2  = 68
        6^2 + 8^2  = 100
        1^2 + 0^2 + 0^2 = 1

    n = 2   ->  False

Constraints:
    1 <= n <= 2^31 - 1

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-02 ──────────────
    def isHappy_20260902(self, n: int) -> bool:
        # if we have seen this number, we are repeating, so a set
        seen = set()

        # now we do the happy number logic
        while n not in seen:
            # add n itself to seen
            seen.add(n)
            currentNum = 0
            for digit in str(n):
                currentNum+=int(digit)**2
            n = currentNum
            if n == 1:
                return True
        
        return False

    # ── Attempt · 2026-08-21 ──────────────
    # ── RECOGNITION — fill BEFORE coding, before the coach says anything ──
    #   shape cues seen →
    #   technique →
    #   discriminator (why this, not the nearest neighbour) →
    def isHappy_20260821(self, n: int) -> bool:
        # we need to define an end point
        # we end when we repeat numbers
        # otherwise we are good to continue

        unhappySet = set()
        happyNumber = n
        # as long as we are not in unhappySet, we are good to continue
        while happyNumber not in unhappySet:
            unhappySet.add(happyNumber)
            currentHappyNumber = 0
            for d in str(happyNumber):
                digit = int(d)
                currentHappyNumber+=(digit**2)
            happyNumber = currentHappyNumber
        
        return happyNumber == 1

    # ── Attempt 1 · 2026-08-10 ────────────────────────────────────────────
    def isHappy(self, n: int) -> bool:
        seen = set()
        def happy(n):
          # we need to define an end point for both success and failure
          if n == 1:
              return True
          if n in seen:
            return False
          
          seen.add(n)
          happyNumber = 0
          for digit in str(n):
              happyNumber+=int(digit)**2
          return happy(happyNumber)
        return happy(n)
