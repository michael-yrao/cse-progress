"""Scaffold a solution file for a problem — the "set up before I start" action.

Creates an empty, dated skeleton so the file is ready before the learner codes.
NEW problem  -> create <root>/<pattern>/<number>_<snake>.py with an Attempt 1 banner.
RETRY (file exists) -> append an `Attempt N · <today>` banner + stub, never a 2nd file.

It writes NO solution logic and NO data-structure classes — only the scaffold
(respects the whiteboard-fidelity + no-code-edits rules).

The learner never pastes the problem statement — the coach fills it in (auto-fetched
from the problem source, or a token-lean compressed version in low-token mode).

Usage:
    python scripts/new_problem.py --number 1 --title "Two Sum" --pattern arrays_and_hash \
        [--url https://leetcode.com/problems/two-sum/] [--method twoSum] [--premium]
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

TEMPLATE = Path("docs/foundations/dsa/templates/solution_template.py")
DEFAULT_ROOT = "dsa/leetcode"

# The learner never pastes the statement. The coach fills this in — auto-fetched
# from the problem source, or a "caveman-compressed" version in low-token mode.
STATEMENT_STUB = (
    "<coach fills this: the problem statement (auto-fetched), or a caveman-"
    "compressed version in low-token mode — the learner never pastes it>"
)


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


def existing_signature(text: str, method: str) -> tuple[str, str] | None:
    """(params, return_annotation) of the problem's existing method, if present.

    A retry stub must carry the real signature (`self, s1: str, s2: str) -> bool`),
    not a bare `(self)` — otherwise the learner retypes it every attempt. Prefer the
    unsuffixed original; fall back to any dated variant.
    """
    for pattern in (
        rf"^\s*def\s+{re.escape(method)}\s*\((?P<params>[^)]*)\)\s*(?P<ret>->[^:]*)?:",
        rf"^\s*def\s+{re.escape(method)}_\w+\s*\((?P<params>[^)]*)\)\s*(?P<ret>->[^:]*)?:",
    ):
        m = re.search(pattern, text, re.M)
        if m:
            return m.group("params").strip(), (m.group("ret") or "").strip()
    return None


def solution_class_end(lines: list[str]) -> int:
    """Index just past the last line belonging to `class Solution`.

    Appending at EOF corrupts files that carry trailing module-level code (e.g. a
    `unittest.TestCase` block + `unittest.main()`): the indented stub lands outside
    the class -> IndentationError. So insert at the end of the Solution class body,
    not the end of the file.
    """
    start = next(
        (i for i, ln in enumerate(lines) if re.match(r"^class\s+Solution\b", ln)),
        None,
    )
    if start is None:
        return len(lines)  # no Solution class -> fall back to EOF
    end = start + 1
    for i in range(start + 1, len(lines)):
        stripped = lines[i].strip()
        if not stripped:
            continue
        # A non-indented, non-comment line means we've left the class body.
        if not lines[i].startswith((" ", "\t")):
            break
        end = i + 1
    return end


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold a solution file (empty dated skeleton).")
    ap.add_argument("--number", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--pattern", required=True, help="category folder, e.g. arrays_and_hash")
    ap.add_argument("--url", default="")
    ap.add_argument("--method", default="")
    ap.add_argument("--premium", action="store_true",
                    help="LC-premium problem → link the free NeetCode mirror instead")
    args = ap.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    stamp = datetime.now().strftime("%Y%m%d")  # method suffix, matches existing convention
    name = snake(args.title)
    method = args.method or camel(args.title)
    slug = name.replace("_", "-")
    if args.url:
        url = args.url
    elif args.premium:
        url = f"https://neetcode.io/problems/{slug}"  # LC statement is paywalled; NC is free
    else:
        url = f"https://leetcode.com/problems/{slug}/"
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
            .replace("{statement}", STATEMENT_STUB)
        )
        path.write_text(body, encoding="utf-8")
        print(f"Created {path} (Attempt 1 · {today}).")
    else:
        text = path.read_text(encoding="utf-8")
        # Carry the real signature over from the existing method — a bare `(self)`
        # stub would make the learner retype the params on every retry.
        sig = existing_signature(text, method)
        if sig:
            params, ret = sig
            head = f"    def {method}_{stamp}({params})" + (f" {ret}" if ret else "") + ":"
        else:
            head = f"    def {method}_{stamp}(self):"
        # Date suffix, not an attempt counter: it can't be wrong on legacy files
        # (which carry no banners to count) and matches the existing convention.
        banner = [
            "",
            f"    # ── Attempt · {today} ──────────────",
            head,
            "        pass",
        ]
        lines = text.splitlines()
        at = solution_class_end(lines)
        lines[at:at] = banner
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"Appended attempt {today} -> {method}_{stamp}() in {path} (line {at + 2}).")


if __name__ == "__main__":
    main()
