"""Pull interview problems to practice — gated by what you've already learned.

Fetches a company's problem list from a public company-wise GitHub repo
(default: liquidslr/leetcode-company-wise-problems, ~470 companies, CSV columns:
Difficulty, Title, Frequency, Acceptance Rate, Link, Topics) and suggests which
to *pull* next: problems whose topics match patterns you've already retired/cleaned,
excluding ones already in your tracker, ranked by interview frequency.

This is the "pull, not push" mechanic made concrete — your knowledge drives the
selection. Nothing is written; it prints suggestions you then log like any problem.

Examples:
    python scripts/pull_interview.py --company Google
    python scripts/pull_interview.py --company Stripe --window 6mo --limit 15
    python scripts/pull_interview.py --company Amazon --difficulty MEDIUM
    python scripts/pull_interview.py --company Meta --no-gate        # ignore the learned-pattern filter
    python scripts/pull_interview.py --local sample.csv              # offline / test with a local CSV

Stdlib only. Reads your learned patterns from the tracker + milestone curriculum.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs" / "foundations" / "dsa" / "mastery" / "dsa_progress.md"
MILESTONE = ROOT / "curriculum" / "dsa" / "milestone.yml"

DEFAULT_REPO = "liquidslr/leetcode-company-wise-problems"
DEFAULT_BRANCH = "main"
WINDOWS = {"30d": "1. Thirty Days", "3mo": "2. Three Months",
           "6mo": "3. Six Months", "all": "5. All"}

# Our milestone categories → the LeetCode topic tags that signal "you know this".
CATEGORY_TO_TOPICS = {
    "Arrays & Hashing": {"Array", "Hash Table"},
    "Two Pointers": {"Two Pointers"},
    "Sliding Window": {"Sliding Window"},
    "Stack": {"Stack", "Monotonic Stack"},
    "Binary Search": {"Binary Search"},
    "Linked List": {"Linked List"},
    "Trees": {"Tree", "Binary Tree", "Binary Search Tree",
              "Depth-First Search", "Breadth-First Search"},
    "Tries": {"Trie"},
    "Heap / Priority Queue": {"Heap (Priority Queue)"},
    "Backtracking": {"Backtracking"},
    "Graphs": {"Graph", "Union Find", "Matrix"},
    "Advanced Graphs": {"Shortest Path", "Topological Sort",
                        "Minimum Spanning Tree", "Strongly Connected Component"},
    "1-D Dynamic Programming": {"Dynamic Programming"},
    "2-D Dynamic Programming": {"Dynamic Programming"},
    "Greedy": {"Greedy"},
    "Intervals": {"Line Sweep"},
    "Math & Geometry": {"Math", "Geometry"},
    "Bit Manipulation": {"Bit Manipulation"},
}

# ── TODO (expansion phases): EXTEND THIS MAP when the learner starts RETIRING
# expansion techniques — not before. Post-NC150 the pool is already wide (all
# NC150 topics); this only matters once advanced techniques are being learned so
# freshly-retired ones widen the pull pool. Two-part change:
#   1. Add each expansion solution-folder slug -> technique name in FOLDER_TO_CATEGORY
#      below (e.g. "segment_tree", "fenwick", "kmp", "suffix_array", ...).
#   2. Add the technique -> LeetCode topic tags here so pulls gate on it:
#        "Segment Tree":        {"Segment Tree"},
#        "Fenwick / BIT":       {"Binary Indexed Tree"},
#        "KMP / Z / Aho-Corasick": {"String Matching"},
#        "Suffix structures":   {"Suffix Array"},
#        "Tarjan's (SCC)":      {"Strongly Connected Component"},
#        "Meet in the middle":  {"Meet in the Middle"},
#        "Reservoir sampling":  {"Reservoir Sampling"},
#        "Number theory":       {"Number Theory"},
#        "Sweep line":          {"Line Sweep"},
# See feedback_expansion_pull_scheduling memory (weekly generation drives pulls).


# Solution-folder slug -> milestone category (so learned-pattern detection works
# in a repo that stores solutions under category folders, e.g. cse-progress).
FOLDER_TO_CATEGORY = {
    "arrays_and_hash": "Arrays & Hashing", "two_pointers": "Two Pointers",
    "sliding_window": "Sliding Window", "stack": "Stack",
    "binary_search": "Binary Search", "linked_list": "Linked List",
    "trees": "Trees", "trie": "Tries", "heap": "Heap / Priority Queue",
    "backtracking": "Backtracking", "graphs": "Graphs",
    "advanced_graphs": "Advanced Graphs", "greedy": "Greedy",
    "intervals": "Intervals", "1d_dynamic_programming": "1-D Dynamic Programming",
    "2d_dynamic_programming": "2-D Dynamic Programming",
    "math_geometry": "Math & Geometry", "bit_manipulation": "Bit Manipulation",
}


def source_root() -> Path:
    cfg = ROOT / "cse.config.yml"
    if cfg.exists():
        m = re.search(r"roots:\s*\[([^\]]*)\]", cfg.read_text(encoding="utf-8"))
        if m:
            first = m.group(1).split(",")[0].strip().strip("'\"")
            if first:
                return ROOT / first
    return ROOT / "dsa" / "leetcode"


def parse_milestone_num_to_category() -> dict[int, str]:
    if not MILESTONE.exists():
        return {}
    num2cat, cat = {}, None
    for line in MILESTONE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s*name:\s*(.+?)\s*$", line)
        if m:
            cat = m.group(1)
            continue
        pm = re.search(r"number:\s*(\d+)", line)
        if pm and cat:
            num2cat[int(pm.group(1))] = cat
    return num2cat


def scan_solution_categories() -> dict[int, str]:
    """Map problem number -> category from solution-file folders (ground truth of
    what the learner actually solved). Works in cse-progress; empty in a fresh repo."""
    root = source_root()
    num2cat: dict[int, str] = {}
    if not root.exists():
        return num2cat
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        m = re.match(r"(\d+)_", path.name)
        if not m:
            continue
        folder = path.parent.name.lower()
        cat = FOLDER_TO_CATEGORY.get(folder)
        if cat:
            num2cat[int(m.group(1))] = cat
    return num2cat


def slug_from_link(link: str) -> str:
    return link.rstrip("/").split("/")[-1].lower()


def read_tracker() -> tuple[set[str], set[int]]:
    """Return (slugs of all logged problems, numbers logged Clean or Retired)."""
    solved_slugs: set[str] = set()
    learned_numbers: set[int] = set()
    if not TRACKER.exists():
        return solved_slugs, learned_numbers
    row_re = re.compile(r"\|[^|]+\|\s*\[(\d+)\.[^\]]+\]\(([^)]+)\)\s*\|\s*(🟢|🟡|🔴|🏆)")
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        m = row_re.match(line)
        if not m:
            continue
        number, url, comfort = int(m.group(1)), m.group(2), m.group(3)
        solved_slugs.add(slug_from_link(url))
        if comfort in ("🟢", "🏆"):
            learned_numbers.add(number)
    return solved_slugs, learned_numbers


def learned_topics() -> tuple[set[str], set[str]]:
    """Return (learned LeetCode topics, learned category names). Category source:
    solution folders (ground truth) merged over the milestone curriculum."""
    num2cat = {**parse_milestone_num_to_category(), **scan_solution_categories()}
    _, learned_numbers = read_tracker()
    cats = {num2cat[n] for n in learned_numbers if n in num2cat}
    topics: set[str] = set()
    for c in cats:
        topics |= CATEGORY_TO_TOPICS.get(c, set())
    return topics, cats


def fetch_csv(repo: str, branch: str, company: str, window: str) -> str:
    fname = WINDOWS[window]
    url = (f"https://raw.githubusercontent.com/{repo}/{branch}/"
           f"{urllib.parse.quote(company)}/{urllib.parse.quote(fname)}.csv")
    req = urllib.request.Request(url, headers={"User-Agent": "cse-coach"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--company",
                    help="company folder(s) in the source repo, comma-separated (e.g. Google,Amazon). "
                         "Multiple companies are UNIONED and de-duplicated by problem, keeping the "
                         "highest frequency seen and noting which companies asked it.")
    ap.add_argument("--technique", action="append", metavar="TOPIC",
                    help="filter to a LeetCode topic tag, e.g. --technique 'Monotonic Stack'. "
                         "Repeatable; a row matches if it carries ANY of them. Case-insensitive. "
                         "NOTE this is FINER than the gate: the gate works on the 11 broad learned "
                         "CATEGORIES (Arrays & Hashing, Graphs, ...), while techniques.yml names 52 "
                         "techniques. Without this flag you can ask for 'a Graphs problem' but not "
                         "for 'one that fills Multi-source BFS'.")
    ap.add_argument("--window", choices=WINDOWS, default="all")
    ap.add_argument("--difficulty", choices=["EASY", "MEDIUM", "HARD"])
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--no-gate", action="store_true",
                    help="skip the learned-pattern filter (show everything)")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--branch", default=DEFAULT_BRANCH)
    ap.add_argument("--local", help="read a local CSV instead of fetching (offline/testing)")
    args = ap.parse_args()

    known, cats = learned_topics()
    solved, _ = read_tracker()

    want_topics = {x.strip().lower() for x in (args.technique or []) if x.strip()}

    # (text, label, company) tuples — one per source fetched.
    sources: list[tuple[str, str]] = []
    if args.local:
        sources.append((Path(args.local).read_text(encoding="utf-8"), args.local))
        label = args.local
    else:
        if not args.company:
            ap.error("--company is required (or use --local). ~470 companies available.")
        companies = [c.strip() for c in args.company.split(",") if c.strip()]
        for c in companies:
            try:
                sources.append((fetch_csv(args.repo, args.branch, c, args.window), c))
            except Exception as e:  # pragma: no cover
                print(f"  ! skipping {c}: {e}", file=sys.stderr)
        if not sources:
            ap.error("no company list could be fetched")
        label = f"{', '.join(c for _, c in sources)} - {WINDOWS[args.window]}"

    # Union across companies, de-duplicated by problem slug. A problem asked by
    # several targets is a stronger signal, so keep the max frequency and record
    # every company that asked it.
    merged: dict[str, tuple[float, dict, set, set]] = {}
    for text, company in sources:
        for row in csv.DictReader(io.StringIO(text)):
            topics = {t.strip() for t in (row.get("Topics") or "").split(",") if t.strip()}
            slug = slug_from_link(row.get("Link", ""))
            if slug in solved:
                continue
            if args.difficulty and (row.get("Difficulty", "").upper() != args.difficulty):
                continue
            if want_topics and not {tp.lower() for tp in topics} & want_topics:
                continue
            matched = topics & known
            if not args.no_gate and not matched:
                continue
            try:
                freq = float(row.get("Frequency") or 0)
            except ValueError:
                freq = 0.0
            if slug in merged:
                pf, prow, pm, pc = merged[slug]
                merged[slug] = (max(pf, freq), prow if pf >= freq else row, pm | matched, pc | {company})
            else:
                merged[slug] = (freq, row, matched, {company})

    candidates = [(f, r, m, c) for f, (_, r, m, c) in
                  ((v[0], v) for v in merged.values())]
    candidates.sort(key=lambda x: x[0], reverse=True)

    print(f"\nPull pool - {label}")
    if args.no_gate:
        print("  (ungated - all unsolved problems)")
    else:
        print(f"  gated by {len(cats)} learned pattern(s): {', '.join(sorted(cats)) or '(none yet)'}")
    if want_topics:
        print(f"  technique filter: {', '.join(sorted(args.technique))}")
    print()
    if not candidates:
        print("  Nothing to pull. Retire more patterns first, or try --no-gate / another company.\n")
        return
    for freq, row, matched, cos in candidates[: args.limit]:
        why = ", ".join(sorted(matched)) if matched else "-"
        if len(cos) > 1:
            why += f"   [{len(cos)}x: {','.join(sorted(cos))}]"
        print(f"  [{row.get('Difficulty','?'):<6}] {row.get('Title','?'):<44} "
              f"freq {freq:>5.1f}  <- {why}")
    print(f"\n  {min(len(candidates), args.limit)} shown of {len(candidates)} eligible. "
          "Pull one, solve it, log it Clean/Shaky/Blank.\n")


if __name__ == "__main__":
    main()
