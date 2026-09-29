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

    # ── Attempt · 2026-09-29 ──────────────
    def isNStraightHand_20260929(self, hand: List[int], groupSize: int) -> bool:
        # sort and then check if current number is starting of a sequence
        # we do need a freq counter as well though to make sure we can use the number
        # we decrement the freq counter when we use them as part of a sequence

        freq_map = Counter(hand)

        hand.sort()

        def is_sequence(num):
            for seq_number in range(num, num + groupSize):
                # if next number does not exist or does not have freq left, return False
                if seq_number not in freq_map or freq_map[seq_number] == 0:
                    return False
                # if it does exist, decrement by 1
                freq_map[seq_number]-=1
            return True

        for num in hand:
            # start of sequence
            if freq_map[num] > 0:
                # if we are not able to do a sequence with num, return False immediately
                if not is_sequence(num):
                    return False
            # if zero, then this is already used by another sequence and just continue
        
        return True

    # ── Attempt · 2026-09-23 ──────────────
    def isNStraightHand_20260923(self, hand: List[int], groupSize: int) -> bool:
        # we can use freqMap here
        # and go from lowest number up
        # but map doesn't keep order, so how do we do this properly
        # let's sort to get the smallest number possible

        hand.sort()

        freqMap = Counter(hand)

        def markSequence(start):
            for i in range(start, start+groupSize):
                # if next number does not exist, return False
                if i not in freqMap or freqMap[i] == 0:
                    return False
                freqMap[i]-=1
            return True

        i = 0
        while i < len(hand):
            # if hand[i] is not 0 in freqMap, it is a start of a sequence
            # so we check if the sequence is of groupSize
            if freqMap[hand[i]] != 0:
                # if we cannot make a sequence out of hand[i], return False
                if not markSequence(hand[i]):
                    return False
            # now that we are out of markSequence, we can continue to the next index
            i+=1
        
        for key,value in freqMap.items():
            if value != 0:
                return False
        
        return True

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
