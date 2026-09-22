"""
22. Generate Parentheses   ·   https://leetcode.com/problems/generate-parentheses/
Pattern: backtracking

Given n pairs of parentheses, write a function to generate all combinations
of well-formed (valid) parentheses.

Return the list in any order.

Example:
    n = 3  ->  ["((()))","(()())","(())()","()(())","()()()"]
    n = 1  ->  ["()"]

Constraints:
    1 <= n <= 8
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-21 ──────────────
    def generateParenthesis_20260921(self, n: int) -> List[str]:
        # generating all combinations = backtracking
        # let's define the elements we need to complete this
        # path = the current string we have generated, since string is immutable, we do not need a copy
        # state = how many open and closed parentheses do we have
        # choice = choose to add an open or closed parentheses
        # validity = we can place an open parentheses if openState < n and we can place a closed parentheses if openState > closedState
        # base case = len(path) == 2 * n

        result = []

        def backtrack(path, openState, closedState):
            if len(path) == 2 * n:
                result.append(path)
                return
            
            # validity and choice

            # choose to add open parentheses
            if openState < n:
                backtrack(path + '(', openState + 1, closedState)
            
            # choose to add closed parentheses
            if openState > closedState:
                backtrack(path + ')', openState, closedState + 1)
        
        backtrack('',0,0)
        return result

    # ── Attempt 1 · 2026-09-19 ────────────────────────────────────────────
    def generateParenthesis(self, n: int) -> List[str]:
        # the two options we have are open or close parentheses
        # states are book keeping, e.g. what do we have to look at to see if my move is legal
        # state = open counter, close counter
        # path = what we have so far
        # base case = len(path) == 2 * n
        # available choices = choose ( or choose )
        # legality = ( is legal if we have not used n ( yet ; ) is legal if count of ( is greater than count of )
        # exploration = choices bases on available choices and legality
        
        result = []
        
        def backtrack(path, openState, closeState):
            # in backtracking, the base case is completion
            # completion in this case is construction of the full parentheses
            # thus, in completion, we record it
            if len(path) == 2 * n:
                # since string is immutable, no need for copy
                result.append(path)
                return

            # if we haven't used all possible open parentheses, we can continue to do so
            # legality check -> choice -> explore via recursion
            if openState < n:
                backtrack(path + '(', openState + 1, closeState)
            
            # if closeState < openState, then we can also use closed parentheses
            # legality check -> choice -> explore via recursion
            if closeState < openState:
                backtrack(path + ')', openState, closeState + 1)
            
        backtrack('', 0, 0)
        
        return result
