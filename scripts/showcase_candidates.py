"""List candidate attempts for the showcase manifest (`dashboard/showcase.yml`) — the
read-only tool that feeds the human pick.

For each given problem NUMBER, or every file under the configured source roots with
`--all`, this prints every viable manifest candidate: for a `Solution`-wrapped file, each
of `Solution`'s own methods; for a design-problem file (a top-level class other than
`Solution`, e.g. `LRUCache`), the class itself. Each row carries its symbol · source line
range · comment-line count (leading banner + inline comments in its body) · attempt date ·
whether it carries a RECOGNITION note · the first inline comment (<=60 chars) — sorted by
comment-line count descending, so the best-documented attempt sorts first.

This never writes `dashboard/showcase.yml` itself — `export_showcase.py --check` is the
tool that enforces the manifest; the pick still needs a human to read the source and
confirm the "why" (see CLAUDE.md's `showcase-contract` decision).

Usage:
    python scripts/showcase_candidates.py 733 200      # one or more problem numbers
    python scripts/showcase_candidates.py --all         # every file under the source roots
    python scripts/showcase_candidates.py 733 --md       # markdown table instead of plain text
    python scripts/showcase_candidates.py --all --stub   # a manifest stub for each file's top pick
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

import _console
import export_showcase as es
import links

_console.force_utf8()

_COMMENT_LINE = re.compile(r"^\s*#")
_RECOGNITION = re.compile(r"RECOGNITION", re.IGNORECASE)


def _candidates_for_file(path: Path) -> list[dict]:
    """Candidates from one file, per the class-vs-methods rule in the module docstring.
    A syntax error (e.g. a stray BOM) is reported and skipped, never a crash."""
    lines = es.read_lines(path)
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError as exc:
        print(f"WARNING: {path}: cannot parse ({exc}); skipped.", file=sys.stderr)
        return []

    table = es.symbol_table(tree)
    rows: list[dict] = []
    for full_symbol, node in table.items():
        if "." in full_symbol:
            container, symbol = full_symbol.split(".", 1)
            if container != es.DEFAULT_CONTAINER:
                continue  # a design class's own methods aren't independent candidates
        else:
            container, symbol = None, full_symbol
            if isinstance(node, ast.ClassDef) and symbol == es.DEFAULT_CONTAINER:
                continue  # the Solution wrapper itself isn't a candidate; its methods are
        rows.append(_candidate_row(path, container, symbol, node, lines))

    rows.sort(key=lambda r: r["commentLines"], reverse=True)
    return rows


def _candidate_row(path: Path, container: str | None, symbol: str, node: ast.AST,
                    lines: list[str]) -> dict:
    start = es.def_start_line(node)
    end = node.end_lineno
    banner = es.leading_comment_block(lines, start)
    banner_lines = lines[banner[0] - 1:banner[1]] if banner else []
    body = lines[start - 1:end]
    inline_comments = [ln for ln in body if _COMMENT_LINE.match(ln)]
    return {
        "file": path,
        "container": container,
        "symbol": symbol,
        "startLine": start,
        "endLine": end,
        "commentLines": len(banner_lines) + len(inline_comments),
        "attemptDate": es.attempt_date(symbol, banner_lines),
        "recognition": any(_RECOGNITION.search(ln) for ln in body),
        "firstComment": next((ln.strip().lstrip("#").strip()[:60] for ln in inline_comments), ""),
    }


def _files_for_numbers(numbers: list[str]) -> list[Path]:
    paths: list[Path] = []
    for number in numbers:
        hits = [p for root in links.source_roots() for p in sorted(root.glob(f"*/{number}_*.py"))]
        if not hits:
            print(f"WARNING: no solution file found for {number}", file=sys.stderr)
        paths.extend(hits)
    return paths


def _all_files() -> list[Path]:
    return [p for root in links.source_roots() for p in sorted(root.glob("*/*.py"))]


def _row_label(row: dict) -> str:
    return f"{row['container']}.{row['symbol']}" if row["container"] else row["symbol"]


def _print_plain(rows: list[dict]) -> None:
    for row in rows:
        rel = row["file"].relative_to(es.REPO).as_posix()
        date = row["attemptDate"] or "-"
        flag = "RECOGNITION" if row["recognition"] else ""
        print(f"{rel} :: {_row_label(row)} · L{row['startLine']}-{row['endLine']} · "
              f"{row['commentLines']} comment-lines · {date} · {flag} · "
              f"{row['firstComment']}")


def _print_md(rows: list[dict]) -> None:
    print("| file | symbol | lines | comment-lines | date | recognition | first comment |")
    print("|---|---|---|---|---|---|---|")
    for row in rows:
        rel = row["file"].relative_to(es.REPO).as_posix()
        date = row["attemptDate"] or "-"
        flag = "yes" if row["recognition"] else ""
        comment = row["firstComment"].replace("|", "\\|")
        print(f"| {rel} | {_row_label(row)} | {row['startLine']}-{row['endLine']} | "
              f"{row['commentLines']} | {date} | {flag} | {comment} |")


def _print_stub(rows_by_file: dict[Path, list[dict]]) -> None:
    for path, rows in rows_by_file.items():
        if not rows:
            continue
        top = rows[0]
        lc_match = re.match(r"(\d+)_", path.name)
        lc = lc_match.group(1) if lc_match else "?"
        rel = path.relative_to(es.REPO).as_posix()
        print(f"  - lc: {lc}")
        print("    variant: TODO")
        if top["container"] is None:
            print("    container: null")
        print(f"    symbol: {top['symbol']}")
        print(f"    file: {rel}  # SUGGESTED — verify by reading the source before trusting this pick.")
        print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("numbers", nargs="*", help="problem number(s), e.g. 733 200")
    ap.add_argument("--all", action="store_true", help="scan every file under the source roots")
    ap.add_argument("--md", action="store_true", help="print a markdown table")
    ap.add_argument("--stub", action="store_true",
                     help="print a manifest stub for the top candidate of each file")
    args = ap.parse_args()

    if not args.all and not args.numbers:
        ap.error("give at least one problem number, or pass --all")

    paths = _all_files() if args.all else _files_for_numbers(args.numbers)
    rows_by_file = {path: _candidates_for_file(path) for path in paths}

    if args.stub:
        _print_stub(rows_by_file)
        return

    all_rows = [row for rows in rows_by_file.values() for row in rows]
    if args.md:
        _print_md(all_rows)
    else:
        _print_plain(all_rows)


if __name__ == "__main__":
    main()
