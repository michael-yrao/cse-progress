"""
Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.

Machine 1 (sender) has the function:

String encode(List<String> strs) {
    // ... your code
    return encoded_string;
}

Machine 2 (receiver) has the function:

List<String> decode(String encoded_string) {
    // ... your code
    return decoded_strs;
}

So Machine 1 does:

String encoded_string = encode(strs);

and Machine 2 does:

List<String> decoded_strs = decode(encoded_string);

decoded_strs in Machine 2 should be the same as the input strs in Machine 1.

Implement the encode and decode methods.

Example 1:

Input: strs = ["Hello","World"]

Output: ["Hello","World"]

Explanation:

Solution solution = new Solution();
String encoded_string = solution.encode(strs);

// Machine 1 ---encoded_string---> Machine 2

List<String> decoded_strs = solution.decode(encoded_string);


Example 2:

Input: strs = [""]

Output: [""]

Constraints:

    0 <= strs.length < 100
    0 <= strs[i].length < 200
    strs[i] contains any possible characters out of 256 valid ASCII characters.


Follow up: Could you write a generalized algorithm to work on any possible set of characters?
"""
from typing import List


# ── Attempt · 2026-07-13 ──────────────
class Solution_20260713:
    # This problem is about Length Prefix Framing
    def encode(self, strs: List[str]) -> str:
        resultStr = ""
        for string in strs:
            lenString = len(string)
            stringToAppend = str(lenString) + "#" + string
            resultStr+=stringToAppend
        return resultStr

    def decode(self, s: str) -> List[str]:
        # we will use two pointers to help us navigate the string
        result = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != '#':
                j+=1
            # now i->j is len of the string
            lenStr = int(s[i:j])
            # and j+1 -> j+1+lenStr is the string
            string = s[j+1:j+1+lenStr]
            result.append(string)
            i = j+1+lenStr
        return result


# region ⚠ PRIOR ATTEMPTS — SPOILERS · fold before you start

class Solution:

    def encode(self, strs: List[str]) -> str:
        # encode each string with length + non-ascii separator
        endString = ""
        for string in strs:
            strLen = len(string)
            strToAttach = str(strLen)+'#'+string
            endString+=strToAttach
        return endString
    def decode(self, s: str) -> List[str]:
        # look at the number befor each delimiter
        # then fetch that number of characters into each index
        result = []
        while len(s) > 0:
            wordLength = s.split('#')[0]
            lenOfLength = len(wordLength)
            # +1 to skip the #
            restOfWord = s[lenOfLength+1:]
            word = ""
            for i in range(int(wordLength)):
                word+=restOfWord[i]
            result.append(word)
            lenOfWordWithDelimiter = lenOfLength + 1 + int(wordLength)
            s = s[lenOfWordWithDelimiter:]
        return result
    
class Solution_20260701:

    def encode(self, strs: List[str]) -> str:
        # encode each string with length + non-ascii separator
        endString = ""
        for string in strs:
            strLen = len(string)
            strToAttach = str(strLen)+'#'+string
            endString+=strToAttach
        return endString
    def decode(self, s: str) -> List[str]:
        # look at the number befor each delimiter
        # then fetch that number of characters into each index
        result = []
        # split takes O(n) so our previous solution is actually O(n^2)
        # so we will use two pointers to help us determine start and end of a word
        # we will use i and j, i to find the start, j to go through the array
        j = 0
        while j < len(s):
            i = j
            while s[i] != '#':
                i+=1
            # now j to i is the length of the string
            lenStr = int(s[j:i]) 
            # we know word starts at i + 1
            wordStart = i+1
            wordEnd = wordStart + lenStr
            word = s[wordStart:wordEnd]
            result.append(word)
            j=wordEnd
        return result
    
class Solution_20260703:

# this problem is the basis of Length Prefix Framing for transmitting over networks
# we provide a length and a delimiter in front of the string so we don't read the string itself
# and just provide based on the length in front

    def encode(self, strs: List[str]) -> str:
        transmissionString = ""
        for string in strs:
            lenPrefix = len(string)
            lenPrefixFrame = str(lenPrefix) + "#" + string
            transmissionString+=lenPrefixFrame
        return transmissionString

    def decode(self, s: str) -> List[str]:
        # to decode, we want to read the len in front and then take that length into result
        # first thought is to do a split on # and get the first part of the split
        # but doing this for the entire string would give us O(n^2)
        # so we will do it manually using pointers
        # need two pointers, one to track start, one to track end of word
        result = []

        i = 0

        while i < len(s):
            j = i
            while s[j] != '#':
                j+=1
            # now we know i -> j is the length
            lenStr = int(s[i:j])
            # now the word is from j+1 -> j+1+lenStr
            word = s[j+1:j+1+lenStr]
            result.append(word)
            i=j+1+lenStr
        return result
# endregion
