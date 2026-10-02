"""Emit the practice-runner data contract (practice.json) for the practice log.

progressiveoverflow.com's practice page runs the learner's Python in the browser against
stored test cases. Those cases used to be a throwaway check script the coach wrote per
rep and discarded. This script keeps them: it reads every hand-authored spec in
`dsa/tests/<number>_<snake_title>.yml` (statement, entry point, signature, comparison mode,
cases as `args` + `expected`) and emits `dashboard/practice.json`, the file the site
fetches. No reference solution is published, only inputs and expected outputs.
See decisions.yml `practice-contract`.

Design constraints this file honours (same as export_showcase.py):

  * NOT FAIL-SOFT. A malformed spec is a hard error (exit 1) naming the spec file — a
    wrong expected value shipped to the site marks a correct solution as failing.

  * ONE signature parser. The stub is rendered with `new_problem.parse_signature`, the
    same helper `new_problem.py --signature` uses, so a scaffold and the site's blank
    editor can never disagree on the signature.

Usage:
    python scripts/export_practice.py             # write dashboard/practice.json
    python scripts/export_practice.py --stdout     # print the JSON, do not write
    python scripts/export_practice.py --check      # build in memory, validate, write nothing;
                                                     # exit 1 on any failure
    python scripts/export_practice.py --date 2026-10-01   # override generatedAt (default: today)

`--check` also fails when `dashboard/practice.json` already exists on disk and differs from
what the specs would produce right now. `generatedAt` is ignored in that comparison, so a
regeneration on a later day is not drift.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import _console
import new_problem

_console.force_utf8()

REPO = Path(__file__).resolve().parent.parent
SPEC_DIR = REPO / "dsa" / "tests"
DASHBOARD = REPO / "dashboard"
OUT = DASHBOARD / "practice.json"

SCHEMA_VERSION = 1

# What the site's worker needs above the stub so the stub runs unmodified.
STUB_PREAMBLE = "from typing import List, Optional\n\n\n"

COMPARE_MODES = frozenset({"exact", "unordered", "unordered-nested"})
REQUIRED_SPEC_KEYS = ("number", "title", "url", "statement", "entry", "signature",
                      "compare", "cases")
REQUIRED_ENTRY_KEYS = ("class", "method")

_FILENAME_NUMBER = re.compile(r"^(\d+)_")


class PracticeError(Exception):
    """A fatal spec/contract problem. Never caught silently — see the module docstring's
    NOT FAIL-SOFT constraint."""


# ── pure helpers (no filesystem access) ─────────────────────────────────────────────

def render_stub(class_name: str, method: str, signature: str) -> str:
    """The blank starting code: `STUB_PREAMBLE` + the class + one `pass` method, with the
    signature parsed by `new_problem.parse_signature` (`self` implied)."""
    params, ret = new_problem.parse_signature(signature)
    ret_suffix = f" {ret}" if ret else ""
    return (f"{STUB_PREAMBLE}class {class_name}:\n"
            f"    def {method}({params}){ret_suffix}:\n"
            f"        pass\n")


def _filename_number(filename: str) -> int | None:
    match = _FILENAME_NUMBER.match(filename)
    return int(match.group(1)) if match else None


def _validate_entry(entry: object, filename: str) -> None:
    if not isinstance(entry, dict):
        raise PracticeError(f"{filename}: 'entry' must be a mapping")
    for key in REQUIRED_ENTRY_KEYS:
        if key not in entry:
            raise PracticeError(f"{filename}: entry is missing '{key}'")
    for key in REQUIRED_ENTRY_KEYS:
        if not isinstance(entry[key], str) or not entry[key].strip():
            raise PracticeError(f"{filename}: entry.{key} must be a non-empty string")


def _validate_cases(cases: object, filename: str) -> None:
    if not isinstance(cases, list) or not cases:
        raise PracticeError(f"{filename}: 'cases' must be a non-empty list")
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise PracticeError(f"{filename}: case {index} must be a mapping")
        if not isinstance(case.get("args"), list):
            raise PracticeError(f"{filename}: case {index} 'args' must be a list")
        if "expected" not in case:
            raise PracticeError(f"{filename}: case {index} has no 'expected'")
    if not any(case.get("example") is True for case in cases):
        raise PracticeError(f"{filename}: no case has 'example: true'")


def validate_spec(spec: object, filename: str) -> None:
    """Raise `PracticeError` naming `filename` on the first way `spec` is unusable."""
    if not isinstance(spec, dict):
        raise PracticeError(f"{filename}: spec must be a mapping")
    for key in REQUIRED_SPEC_KEYS:
        if key not in spec:
            raise PracticeError(f"{filename}: missing required key '{key}'")
    if spec["number"] != _filename_number(filename):
        raise PracticeError(
            f"{filename}: number {spec['number']!r} does not match the filename's "
            f"leading number")
    _validate_entry(spec["entry"], filename)
    if spec["compare"] not in COMPARE_MODES:
        raise PracticeError(
            f"{filename}: compare {spec['compare']!r} is not one of "
            f"{sorted(COMPARE_MODES)}")
    _validate_cases(spec["cases"], filename)


def build_problem(spec: dict) -> dict:
    """One `problems` entry from a validated spec."""
    entry = spec["entry"]
    return {
        "number": spec["number"],
        "title": spec["title"],
        "url": spec["url"],
        "statement": str(spec["statement"]).rstrip("\n"),
        "stub": render_stub(entry["class"], entry["method"], spec["signature"]),
        "entry": {"className": entry["class"], "method": entry["method"]},
        "compare": spec["compare"],
        "cases": [
            {"args": case["args"], "expected": case["expected"],
             "example": case.get("example") is True}
            for case in spec["cases"]
        ],
    }


def build_payload(named_specs: list[tuple[str, object]], today: dt.date) -> dict:
    """The practice.json payload from `(filename, spec)` pairs. Validates every spec and
    refuses a number two specs share."""
    seen: dict[int, str] = {}
    problems = []
    for filename, spec in named_specs:
        validate_spec(spec, filename)
        number = spec["number"]
        if number in seen:
            raise PracticeError(
                f"{filename}: number {number} is already used by {seen[number]}")
        seen[number] = filename
        problems.append(build_problem(spec))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": today.isoformat(),
        "problems": sorted(problems, key=lambda p: p["number"]),
    }


def _without_date(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if key != "generatedAt"}


def stale_reasons(payload: dict, existing: object) -> list[str]:
    """Every way the parsed on-disk practice.json differs from `payload`, ignoring
    `generatedAt`. Empty when it is current."""
    if not isinstance(existing, dict) or not isinstance(existing.get("problems"), list):
        return ["practice.json: top level must be an object with a 'problems' list"]
    if _without_date(existing) == _without_date(payload):
        return []
    new_by_number = {p["number"]: p for p in payload["problems"]}
    old_by_number = {p.get("number"): p for p in existing["problems"]
                     if isinstance(p, dict)}
    reasons = []
    added = sorted(new_by_number.keys() - old_by_number.keys())
    removed = sorted(old_by_number.keys() - new_by_number.keys(), key=str)
    if added or removed:
        reasons.append(f"problem set changed — added {added}, removed {removed}")
    for number in sorted(new_by_number.keys() & old_by_number.keys()):
        if new_by_number[number] != old_by_number[number]:
            reasons.append(f"{number}: differs from the committed practice.json — "
                           f"regenerate")
    return reasons or ["practice.json: differs from the specs — regenerate"]


# ── filesystem access ────────────────────────────────────────────────────────────────

def load_specs(spec_dir: Path) -> list[tuple[str, object]]:
    """`(filename, parsed YAML)` for every `*.yml` in `spec_dir`, sorted by filename."""
    import yaml  # noqa: PLC0415 — only this loader needs PyYAML

    named_specs = []
    for path in sorted(spec_dir.glob("*.yml")):
        try:
            named_specs.append((path.name, yaml.safe_load(path.read_text(encoding="utf-8"))))
        except (OSError, yaml.YAMLError) as exc:
            raise PracticeError(f"{path.name}: cannot read spec: {exc}") from exc
    return named_specs


def read_existing(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"cannot read existing {path}: {exc}"


# ── CLI ───────────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stdout", action="store_true", help="print the JSON, do not write")
    ap.add_argument("--check", action="store_true",
                     help="build in memory, validate, never write; exit 1 on any failure")
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                     help="override generatedAt (default: today)")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()

    try:
        payload = build_payload(load_specs(SPEC_DIR), today)
    except PracticeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    count = len(payload["problems"])
    if args.check:
        if OUT.exists():
            existing = read_existing(OUT)
            reasons = ([existing] if isinstance(existing, str)
                       else stale_reasons(payload, existing))
            if reasons:
                print("ERROR: dashboard/practice.json is stale:", file=sys.stderr)
                for reason in reasons:
                    print(f"  - {reason}", file=sys.stderr)
                sys.exit(1)
        print(f"ok: {count} practice problems verified", file=sys.stderr)
        return

    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.stdout:
        print(rendered)
        return

    DASHBOARD.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({count} problems)")


if __name__ == "__main__":
    main()
