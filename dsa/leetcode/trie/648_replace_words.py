"""
648. Replace Words   ·   https://leetcode.com/problems/replace-words/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

In English, we have a concept called root, which can be followed by some other word
to form another longer word — let's call this word a successor. For example, when the
root "an" is followed by the successor word "other", we can form a new word "another".

Given a dictionary consisting of many roots and a sentence consisting of words
separated by spaces, replace all the successors in the sentence with the root forming
it. If a successor can be replaced by more than one root, replace it with the root that
has the shortest length.

Return the sentence after the replacement.

Example 1:
  dictionary = ["cat","bat","rat"]
  sentence   = "the cattle was rattled by the battery"
  ->  "the cat was rat by the bat"

Example 2:
  dictionary = ["a","b","c"]
  sentence   = "aadsfasf absbs bbab cadsfafs"
  ->  "a a b c"

Constraints:
    1 <= dictionary.length <= 1000
    1 <= dictionary[i].length <= 100
    dictionary[i] consists of only lowercase letters.
    1 <= sentence.length <= 10^6
    sentence consists of only lowercase letters and spaces.
    The number of words in sentence is in the range [1, 1000].
    Each word in sentence is separated by a single space.

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        # create a Trie for the dictionary
        # now for each word in sentence, we stop at the first isWord we encounter
        root = TrieNode()
        for word in dictionary:
            traversal = root
            for char in word:
                if char not in traversal.children:
                    traversal.children[char] = TrieNode()
                traversal = traversal.children[char]
            traversal.isWord = True
        
        def findShortestWord(word):
            shortestWord = []
            traversal = root
            for char in word:
                # if we never seen this char, return None
                if char not in traversal.children:
                    return None
                # if we have add to the wordList
                shortestWord.append(char)
                traversal = traversal.children[char]
                if traversal.isWord:
                    return "".join(shortestWord)
            return None

        result = []
        wordSplit = sentence.split()
        # go through each word, look for closest isTrue
        for word in wordSplit:
            shortestWord = findShortestWord(word)
            # if not found, just add the word
            if shortestWord == None:
                result.append(word)
            else:
                result.append(shortestWord)
        
        return " ".join(result)