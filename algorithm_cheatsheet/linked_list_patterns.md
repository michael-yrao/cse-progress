# Linked List Patterns

## Quick Reference

| Approach | What it is | When to Use | Example |
|----------|------------|-------------|---------|
| **Dummy node** | Sentinel before head to unify edge cases | Remove or insert at head, delete nodes | Remove Nth From End, Merge Two Lists |
| **Two pointers** | Maintain two references at different speeds or gap | Find middle, detect cycle, nth from end | Cycle Detection, Middle of Linked List |
| **Reverse in-place** | Rewire `next` pointers iteratively | Reverse list, reorder, check palindrome | Reverse Linked List, Reorder List |
| **Recursion** | Use call stack to process nodes | Backtracking, reverse, remove recursively | Reverse List, Remove Nth From End |
| **Partition / merge** | Build new sublists and reconnect | Split by value, merge sorted lists | Partition List, Merge Two Sorted Lists |

---

## Overview

Linked lists require pointer rewiring instead of index access. Key properties:
- No random access: use `next` traversal only
- Head may change during deletion/insertion
- Use sentinel node to avoid special head logic
- Use multiple pointers to locate relative nodes
- Recursion can replace explicit stack tracking

Common linked list operations:
- Traverse with `current`
- Track predecessor with `prev`
- Insert by setting `prev.next`
- Delete by skipping `current`
- Reverse by changing `current.next`

---

## 1. Dummy Node / Sentinel

**Use Case**: Simplify head-edge cases for insertion and deletion

| Component | Value |
|-----------|-------|
| **Purpose** | Add fake node before head |
| **Why** | Avoid special-case head operations |
| **Common use** | Remove head, insert at start, merge lists |

### Pattern

```python
dummy = ListNode(0)
dummy.next = head
prev = dummy
current = head
```

### Example: remove first node or nth from end

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    slow = dummy
    fast = head
    for _ in range(n):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
```

### Pattern recognition

- Deleting a node without knowing if it is head? Use dummy
- Inserting at front or merging lists? Use dummy
- Want uniform logic for all nodes? Use dummy

---

## 2. Two Pointers

**Use Case**: Solve relative-position problems without a length count

| Component | Value |
|-----------|-------|
| **Types** | Fast/slow, gap pointers, twin pointers |
| **Why** | One pass, relative offset, cycle detection |
| **Common use** | Middle, nth-from-end, cycle, palindrome |

### Fast/slow

```python
def middle_node(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Gap pointer

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = head
    second = dummy
    for _ in range(n):
        first = first.next
    while first:
        first = first.next
        second = second.next
    second.next = second.next.next
    return dummy.next
```

### Cycle detection

```python
def has_cycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### Pattern recognition

- Need node relative to end or middle? Use gap pointer
- Need detect cycle or entry point? Use fast/slow
- Need compare pairs from ends? Use reverse + slow pointer

---

## 3. Reverse In-Place

**Use Case**: Rewire list direction without extra nodes

| Component | Value |
|-----------|-------|
| **Purpose** | Reverse `next` pointers |
| **Why** | Palindrome check, reorder, merge from tail |
| **Common use** | Reverse list, reverse sublist |

### Iterative reverse

```python
def reverse_list(head):
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev
```

### Recursive reverse

```python
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

### Pattern recognition

- Need process nodes from tail to head? Reverse list
- Need compare front/back values? Reverse second half first
- Need reorder by alternating ends? Reverse second half and merge

---

## 4. Recursion

**Use Case**: Use call stack to move forward and process on unwind

| Component | Value |
|-----------|-------|
| **Purpose** | Replace manual stack with recursion |
| **Why** | Cleaner reversal/removal logic |
| **Common use** | Reverse list, remove recursively, build stack-based output |

### Typical recursive pattern

```python
def recurse(node):
    if not node:
        return None
    result = recurse(node.next)
    # use node after recursive call
    return result
```

### Example: recursive reverse

```python
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

### Pattern recognition

- Need deep backtracking? Recursion
- Need process after reaching tail? Recursion
- Need simple code for linked structure? Recursion

---

## 5. Partition and Merge

**Use Case**: Build new ordered sublists then reconnect

| Component | Value |
|-----------|-------|
| **Purpose** | Separate nodes into buckets or combined sorted lists |
| **Why** | Preserve relative order while rearranging |
| **Common use** | Partition by value, merge sorted lists |

### Partition example

```python
def partition(head, x):
    before_head = ListNode(0)
    after_head = ListNode(0)
    before = before_head
    after = after_head
    while head:
        if head.val < x:
            before.next = head
            before = before.next
        else:
            after.next = head
            after = after.next
        head = head.next
    after.next = None
    before.next = after_head.next
    return before_head.next
```

### Merge example

```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val < l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
```

### Pattern recognition

- Need keep relative order while splitting? Partition
- Need merge sorted halves? Merge with dummy tail
- Need build output list cleanly? Use dummy + tail

---

## Choosing Your Approach

| Question | Approach |
|----------|----------|
| Need remove or insert at head cleanly? | Dummy node |
| Need nth-from-end or middle? | Two pointers |
| Need reverse or compare back-to-front? | Reverse in-place |
| Need backtracking or unwind logic? | Recursion |
| Need reorder by value or merge sorted lists? | Partition / merge |

---

## Time and Space Complexity

Most linked list operations are O(n) time.
- Single pass algorithms: O(n)
- Reversal / merge: O(n)
- Recursive depth: O(n) stack for recursion
- Extra space: O(1) for in-place pointer rewiring, O(n) only for recursion stack
