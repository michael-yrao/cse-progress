# Graph — Technique Hub

Nodes + edges, represented as an adjacency map/list (or an implicit grid). This page maps graph problems to the techniques you reach for.

## Structure facts

- Represent as `adj = defaultdict(list)`; **undirected = add both directions**.
- Grids are implicit graphs: cell `(r,c)` neighbors are up/down/left/right.
- Track `visited` (nodes, not (node,parent) pairs) to avoid re-processing / infinite loops.

## Techniques used on graphs

| Technique | Reach for it when | Doc |
|---|---|---|
| **BFS / DFS traversal** | Reachability, components, flood fill, shortest # of edges (BFS) | see [tree_bfs](../techniques/tree_bfs.md) / [tree_dfs](../techniques/tree_dfs.md) (same idea + a `visited` set) |
| **Union-Find** | Connectivity, grouping, cycle detection (undirected) | [techniques/union_find](../techniques/union_find.md) |
| **Topological sort** | Ordering with dependencies on a DAG | [techniques/topological_sort](../techniques/topological_sort.md) |

*(Dijkstra / heap shortest-path arrives with the Advanced Graphs block — will get its own doc then.)*

## Deciding fast

| Question | Technique |
|---|---|
| How many connected components? | Union-Find, or BFS/DFS flood fill |
| Is there a cycle (undirected)? | Union-Find (union of already-connected = cycle) |
| Valid tree? | Union-Find + `edges == n-1` connectivity check |
| Order tasks with prerequisites? | Topological sort (Kahn's / DFS) |
| Shortest # of steps in a grid/graph? | BFS (multi-source BFS if many starts, e.g. rotting oranges) |

## Representative problems

200 Number of Islands, 133 Clone Graph, 207/210 Course Schedule, 261 Graph Valid Tree, 323 Connected Components, 684 Redundant Connection, 130 Surrounded Regions, 994 Rotting Oranges, 417 Pacific Atlantic, 695 Max Area of Island.
