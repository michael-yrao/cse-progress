"""
17. Letter Combinations of a Phone Number   ·   https://leetcode.com/problems/letter-combinations-of-a-phone-number/
Pattern: backtracking

Given a string containing digits from 2-9 inclusive, return all possible
letter combinations that the number could represent. Return the answer in
any order.

A mapping of digits to letters (just like on the telephone buttons) is
given below. Note that 1 does not map to any letters.

    2: abc    3: def    4: ghi    5: jkl
    6: mno    7: pqrs   8: tuv    9: wxyz

Example 1:
    Input:  digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
    Input:  digits = "2"
    Output: ["a","b","c"]

Constraints:
    1 <= digits.length <= 4
    digits[i] is a digit in the range ['2', '9'].
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-09 ──────────────
    def letterCombinations_20261009(self, digits: str) -> List[str]:
        # we need to map 2 through 9 to their respective letters
        # then backtrack via a for loop, reason for for loop is because we are not doing a pick or not pick, we are doing a pick one of the these values associated with a key
        # path: current string
        # base case: len(path) == len(digits)

        result = []

        num_to_char = {
            '2' : ['a', 'b', 'c'],
            '3' : ['d', 'e', 'f'],
            '4' : ['g', 'h', 'i'],
            '5' : ['j', 'k', 'l'],
            '6' : ['m', 'n', 'o'],
            '7' : ['p', 'q', 'r', 's'],
            '8' : ['t', 'u', 'v'],
            '9' : ['w', 'x', 'y', 'z'],
        }

        def backtrack(path):
            if len(path) == len(digits):
                result.append("".join(path.copy()))
                return
            
            for char in num_to_char[digits[len(path)]]:
                path.append(char)
                backtrack(path)
                path.pop()
        
        backtrack([])
        return result

    # ── Attempt 1 · 2026-10-07 ────────────────────────────────────────────
    def letterCombinations(self, digits: str) -> List[str]:
        # map each number to the letters they are associated with, so a num_char map
        # then if we look at this problem, we are saying we want to pick any of these letters and not 'choose or not choose'
        # so this tells me it is a for loop style backtracking problem. 
        # path: current strings so far
        # base case: len(path) == len(digits), add to result

        num_char_map = {
            '2' : ['a','b','c'],
            '3' : ['d','e','f'],
            '4' : ['g','h','i'],
            '5' : ['j','k','l'],
            '6' : ['m','n','o'],
            '7' : ['p','q','r','s'],
            '8' : ['t','u','v'],
            '9' : ['w','x','y','z'],
        }

        result = []

        if len(digits) == 0:
            return result

        def backtrack(path):
            if len(path) == len(digits):
                result.append("".join(path.copy()))
                return
            
            # now we go through the values of each digit and use all of them
            # we can't do this by doing for digit in digits because it will then start doing subsets
            # we are looking for combinations here
            for char in num_char_map[digits[len(path)]]:
                path.append(char)
                backtrack(path)
                path.pop()
        
        backtrack([])
        return result
