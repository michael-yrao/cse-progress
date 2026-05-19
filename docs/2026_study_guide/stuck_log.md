# Stuck Log

## 1. LeetCode 19 - Remove Nth Node From End of List (Recursive)
* **Date**: May 18, 2026
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

## 2. ❌ LeetCode 20 - Valid Parentheses (Intuitive Set Filter)
* **Date**: May 19, 2026
* **Topic(s)**: Stacks / Set-Membership Optimization

### a. Where did I get stuck?
* **Hidden Inner Loops**: My initial design used `if char in openToCloseMap.values()`. This introduced a hidden sequential lookup time because Python must linearly scan through a dictionary's values on every single character iteration.

### b. The Core Realization
* Readability and intuition are paramount. To keep my intuitive, forward-facing map configuration (`openToCloseMap = {'(': ')'}`), I can decouple the values into an independent, pre-calculated Python Set (`closing_set = set(openToCloseMap.values())`). Because Sets leverage internal hash tables, checking `if char in closing_set` runs in pure \(O(1)\) constant time. This keeps my logic deeply readable to me while preserving mathematically flawless execution speed.

### c. Code Snippet to Remember
```python
openToCloseMap = {'(': ')', '{': '}', '[': ']'}
closing_set = set(openToCloseMap.values()) # Pre-calculate once for O(1) searches

for char in s:
    if char in closing_set:         # Pure O(1) Set Lookup
        if not stack or openToCloseMap[stack[-1]] != char: return False
        stack.pop()
    elif char in openToCloseMap:    # Pure O(1) Key Lookup
        stack.append(char)
```
