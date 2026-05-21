# 🧠 Recursion & Call Stack Traversal Patterns

## Quick Reference


| Pattern | Execution Order | Stack Frame Lifecycle | Core Use Case |
| :--- | :--- | :--- | :--- |
| **Forward Recursion** | State updates on the way **DOWN** | Evaluated *before* diving to next frame | Building pipelines, tree down-traversal, accumulations |
| **Backward Recursion**| State updates on the way **UP** | Evaluated *after* returning from base case | Counting from tail, reversing chains, post-order trees |

---

## 1. Forward Recursion (Pre-Order Execution)

**Use Case**: Building structural pipelines forward, or executing state evaluations on the way down toward the base case.


| Component | Value |
| :--- | :--- |
| **Work Execution** | Evaluated **before** invoking the recursive function call |
| **Data Stream Direction** | Emits processing results from start boundary to end boundary |
| **State Retention** | Passed forward directly into the next frame's input parameters |

**Implementation**:
```python
def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
    # Base Case: If either list runs out, return the remaining pool
    if not list1: return list2
    if not list2: return list1
    
    # WORK HAPPENS FIRST: Compare current head elements
    if list1.val < list2.val:
        # Delegate remaining pipeline structure to the next frame
        list1.next = self.mergeTwoLists(list1.next, list2)
        return list1 # Return current node as the confirmed segment head
    else:
        list2.next = self.mergeTwoLists(list1, list2.next)
        return list2 # Return current node as the confirmed segment head
```

**Example**: [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com)

---

## 2. Backward Recursion (Post-Order Execution)

**Use Case**: Traversing to an unknown endpoint (like a tail pointer) first, then running evaluations backward relative to that end boundary.


| Component | Value |
| :--- | :--- |
| **Work Execution** | Evaluated **after** the nested recursive call returns |
| **Data Stream Direction** | Emits processing results backwards from end boundary to start boundary |
| **State Retention** | Managed implicitly by the hardware Call Stack frames popping off |

**Implementation**:
```python
def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
    self.counter = 0 # Explicit global scope primitive to track return index
    
    def helper(node):
        if not node: return None # Base case: plant flag at the absolute tail
        
        # DIVING PHASE: Push frames forward until tail boundary is reached
        node.next = helper(node.next)
        
        # POPPING PHASE: This logic executes in reverse order on the way up
        self.counter += 1 
        if self.counter == n:
            return node.next # Drop target node by returning its successor pointer
            
        return node # Preserve untouched structural links
        
    dummy = ListNode(0, head)
    dummy.next = helper(head)
    return dummy.next
```

**Example**: [LeetCode 19 - Remove Nth Node From End of List](https://leetcode.com)

---

## Understanding Call Stack Traversal Direction

### What is it?
The **Call Stack Lifecycle** dictates the direction of logic processing by breaking a recursive runtime into two discrete vector fields: the journey down (Diving Phase) and the journey up (Popping Phase).

### Why it matters
Failing to recognize execution direction causes pointer truncation or counter shifts. For instance, in a singly linked list, counting forward is trivial, but counting from the end requires you to leverage the hardware stack frames to act as an implicit backward pointer engine.

### Real Examples

#### Example 1: Forward Accumulation Tree Depth (Forward Pattern)
```python
def maxDepthForward(self, root: TreeNode, current_depth: int = 1) -> int:
    if not root: return current_depth - 1
    # State is accumulated on the way down via argument updates
    left = self.maxDepthForward(root.left, current_depth + 1)
    right = self.maxDepthForward(root.right, current_depth + 1)
    return max(left, right)
```

#### Example 2: Evaluative Bottom-Up Tree Depth (Backward Pattern)
```python
def maxDepthBackward(self, root: TreeNode) -> int:
    if not root: return 0
    # Dive completely to leaf nodes before running math calculations
    left = self.maxDepthBackward(root.left)
    right = self.maxDepthBackward(root.right)
    # Work happens on the return path up the stack frames
    return max(left, right) + 1
```

### Pattern Recognition


| Context | How to Identify |
| :--- | :--- |
| **Pipeline/Chain Construction** | If current nodes must immediately resolve their connections to lookups before evaluating children, choose **Forward**. |
| **End-Relative Analytics** | If constraints require metric calculations relative to an unknown end boundary, choose **Backward**. |

---

## Key Insights

### Why Call Stack Position Matters

*   **Pre-Call Location**: Code written before the helper execution runs in standard, predictable index increments. It protects memory scales because failures can exit early before exhausting system resources.
*   **Post-Call Location**: Code written after the helper execution defers processing entirely. It consumes memory space because the system must cache every single state context variable simultaneously until the final leaf node or null reference unblocks the chain.

### Mental Model

```text
FORWARD EXECUTION LOGIC              BACKWARD EXECUTION LOGIC
      (Diving Down)                        (Popping Up)
 ┌─────────────────────────┐          ┌─────────────────────────┐
 │  Step 1: Do Local Work  │          │  Step 3: Do Local Work  │
 └────────────┬────────────┘          └────────────▲────────────┘
              │                                    │
              ▼                                    │
 ┌─────────────────────────┐          ┌────────────┴─────────────┐
 │  Step 2: Recursive Call │          │ Step 2: Recursive Return │
 └─────────────────────────┘          └──────────────────────────┘
```
