"""
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

    Open brackets must be closed by the same type of brackets.
    Open brackets must be closed in the correct order.
    Every close bracket has a corresponding open bracket of the same type.

Example 1:

Input: s = "()"

Output: true

Example 2:

Input: s = "()[]{}"

Output: true

Example 3:

Input: s = "(]"

Output: false

Example 4:

Input: s = "([])"

Output: true

Example 5:

Input: s = "([)]"

Output: false

Constraints:

    1 <= s.length <= 104
    s consists of parentheses only '()[]{}'.
"""
from collections import deque


class Solution:
    def isValid(self, s: str) -> bool:
        # basically a bunch of if else statements
        # we can insert into stack on opening bracket
        # pop on ending if it matches, return False if not match
        # so one thing we can do is just do an open to close map
        
        openToCloseMap = {'(' : ')', '{' : '}', '[' : ']'}

        stack = deque()

        for char in s:
            # check first if it is a closing bracket
            if char in openToCloseMap.values():
                # if stack is empty and we see an closing bracket, return false
                # if map[peek] != char, also return false
                if not stack or openToCloseMap.get(stack[-1],None) != char:
                    return False
                # otherwise we got a match, pop out opening bracket
                stack.pop()
            if char in openToCloseMap:
                stack.append(char)
        return not stack
    
    def isValidSet(self, s: str) -> bool:
        # basically a bunch of if else statements
        # we can insert into stack on opening bracket
        # pop on ending if it matches, return False if not match
        # so one thing we can do is just do an open to close map
        
        openToCloseMap = {'(' : ')', '{' : '}', '[' : ']'}

        closeBrackets = set(openToCloseMap.values())

        stack = deque()

        for char in s:
            # check first if it is a closing bracket
            if char in closeBrackets:
                # if stack is empty and we see an closing bracket, return false
                # if map[peek] != char, also return false
                if not stack or openToCloseMap.get(stack[-1],None) != char:
                    return False
                # otherwise we got a match, pop out opening bracket
                stack.pop()
            if char in openToCloseMap:
                stack.append(char)
        return not stack
    def isValid_20260630(self, s: str) -> bool:
        # use a map of open -> close brackets
        # use a stack, when we see a key, we push, when we see a value not in the key, we peek and pop
        # actually, that makes it easier to push when not in key especially since we are given s is only parentheses
        parenthesesMap = {')':'(', '}':'{', ']':'['}

        stack = []

        for char in s:
            # if open parentheses, put in stack
            if char not in parenthesesMap:
                stack.append(char)
            else:
                # if closed parentheses, check if top of the stack is the matching open parentheses
                if not stack or stack[-1] != parenthesesMap[char]:
                    return False
                # if it is, pop and continue
                stack.pop()
        
        return len(stack) == 0