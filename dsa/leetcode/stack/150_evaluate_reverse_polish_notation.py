"""
150. Evaluate Reverse Polish Notation   ·   https://leetcode.com/problems/evaluate-reverse-polish-notation/
Pattern: stack

You are given an array of strings `tokens` that represents an arithmetic
expression in Reverse Polish Notation (operators come AFTER their operands).

Evaluate the expression and return an integer that represents its value.

Note:
  - The valid operators are '+', '-', '*', and '/'.
  - Each operand may be an integer or another expression.
  - The division between two integers always TRUNCATES TOWARD ZERO.
  - There will not be any division by zero.
  - The input represents a valid arithmetic expression in RPN.
  - The answer and all intermediate calculations fit in a 32-bit integer.

    tokens = ["2","1","+","3","*"]        ->  9      ((2 + 1) * 3)
    tokens = ["4","13","5","/","+"]       ->  6      (4 + (13 / 5))
    tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]  ->  22

Constraints:
    1 <= tokens.length <= 10^4
    tokens[i] is either an operator ("+", "-", "*", "/") or an integer
    in the range [-200, 200]
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-01 ──────────────
    def evalRPN_20260901(self, tokens: List[str]) -> int:
        # insert into the stack until we see an operator
        # we never insert operators in, so insert the result in each time

        stack = []

        for token in tokens:
            if token in ('+','-','/','*'):
                # problem says this is always valid
                # thus these two should always work without me checking
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                result = 0
                if token == '+':
                    result+=(firstNumber+secondNumber)
                elif token == '-':
                    result+=(firstNumber-secondNumber)
                elif token == '*':
                    result+=(firstNumber*secondNumber)
                elif token == '/':
                    result+=(firstNumber/secondNumber)
                # never actually gets here
                else:
                    result+=0
                stack.append(result)
            # if not symbol then it's a number
            else:
                stack.append(token)
        
        return int(stack[-1])

    # ── Attempt · 2026-08-21 ──────────────
    # ── RECOGNITION — fill BEFORE coding, before the coach says anything ──
    #   shape cues seen →
    #   technique →
    #   discriminator (why this, not the nearest neighbour) →
    def evalRPN_20260821(self, tokens: List[str]) -> int:
        # stack, ideally we store indices by default
        # but since we need to stored calc'd numbers with no indices
        # we need to store the values instead
        # if not operator, push in
        # if operator, pop two, calc result, push in result

        operators = {'+','-','*','/'}
        stack = []

        for token in tokens:
            # if number, just add to stack
            if token not in operators:
                stack.append(token)
            # if not token, pop twice
            else:
                if not stack:
                    return -1
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                result = 0
                if token == '-':
                    result = firstNumber - secondNumber
                elif token == '+':
                    result = firstNumber + secondNumber
                elif token == '*':
                    result = firstNumber * secondNumber
                elif token == '/':
                    result = firstNumber / secondNumber
                stack.append(result)
        
        return int(stack[-1])

    # ── Attempt 1 · 2026-08-11 ────────────────────────────────────────────
    def evalRPN(self, tokens: List[str]) -> int:
        # push when we see number
        # pop two when we see an operator
        stack = []
        
        for token in tokens:
            if token == '+':
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                stack.append(firstNumber + secondNumber)
            elif token == '*':
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                stack.append(firstNumber * secondNumber)
            elif token == '-':
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                stack.append(firstNumber - secondNumber)
            elif token == '/':
                secondNumber = int(stack.pop())
                firstNumber = int(stack.pop())
                stack.append(firstNumber / secondNumber)
            else:
                stack.append(token)
        
        return int(stack.pop())
