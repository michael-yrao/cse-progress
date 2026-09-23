# Plan: rebuild `/learn` as a technique cheat sheet, generated from this repo

**Status:** APPROVED Sep 22, 2026 — Phase B in progress (site repo). Phase C not started.
**Route chosen:** B (richer schema + technique-keyed UI) then C (single source in cse-progress).
Route D (personal-miss layer from `recognition_gotchas.md` / `stuck_log.md`) is explicitly out of scope
here; the contract below leaves room for it.

## Why

progressiveoverflow.com/learn is a hand-written cheat sheet in the site repo
(`michael-yrao.github.io/src/app/core/data/cheat-sheets.data.ts`, 10 entries). It falls short in three ways:

| Problem | Evidence |
|---|---|
| **Wrong unit** — keyed by data-structure bucket, not technique | "trees" holds BFS, postorder DFS and inorder BST on one page; "sliding-window" has one template where `techniques/sliding_window.md` has three variants |
| **No discriminator** — signals but no *picking feature* | the recognition gate trains "the one feature that picks it over the nearest neighbour"; `recognition_gotchas.md` records it; the site never shows it |
| **Second copy** — hand-maintained duplicate of `docs/foundations/dsa/patterns/` | 18 technique docs + 5 hubs + `intuition_cheatsheet.md` + `techniques.yml` already exist here; the site copy is the one nobody executes from |

## Target end state

- `/learn` opens on a **signal → technique table** (the `intuition_cheatsheet.md` table), then technique cards grouped by family.
- `/learn/<technique>` is one technique: when to use · signals · **picking feature + "not this when"** · one template
  **per variant**, each with time/space and a why-clause · pitfalls · key problems · link to the full doc.
- The content is **generated** by `scripts/build_cheatsheets.py` from the technique docs into
  `dashboard/cheat-sheets.json`, validated on pre-commit, and fetched by the site the same way it fetches
  `dashboard/progress.json`. The site keeps a bundled copy as a fallback.

## The contract (`dashboard/cheat-sheets.json`)

```jsonc
{
  "schemaVersion": 1,
  "generatedAt": "2026-09-22T..",
  "signals": [                                  // the landing table, from intuition_cheatsheet.md
    { "see": "Sorted array + pair/triple summing to target", "reach": "two-pointer", "note": "converge from ends" }
  ],
  "techniques": [
    {
      "id": "sliding-window",                   // slug of the .md filename
      "name": "Sliding Window",
      "family": "arrays_and_hash",              // from techniques.yml
      "tier": "core",                           // from techniques.yml (default core)
      "whenToUse": "…one sentence…",
      "signals": ["\"contiguous subarray/substring\" + a constraint", "…"],
      "picking": {
        "feature": "contiguous + window monotonicity",
        "notWhen": [ { "technique": "prefix-sum", "because": "the constraint is a sum with negatives — the window is not monotonic" } ]
      },
      "variants": [
        {
          "title": "Fixed window",
          "when": "static width k",
          "code": "…python…",
          "complexity": { "time": "O(n)", "space": "O(1)", "why": "each index enters and leaves the window once; a single running sum" }
        }
      ],
      "pitfalls": ["…"],
      "keyProblems": [ { "lcNumber": 3, "title": "…" } ],   // site resolves lcNumber → visualizer route if it has one, else LeetCode
      "docUrl": "https://github.com/michael-yrao/cse-progress/blob/main/docs/foundations/dsa/patterns/techniques/sliding_window.md"
    }
  ]
}
```

A JSON Schema (`dashboard/cheat-sheets.schema.json`) pins this, mirroring how `progress.schema.json` pins the
progress contract. Additive changes bump nothing; a field removal bumps `schemaVersion`.

**Deltas accepted from the Phase B build (Sep 22, 2026):**

- `signals[].page?: boolean` and `notWhen[].technique` may be a plain **label** with `page: false` (heap,
  Boyer-Moore, cyclic sort, two heaps, quickselect, Dijkstra, Bellman-Ford, BFS, "DFS/BFS") — for a
  neighbour that has no technique page. The generator emits an id when a technique doc with that slug
  exists, else the label + `page: false`; the validator does **not** fail on a label.
- `keyProblems[].title` must be the **real LeetCode title** — the site derives the LeetCode URL from it
  when it has no visualizer for that number. "Remove Duplicates" or "Diameter" 404s.
- The B2 seed carries tech-lead-authored content that the docs do not yet have: every `picking.feature` and
  `notWhen`, every per-variant complexity line, pitfalls for backtracking / binary-search / recursion /
  sliding-window / two-pointer, six `whenToUse` sentences, and a full Prim's template. **C1 copies these
  INTO the docs** (the seed is the source for that pass); the C2 generator must then reproduce the seed.
- `techniques.yml` has no entry for `backtracking` or `recursion`; C1 adds both (family keys as in the
  seed). `dummy-node → linked_list`, `memoization → dynamic_programming / dp`, `tree-dfs ↔ "Tree DFS
  (recursive)"` were guesses that C1 confirms or corrects in the same pass.

## The markdown contract (what each technique doc must carry)

The docs stay prose for the learner; the generator reads **only** these headings and ignores everything else
(the "Understanding …" / "Key Insights" deep-dives stay, untouched, and are reachable via `docUrl`).

| Heading (exact) | Parsed as | Rule |
|---|---|---|
| `## When to reach for it` | `whenToUse` = first paragraph; `signals` = the bullet list that follows | required |
| `## Picking feature` | first line → `picking.feature`; bullets of the form `- **not <technique>** — <because>` → `notWhen[]` | required (new in most docs) |
| `## Template: <title>` (one heading per variant) | `when` = optional first line `*When:* …`; `code` = the first ```python fence; complexity = the line `Complexity: O(..) time · O(..) space — <why>` directly after the fence | ≥ 1 required; complexity line required per template |
| `## Common pitfalls` | bullet list → `pitfalls[]` | required |
| `## Practice` | bullets containing `LC <n>` or `[<n>` → `keyProblems[]` | required, ≥ 1 |

`scripts/check_cheatsheets.py --check` fails on any missing required heading, a template without a
complexity line, or a `not <technique>` slug that doesn't resolve. It runs report-only from the pre-commit
hook first (like `check_single_source.py`), and is promoted to blocking once all 18 docs pass.

**Why headings, not a sidecar YAML:** a sidecar would be a *third* copy of templates and pitfalls. The
headings keep one file per technique that is both the learner's doc and the site's source; the validator
is what stops drift. The single-source rule in CLAUDE.md is the precedent.

**Doc styles to reconcile.** Two families exist today: 9 docs already use `When to reach for it / Template /
Practice / Common pitfalls` (dummy_node, fast_slow_pointer, in_place_reversal, monotonic_stack, prefix_sum,
topological_sort, tree_bfs, tree_dfs, union_find) and need mostly `## Picking feature` + complexity lines;
7 use `Quick Reference / 1. Pattern / Key Insights` (backtracking, binary_search, memoization, recursion,
sliding_window, two_pointer, intervals) and need their numbered sections re-headed as `## Template: …`;
2 are algorithm write-ups (floyd_warshall, prims_mst) whose `Recognition triggers` / `Implementation
gotchas` / `Problems` sections map onto the contract by rename. Content is preserved verbatim in every
case — this step **moves headings, it does not rewrite prose.**

## Phases, slices, engineers

Per the execution workflow: tech lead plans/reviews only; every edit goes to a Sonnet `engineer`; two or
more engineers in a phase get an Opus `team-lead`. Phases are sequential; slices inside a phase are
parallel.

### Phase B — schema + technique-keyed UI (site repo only)

Deliverable: `/learn` renders the new shape from a **bundled** `src/assets/cheat-sheets.json` that already
matches the contract above. No cse-progress change yet.

| Slice | Engineer | Work |
|---|---|---|
| B1 · model + UI | E1 | `core/models/cheat-sheet.model.ts` (the contract types); `CheatSheetService` loading `assets/cheat-sheets.json`; `learn-list` gains the signals table + family-grouped cards; `cheat-sheet` page renders picking feature, `notWhen`, per-variant template + complexity, pitfalls, key problems (lcNumber → `ALL_ALGORITHMS` route when present, else the LeetCode URL); route becomes `/learn/:technique`; old `/learn/:category` slugs redirect via a 10-row map so existing links don't 404; unit tests for the service, the redirect map, and the lcNumber resolver; `ng lint` + `ng build` clean |
| B2 · seed content | E2 | Author `src/assets/cheat-sheets.json` for all 18 techniques by **extracting** from the technique docs + `intuition_cheatsheet.md` + `techniques.yml` — no invented content; where a doc has no picking feature yet, pull it from `recognition_gotchas.md`'s trigger table or leave `picking.feature` as `TODO` and list it in the report. Validate against `cheat-sheets.schema.json` (E2 writes the schema; E1 types from it) |

Lead: one `team-lead` owns B1 + B2. Review gate: I read every `picking.feature` and `notWhen` line
myself before it lands — that text is the coaching payload and is not delegated judgement.

### Phase C — single source (cse-progress + site switch)

Deliverable: `dashboard/cheat-sheets.json` generated here, validated on commit; the site fetches it and
falls back to the bundled copy.

| Slice | Engineer | Work |
|---|---|---|
| C1 · docs conformance | E3 | Re-head all 18 technique docs to the markdown contract, preserving prose verbatim; add `## Picking feature` (from B2's JSON, which was itself extracted) and the `Complexity:` line after every template; update `patterns/README.md` to state the contract once |
| C2 · generator + validator | E4 | `scripts/build_cheatsheets.py` (parses the contract, joins `techniques.yml` for family/tier, emits `dashboard/cheat-sheets.json` + `dashboard/cheat-sheets.schema.json`); `scripts/check_cheatsheets.py --check`; pre-commit wiring (report-only); tests in `scripts/test_build_cheatsheets.py` with a fixture doc per style family; `check_single_source.py` must stay green (the generator copies no tuned number) |
| C3 · site switch | E5 | `CheatSheetService` fetches `dashboard/cheat-sheets.json` through the same Contents-API path as `ProgressService` (reuse its fetch helper, honour `?repo=`), falls back to the bundled asset on 404/schema mismatch; a "generated <date> from cse-progress" footer; tests for the fallback |

Leads: C1 + C2 under one `team-lead` (they share the contract and must agree on it — C2's parser is the
arbiter, C1 conforms to it); C3 supervised by the tech lead directly. C3 starts once C2's JSON is emitted
on `main`, since the site fetches from `main`.

Bookkeeping in the same landing edit for Phase C: a `decisions.yml` entry `learn-cheatsheet-contract-sep22`
(the technique docs gained a machine-read contract; the site stopped carrying its own copy);
`project_gamification.md` gains one line pointing at the second contract file; `AGENTS.md`/`README.md`
mention `build_cheatsheets.py` next to `gamify.py`.

## Sequencing and the rollback line

1. B lands and deploys — the site is already better with a bundled file. Rollback = revert one site commit.
2. C1 + C2 land here; the emitted JSON is diffed against B2's seed — **they must match modulo `generatedAt`
   and `docUrl`.** A diff is a parser bug or a doc miss, fixed before C3 starts.
3. C3 lands; the bundled asset is kept as the fallback and refreshed by hand only when the schema bumps.

## Verification (what "done" means)

- Site: `ng lint`, `ng build`, `ng test` clean; `/learn` and every `/learn/<technique>` render; every old
  `/learn/<category>` URL redirects; every `keyProblems` entry resolves to a route or a LeetCode URL.
- Repo: `python scripts/check_cheatsheets.py --check` passes on all 18 docs; `python scripts/build_cheatsheets.py`
  is idempotent (second run is a no-op diff); `check_single_source.py --check` and `reconcile.py` unchanged.
- Cross-repo: `dashboard/cheat-sheets.json` byte-equals the B2 seed modulo the two volatile fields.
- `advisor` runs before each commit, per the execution workflow.

## Risks and calls made

- **Spoiler surface.** A public signal → technique table spoils a recognition probe if opened mid-rep.
  Call: the page is positioned as post-rep review (a one-line notice on `/learn`); the coach never links it
  in a probe. No mechanical guard — it's the learner's page.
- **Content authoring drifts into teaching.** B2/C1 are extraction and re-heading, not writing. Anything a
  doc doesn't already say is reported as `TODO`, not invented; I fill those inline, since that is coaching
  content.
- **Two repos, one contract.** The schema file lives in cse-progress (C2) and is copied into the site's
  types by hand (B1 types it from the draft in this plan). A later step could generate the TS types from
  the schema; not now (YAGNI).
- **Category → technique fan-out.** 10 category slugs become 18 technique slugs. The site's
  `ALL_ALGORITHMS` still carries `category`; the cheat sheet no longer depends on it except for the
  visualizer route lookup, so nothing else in the site changes.
- **Docs not in scope:** the 5 data-structure hubs and `big_o.md` are not part of the contract. The heap /
  Boyer-Moore / cyclic-sort / two-heaps / quickselect one-trick entries in `intuition_cheatsheet.md` ride
  along in `signals[]` only (no technique page) — same as today's doc.

## Estimated shape

| Phase | Engineers | Leads | Lands where |
|---|---|---|---|
| B | 2 | 1 | site repo, one PR |
| C | 3 | 1 (+ tech lead for C3) | cse-progress one PR (C1+C2), site one PR (C3) |
