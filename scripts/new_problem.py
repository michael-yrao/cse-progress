"""Scaffold a solution file for a problem — the "set up before I start" action.

Creates an empty, dated skeleton so the file is ready before the learner codes.
NEW problem  -> create <root>/<pattern>/<number>_<snake>.py with an Attempt 1 banner.
RETRY (file exists) -> insert an `Attempt · <today>` banner + stub at the TOP of the
Solution class and fold everything below it into a spoiler region, never a 2nd file.

The retry stub goes first, not last, so opening the file lands on a blank page rather
than on the previous solution — reading your own prior answer before a retry destroys
the rep. Prior attempts stay in the same file (the dated history feeds streak/retirement
tracking) but sit inside a `# region` the editor can collapse.

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

# Fold markers around prior attempts. Comments carry no indentation meaning in Python,
# so the region may open inside a class body and close at module level — which is what
# lets one region cover every prior attempt regardless of how a file is laid out
# (methods inside `class Solution`, or sibling `class Solution_<date>` blocks).
REGION_HEAD = "# region ⚠ PRIOR ATTEMPTS — SPOILERS · fold before you start"
REGION_END = "# endregion"


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


def parse_signature(spec: str) -> tuple[str, str]:
    """`--signature` spec → (params, return_annotation), both ready to interpolate.

    A NEW problem has no prior method to read a signature from, so without this the
    stub is a bare `(self)` and the learner retypes the signature every attempt —
    transcription, not recall. Write it the way it reads on the problem page:

        --signature "times: List[List[int]], n: int, k: int -> int"
        → ("self, times: List[List[int]], n: int, k: int", "-> int")

    `self` is prepended unless you wrote it yourself; the return annotation is
    optional. `->` inside the params (a callable annotation) would break the split,
    so pass such a signature with an explicit leading `self` and split it yourself.
    """
    spec = spec.strip()
    if not spec:
        return "self", ""
    params, _, ret = spec.partition("->")
    params = params.strip().rstrip(",")
    ret = ret.strip()
    if not params:
        params = "self"
    elif params != "self" and not re.match(r"^self\b", params):
        params = f"self, {params}"
    return params, (f"-> {ret}" if ret else "")


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


def solution_class_start(lines: list[str]) -> int | None:
    """Index of the `class Solution:` header line, if the file has one.

    `\\b` after `Solution` won't match `class Solution_20260703` (an underscore is a
    word character), so dated sibling classes are correctly skipped.
    """
    return next(
        (i for i, ln in enumerate(lines) if re.match(r"^class\s+Solution\b", ln)),
        None,
    )


def strip_spoiler_region(lines: list[str]) -> list[str]:
    """Remove the previous run's fold markers so this run can re-wrap from scratch.

    Only our own region head is dropped, plus a trailing `# endregion` — an
    `# endregion` anywhere else belongs to the learner and is left alone.
    """
    out = [ln for ln in lines if not ln.strip().startswith(REGION_HEAD)]
    while out and not out[-1].strip():
        out.pop()
    if out and out[-1].strip() == REGION_END:
        out.pop()
    return out


def module_level_insert_at(lines: list[str]) -> int:
    """Index just past the module docstring and the import block.

    Where a dated `class Solution_<stamp>` goes when the attempt can't be expressed as
    a single method on `class Solution` (a multi-method problem like 271 encode/decode,
    or a legacy file with no `class Solution` at all).
    """
    i = 0
    if i < len(lines) and lines[i].lstrip().startswith(('"""', "'''")):
        quote = lines[i].lstrip()[:3]
        # A one-line docstring opens and closes on the same line.
        if lines[i].strip() != quote and lines[i].rstrip().endswith(quote):
            i += 1
        else:
            i += 1
            while i < len(lines) and quote not in lines[i]:
                i += 1
            i += 1
    last_import = i
    for j in range(i, len(lines)):
        if re.match(r"^(import|from)\s", lines[j]):
            last_import = j + 1
        elif lines[j].strip() and not lines[j].startswith("#"):
            break  # first real code — imports are done
    return last_import


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold a solution file (empty dated skeleton).")
    ap.add_argument("--number", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--pattern", required=True, help="category folder, e.g. arrays_and_hash")
    ap.add_argument("--url", default="")
    ap.add_argument("--method", default="",
                    help="method name; comma-separate for a multi-method problem "
                         "(e.g. --method encode,decode), which scaffolds a dated "
                         "`class Solution_<stamp>` instead of dated methods")
    ap.add_argument("--signature", action="append", default=[],
                    help="the method's real signature, e.g. "
                         "--signature \"times: List[List[int]], n: int, k: int -> int\". "
                         "`self` is implied. Repeat once per --method, in the same order. "
                         "Only used for a NEW problem — on a retry the signature is read "
                         "from the existing method, which always wins")
    ap.add_argument("--premium", action="store_true",
                    help="LC-premium problem → link the free NeetCode mirror instead")
    ap.add_argument("--force-new", action="store_true",
                    help="create a new file even though this number already exists on "
                         "disk under a different filename (normally refused — it forks "
                         "the attempt history)")
    args = ap.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    stamp = datetime.now().strftime("%Y%m%d")  # method suffix, matches existing convention
    name = snake(args.title)
    methods = [m.strip() for m in args.method.split(",") if m.strip()] or [camel(args.title)]
    method = methods[0]
    # Aligned with `methods` by position; a method with no --signature falls back to (self).
    signatures = [parse_signature(s) for s in args.signature]
    signatures += [("self", "")] * (len(methods) - len(signatures))
    slug = name.replace("_", "-")
    if args.url:
        url = args.url
    elif args.premium:
        url = f"https://neetcode.io/problems/{slug}"  # LC statement is paywalled; NC is free
    else:
        url = f"https://leetcode.com/problems/{slug}/"
    root = source_root()
    path = root / args.pattern / f"{args.number}_{name}.py"

    # A retry must never mint a second file. But the target path is derived from --title,
    # so a title that differs from the one already on disk ("Encode and Decode Strings"
    # vs the existing ...string.py) silently creates a duplicate and the attempt history
    # forks in two — which quietly breaks streak/retirement tracking. Same if --pattern
    # is wrong. The problem NUMBER is the real identity, so match on that and refuse.
    if not path.exists():
        twins = [p for p in root.glob(f"*/{args.number}_*.py") if p != path]
        if twins and not args.force_new:
            existing = "\n  ".join(str(p) for p in twins)
            ap.error(
                f"problem {args.number} already exists on disk:\n  {existing}\n"
                f"but --title/--pattern resolve to a different file:\n  {path}\n"
                f"This would fork the attempt history into two files. Re-run with the "
                f"existing filename's title (and its folder), or pass --force-new if "
                f"this really is a distinct problem that happens to share a number."
            )

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
            .replace("{params}", signatures[0][0])
            .replace("{ret}", f" {signatures[0][1]}" if signatures[0][1] else "")
            .replace("{statement}", STATEMENT_STUB)
        )
        path.write_text(body, encoding="utf-8")
        print(f"Created {path} (Attempt 1 · {today}).")
    else:
        text = path.read_text(encoding="utf-8")

        def stub(name_: str, indent: str, suffix: str) -> list[str]:
            """A blank `def` carrying the problem's real signature, never a bare (self).

            Retyping `(self, s1: str, s2: str) -> bool` on every retry is transcription,
            not recall — it isn't the rep, so the scaffolder does it.

            The file's own method wins over --signature: it's the signature the learner
            has actually been solving against, and it can't drift from what's on disk.
            --signature is the fallback for a legacy file whose method can't be parsed.
            """
            sig = existing_signature(text, name_)
            if not sig and name_ in methods:
                given = signatures[methods.index(name_)]
                sig = given if given != ("self", "") else None
            params, ret = sig if sig else ("self", "")
            head = f"{indent}def {name_}{suffix}({params})" + (f" {ret}" if ret else "") + ":"
            return [head, f"{indent}    pass"]

        lines = strip_spoiler_region(text.splitlines())
        cls = solution_class_start(lines)

        # One invariant, two layouts: the scaffold block ALWAYS ends with the region
        # head, and the region ALWAYS closes at EOF. So the fold spans exactly
        # "everything below today's stub" without the script ever having to understand
        # the shape of the prior attempts — which vary (dated methods, dated sibling
        # classes, trailing unittest blocks) and are not ours to parse.
        if len(methods) == 1 and cls is not None:
            # Dated method on the existing `class Solution` — the common case.
            at = cls + 1
            block = ["", f"    # ── Attempt · {today} ──────────────"]
            block += stub(method, "    ", f"_{stamp}")
            block += ["", f"    {REGION_HEAD}"]
            what = f"{method}_{stamp}()"
        else:
            # Dated sibling class — for multi-method problems (271 encode/decode), and
            # for legacy files with no `class Solution` to hang a method on.
            at = module_level_insert_at(lines)
            block = ["", "", f"# ── Attempt · {today} ──────────────", f"class Solution_{stamp}:"]
            for m in methods:
                block += [""] + stub(m, "    ", "")
            block += ["", "", REGION_HEAD]
            what = f"class Solution_{stamp}: {', '.join(m + '()' for m in methods)}"

        lines[at:at] = block
        lines.append(REGION_END)
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"Inserted attempt {today} -> {what} in {path} (line {at + 2}); "
              f"prior attempts folded.")


if __name__ == "__main__":
    main()
