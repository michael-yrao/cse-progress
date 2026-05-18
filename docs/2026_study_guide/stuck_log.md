# Stuck Log

## 1. ❌ LeetCode 19 - Remove Nth Node From End of List (Recursive)
* **Date**: May 19, 2026
* **Topic(s)**: Recursion / Call Stack Traversal

### a. Where did I get stuck?
* **Visualizing backward counting**: I couldn't wrap my head around how recursion counts from the end of a singly linked list without a `prev` pointer.

### b. The Core Realization
* The computer's call stack acts as a natural memory engine. By placing the `counter += 1` statement *after* the recursive function call, the code executes in exact reverse order (backwards from the tail) as the function execution contexts pop off the stack. 

### c. Code Snippet to Remember
```python
# The recursive reverse execution pattern:
head.next = removeFromEnd(node.next) # 1. Go all the way to the end first
counter += 1             # 2. This increments from the back on the way up
```

Refer to the drawing in the surface for traces