# Dummy Node (Sentinel)

A fake node placed **before the head** of a linked list so that operations on the head need no special-casing. Also the backbone of "build a new list" (merge/partition) via a `dummy` + `tail`.

## When to reach for it (recognition signal)

- deleting or inserting at the **head** (head may change)
- **building** a new list (merge two lists, partition, add two numbers)
- you catch yourself writing `if node == head: ...` special cases

## Template

```python
dummy = ListNode(0)
dummy.next = head
prev = dummy
# ... walk prev/curr, splice via prev.next ...
return dummy.next          # NOT head — head may have changed
```

### Build-a-list variant (merge / partition)

Keep a `tail` you append to; return `dummy.next`:

```python
def merge_two_lists(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val < b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b       # attach the remainder
    return dummy.next
```

## Practice

| Problem | NC150? | Wrinkle |
|---|---|---|
| 21. Merge Two Sorted Lists | ✅ | dummy + tail build |
| 19. Remove Nth Node From End | ✅ | dummy so removing the head is uniform |
| 2. Add Two Numbers | ✅ | dummy + tail, carry |
| 83 / 82. Remove Duplicates | No | dummy for 82 (head may be a dup) |
| 86. Partition List | No | two dummies (before / after), splice |

## Common pitfalls

- **Returning `head` instead of `dummy.next`** — if the head was removed/changed, `head` is stale.
- **Forgetting to advance `prev`/`tail`** — leaves the list mis-wired.
- **Not terminating the tail** (`tail.next = None`) in partition-style splits → accidental cycle.
