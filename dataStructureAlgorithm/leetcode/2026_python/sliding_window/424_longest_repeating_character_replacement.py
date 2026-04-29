"""
You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.

Example 1:

Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.

Example 2:

Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.

Constraints:

    1 <= s.length <= 105
    s consists of only uppercase English letters.
    0 <= k <= s.length

"""

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # longest substring is a two pointer / sliding window problem
        # length of substring is based on length of highest frequency value in the substring
        # frequency, so we can do either an array of size 26 since we know it's only uppercase letters
        # or we can do a map to account for all characters and ignore that constraint
        # So one thing to note is that a max length of current substring possible
        # is map.get(maxfreqChar) + k so if (r - l) > map.get(maxfreqChar) + k, we need to shift l
        # so how do we know maxfreqChar in our current substring in constant time
        # in sliding window, we have l and r
        # i want to use r to loop through the string and add freq
        # i want l to keep track of lower bound of the window
        # technically we have constant time to find maxFreqChar due to constraint of uppercase letters making this O(26) -> O(1)

        longestSubstringLength = 0
        l = r = 0
        freqMap = {}

        def maxFreqCharInMap() -> int:
            maxChar = maxFreq = 0
            for char, freq in freqMap.items():
                if freq > maxFreq:
                    maxChar = char
                maxFreq = max(maxFreq,freq)
            return maxChar

        while r < len(s):
            freqMap[s[r]] = freqMap.get(s[r],0) + 1
            maxFreqChar = maxFreqCharInMap()
            # If we are out of bounds, remove frequency from s[l] until we are in bound
            # We do have to keep in mind maxFreqChar in map will change as we decrement s[l]
            while (r - l + 1) > freqMap.get(maxFreqChar,0) + k:
                freqMap[s[l]] = freqMap.get(s[l],0) - 1
                l+=1
                maxFreqChar = maxFreqCharInMap()
            # now we know r - l is valid
            longestSubstringLength = max(longestSubstringLength, r - l + 1)
            r+=1
        return longestSubstringLength
    
    def characterReplacementEfficient(self, s: str, k: int) -> int:
        freqMap = {}
        longestSubstringLength = 0
        
        l = r = 0

        maxFreqCharCount = 0

        while r < len(s):
            freqMap[s[r]] = freqMap.get(s[r],0) + 1
            # we can just do a comparison of current max with current char to get max freq char
            # this way we also don't have to calculate it in the while loop to decrement s[l]
            maxFreqCharCount = max(maxFreqCharCount, freqMap[s[r]])

            # if we are out of range, get rid of s[l] until we are good to go
            while r - l + 1 > maxFreqCharCount + k:
                freqMap[s[l]] = freqMap.get(s[l],0) - 1
                l+=1

            # knowing we are valid, we update max length

            longestSubstringLength = max(longestSubstringLength, r - l + 1)
        
        return longestSubstringLength