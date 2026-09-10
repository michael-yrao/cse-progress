"""
763. Partition Labels   ·   https://leetcode.com/problems/partition-labels/
Pattern: greedy

You are given a string s. We want to partition the string into as many parts as
possible so that each letter appears in at most one part. For example, the string
"ababcc" can be partitioned into ["abab", "cc"], but partitions such as
["aba", "bcc"] or ["ab", "ab", "cc"] are invalid.

Note that the partition is done so that after concatenating all the parts in order,
the resultant string should be s.

Return a list of integers representing the size of these parts.

Example:
  s = "ababcbacadefegdehijhklij"  ->  [9, 7, 8]
  ("ababcbaca", "defegde", "hijhklij")

Constraints:
  1 <= s.length <= 500
  s consists of lowercase English letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-09 ────────────────────────────────────────────
    def partitionLabels(self, s: str) -> List[int]:
        # this is asking for maximum amount of partitions
        # we should initialize a frequency map
        # go through the list, if we see a char, go until we get the last index of it
        # if we finished all the freq of the numbers in this window, we mark that as a component
        # another thing we can do is to have a lastIndexMap that tells us whether or not we have finished which is actually cleaner
        # because we can keep track of the max last index based on what char we've seen so far
        lastIndexMap = {}
        result = []

        # initialize lastIndexMap
        for i in range(len(s)):
            lastIndexMap[s[i]] = i

        maxLastIndex = -math.inf

        # keep track of where the prior one ended
        priorEnd = 0

        # now we go through again, this time, we keep track of the indices
        # if we reached maxLastIndex, it means we finished a component
        for i in range(len(s)):
            # get the last time we see this character
            lastCharIndex = lastIndexMap[s[i]]
            maxLastIndex = max(maxLastIndex, lastCharIndex)
            # if this is the last time we see this char, we mark a component
            if maxLastIndex == i:
                # if we added something already, i - len gives us this component's length
                if result:
                    result.append(i - priorEnd)
                # append length if we haven't added anything yet
                else:
                    result.append(i+1)
                # reset the maxLastIndex
                maxLastIndex = -math.inf
                priorEnd = i
        
        return result