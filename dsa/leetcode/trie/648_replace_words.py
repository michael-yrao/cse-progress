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

    # ── Attempt · 2026-10-06 ──────────────
class TrieNode_20261006:
    def __init__(self):
        self.children = {}
        self.isWord = False


class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False


class Solution:
    def replaceWords_20261006(self, dictionary: list[str], sentence: str) -> str:
        # this is a Trie problem, we basically put dictionary into a Trie
        # go through each word in the sentence, when we get a first hit, we use it

        result = []

        root = TrieNode_20261006()

        for word in dictionary:
            traversal = root
            for char in word:
                if char not in traversal.children:
                    traversal.children[char] = TrieNode_20261006()
                traversal = traversal.children[char]
            traversal.isWord = True
        
        # now that the dictionaries are setup, let's go through each word in sentence

        words = sentence.split()

        for word in words:
            traversal = root
            for i in range(len(word)):
                # if char doesn't exist in it, just use the word itself
                if word[i] not in traversal.children:
                    result.append(word)
                    break
                # if exists, increment traversal
                traversal = traversal.children[word[i]]
                # if it does exist and is a word, add to result and go next
                if traversal.isWord:
                    result.append(word[:i+1])
                    break
            else:
                result.append(word)
        
        new_sentence = " ".join(result)

        return new_sentence

    # ── Attempt · 2026-09-26 ──────────────
    def replaceWords_20260926(self, dictionary: List[str], sentence: str) -> str:
        # trie problem, put each word in dictionary in our trie
        # convert words in the sentence into a list then go through each word
        # return on the first match we find, if no match found, return itself

        root = TrieNode()

        for word in dictionary:
            traversal = root
            for char in word:
                if char not in traversal.children:
                    traversal.children[char] = TrieNode()
                traversal = traversal.children[char]
            traversal.isWord = True
        
        result = []

        wordList = sentence.split()

        def find_shortest_word(word, node):
            # finding the first isWord here
            for i in range(len(word)):
                if word[i] not in node.children:
                    return word
                node = node.children[word[i]]
                if node.isWord:
                    # return the word including ith index
                    return word[:i+1]
            return word

        for word in wordList:
            traversal = root
            result.append(find_shortest_word(word,traversal))
        
        return " ".join(result)

    # ── Attempt · 2026-09-24 ──────────────
    def replaceWords_20260924(self, dictionary: List[str], sentence: str) -> str:
        # we can place all the dictionaries into a trie but what does that accomplish
        # we want the shortest path so we do prefix search
        root = TrieNode()

        for word in dictionary:
            traversal = root
            for char in word:
                if char not in traversal.children:
                    traversal.children[char] = TrieNode()
                traversal = traversal.children[char]
            traversal.isWord = True

        resultWords = []
        # now let's try to BFS on each word in the sentence
        # if not found, just use the word itself

        def prefixSearch(word):
          node = root
          for index, char in enumerate(word):
            # we use the word itself if we cannot find a this word in the Trie
            if char not in node.children:
              return word
            # if we can, increment node
            node = node.children[char]
            if node.isWord:
              return word[:index+1]
          return word
          
        words = sentence.split()

        for word in words:
            resultWords.append(prefixSearch(word))
        
        return " ".join(resultWords)

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
