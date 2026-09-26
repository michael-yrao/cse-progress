- **2026-09-26 · 169 Majority Element** (🟢 s2 review; retry, half-spoiled: tracker names Boyer-Moore) — ✅ **hit.**
  Boyer-Moore named in the top comment; first written as the 1-slot generalised form (a one-key map with
  decrement-all), then the two-variable form on request, both unaided and correct (v2 fuzzed 20k valid inputs).
  Learner's own aside: "same reset instinct as Kadane's" — a cross-technique link made unprompted. → 🟢 s3 → 🎓.
- **2026-09-26 · 787 Cheapest Flights Within K Stops** (🟢 prov lock-down; retry, half-spoiled: graphs folder) — ✅ **hit.**
  "Cheapest → shortest path, k stops → Bellman-Ford" plus the picking feature stated outright: one edge per round, so
  relax off a snapshot copy. Blank page, correct first run. → 🟢 s1 (lock-down held).
- **2026-09-26 · 34 Find First and Last Position** (🟡 re-rep; retry, half-spoiled: binary_search folder) — ✅ **hit.**
  Two-boundary binary search called in the top comment; the deciding detail (round the upper-bound midpoint up so a
  two-element window terminates) was in the code unprompted. Blank page, correct first run. → 🟢 s1.
- **2026-09-26 · 1631 Path With Minimum Effort** (🆕 consolidation rep; half-spoiled: the schedule header named
  "Dijkstra consolidation") — ✅ **hit.** Dijkstra named unaided ("obviously"); the heap-vs-array pick was reasoned
  from the grid's ≤4 neighbours after a general question on when each wins (answered as a teach, not a hint). The
  min-over-max feature came out in the code (running max at pop), not in the comment. Blank page, correct in one
  pass. → 🟢 s1. ⚙️ The pruned distance-array variant was then attempted on request and needed three corrections
  (compare target, dropped max, stale overwrite) — carded as a variant rep, not a rating input.
- **2026-09-26 · 648 Replace Words** (🔴 re-rep; retry, half-spoiled: trie folder) — ✅ **hit.** Trie named unaided
  AND the operation called correctly this time: "return on the first match we find" — the first word-end on the
  single walk IS the shortest root, the exact picking feature that was coach-supplied Sep 14 and Sep 24. Coded in
  one pass, no hints. → 🟢 prov.
- **2026-09-25 · 46 Permutations** (🆕 new, measured; folder half-spoils) — ⚠️ **partial.** Backtracking named unaided, but the
  picking feature vs 78/39 (order matters ⟹ every unused element is a candidate for the next slot ⟹ a `for` over candidates,
  not a take/skip on an index) was coach-supplied after the take/skip version failed; pseudocode given on request. → 🟡.
- **2026-09-25 · 55 Jump Game** (🟡 re-rep; retry, half-spoiled: greedy folder) — ⚠️ **partial.** Shape called unaided
  (reachability via `i + nums[i]`, no path needed), but the technique was never named and the picking feature (one
  running value — furthest-reachable forward, or the moving goal backward — replaces enumerating jumps) came from two
  coach questions; the backward loop's shape was coach-supplied after the forward version missed the `i > furthest` check. → 🟡.


- **2026-09-23 · 1489 Critical/Pseudo-Critical MST Edges** (🟡 retry, half-spoiled: schedule tag named Kruskal) —
  ⚠️ **partial.** Learner asked "why Kruskal not Prim"; the picking feature (per-edge answers by original index →
  an edge-list MST where one edge can be excluded/forced) was coach-supplied, and it named the exclude/include
  mechanism. → 🟡.
- **2026-09-23 · 846 Hand of Straights** (🟡 retry, half-spoiled) — ⚠️ **partial.** Count map + "lowest first"
  called unaided; the picking feature (the smallest card left can only START a group, so the greedy choice is
  forced) needed a coach position table. → 🟡.
- **2026-09-24 · 648 Replace Words** (🟡 re-rep; retry, blank page) — ⚠️ **partial.** Trie named unaided ("place all the
  dictionaries into a trie"), but the *operation* was mis-called: "shortest → trie with BFS". The picking feature (a fixed
  word dictates one child per step, so there is a single path and no frontier; the first word-end on it IS the shortest
  root) came out of two coach questions, and the prefix-search template was given on request. Same half-miss as Sep 14
  (then: a "needed Word Break" over-association) — the structure is recognised, the lookup on it is not. → 🔴 (learner's call).
- **2026-09-23 · 39 Combination Sum** (🆕 new, measured) — ⚠️ **partial.** Backtracking shape named via the
  5-slot template, but the picking feature vs 78 Subsets (unique by *count*, reuse allowed → a start bound
  that stays put on take) left as `state = n/a?`; came from a coach hint. → 🔴.
- **2026-09-22 · 901 Online Stock Span** (🟢 s1 review; retry, half-spoiled) — ⚠️ **partial.** Monotonic stack
  named, but direction (decreasing — keep the nearest *higher* left price) and the picking mechanic (carry the
  absorbed span with each entry) both needed coach input. → 🟡.
