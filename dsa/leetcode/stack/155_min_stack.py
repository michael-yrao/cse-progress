"""
155. Min Stack   ·   https://leetcode.com/problems/min-stack/
Pattern: stack

Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

Implement the MinStack class:
  - MinStack()      initializes the stack object.
  - push(val)       pushes val onto the stack.
  - pop()           removes the element on the top of the stack.
  - top()           gets the top element of the stack.
  - getMin()        retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for EACH function.

Example:
    push(-2); push(0); push(-3)
    getMin() -> -3
    pop()
    top()    -> 0
    getMin() -> -2

Constraints:
    -2^31 <= val <= 2^31 - 1
    pop, top and getMin are always called on a non-empty stack.
    At most 3 * 10^4 calls will be made to push, pop, top, and getMin.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


# ── Attempt 1 · 2026-08-12 ────────────────────────────────────────────
class MinStack:
# we store (value, min(stack)) at each value in the stack
    def __init__(self):
        self.stack = []

    def push(self, value: int) -> None:
        # if stack does not exist, push itself as value, min
        if not self.stack:
            self.stack.append((value, value))
        else:
            # if stack does have value already, get latest currentMin
            currentMin = self.stack[-1][1]
            self.stack.append((value, min(currentMin, value)))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
