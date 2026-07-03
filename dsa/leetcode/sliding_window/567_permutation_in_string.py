"""
Given two strings s1 and s2, return true if s2 contains a of s1, or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.

Example 1:

Input: s1 = "ab", s2 = "eidbaooo"
Output: true
Explanation: s2 contains one permutation of s1 ("ba").

Example 2:

Input: s1 = "ab", s2 = "eidboaoo"
Output: false

Constraints:

    1 <= s1.length, s2.length <= 104
    s1 and s2 consist of lowercase English letters.

"""

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # basically we are looking for some form of s1 in s2
        # we can just assume a window of size s1
        # permutation is same as anagram, so we can just do map of frequency
        # so we start with s1FreqMap
        # go through the window of s1 in s2, compare s1FreqMap vs s2FreqMap and return
        # problem is that map comparison is O(n) so this solution is O(n*m) where n is size of s2 and m is size of s1
        # if instead of a map, we use an array of size 26 due to constraint of lowercase English letters
        # we can reduce comparison to O(26) so we get O(n)

        def compareS1andS2() -> bool:
            for i in range(26):
                if s1Array[i] != s2Array[i]:
                    return False
            return True

        s1Array = [0] * 26
        s2Array = [0] * 26

        l = r = 0

        # invalid query if s1 > s2

        if len(s1) > len(s2):
            return False

        # populate s1Array with frequency from s1

        for i in range(len(s1)):
            s1Array[ord(s1[i]) - ord('a')] += 1

        # now we go through s2 with sliding window and increment/decrement from s2Array

        while r < len(s2):
            s2Array[ord(s2[r]) - ord('a')] += 1
            # make sure size of window isn't bigger than size of s1
            # this is never actually going to run to O(len(s1)) since it runs every iteration 
            # it will at most be ran 1 iteration each outer iteration
            while r - l + 1 > len(s1):
                s2Array[ord(s2[l]) - ord('a')] -= 1
                l+=1
            # now that we are valid, compare the two arrays
            if compareS1andS2():
                return True
            r+=1
        return False
    def checkInclusion_20260702(self, s1: str, s2: str) -> bool:
        # we are given s1 and s2 are lowercase
        # so we can use a frequency array to represent these strings

        if len(s1) > len(s2):
            return False

        s1FreqArray = [0] * 26
        s2FreqArray = [0] * 26

        for char in s1:
            charPosition = ord(char) - ord('a')
            s1FreqArray[charPosition]+=1

        def checkS2ContainsS1():
            for i in range(26):
                if s1FreqArray[i] != s2FreqArray[i]:
                    return False
            return True

        # basically we are to keep track of a window of size s1 in s2
        l = r = 0
        while r < len(s2):
            charPosition = ord(s2[r]) - ord('a')
            s2FreqArray[charPosition]+=1
            # keep window size smaller or equal to len(s1)
            if r - l + 1 > len(s1):
                charPosition = ord(s2[l]) - ord('a')
                s2FreqArray[charPosition]-=1
                l+=1
            # now that we know the size is valid, check if s1 is within s2 starting from this index
            if checkS2ContainsS1():
                return True
            r+=1
        return False