"""
Given two strings s and t of lengths m and n respectively, return the minimum window of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Example 1:

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:

Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.

Example 3:

Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

Constraints:

    m == s.length
    n == t.length
    1 <= m, n <= 105
    s and t consist of uppercase and lowercase English letters.

Follow up: Could you find an algorithm that runs in O(m + n) time?
"""
class Solution:

    def minWindow(self, s: str, t: str) -> str:
        # I initially assumed minimum window must start/end with a char from t
        # but it fails with scenarios like s = "aaab" and t = "ab"
        # where the shortest is size 2 but our initial solution would give size 4
        # we will still use maps of freq
        # but we will keep track of what we have (sMap) vs what we need (tMap)
        # we will update result iff sMap has same count for each char as tMap
        return "TBD"


    def minWindowIncorrect(self, s: str, t: str) -> str:
        # this is similar to character replacement and permutation
        # so we do sliding window and we have formula of (r - l + 1) = permutation + k
        # big thing here is that k is a variable and we want to minimize it essentially
        # also a big thing to note here is that a potential result substring must start and finish with a char in t
        # we do care for freq like we did in both character replacement and permutation
        # so we should use a map
        # if potential solutions must start and end with a char in t, we should just have a map for t's frequency only
        # and then another for s's frequency
        
        result = ""
        if len(t) > len(s):
            return result
        
        sMap = {}
        tMap = {}

        for i in range(len(t)):
            tMap[t[i]] = 1 + tMap.get(t[i],0)

        def isResultComplete()->bool:
            # check if all of tMap is in result
            # result's frequency is in sMap
            for key in tMap.keys():
                # sMap can have more but not less than tMap
                if sMap[key] - tMap[key] < 0:
                    return False
            return True

        l = r = 0

        while r < len(s):
            sMap[s[r]] = 1 + sMap.get(s[i],0)
            result.append(s[r])
            # so we want to make sure result starts with a char from t
            while s[l] not in tMap:
                # remove first element from result
                result=result[1:]
                l+=1
            # now that we know we are on a possible result
            # we need to make sure all characters of t are covered in the result
            if s[r] in tMap:
                # i have these on different ifs to reduce some runtime
                if isResultComplete:
                    return result
            # if not a potential result, we just keep adding to result and increment r
            r+=1
        
        # if we exited loop, we did not find a result
        return ""