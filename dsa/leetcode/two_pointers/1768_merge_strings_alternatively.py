"""
Docstring for dsa.leetcode.two_pointers.1768_merge_strings_alternatively
You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.

Return the merged string.

 

Example 1:

Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
Explanation: The merged string will be merged as so:
word1:  a   b   c
word2:    p   q   r
merged: a p b q c r

Example 2:

Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
Explanation: Notice that as word2 is longer, "rs" is appended to the end.
word1:  a   b 
word2:    p   q   r   s
merged: a p b q   r   s

Example 3:

Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
Explanation: Notice that as word1 is longer, "cd" is appended to the end.
word1:  a   b   c   d
word2:    p   q 
merged: a p b q c   d

Constraints:

    1 <= word1.length, word2.length <= 100
    word1 and word2 consist of lowercase English letters.

"""

class Solution:

    # ── Attempt · 2026-08-06 ──────────────
    def mergeAlternately_20260806(self, word1: str, word2: str) -> str:
        w1t, w2t = 0, 0
        result = []
        while w1t < len(word1) and w2t < len(word2):
            result.append(word1[w1t])
            result.append(word2[w2t])
            w1t+=1
            w2t+=1
        
        while w1t < len(word1):
            result.append(word1[w1t])
            w1t+=1
        
        while w2t < len(word2):
            result.append(word2[w2t])
            w2t+=1
        
        return "".join(result)

    def mergeAlternately(self, word1: str, word2: str) -> str:
        result = ""
        p1 = p2 = 0
        while p1 < len(word1) and p2 < len(word2):
            result += word1[p1]
            result += word2[p2]
            p1+=1
            p2+=1
        result += word1[p1:]
        result += word2[p2:]
        return result
