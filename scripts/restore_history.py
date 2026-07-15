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


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def attempt_has_body(lines: list[str], stamp: str) -> bool:
    """True if the dated attempt contains anything beyond `pass` / comments / blanks."""
    head = re.compile(DATED_ATTEMPT.format(stamp=re.escape(stamp)))
    start = next((i for i, ln in enumerate(lines) if head.match(ln)), None)
    if start is None:
        return False

    base = indent_of(lines[start])
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        if indent_of(line) <= base and not line.lstrip().startswith("#"):
            break
        stripped = line.strip()
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


def restore_stash(stash: Path, stamp: str | None, dry_run: bool) -> str | None:
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

    if not dry_run:
        body = strip_pointer(src_lines)             # drop the breadcrumb
        merged = body + [""] + stash.read_text(encoding="utf-8").splitlines()
        src.write_text("\n".join(merged).rstrip() + "\n", encoding="utf-8")
        stash.unlink()
    return None


def strip_legacy_region(path: Path, stamp: str | None, dry_run: bool) -> str | None:
    """Strip a pre-stash `# region` fold from `path`. Returns a skip reason, or None if done."""
    text = path.read_text(encoding="utf-8")
    if REGION_HEAD not in text:
        return "no region"
    lines = text.splitlines()
    if stamp is not None and not attempt_has_body(lines, stamp):
        return f"attempt {stamp} still empty — keeping the fold"
    if not dry_run:
        path.write_text("\n".join(strip_spoiler_region(lines)) + "\n", encoding="utf-8")
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"),
                    help="session datestamp (YYYYMMDD); default today")
    ap.add_argument("--all", action="store_true",
                    help="restore every stash / strip every region unconditionally, even "
                         "an un-attempted one — for reconciling old files, not session end")
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args()

    stamp = None if args.all else args.date
    verb = "Would restore" if args.dry_run else "Restored"
    done, kept = [], []

    # 1. Restore stashes written by the new extract path.
    hist = history_dir()
    if hist.exists():
        for stash in sorted(hist.glob("*.txt")):
            reason = restore_stash(stash, stamp, args.dry_run)
            (kept if reason else done).append((stash, reason))

    # 2. Migrate any legacy folded files (their code never left the file).
    for path in sorted(source_root().glob("*/*.py")):
        reason = strip_legacy_region(path, stamp, args.dry_run)
        if reason == "no region":
            continue
        (kept if reason else done).append((path, reason))

    for target, _ in done:
        print(f"{verb} {target}")
    for target, reason in kept:
        print(f"Kept {target} ({reason})")
    if not done:
        print("Nothing to restore.")


if __name__ == "__main__":
    main()
