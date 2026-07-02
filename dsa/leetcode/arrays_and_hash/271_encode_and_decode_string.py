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