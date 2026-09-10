"""
472. Concatenated Words   ·   https://leetcode.com/problems/concatenated-words/
Pattern: tries

Given an array of strings words (without duplicates), return all the concatenated
words in the given list of words.

A concatenated word is defined as a string that is comprised entirely of at least
two shorter words (not necessarily distinct) in the given array.

Example:
  words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses",
           "rat","ratcatdogcat"]
  -> ["catsdogcats","dogcatsdog","ratcatdogcat"]
  ("catsdogcats" = cats+dog+cats; "dogcatsdog" = dog+cats+dog;
   "ratcatdogcat" = rat+cat+dog+cat)

Example:
  words = ["cat","dog","catdog"]  ->  ["catdog"]

Constraints:
  1 <= words.length <= 10^4
  1 <= words[i].length <= 30
  words[i] consists of only lowercase English letters.
  0 <= sum(words[i].length) <= 10^5
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from functools import lru_cache
from typing import List, Optional

class TrieNode:
    def __init__(self):
        # char to TrieNode map
        self.children = {}
        self.isWord = False

class Solution:
    # ── Attempt 1 · 2026-09-09 ────────────────────────────────────────────
    def concatenatedWords(self, words: List[str]) -> List[str]:
        # so we construct trie for the words in here
        # it's pretty clear we need the shorter words in the front for us to build the Trie
        # so essentially for each word, if we reach a char that has isWord = True
        # that means we should consider this word as a result candidate
        root = TrieNode()
        
        result = []

        # Let's first put the words in the Trie
        for word in words:
            traversal = root
            for char in word:
                # if we do not have this char yet, add it
                if char not in traversal.children:
                    traversal.children[char] = TrieNode()
                traversal = traversal.children[char]
            traversal.isWord = True

        # we use index to check the next shorter word's start index
        # count to track how many smaller words we've encountered
        @lru_cache(None)
        def dfs(word, root, index, count):
            # if we are out of bounds, return whether or not we have 2 or more count
            if index >= len(word):
                return count > 1
            traversal = root
            for i in range(index, len(word)):
                # if we never seen this char, no match, return False
                if word[i] not in traversal.children:
                  return False
                # move traversal to current char
                traversal = traversal.children[word[i]]
                # if this is a shorter word, we increment count and check the next word
                # we need to reset the trie node to root
                if traversal.isWord:
                    if dfs(word, root, i+1, count+1):
                        return True
            return False

        for word in words:
            # we will use dfs to see if we found a word that has two words in it
            # we also need to do memoization since we need to re-check from root
            # each time we find a sub-word
            if dfs(word, root, 0, 0):
                result.append(word)
        
        return result