"""Scaffold a solution file for a problem — the "set up before I start" action.

Creates an empty, dated skeleton so the file is ready before the learner codes.
NEW problem  -> create <root>/<pattern>/<number>_<snake>.py with an Attempt 1 banner.
RETRY (file exists) -> append an `Attempt N · <today>` banner + stub, never a 2nd file.

It writes NO solution logic and NO data-structure classes — only the scaffold
(respects the coach's whiteboard-fidelity + no-code-edits rules).

Usage:
    python scripts/new_problem.py --number 1 --title "Two Sum" --pattern arrays_and_hash \
        [--url https://leetcode.com/problems/two-sum/] [--method twoSum]
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

TEMPLATE = Path("docs/foundations/dsa/templates/solution_template.py")
DEFAULT_ROOT = "dsa/leetcode"


def source_root() -> Path:
    cfg = Path("cse.config.yml")
    if cfg.exists():
        m = re.search(r"roots:\s*\[([^\]]*)\]", cfg.read_text(encoding="utf-8"))
        if m:
            first = m.group(1).split(",")[0].strip().strip("'\"")
            if first:
                return Path(first)
    return Path(DEFAULT_ROOT)


def snake(title: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", title.strip().lower())
    return re.sub(r"_+", "_", s).strip("_")


def camel(title: str) -> str:
    parts = [p for p in re.split(r"[^0-9a-zA-Z]+", title.strip()) if p]
    if not parts:
        return "solve"
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def next_attempt_n(text: str) -> int:
    ns = [int(n) for n in re.findall(r"Attempt\s+(\d+)\s+·", text)]
    return (max(ns) + 1) if ns else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold a solution file (empty dated skeleton).")
    ap.add_argument("--number", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--pattern", required=True, help="category folder, e.g. arrays_and_hash")
    ap.add_argument("--url", default="")
    ap.add_argument("--method", default="")
    args = ap.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    name = snake(args.title)
    method = args.method or camel(args.title)
    url = args.url or f"https://leetcode.com/problems/{name.replace('_', '-')}/"
    path = source_root() / args.pattern / f"{args.number}_{name}.py"
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        body = TEMPLATE.read_text(encoding="utf-8")
        body = (
            body.replace("{number}", str(args.number))
            .replace("{title}", args.title)
            .replace("{url}", url)
            .replace("{pattern}", args.pattern)
            .replace("{date}", today)
            .replace("{method}", method)
        )
        path.write_text(body, encoding="utf-8")
        print(f"Created {path} (Attempt 1 · {today}).")
    else:
        text = path.read_text(encoding="utf-8")
        n = next_attempt_n(text)
        banner = (
            f"\n    # ── Attempt {n} · {today} "
            f"──────────────\n"
            f"    def {method}_v{n}(self):\n        pass\n"
        )
        path.write_text(text.rstrip() + "\n" + banner, encoding="utf-8")
        print(f"Appended Attempt {n} · {today} to existing {path}.")


if __name__ == "__main__":
    main()
