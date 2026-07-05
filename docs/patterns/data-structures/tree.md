# Tree Patterns

## Quick Reference

| Traversal | Order | When to Use | Use Case |
|-----------|-------|------------|----------|
| **Preorder** | Root → Left → Right | Process parent first | Copy tree, serialization, build expression tree |
| **Inorder** | Left → Root → Right | Process parent middle | BST sorted output, debug structure |
| **Postorder** | Left → Right → Root | Process children first | Delete tree, compute properties, dependent calculations |
| **BFS** | Level by level | Process nodes by depth | Level order traversal, minimum depth, closest node |

---

## DFS (Depth-First Search)

### Overview

DFS explores as far as possible along one branch before backtracking. Two implementations:
- **Recursive**: Call stack handles backtracking implicitly
- **Iterative**: Explicit stack for backtracking control

| Component | Value |
|-----------|-------|
| **Data structure** | Stack (LIFO) |
| **Traversal style** | Deep first |

Both traverse all nodes; choice depends on problem needs.

---

## BFS (Breadth-First Search)

### Overview

BFS visits nodes by level, one depth at a time. It uses a queue instead of a stack and explores all nodes at the current depth before moving deeper.

**Use Case**: Process nodes by distance or level order.

| Component | Value |
|-----------|-------|
| **When** | Level by level |
| **Process order** | Current node, then children |
| **Data structure** | Queue (FIFO) |
| **Return** | Values grouped by depth |

### Iterative

```python
def bfs(root):
    if not root:
        return []
    queue = [root]
    result = []
    while queue:
        level_size = len(queue)
        level_vals = []
        for _ in range(level_size):
            node = queue.pop(0)
            level_vals.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_vals)
    return result
```

### Pattern Recognition

- **Need level grouping?** BFS
- **Need shortest path / minimum depth?** BFS
- **Need first found nearest node?** BFS
- **Need tree serialized by levels?** BFS

### Example

Tree: `1 / \ 2 3`  
Output: `[[1], [2, 3]]`

**LeetCode**: [102 - Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

---

## 1. Preorder Traversal (Root → Left → Right)

**Use Case**: Process node before visiting subtrees

| Component | Value |
|-----------|-------|
| **When** | After arriving at node |
| **Process order** | Node first, children after |
| **Return** | Process value immediately |

### Recursive

```python
def preorder(node):
    if not node:
        return
    process(node.val)      # Visit root FIRST
    preorder(node.left)
    preorder(node.right)
```

### Iterative

```python
def preorder_iterative(root):
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        if not node:
            continue
        result.append(node.val)
        # Push right first (stack is LIFO, so left processes first)
        stack.append(node.right)
        stack.append(node.left)
    return result
```

### Pattern Recognition

- **Need parent info available to children?** Preorder
- **Copying tree structure?** Preorder (set children after processing parent)
- **Serialization for deserialization?** Preorder with None markers

### Example

Tree: `1 / \ 2 3`  
Output: `1, 2, 3`

**LeetCode**: [144 - Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/)

---

## 2. Inorder Traversal (Left → Root → Right)

**Use Case**: Process node between left and right subtrees

| Component | Value |
|-----------|-------|
| **When** | After left subtree, before right subtree |
| **Process order** | Left child, node, right child |
| **Special property** | BST inorder = sorted ascending |

### Recursive

```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    process(node.val)      # Visit root MIDDLE
    inorder(node.right)
```

### Iterative

```python
def inorder_iterative(root):
    stack = []
    result = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result
```

### Pattern Recognition

- **Need sorted BST sequence?** Inorder
- **Validate BST property?** Inorder (check if output is sorted)
- **Need values in ascending order?** Inorder

### Example

Tree: `1 / \ 2 3`  
Output: `2, 1, 3`

BST: `2 / \ 1 3` → Inorder: `1, 2, 3` (sorted)

**LeetCode**: [94 - Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/)

---

## 3. Postorder Traversal (Left → Right → Root)

**Use Case**: Process node after visiting children

| Component | Value |
|-----------|-------|
| **When** | After visiting both subtrees |
| **Process order** | Children first, node last |
| **Dependency** | Need child results to process parent |

### Recursive

```python
def postorder(node):
    if not node:
        return
    postorder(node.left)
    postorder(node.right)
    process(node.val)      # Visit root LAST
```

### Iterative

```python
def postorder_iterative(root):
    stack = [root]
    result = []
    prev = None
    while stack:
        current = stack[-1]
        if not current:
            stack.pop()
            continue
        # Visit only when both children processed
        if not current.left and not current.right:
            result.append(current.val)
            stack.pop()
        elif prev and (prev == current.left or prev == current.right):
            result.append(current.val)
            stack.pop()
        else:
            # Push right then left (stack is LIFO)
            stack.append(current.right)
            stack.append(current.left)
        prev = current
    return result
```

### Pattern Recognition

- **Need child results first?** Postorder
- **Deleting tree nodes?** Postorder (free children before parent)
- **Computing tree height or depth?** Postorder (height depends on children)
- **Checking if balanced?** Postorder (need child heights first)

### Example

Tree: `1 / \ 2 3`  
Output: `2, 3, 1`

Balanced check: Must compute child heights before determining parent balance.

**LeetCode**: [145 - Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/)

---

## Common DFS Patterns

### Pattern 1: Compute Tree Height
Postorder needed (child results first).

```python
def height(node):
    if not node:
        return 0
    left_h = height(node.left)      # Get left height
    right_h = height(node.right)    # Get right height
    return max(left_h, right_h) + 1 # Use heights to compute parent
```

### Pattern 2: Delete Tree
Postorder needed (delete children before parent).

```python
def delete(node):
    if not node:
        return None
    delete(node.left)               # Delete left subtree
    delete(node.right)              # Delete right subtree
    node.next = None                # Delete current (safe because children gone)
    return None
```

### Pattern 3: Validate BST
Inorder produces sorted sequence; check if ascending.

```python
def is_bst(node):
    def inorder_check(node):
        if not node:
            return True, float('-inf')
        left_valid, max_left = inorder_check(node.left)
        if not left_valid or node.val <= max_left:
            return False, node.val
        right_valid, max_right = inorder_check(node.right)
        return right_valid and node.val < max_right, max_right
    
    valid, _ = inorder_check(node)
    return valid
```

---

## Choosing Your Traversal

| Question | Answer | Traversal |
|----------|--------|-----------|
| Do I need parent info before processing children? | Yes | Preorder |
| Do I need sorted BST output? | Yes | Inorder |
| Do I need child results before processing parent? | Yes | Postorder |
| Do I need to modify structure (delete/restructure)? | Yes | Postorder |
| Do I need to apply operation before accessing children? | Yes | Preorder |

---

## Time and Space Complexity

All three traversals:
- **Time**: O(n) - visit each node once
- **Space**: O(h) - recursion stack depth, where h = tree height
  - Balanced tree: O(log n)
  - Skewed tree: O(n) worst case

