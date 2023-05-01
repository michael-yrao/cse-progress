import unittest

class Solution:
    def validPalindrome(self, s: str) -> bool:
        # 1. Create l,r=0,len-1 to start our palindrome validation
        # 2. When the values don't match, we want to check if we remove one or the other if the rest of the string is palindrome

        l,r = 0,len(s)-1
        while r > l:
            if s[l] != s[r]:
                # python doesn't include last char in substring, so need r+1 to get r
                skipLeft = s[l+1:r+1] 
                skipRight = s[l:r]
                # If either one is a palindrome after skipping a char, we know we have a palindrome
                # If neither are, then we should be returning false here
                return skipLeft == skipLeft[::-1] or skipRight == skipRight[::-1]
            l+=1
            r-=1
        return True
    
class UnitTest(unittest.TestCase):
    def testValidPalindromeII(self):
        input = "abca"
        expectedAnswer = True
        result = Solution().validPalindrome(input)
        self.assertEqual(expectedAnswer,result)

unittest.main()