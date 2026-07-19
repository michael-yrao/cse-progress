"""
127. Word Ladder   ·   https://leetcode.com/problems/word-ladder/
Pattern: graphs

A transformation sequence from word `beginWord` to word `endWord` using a dictionary
`wordList` is a sequence beginWord -> s1 -> s2 -> ... -> sk such that:
  - Every adjacent pair of words differs by a single letter.
  - Every si (1 <= i <= k) is in wordList. Note beginWord need not be in wordList.
  - sk == endWord

Given beginWord, endWord, and wordList, return the number of words in the SHORTEST
transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Example 1:
    Input:  beginWord = "hit", endWord = "cog",
            wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: "hit" -> "hot" -> "dot" -> "dog" -> "cog" is 5 words long.

Example 2:
    Input:  beginWord = "hit", endWord = "cog",
            wordList = ["hot","dot","dog","lot","log"]
    Output: 0
    Explanation: endWord "cog" is not in wordList, so no valid sequence.

Constraints:
    1 <= beginWord.length <= 10
    endWord.length == beginWord.length
    1 <= wordList.length <= 5000
    wordList[i].length == beginWord.length
    beginWord, endWord, wordList[i] are lowercase English letters.
    beginWord != endWord; all words in wordList are unique.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-07-18 ────────────────────────────────────────────
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # so we need to build an adjmap of beginWord, endWord and wordList
        # this will construct us a graph of equal edge size
        # from here, we can BFS to find path from beginWord to endWord

        wildcardMap = collections.defaultdict(set)

        allWords = []
        allWords.append(beginWord)
        allWords+=wordList

        # building the adjacency map normally would cost us O(n^2)
        # we can do better by building with wildcard like how we do for word search in Trie
        # so we will have wildcardMap instead of adjMap where *ot -> [hot, tot, dot, lot]

        for word in allWords:
            # we need to check if wildcard is a key already, if not create it
            for i in range(len(word)):
                wildcardWord = word[:i] + '*' + word[i+1:]
                wildcardMap[wildcardWord].add(word)
        
        # now that we have our adjacency map, let's do our BFS with visited set and queue

        visited = set()
        queue = collections.deque()
        queue.append(beginWord)
        visited.add(beginWord)
        level = 0
        # while we still have pathes to go and have not yet visited endWord
        while queue and endWord not in visited:
            level+=1
            wordPerLevel = len(queue)
            for _ in range(wordPerLevel):
                currentWord = queue.popleft()
                # go through all wildcards that match the current word
                # we actually need to go level by level, so we know exactly how many levels it took to get to endWord
                for i in range(len(currentWord)):
                    wildcardWord = currentWord[:i] + '*' + currentWord[i+1:]
                    # now we get all words in the wildcard into the queue
                    for nextWord in wildcardMap[wildcardWord]:
                        if nextWord == endWord:
                            return level + 1
                        if nextWord not in visited:
                            visited.add(nextWord)
                            queue.append(nextWord)
        
        return 0