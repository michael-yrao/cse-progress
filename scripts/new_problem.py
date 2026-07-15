"""Scaffold a solution file for a problem — the "set up before I start" action.

Creates an empty, dated skeleton so the file is ready before the learner codes.
NEW problem  -> create <root>/<pattern>/<number>_<snake>.py with an Attempt 1 banner.
RETRY (file exists) -> insert an `Attempt · <today>` banner + stub at the TOP of the
Solution class and MOVE everything below it (the prior attempts) into a per-problem stash
at <root>/.history/<number>_<snake>.txt, leaving a one-line pointer in the file.

The retry stub goes first, not last, so opening the file lands on a blank page rather
than on the previous solution — reading your own prior answer before a retry destroys
the rep. The prior attempts are physically absent from the file while you work, so no
editor/extension is needed to hide them (portable to any editor, GitHub, plain diff).
scripts/restore_history.py pastes them back at session end, reconstructing the single
file with full dated history — unless the attempt was never made, in which case the
stash stays out so the file remains a blank page for next time.

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


def design_class_base(lines: list[str]) -> str | None:
    """Base name of a multi-method problem's own class — `Twitter` from `class Twitter`
    or `class Twitter_20260706` — so a retry's dated sibling class mirrors the real name
    (`Twitter_<stamp>`) instead of a generic `Solution_<stamp>`. Returns None when the
    file's classes are all `Solution` (e.g. 271 encode/decode), where the generic name
    is correct. The non-greedy group + optional `_<8 digits>` strips any dated suffix.
    """
    for ln in lines:
        m = re.match(r"^class\s+([A-Za-z_]\w*?)(?:_\d{8})?\s*[:(]", ln)
        if m and m.group(1) != "Solution":
            return m.group(1)
    return None


def class_defines_init(lines: list[str]) -> bool:
    """True if the existing attempts declare an `__init__` — the signal that this
    design problem's scaffold needs a constructor stub too (Twitter, LRUCache), versus
    a stateless codec (271 encode/decode) that has none. LeetCode hands you the
    `def __init__(self):` line, so it's an externally-fixed signature the scaffold owns,
    not something to recall.
    """
    return any(re.match(r"^\s*def\s+__init__\s*\(", ln) for ln in lines)


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


HISTORY_DIRNAME = ".history"
# Footer breadcrumb left in the active file while its prior attempts are stashed. It's
# how restore_history.py (and a human) knows history has been extracted, and it's stripped
# on restore. Match on this prefix — the tail carries the stash path.
POINTER_PREFIX = "# ⤵ prior attempts stashed"

DEF_OR_CLASS = re.compile(r"^\s*(?:async\s+def|def|class)\s+\w")


def history_dir() -> Path:
    """`<source_root>/.history/` — the session-scoped stash for extracted attempts.

    `.txt` files here never match the `*.py` source glob, so the tracker's discovery
    (scripts/update_review_dates.py) ignores them and no phantom rows appear.
    """
    return source_root() / HISTORY_DIRNAME


def stash_path(number: str, name: str) -> Path:
    return history_dir() / f"{number}_{name}.txt"


def make_pointer(stash: Path) -> str:
    return (f"{POINTER_PREFIX} in {stash.as_posix()} — "
            f"restored at session end (python scripts/restore_history.py)")


def strip_pointer(lines: list[str]) -> list[str]:
    """Drop the stash breadcrumb + any trailing blanks it left behind."""
    out = [ln for ln in lines if not ln.strip().startswith(POINTER_PREFIX)]
    while out and not out[-1].strip():
        out.pop()
    return out


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def block_has_real_body(lines: list[str], start: int) -> bool:
    """True if the def/class at `start` holds anything past pass / ... / comments / blanks.

    A dedent to or past the header's indent (on a non-comment line) ends its block. Nested
    def/class *headers* are skipped — structure, not solution content — but their bodies are
    still scanned, so a real inner statement counts. This is what tells an un-attempted stub
    (`def m(self): pass`) apart from a written solution.
    """
    base = _indent(lines[start])
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        if _indent(line) <= base and not line.lstrip().startswith("#"):
            break
        s = line.strip()
        if s in ("pass", "...") or s.startswith("#") or DEF_OR_CLASS.match(line):
            continue
        return True
    return False


def slice_has_real_attempt(lines: list[str]) -> bool:
    """True if any def/class in `lines` carries a real body — i.e. worth stashing."""
    return any(
        DEF_OR_CLASS.match(ln) and block_has_real_body(lines, i)
        for i, ln in enumerate(lines)
    )


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
                         "sibling class instead of dated methods — mirroring the "
                         "existing class name and its __init__ on a retry")
    ap.add_argument("--signature", action="append", default=[],
                    help="the method's real signature, e.g. "
                         "--signature \"times: List[List[int]], n: int, k: int -> int\". "
                         "`self` is implied. Repeat once per --method, in the same order. "
                         "Only used for a NEW problem — on a retry the signature is read "
                         "from the existing method, which always wins")
    ap.add_argument("--premium", action="store_true",
                    help="LC-premium problem -> link the free NeetCode mirror instead")
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

        # Also strips a prior run's spoiler region (legacy folded files migrate cleanly:
        # the markers are dropped, the code they wrapped becomes ordinary prior attempts)
        # and any leftover stash pointer.
        lines = strip_pointer(strip_spoiler_region(text.splitlines()))
        cls = solution_class_start(lines)

        # One invariant, two layouts: today's stub goes at the TOP (of `class Solution`,
        # or as a dated sibling class), and EVERYTHING BELOW IT is "the prior attempts" —
        # a verbatim line slice the script moves to the stash without ever parsing its
        # shape (dated methods, dated sibling classes, trailing unittest blocks all vary
        # and are not ours to interpret). restore_history.py pastes that same slice back
        # after the completed attempt at session end, reconstructing the single file.
        if len(methods) == 1 and cls is not None:
            # Dated method on the existing `class Solution` — the common case.
            at = cls + 1
            block = ["", f"    # ── Attempt · {today} ──────────────"]
            block += stub(method, "    ", f"_{stamp}")
            what = f"{method}_{stamp}()"
        else:
            # Dated sibling class — for multi-method problems (271 encode/decode, design
            # problems like 355 Twitter), and for legacy files with no `class Solution`.
            at = module_level_insert_at(lines)
            base = design_class_base(lines) or "Solution"  # mirror the real class name
            members = methods[:]
            # A design problem's constructor is externally fixed too (LeetCode provides the
            # `__init__` line) — mirror it as a blank stub, with its real signature, when the
            # existing class declares one. `stub` reads that signature from disk, so
            # `LRUCache(capacity)` scaffolds as `__init__(self, capacity: int)`, not `()`.
            if class_defines_init(lines) and "__init__" not in members:
                members.insert(0, "__init__")
            block = ["", "", f"# ── Attempt · {today} ──────────────", f"class {base}_{stamp}:"]
            for m in members:
                block += [""] + stub(m, "    ", "")
            what = f"class {base}_{stamp}: {', '.join(m + '()' for m in members)}"

        lines[at:at] = block
        prior = lines[at + len(block):]          # everything below today's stub
        while prior and not prior[0].strip():    # trim framing blanks off the slice
            prior.pop(0)
        while prior and not prior[-1].strip():
            prior.pop()

        stash = stash_path(args.number, name)
        active = lines[:at + len(block)]
        stashed = True
        if slice_has_real_attempt(prior):
            # Real prior attempts → move them out. A pre-existing stash (a session cut
            # short before restore) keeps its older attempts; today's prior goes on top.
            history_dir().mkdir(parents=True, exist_ok=True)
            body = "\n".join(prior)
            if stash.exists():
                body = body + "\n\n" + stash.read_text(encoding="utf-8").rstrip("\n")
            stash.write_text(body + "\n", encoding="utf-8")
        elif not stash.exists():
            # Nothing real to hide and no stash — leave the file whole (no pointer).
            active, stashed = lines, False
        # else: prior is just an un-attempted stub; the real history is already stashed —
        # drop the stub (active already excludes it) and keep the stash untouched.

        if stashed:
            while active and not active[-1].strip():
                active.pop()
            active += ["", make_pointer(stash)]

        path.write_text("\n".join(active).rstrip() + "\n", encoding="utf-8")
        where = f"stashed → {stash.as_posix()}" if stashed else "no prior attempts to stash"
        print(f"Inserted attempt {today} -> {what} in {path} (line {at + 2}); {where}.")


if __name__ == "__main__":
    main()
