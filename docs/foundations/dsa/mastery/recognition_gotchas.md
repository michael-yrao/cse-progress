- **2026-10-02 · 127 Word Ladder** (🟢 s1 review; retry, half-spoiled: graphs folder, tracker title names BFS) — ✅
  **hit.** Top comment, unaided: wildcard-pattern map (`.it`, `h.t`, `hi.`), "this is actually just a BFS navigating
  to nearest neighbors"; visited marked on enqueue, levels counted. 3,000/3,000 against a reference BFS. → 🟢 s2.
- **2026-10-02 · 9004 Minimum Spanning Tree** (🆕 new, measured; the title names the object, the folder says graphs) —
  ✅ **hit.** Top comment, unaided: "since we already have edges here, this is Kruskal's MST, so we sort and do UF",
  with the no-tree condition "not all nodes are connected". Union-Find written correctly from a blank page. The sort
  key (`edges.sort()` sorted by u, not weight) was coach-located; output format pointed out. 33/33 stored cases. → 🟡.
- **2026-10-02 · 901 Online Stock Span** (🟡 re-rep; retry, half-spoiled: stack folder) — ✅ **hit.** Top comment,
  unaided: "non increasing stack (decreasing with equality check), each stack node keeps its span so (value, span)
  tuple". Both pieces that needed coach input on Sep 22 (direction, carrying the span) came unaided. 2,000/2,000
  random runs against a brute-force span. → 🟢 s1.
- **2026-10-02 · 1552 Magnetic Force Between Two Balls** (🟡 re-rep; retry, half-spoiled: binary_search folder) — ✅
  **hit.** Top comment, unaided: "this is a solution based binary search", sort first, bounds 1 and
  `position[-1] - position[0]`, maximizing. Greedy left-to-right check and the upper-mid form written without help.
  3,000/3,000 against a brute force. → 🟢 s1.
- **2026-10-02 · 131 Palindrome Partitioning** (🔴 re-rep; retry, half-spoiled: backtracking folder) — ⚠️ **partial.**
  Backtracking with path, state (start, end) and validity (palindrome) named unaided, choosing a new take/skip form
  over Sep 30's loop. The decision rule ("cut only if palindrome, else extend" → extend always, cut on a palindrome)
  and the base case (`start == len(s)`) were coach-supplied. Two code bugs coach-located. 2,000/2,000 after the fix. → 🔴.
- **2026-10-02 · 40 Combination Sum II** (🔴 re-rep; retry, half-spoiled: backtracking folder) — ✅ **hit.** Top
  comment, unaided: sort first; decision "pick or not pick value at current index"; validity "if not adding, ignore
  other values that are equal". The duplicate skip sits on the not-pick branch, the piece missed on Sep 28 and Sep 30.
  Blank page, no hints (the coach was running the meta-review). 3,000/3,000 against a brute force. → 🟢 s0 (provisional).
- **2026-10-01 · 202 Happy Number (Seen-Set)** (🟢 s1 review; retry, half-spoiled: the tracker row names the method,
  the stub still reads "recognition probe") — ✅ **hit.** Top comment: "we can use a set to make sure we don't revisit
  the same number". Blank page, no hints on the code; the learner asked for the Big-O variables and was given n and d
  only. 20,003/20,003 against a reference. → 🟢 s2.
- **2026-10-01 · 128 Longest Consecutive Sequence** (🟢 s2 review; retry, half-spoiled: arrays_and_hash folder, no
  pattern line in the stub) — ✅ **hit.** Top comment: "we want to find the start number here and just check if the
  next number exists so that means we should convert nums to a set". Blank page, no hints; loops over the set, so a
  duplicate start is counted once; 3,000/3,000 against a sort-based reference. → 🎓.
- **2026-10-01 · 271 Encode and Decode Strings** (🟢 s1 review; retry, half-spoiled: arrays_and_hash folder, no
  pattern line in the stub) — ✅ **hit.** Comment above the methods: "prefix length framing … length + # + string +
  length + # + string". Blank page, no hints; the scan compares the character (`s[j] != '#'`), so the Jul 3 / Aug 2
  index-vs-value bug held; 3,000/3,000 round trips over all 256 characters. → 🟢 s2.
- **2026-10-01 · 150 Evaluate Reverse Polish Notation** (🟢 s1 review; retry, fully spoiled: the stub's `Pattern: stack`
  line and the folder) — ✅ **hit, habit only.** Top comment: "stack problem … we see an operator, we pop the two latest
  and push result into the stack". Blank page, no hints; both old bugs held (first pop is the right-hand operand,
  `int()` on the float truncates toward zero); 3,000/3,000 against a reference evaluator. → 🟢 s2.
- **2026-10-01 · 22 Generate Parentheses** (🟢 s0 lock-down; retry, fully spoiled: the stub's `Pattern: backtracking`
  line and the folder) — ✅ **hit, habit only.** Top comment: the five slots, no technique word, with both prune rules
  stated ("if left parentheses < n, we can add left, if right counter is less than left, we can add right") and the base
  case at length 2n. Blank page, no hints. → 🟢 s1.
- **2026-10-01 · 9001 Single Source Shortest Path, Negative Weights** (🆕 new, measured; the title names the shape, the
  `graphs` folder does not name the method) — ✅ **hit.** Before any code: "first thing that comes to mind is bellman ford
  since it helps me handle negative edges", and the top comment says the same. Shape, technique and picking feature all
  stated unprompted. The rating follows execution: the round count and the cycle handling were coach-taught. → 🔴.
- **2026-10-01 · 90 Subsets II** (🆕 new, measured; folder half-spoils) — ⚠️ **partial.** Top comment, unaided: "we are
  getting all subsets but this time we have duplicates in here", then the five slots in the take/skip form (state = the
  index being decided). Backtracking is never named as a word; the five-slot plan is the call. The picking feature vs 78
  (a repeated value is decided once: sort, and the exclude branch jumps every copy) was not named. It was asked for
  before any attempt and coach-supplied, the same rule taught on 40 on Sep 28. → 🔴.
- **2026-09-30 · 131 Palindrome Partitioning** (🆕 new, measured; folder half-spoils) — ⚠️ **partial.** "all possible
  palindrome is obviously backtracking" in the top comment, unaided. The picking feature (the choice is where the
  next piece ends, so each child is one whole substring and the path is a list of pieces) was not named: choice and
  validity were both "n/a ?", and the five slots were coach-supplied on request. → 🔴.
- **2026-09-30 · 78 Subsets** (🟡 re-rep; retry, half-spoiled: backtracking folder) — ✅ **hit.** Top comment: "the
  basic backtracking problem where we choose or not choose a number", five slots with validity none and the index as
  state. Blank page, no hints; both Sep 20 coach fixes held (`>=` base case, `return` after recording). Still the
  `path + [x]` form, so the append/pop undo watch item stays open. Same session as the 40 loop-form teach. → 🟢 s1.
- **2026-09-30 · 84 Largest Rectangle in Histogram** (🟡 re-rep; retry, half-spoiled: stack folder, the stub names
  the pattern) — ✅ **hit.** Top comment: "when we see a lower boundary, we calc the area of what the boundaries
  contain … increasing stack", both boundaries excluded, width = max boundary − min boundary − 1, a `-math.inf`
  sentinel to flush a rising run. Blank page, no hints; 3,007/3,007 against brute force. → 🟢 s1.
- **2026-09-30 · 40 Combination Sum II** (🔴 re-rep; retry, half-spoiled: backtracking folder) — ⚠️ **partial.**
  Backtracking + "sort" + "no duplicate combinations, handle in validity" in the top comment, unaided. The picking
  feature (a repeated value is tried once per node's loop, so equal siblings are skipped) was not named; the take/skip
  `setState` stand-in came back, and the sibling-skip rule was coach-taught. → 🔴.
- **2026-09-29 · 53 Maximum Subarray (Kadane)** (🟢 s2 review; retry, fully spoiled: the stub's method name says
  Kadane) — ✅ **hit, habit only.** Top comment "kadane's"; max taken before the reset so an all-negative array
  returns its largest element. Blank page, no hints. → 🎓.
- **2026-09-29 · 79 Word Search** (🆕 new, measured; folder half-spoils) — ⚠️ **partial.** Asked "is this
  backtracking?", then "this can be done with DFS". The picking feature — a cell is visited only for the current
  path, so it is unmarked on return and another path can reuse it — came after the "what does visited mean here?"
  prompt; the learner's Hierholzer analogy was corrected (Hierholzer never undoes). → 🟡.
- **2026-09-29 · 846 Hand of Straights** (🟡 re-rep; retry, half-spoiled: greedy folder) — ✅ **hit.** Top comment:
  "sort and then check if current number is starting of a sequence … freq counter … decrement when we use them" —
  count map + smallest-first, unaided. Sep 23 watch item half met: the *why* (the smallest card left can only start a
  group) was not stated, though the code relies on it correctly; `range(num, num + groupSize)` bound right. → 🟢 s1.
- **2026-09-29 · 763 Partition Labels** (🟡 re-rep; retry, half-spoiled: greedy folder) — ✅ **hit.** Top comment:
  freq map counted down + "a set for the current items seen … if set is empty, we add length into the result" — the
  cut is a property of the whole window, not the current char (the Sep 19 coach-supplied fix, now unaided). Blank
  page, no hints. → 🟢 s1.
- **2026-09-28 · 853 Car Fleet** (🟢 s1 review; retry, half-spoiled: stack folder) — ⚠️ **partial.** Top comment named
  sort-by-position (the car ahead can't be passed) + time-to-target, unaided. The picking feature — a stack of fleet
  times, a car starting a new fleet only when strictly slower than `fleet[-1]` — needed an outside hint. → 🟡.
- **2026-09-28 · 155 Min Stack** (🟢 review; retry, half-spoiled: stack folder) — ✅ **hit.** Top comment: "key here
  is really to store a tuple so the stack stores the min with it" — pair each value with the min-so-far. Blank page,
  no hints. → 🟢 s2.
- **2026-09-28 · 572 Subtree Of Another Tree** (🟢 review; retry, half-spoiled: trees folder) — ✅ **hit.** Top
  comment: "find the first node that matches the root of subroot, then see if same tree" — tree DFS with a
  same-tree check at each candidate. Blank page, no hints; time O(m·n) and space O(h) both correct. → 🟢 s2.
- **2026-09-28 · 40 Combination Sum II** (🆕 new, measured; folder half-spoils) — ⚠️ **partial.** Backtracking named
  unaided via the 5-slot template (take/skip, state = index). The picking feature vs 39 — **candidates repeat, so
  equal values must be decided once (sort + skip every copy)** — was not named; `setState` of indices was the stand-in,
  and the dedup was coach-taught after two "no idea"s. → 🔴.
- **2026-09-28 · 45 Jump Game II** (🟡 re-rep; retry, half-spoiled: greedy folder) — ✅ **hit.** Greedy called in the
  top comment: "`i + nums[i]` is our jump distance … go to the one with the highest jump potential". Both Sep 18
  coach-surfaced fixes held unaided (`>=` tie-break so the pick never stalls at `i`; window-covers-end → +1 exit).
  Blank page, no hints. → 🟢 s1.
- **2026-09-27 · 2812 Find the Safest Path in a Grid** (🆕 consolidation rep; half-spoiled: the schedule named the
  Dijkstra max-min seat and the learner asked for the swap by shape) — ✅ **hit on Dijkstra, ❌ miss on the precompute.**
  "this is clearly dijkstra's … maxHeap … start all nodes with -math.inf" cold. The nearest-thief distance was first
  a per-thief scan; multi-source BFS was named only after the "thieves reach out to the cells" hint. → 🟡.
- **2026-09-27 · 721 Accounts Merge** (🟡 re-rep; retry, half-spoiled: tracker names Union-Find) — ✅ **hit.**
  "this is union find" in the top comment, with a 5-step plan (UF over account indices → email→indices map →
  union co-owners → root→email-set → sorted rows). Steps 0–2 clean; steps 3–4 had three index-vs-value slips
  (`find(name)`, `enumerate` for `.items()`, row led by the index), fixed after a step-level localization hint.
  Coach proposed 🟡; **learner overrode to 🟢** and asked for a new problem instead of more 721 reps → 1202 queued.
- **2026-09-27 · 560 Subarray Sum Equals K** (🟡 re-rep; retry, half-spoiled: arrays_and_hash folder) — ✅ **hit.**
  Prefix sum + running-sum hashmap called in the top comment, with the `prefix[j] - prefix[i] == k` identity. All
  three past misses held: signed `runningSum - k` (no `abs`), `{0: 1}` seed, lookup-before-insert. Map still named
  `diffMap` (holds prefix sums). Blank page, no hints. → 🟢 s1.
- **2026-09-27 · 540 Single Element in a Sorted Array** (🟡 re-rep; retry, half-spoiled: binary_search folder) — ✅ **hit.**
  "min boundary" in the top comment. The recurring stuck-log card held: snap to the pair start with index math
  (`if m % 2: m -= 1`), then one `nums[m] != nums[m+1]` compare picks the side. Blank page, no hints; failed
  submissions fixed unaided. → 🟢 s1.
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
