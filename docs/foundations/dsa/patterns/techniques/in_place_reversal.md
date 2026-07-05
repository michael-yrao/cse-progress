# In-Place Linked List Reversal

Reverse a list (or sublist) by **rewiring `next` pointers** — O(1) extra space, no new nodes.

## When to reach for it (recognition signal)

- "reverse the list" / "reverse nodes between i and j" / "reverse in groups of k"
- process nodes **tail-to-head** (you have only forward pointers)
- palindrome check or reorder (reverse the second half, then compare/merge)

## Iterative template (prev / curr / next)

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next     # SAVE next before you clobber it
        curr.next = prev    # flip
        prev = curr         # advance
        curr = nxt
    return prev             # new head
```

The one rule: **save `curr.next` before rewiring**, or you lose the rest of the list.

## Recursive template

```python
def reverse(head):
    if not head or not head.next:
        return head
    new_head = reverse(head.next)   # reverse the rest (trust it)
    head.next.next = head           # the node after me points back to me
    head.next = None                # I become the tail
    return new_head                 # relayed up unchanged
```

Key insight (the confusing part): the **work** is the two pointer flips (side effects on `head`/`head.next`); `new_head` is just **the answer being relayed up the call stack** — it's found once at the base case and passed through every frame untouched. Return value and work are separate jobs.

## Practice

| Problem | NC150? | Wrinkle |
|---|---|---|
| 206. Reverse Linked List | ✅ | Bare reversal, both forms |
| 92. Reverse Linked List II | No | Reverse only `[left, right]` |
| 234. Palindrome Linked List | No | Reverse second half, compare |
| 143. Reorder List | No | Find middle → reverse half → merge |
| 25. Reverse Nodes in k-Group | No | Reverse fixed-size windows |

## Common pitfalls

- **Clobbering `next`** before saving it (iterative) — always `nxt = curr.next` first.
- **Recursive `head.next = None` omitted** → the old head still points forward, creating a cycle.
- **Expecting `new_head` to change per frame** — it doesn't; it's a pass-through payload. See [recursion](recursion.md).
