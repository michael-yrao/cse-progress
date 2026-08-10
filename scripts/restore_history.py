"""Restore stashed prior attempts back into their solution files at session end.

new_problem.py extracts a retried problem's prior attempts into <root>/.history/<n>_<name>.txt
so the file opens on a blank page (no fold, no extension — the spoiler is physically gone).
This puts them back once the rep is done, reconstructing the single file with full dated
history exactly as it was before the extract.

    python scripts/restore_history.py                 # today's completed attempts
    python scripts/restore_history.py --date 20260713 # a specific session
    python scripts/restore_history.py --all           # restore every stash, unconditionally
    python scripts/restore_history.py --dry-run       # report, change nothing

**A file is only restored once its dated attempt has a real body.** A retry that was
scaffolded but never attempted still has `pass` under today's stub — pasting the prior
attempts back would expose the old solution before the rep ever happened, the exact failure
the extract exists to prevent. So an un-attempted problem keeps its stash out of the file
(and, being committed, that stash survives a cut-short session onto the next machine).

Also migrates LEGACY folded files: a solution file still carrying an old
`# region ⚠ PRIOR ATTEMPTS` (from the pre-stash era) has the markers stripped here, same
attempt-has-body guard applied. No stash is involved for those — the code never left.
"""
from __future__ import annotations

import argparse
import ast
import re
from datetime import datetime
from pathlib import Path

from new_problem import (
    REGION_HEAD,
    history_dir,
    source_root,
    strip_pointer,
    strip_spoiler_region,
)

# `def maxPathSum_20260713(...)` or `class Solution_20260713:` / `class StockSpanner_20260713:`
# — the dated attempt. The class arm matches ANY dated class name, not just `Solution`, so a
# design problem (StockSpanner, LRUCache, …) is correctly seen as attempted.
DATED_ATTEMPT = r"^\s*(?:def\s+\w+_{stamp}\s*\(|class\s+\w+_{stamp}\b)"
# The banner new_problem.py writes above a dated stub; not code, never counts as a body.
BANNER = re.compile(r"^\s*#\s*──.*Attempt")
# Inside a dated *class* attempt these are scaffold new_problem.py wrote, not the learner's work.
DEF_HEAD = re.compile(r"^\s*(?:async\s+)?def\s+\w+\s*\(")
DECORATOR = re.compile(r"^\s*@\w")


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def attempt_has_body(lines: list[str], stamp: str) -> bool:
    """True if the dated attempt contains anything beyond `pass` / comments / blanks.

    A dated *class* attempt (a design problem — `class KthLargest_20260810:`) carries its own
    method signatures, which new_problem.py wrote as part of the scaffold. Those are not the
    learner's work, so they must not count as a body: treating them as one made every
    multi-method scaffold look attempted, and the guard would then paste the prior solution
    back into the file before the rep had run — the exact spoiler the extract exists to
    prevent. Found Aug 10, 2026 on 703.
    """
    head = re.compile(DATED_ATTEMPT.format(stamp=re.escape(stamp)))
    start = next((i for i, ln in enumerate(lines) if head.match(ln)), None)
    if start is None:
        return False

    is_class_attempt = lines[start].lstrip().startswith("class")
    base = indent_of(lines[start])
    in_signature = False
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        if indent_of(line) <= base and not line.lstrip().startswith("#"):
            break
        stripped = line.strip()
        if in_signature:
            in_signature = not stripped.endswith(":")
            continue
        if is_class_attempt and (DECORATOR.match(line) or DEF_HEAD.match(line)):
            in_signature = not stripped.endswith(":")
            continue
        if stripped in ("pass", "..."):
            continue
        if stripped.startswith("#") or BANNER.match(line):
            continue
        return True
    return False


def find_source(number: str) -> Path | None:
    """The solution .py for a problem number — the stash filename drops the pattern folder,
    but the number is the identity, so glob it back (mirrors new_problem's twin check)."""
    matches = sorted(source_root().glob(f"*/{number}_*.py"))
    return matches[0] if matches else None


DATED_DEF_OR_CLASS = re.compile(r"^\s*(?:def\s+\w+|class\s+\w+)_(\d{8})\b", re.M)


def detect_session_stamp() -> str | None:
    """Newest dated-attempt stamp (`_YYYYMMDD`) across the stashed problems' source files.

    Restore runs at session end, and the stash exists only for problems touched THIS
    session — each such file carries today's dated attempt at the top. Defaulting to this
    instead of the wall clock is what keeps a **past-midnight close-out correct**: the stubs
    are stamped with the session's start date, so `now()` (already rolled to the next day)
    would look for an attempt that doesn't exist and wrongly declare every problem
    un-attempted, keeping all stashes out. Returns None (→ caller falls back to now()) when
    there's no stash or no stamp to read.
    """
    stamps: list[str] = []
    hist = history_dir()
    if hist.exists():
        for stash in hist.glob("*.txt"):
            m = re.match(r"(\d+)_", stash.name)
            src = find_source(m.group(1)) if m else None
            if src is None:
                continue
            stamps += DATED_DEF_OR_CLASS.findall(src.read_text(encoding="utf-8"))
    return max(stamps) if stamps else None


def duplicate_top_level_names(text: str) -> list[tuple[str, list[int]]]:
    """Top-level classes/functions defined more than once, as (name, line numbers).

    Why this check exists. Restore pastes the prior attempts back as a **verbatim line
    slice** and deliberately never parses their shape — that opacity is the invariant
    that keeps it working across dated methods, dated sibling classes and trailing
    unittest blocks. The cost is that it cannot notice when the merge lands two classes
    with the SAME name in one file, and Python silently binds the LAST one: today's
    attempt then runs a *previous attempt's* helper class.

    The scaffold banner already asks the learner to date their helpers
    (`TrieNode_20260802`), but a banner is prose, and on 2026-08-02 in problem 211 it was
    skipped — today's undated `TrieNode` was shadowed by the Jul 21 one. The classes
    happened to be identical, so nothing crashed, which is the bad case: silently wrong.

    Checking the merged text is cheap, needs no knowledge of the slice's shape, and so
    doesn't weaken the invariant above — it reads the RESULT, not the parts.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []  # a file mid-edit is not this check's problem
    seen: dict[str, list[int]] = {}
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            seen.setdefault(node.name, []).append(node.lineno)
    return [(name, lines) for name, lines in seen.items() if len(lines) > 1]


def collision_warnings(path: Path, text: str) -> list[str]:
    """Human-readable warnings for duplicate definitions in `text`."""
    return [
        f"{path}: '{name}' defined {len(lines)}× (lines {', '.join(map(str, lines))}) — "
        f"Python binds the LAST one, so the newest attempt may be running an older "
        f"attempt's helper. Suffix the newest with its date."
        for name, lines in duplicate_top_level_names(text)
    ]


def restore_stash(stash: Path, stamp: str | None, dry_run: bool,
                  warnings: list[str]) -> str | None:
    """Paste `stash` back into its source file. Returns a skip reason, or None if restored."""
    m = re.match(r"(\d+)_", stash.name)
    if not m:
        return "unrecognized stash name"
    src = find_source(m.group(1))
    if src is None:
        return f"no source file for {m.group(1)}"

    src_lines = src.read_text(encoding="utf-8").splitlines()
    if stamp is not None and not attempt_has_body(src_lines, stamp):
        return f"attempt {stamp} still empty — keeping stash out"

    body = strip_pointer(src_lines)                 # drop the breadcrumb
    merged = body + [""] + stash.read_text(encoding="utf-8").splitlines()
    text = "\n".join(merged).rstrip() + "\n"
    # Checked on --dry-run too: the whole point is to see the collision BEFORE it lands.
    warnings.extend(collision_warnings(src, text))

    if not dry_run:
        src.write_text(text, encoding="utf-8")
        stash.unlink()
    return None


def strip_legacy_region(path: Path, stamp: str | None, dry_run: bool,
                        warnings: list[str]) -> str | None:
    """Strip a pre-stash `# region` fold from `path`. Returns a skip reason, or None if done."""
    text = path.read_text(encoding="utf-8")
    if REGION_HEAD not in text:
        return "no region"
    lines = text.splitlines()
    if stamp is not None and not attempt_has_body(lines, stamp):
        return f"attempt {stamp} still empty — keeping the fold"
    unfolded = "\n".join(strip_spoiler_region(lines)) + "\n"
    warnings.extend(collision_warnings(path, unfolded))
    if not dry_run:
        path.write_text(unfolded, encoding="utf-8")
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", default=None,
                    help="session datestamp (YYYYMMDD); default = auto-detect from the "
                         "stashed files' newest dated attempt (correct across midnight), "
                         "else today")
    ap.add_argument("--all", action="store_true",
                    help="restore every stash / strip every region unconditionally, even "
                         "an un-attempted one — for reconciling old files, not session end")
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args()

    # Explicit --date wins; else auto-detect the session date from the stubs themselves
    # (survives a past-midnight close-out); else fall back to the wall clock.
    session_date = args.date or detect_session_stamp() or datetime.now().strftime("%Y%m%d")
    if not args.all and not args.date and session_date != datetime.now().strftime("%Y%m%d"):
        print(f"Using session date {session_date} (auto-detected from stubs; "
              f"wall clock is {datetime.now().strftime('%Y%m%d')}).")
    stamp = None if args.all else session_date
    verb = "Would restore" if args.dry_run else "Restored"
    done, kept, warnings = [], [], []

    # 1. Restore stashes written by the new extract path.
    hist = history_dir()
    if hist.exists():
        for stash in sorted(hist.glob("*.txt")):
            reason = restore_stash(stash, stamp, args.dry_run, warnings)
            (kept if reason else done).append((stash, reason))

    # 2. Migrate any legacy folded files (their code never left the file).
    for path in sorted(source_root().glob("*/*.py")):
        reason = strip_legacy_region(path, stamp, args.dry_run, warnings)
        if reason == "no region":
            continue
        (kept if reason else done).append((path, reason))

    for target, _ in done:
        print(f"{verb} {target}")
    for target, reason in kept:
        print(f"Kept {target} ({reason})")
    if not done:
        print("Nothing to restore.")

    # Surface loudly and last, so it survives a wall of "Restored ..." lines. Not fatal:
    # the paste itself is correct and the rename is the learner's to make (their code).
    if warnings:
        print(f"\n⚠️  {len(warnings)} name collision(s) in the merged file(s):")
        for warning in warnings:
            print(f"   - {warning}")


if __name__ == "__main__":
    main()
