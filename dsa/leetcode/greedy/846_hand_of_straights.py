"""
846. Hand of Straights   ·   https://leetcode.com/problems/hand-of-straights/
Pattern: greedy

Alice has some cards, each with an integer written on it. She wants to rearrange
the cards into groups so that each group is of size groupSize, and consists of
groupSize consecutive cards.

Given an integer array hand where hand[i] is the value on the i-th card, and an
integer groupSize, return true if she can rearrange the cards, or false otherwise.

Example:
  hand = [1,2,3,6,2,3,4,7,8], groupSize = 3  ->  true
      ([1,2,3], [2,3,4], [6,7,8])
  hand = [1,2,3,4,5], groupSize = 4           ->  false
      (the hand cannot be rearranged into groups of 4)

Constraints:
  1 <= hand.length <= 10^4
  0 <= hand[i] <= 10^9
  1 <= groupSize <= hand.length
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from collections import Counter
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-11 ────────────────────────────────────────────
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        # first thought of longest consecutive sequence
        # easiest way is do a sort and then do a freqMap
        
        freqMap = Counter(hand)

        hand.sort()

        def isStraightHand(startingNumber):
            number = startingNumber
            while number < startingNumber + groupSize:
                # if next number does not exist in the map or is at 0
                # we don't have a hand of straight
                if number not in freqMap or freqMap[number] <= 0:
                    return False
                freqMap[number]-=1
                number+=1
            return True


        for num in hand:
            # since we are sorted, if freq >= 1, it must be the start
            if freqMap[num] > 0:
                if not isStraightHand(num):
                    return False
        
        return True