"""
269. Alien Dictionary   ·   https://neetcode.io/problems/alien-dictionary
Pattern: graphs

There is a new alien language that uses the English alphabet, but the ORDER of the
letters is unknown to you. You are given a list `words` of words from the alien
language's dictionary, and the words are sorted lexicographically by the rules of
this new language.

Return a string of the unique letters in the new language, sorted in the new
language's order. If there is no solution, return "". If there are multiple
solutions, return any of them.

Note: a string `a` is lexicographically smaller than a string `b` if, at the first
position where they differ, `a`'s letter comes before `b`'s in the alien order. If
the first `min(len(a), len(b))` characters are equal, then `a` is smaller iff
`len(a) < len(b)`.

Example 1:
    Input:  words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"

Example 2:
    Input:  words = ["z","x"]
    Output: "zx"

Example 3:
    Input:  words = ["z","x","z"]
    Output: ""          # the ordering is invalid — no valid alien order exists

Constraints:
    1 <= words.length <= 100
    1 <= words[i].length <= 100
    words[i] consists of only lowercase English letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-07-27 ────────────────────────────────────────────
    def alienOrder(self, words: List[str]) -> str:
        # build adjacency map of letters
        # then afterwards, we can build a word using BFS or DFS
        # we need to know the basic idea of where to start for BFS/DFS
        # so we need to find the char that has no preceding character
        # so we can keep track of that, we can do something like course schedule
        # increment the letters that have predecessors

        adjMap = {char : set() for word in words for char in word}
        rankMap = {char: 0 for char in adjMap}
        
        def buildAdjMap(firstWord, secondWord):
            # if we cannot build a mapping at any point, return empty string
            # abc -> ab
            minLen = min(len(firstWord), len(secondWord))
            if len(firstWord) > len(secondWord) and firstWord[:len(secondWord)] == secondWord:
                return ""
            for i in range(minLen):
                # at the first position different, check lexicographical difference
                if firstWord[i] != secondWord[i]:
                    if secondWord[i] not in adjMap[firstWord[i]]:
                        adjMap[firstWord[i]].add(secondWord[i])
                        rankMap[secondWord[i]]+=1
                    # break here regardless since lexicographical order has been checked
                    break
        
        for i in range(len(words)-1):
            firstWord = words[i]
            secondWord = words[i+1]
            if buildAdjMap(firstWord, secondWord) == "":
                return ""

        result = []
        queue = collections.deque()
        # add only the ones with rank of 0
        for key in rankMap:
            if rankMap[key] == 0:
                queue.append(key)

        # BFS on the adjacency map and rank map
        while queue:
            currentChar = queue.popleft()
            result.append(currentChar)
            # now decrement rank of its neighbors
            for neighbor in adjMap[currentChar]:
                rankMap[neighbor]-=1
                if rankMap[neighbor] == 0:
                    queue.append(neighbor)

        # check if we mapped all edges
        # rankMap has all distinct nodes, thus if len(rankMap) == len(result), we are good
        # otherwise, return ""

        if len(rankMap) != len(result):
            return ""

        return "".join(result)