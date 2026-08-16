# Tree characterization — pick any two, get the third

For a graph on **n** vertices, these three are so linked that **any two force the third**:

1. **connected**
2. **acyclic**
3. **exactly `n − 1` edges**

## Why

Connected + `n−1` edges ⟹ acyclic. Suppose there were a cycle. Delete one of its
edges — the graph is *still* connected, because the rest of the cycle detours around
it. That leaves `n` vertices connected by `n−2` edges, and connecting `n` vertices
needs at least `n−1`. Contradiction.

## Where it shows up

**261 Graph Valid Tree** — this is the whole problem. Two ways to spend it:

| | Check directly | Get free |
|---|---|---|
| **DFS** | connected (`len(visited) == n`) + edge count | acyclic |
| **Union-Find** | acyclic (a `find` collision *is* a cycle) + connected | edge count |

⚠️ **DFS cannot drop the edge-count line.** A triangle `n=3, [[0,1],[1,2],[2,0]]`
visits all three nodes, so `len(visited) == n` passes on a graph that is not a tree.
Union-Find *can* drop it — it sees the cycle happen rather than inferring it.

**Rooted trees** get a fourth equivalent: every node has exactly one parent except
the root. That is what makes a parent-pointer check enough in tree problems.
