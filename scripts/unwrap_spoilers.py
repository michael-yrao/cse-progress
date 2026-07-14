"""Remove the prior-attempts spoiler region from solution files that are DONE.

The region (`# region ⚠ PRIOR ATTEMPTS` … `# endregion`, written by new_problem.py) is
protection *before* the rep: it keeps a retry from opening on the previous answer. Once
the attempt is written, that protection has done its job and the fold is just clutter
hiding the learner's own history. This strips it at end of session.

    python scripts/unwrap_spoilers.py                 # today's completed attempts
    python scripts/unwrap_spoilers.py --date 20260713 # a specific session
    python scripts/unwrap_spoilers.py --all           # every file carrying a region
    python scripts/unwrap_spoilers.py --dry-run       # report, change nothing

**A file is only unwrapped once the dated attempt has a real body.** A retry that was
scaffolded but never attempted still has `pass` under today's stub — stripping that one
would expose the old solution before the rep ever happened, which is the exact failure
the region exists to prevent. So an untouched scaffold keeps its fold.
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from new_problem import REGION_END, REGION_HEAD, source_root, strip_spoiler_region

# `def maxPathSum_20260713(...)` or `class Solution_20260713:` — the dated attempt.
DATED_ATTEMPT = r"^\s*(?:def\s+\w+_{stamp}\s*\(|class\s+Solution_{stamp}\b)"
# The banner new_problem.py writes above a dated stub; not code, so it never counts
# as a body.
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
        # Dedent to or past the def/class header ends the attempt's block.
        if indent_of(line) <= base and not line.lstrip().startswith("#"):
            break
        stripped = line.strip()
        if stripped in ("pass", "..."):
            continue
        if stripped.startswith("#") or BANNER.match(line):
            continue
        return True
    return False


def unwrap(path: Path, stamp: str | None, dry_run: bool) -> str | None:
    """Strip the region from `path`. Returns a skip reason, or None if unwrapped."""
    text = path.read_text(encoding="utf-8")
    if REGION_HEAD not in text:
        return "no region"

    lines = text.splitlines()
    if stamp is not None and not attempt_has_body(lines, stamp):
        return f"attempt {stamp} still empty — keeping the fold"

    if not dry_run:
        stripped = strip_spoiler_region(lines)
        path.write_text("\n".join(stripped) + "\n", encoding="utf-8")
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"),
                    help="session datestamp (YYYYMMDD); default today")
    ap.add_argument("--all", action="store_true",
                    help="unwrap every file carrying a region, regardless of whether "
                         "an attempt was written — use when reconciling old files, not "
                         "at end of session")
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args()

    stamp = None if args.all else args.date
    unwrapped, skipped = [], []

    for path in sorted(source_root().glob("*/*.py")):
        reason = unwrap(path, stamp, args.dry_run)
        (skipped if reason else unwrapped).append((path, reason))

    verb = "Would unwrap" if args.dry_run else "Unwrapped"
    for path, _ in unwrapped:
        print(f"{verb} {path}")
    for path, reason in skipped:
        if reason != "no region":  # silent on the overwhelming majority
            print(f"Kept fold on {path} ({reason})")
    if not unwrapped:
        print("Nothing to unwrap.")


if __name__ == "__main__":
    main()
