"""
Problem Description

You are given a string s and an integer k. Your task is to determine if the string is a k-palindrome.

A string is considered a k-palindrome if you can transform it into a palindrome by removing at most k characters from it.

For example:

    If s = "abcdeca" and k = 2, you can remove characters 'b' and 'e' to get "acdca", which is a palindrome. So this would return true.
    If a string is already a palindrome, it's a k-palindrome for any k ≥ 0.
    If you need to remove more than k characters to make it a palindrome, then it's not a k-palindrome.

The function should return true if the string can be made into a palindrome by removing at most k characters, and false otherwise.
"""

class Solution:
    def kPalindrome(self, s: str, k: int) -> bool:
        # we'll leverage the same idea we did for valid palindrome 2
        # we use left and right pointer like we would for valid palindrome 1
        # and then we keep a counter every time we skip an element
        # now issue becomes, what happens if we can skip on both sides
        # then doesn't this become a backtracking problem where we need to decide which side to skip?

        def backtrack(l,r,skipsRemaining):
            if skipsRemaining < 0:
                return False

            while l < r:
                if s[l] == s[r]:
                    l+=1
                    r-=1
                else:
                    # choose whether to go left or right
                    return backtrack(l+1, r, skipsRemaining-1) or backtrack(l,r-1,skipsRemaining-1)
            return True

        return backtrack(0,len(s)-1,k)