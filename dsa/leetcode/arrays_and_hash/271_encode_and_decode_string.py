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


# ── Attempt · 2026-09-01 ──────────────
class Solution_20260901:
# prefix length framing
# pick any special char to separate when we encode
    def encode(self, strs: List[str]) -> str:
        result = []
        for string in strs:
            lenString = str(len(string))
            result.append(lenString)
            result.append('#')
            result.append(string)
        return "".join(result)
    def decode(self, s: str) -> List[str]:
        # bootleg two pointer technique to avoid expensive substr
        result = []
        i = 0
        while i < len(s):
            j = i + 1
            while s[j] != '#':
                j+=1
            # now that j is at #, we know i to j is the length
            lenString = int(s[i:j])
            # now we fetch j+1 to j+1+lenString to get the actualString
            string = s[j+1:j+1+lenString]
            # add to result
            result.append(string)
            # move i to past this word
            i = j+1+lenString
        return result

# ── Attempt · 2026-08-22 ──────────────
class Solution_20260822:
# prefix length framing
# we use any special char as a way to distinguish current char and next
# we prefix all of this with the length of each string
    def encode(self, strs: List[str]) -> str:
        # having a bit of fun today and doing array of strings
        # this avoids us creating new strings each time
        # but we are using a lot of arrays which doesn't really save space
        result = []
        for string in strs:
            singleString = []
            lenStr = str(len(string))
            singleString.append(lenStr)
            singleString.append('#')
            singleString.append(string)
            appendString = "".join(singleString)
            result.append(appendString)
        return "".join(result)

    def decode(self, s: str) -> List[str]:
        # 'two pointers' technique
        result = []
        i = 0
        while i < len(s):
            j = i + 1
            while s[j] != '#':
                j+=1
            # now we have i to j, exclusive of j is the length
            lenString = int(s[i:j])
            # the actual string would be j+1 to j+1+lenString
            actualString = s[j+1:j+1+lenString]
            result.append(actualString)
            i = j + 1 + lenString
        return result

# ── Attempt · 2026-08-12 ──────────────
# NOTE: suffix any helper you write with _20260812 — an undated helper collides with the restored canonical one.
class Solution_20260812:
# prefix length framing
# len#str
    def encode(self, strs: List[str]) -> str:
        result = []
        # since string is immutable, we will use an array
        # then convert to a string afterwards
        for string in strs:
            lenString = len(string)
            result.append(str(lenString))
            result.append('#')
            result.append(string)
        return "".join(result)

    def decode(self, s: str) -> List[str]:
        # two pointer technique
        # find the length of each string
        result = []
        i = 0
        while i < len(s):
            j = i + 1
            while s[j] != '#':
                j+=1
            # now i to j is the length
            lenString = int(s[i:j])
            # that means j + 1 to j + 1 + lenString is the string
            string = s[j+1:j+1+lenString]
            result.append(string)
            i = j + 1 + lenString
        return result

# ── Attempt · 2026-08-02 ──────────────
class Solution_20260802:
# classic network prefix length framing
# encoding is add length + a special char in front and concatting all the strings
# decoding is using two pointers to parse out the length and then getting the word without ever reading the word ourselves
    def encode(self, strs: List[str]) -> str:
        # string is immutable, so each time we do string+=string, we are rebuilding a new string
        # this adds up fast for time complexity
        # so we will do an array and convert to a string at the end
        result = []
        for string in strs:
            lenString = len(string)
            result.append(str(lenString))
            result.append("#")
            result.append(string)
        return "".join(result)

    def decode(self, s: str) -> List[str]:
        # two pointers to avoid us ever reading the content of the string other than the length
        result = []

        i = 0
        while i < len(s):
            # i is at the start of the length
            j = i + 1
            while s[j] != '#':
                j+=1
            # python substring is not inclusive of the end
            # j is now at the #, so i to j is the length
            lenString = int(s[i:j])
            # string is then from j+1 to j+1+lenString
            string = s[j+1:j+1+lenString]
            result.append(string)
            i = j+1+lenString

        return result

# ── Attempt · 2026-07-23 ──────────────
class Solution_20260723:
    # Prefix Length Framing
    # Used in transmitting messages across networks without ever reading the messages
    # prefix string with <length># so it becomes <length>#<string><length>#<string>....
    def encode(self, strs: List[str]) -> str:
        resultStr = ""
        for string in strs:
            lenStr = len(string)
            resultStr+=str(lenStr)
            resultStr+="#"
            resultStr+=string
        return resultStr

    def decode(self, s: str) -> List[str]:
        # somewhat two pointer method, one to keep track of beginning of len
        # another to get end of len, which is also at #
        # then we use len to get full word without ever reading the word
        
        result = []
        
        i = 0
        while i < len(s):
            j = i + 1
            while s[j] != '#':
                j+=1
            lenStr = int(s[i:j])
            word = s[j+1:j+1+lenStr]
            result.append(word)
            i=j+1+lenStr
        
        return result

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
