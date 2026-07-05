# Tree DFS (Depth-First Traversal)

Explore one branch fully before backtracking, via recursion (call stack) or an explicit stack. The **order you process the node relative to its children** — pre / in / post — is the whole choice.

## When to reach for it (recognition signal)

- compute a property that depends on children (height, balanced, diameter) → **postorder**
- need parent context available before children → **preorder**
- need sorted output from a **BST**, or validate BST → **inorder**

## The three orders (recursive)

```python
def pre(node):   # Root, Left, Right
    if not node: return
    visit(node); pre(node.left); pre(node.right)

def ino(node):   # Left, Root, Right   — BST inorder = sorted ascending
    if not node: return
    ino(node.left); visit(node); ino(node.right)

def post(node):  # Left, Right, Root   — child results ready before parent
    if not node: return
    post(node.left); post(node.right); visit(node)
```

## Two facts that pick the order for you

- **Postorder = "compute from children."** Height, balanced-check, diameter, subtree sums — anything where the parent's answer needs the children's answers first.
- **Inorder of a BST is sorted.** Validate-BST and kth-smallest fall out of this — but the comparison must sit *between* the left and right recursion (carry a running `prev`), not before/after both.

## Common DFS shapes

```python
def height(node):                      # postorder
    if not node: return 0
    return 1 + max(height(node.left), height(node.right))

def is_valid_bst(node, lo=float('-inf'), hi=float('inf')):
    if not node: return True
    if not (lo < node.val < hi): return False
    return (is_valid_bst(node.left, lo, node.val) and
            is_valid_bst(node.right, node.val, hi))
```

## Practice

| Problem | NC150? | Order |
|---|---|---|
| 104. Maximum Depth | ✅ | postorder (height) |
| 110. Balanced Binary Tree | ✅ | postorder (child heights, -1 sentinel) |
| 543. Diameter | ✅ | postorder (local max at each node) |
| 98. Validate BST | ✅ | inorder / bounds |
| 226. Invert Tree | ✅ | any order |
| 236. Lowest Common Ancestor | ✅ | postorder |

## Common pitfalls

- **Missing the null base case** → crash on leaf children.
- **Confusing "depth returned upward" with "answer tracked globally"** — e.g. diameter is a local max at every node, *separate* from the height you return (543 trap).
- **Sentinel propagation** — balanced-check returns `-1` for "unbalanced"; you must short-circuit on it before arithmetic (110 trap).
- **Recursion depth** — O(h) stack; a skewed tree is O(n).
