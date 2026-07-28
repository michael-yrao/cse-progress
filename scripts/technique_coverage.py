#!/usr/bin/env python3
"""Generate the DSA technique-coverage report.

The spaced-repetition tracker (`dsa_progress.md`) is keyed by **problem**. That is the
right key for scheduling reviews and the wrong key for answering "do I actually know
topological sort?" — a question about a *technique*, which is spread across several
problems and sometimes several methods of the same problem.

This script joins a hand-authored technique vocabulary (`techniques.yml`) against the
tracker and emits `technique_coverage.md`, one row per technique, with three gap checks:

  no-green   no problem for this technique has ever come back 🟢 — a phase-exit blocker
             under the per-algorithm exit rule (recognition + execution, >=1 🟢 each)
  thin       fewer problems than `min_problems` — a technique needs 3-4 surface forms
             before it is a skill rather than recall of one problem's solution
  variant    a declared method variant with zero problems behind it (the Kahn's-vs-DFS
             case that prompted this tool). Variants already sitting in the Waiting Room
             or Expansion Queue are marked `queued:` in the YAML and reported separately,
             so a known gap never masquerades as a new finding.

It also reports **unmapped** tracker rows. That is the anti-drift guard: a newly solved
problem shows up as unmapped until someone assigns it a technique, so the vocabulary
cannot silently fall behind the tracker the way the method parentheticals did.

Usage:
    python scripts/technique_coverage.py            # write the report
    python scripts/technique_coverage.py --check    # exit 1 if the report is stale
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTERY = REPO_ROOT / "docs" / "foundations" / "dsa" / "mastery"
TECHNIQUES_YML = MASTERY / "techniques.yml"
TRACKER_MD = MASTERY / "dsa_progress.md"
REPORT_MD = MASTERY / "technique_coverage.md"

DEFAULT_MIN_PROBLEMS = 3

# Comfort tiers, weakest to strongest. Ordering drives "best comfort" and the
# no-green check; 🎓 and 🏆 both imply the technique has been executed cleanly.
COMFORT_ORDER = ["🔴", "🟡", "🟢", "🎓", "🏆"]
COMFORT_RANK = {c: i for i, c in enumerate(COMFORT_ORDER)}
GREEN_OR_BETTER = {"🟢", "🎓", "🏆"}

# Matches a review row in dsa_progress.md. Deliberately looser than the tracker's own
# ROW_RE (which owns rewriting the file) — this script only ever reads.
ROW_RE = re.compile(
    r"^\|\s*(?P<difficulty>[^|]+?)\s*\|\s*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*\|\s*"
    r"(?P<comfort>" + "|".join(COMFORT_ORDER) + r")\s*\|\s*(?P<streak>\d+)\s*\|"
)
# "210. Course Schedule II (Kahn's)" -> number 210, method "Kahn's"
TITLE_RE = re.compile(r"^(?P<number>\d+)\.\s*(?P<name>.+?)(?:\s*\((?P<method>[^)]+)\))?$")


@dataclass(frozen=True)
class Row:
    """One solved-problem row in the tracker."""

    number: int
    name: str
    method: str | None
    comfort: str
    streak: int
    difficulty: str

    @property
    def label(self) -> str:
        return f"{self.number} {self.name}" + (f" ({self.method})" if self.method else "")


@dataclass
class Resolved:
    """A technique after its YAML entry has been joined against the tracker."""

    name: str
    family: str
    min_problems: int
    rows: list[Row] = field(default_factory=list)
    variant_rows: dict[str, list[Row]] = field(default_factory=dict)
    queued_variants: dict[str, str] = field(default_factory=dict)
    needs_review: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    @property
    def best_comfort(self) -> str:
        if not self.rows:
            return "—"
        return max((r.comfort for r in self.rows), key=lambda c: COMFORT_RANK[c])

    @property
    def has_green(self) -> bool:
        return any(r.comfort in GREEN_OR_BETTER for r in self.rows)

    @property
    def gaps(self) -> list[str]:
        out: list[str] = []
        if not self.has_green:
            out.append("**no-green**")
        if len(self.rows) < self.min_problems:
            out.append(f"thin ({len(self.rows)}/{self.min_problems})")
        for variant, rows in self.variant_rows.items():
            if not rows and variant not in self.queued_variants:
                out.append(f"variant: **{variant}**")
        return out


def parse_tracker(path: Path) -> list[Row]:
    """Read every review row out of the tracker. Non-table lines are ignored."""
    if not path.exists():
        raise SystemExit(f"Tracker not found: {path}")

    rows: list[Row] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        match = ROW_RE.match(line)
        if not match:
            continue
        title_match = TITLE_RE.match(match.group("title").strip())
        if not title_match:
            continue
        rows.append(
            Row(
                number=int(title_match.group("number")),
                name=title_match.group("name").strip(),
                method=(title_match.group("method") or "").strip() or None,
                comfort=match.group("comfort"),
                streak=int(match.group("streak")),
                difficulty=match.group("difficulty").strip(),
            )
        )
    return rows


def _matches(row: Row, spec: dict) -> bool:
    """Does a tracker row satisfy a YAML problem spec?

    `method` is the join key for problems carrying several rows (200 DFS vs BFS,
    323 DFS/BFS/Union-Find). Omit it to match every row for that number.
    """
    if row.number != spec["number"]:
        return False
    method = spec.get("method")
    return True if method is None else row.method == method


def resolve(config: dict, rows: list[Row]) -> tuple[list[Resolved], set[str]]:
    """Join the technique vocabulary against the tracker rows."""
    default_min = config.get("defaults", {}).get("min_problems", DEFAULT_MIN_PROBLEMS)
    resolved: list[Resolved] = []
    claimed: set[str] = set()

    for entry in config.get("techniques", []):
        tech = Resolved(
            name=entry["name"],
            family=entry.get("family", "—"),
            min_problems=entry.get("min_problems", default_min),
        )
        for variant in entry.get("variants", []) or []:
            tech.variant_rows[variant["name"]] = []
            if variant.get("queued"):
                tech.queued_variants[variant["name"]] = variant["queued"]

        for spec in entry.get("problems", []) or []:
            matched = [r for r in rows if _matches(r, spec)]
            if not matched:
                label = str(spec["number"]) + (f" ({spec['method']})" if spec.get("method") else "")
                tech.missing.append(label)
                continue
            for row in matched:
                tech.rows.append(row)
                claimed.add(row.label)
                variant = spec.get("variant") or spec.get("method")
                if variant and variant in tech.variant_rows:
                    tech.variant_rows[variant].append(row)
                if spec.get("review"):
                    tech.needs_review.append(row.label)

        resolved.append(tech)

    return resolved, claimed


def render(resolved: list[Resolved], rows: list[Row], claimed: set[str]) -> str:
    """Build the markdown report."""
    lines: list[str] = []
    add = lines.append

    add("# DSA Technique Coverage")
    add("")
    add("<!-- GENERATED by scripts/technique_coverage.py — do not edit by hand.")
    add("     Source of truth is techniques.yml (vocabulary) + dsa_progress.md (comfort).")
    add("     Regenerate: python scripts/technique_coverage.py -->")
    add("")
    add(
        "> The tracker is keyed by **problem**; this is keyed by **technique**. Use it at the "
        "weekly build to decide what to pull, and at phase exit to check the per-algorithm bar "
        "(recognition + execution, ≥1 🟢 each)."
    )
    add("")

    blockers = [t for t in resolved if not t.has_green and t.rows]
    thin = [t for t in resolved if len(t.rows) < t.min_problems]
    variant_gaps = [
        (t, v)
        for t in resolved
        for v, vr in t.variant_rows.items()
        if not vr and v not in t.queued_variants
    ]

    add(
        f"> **{len(resolved)}** techniques &nbsp;·&nbsp; "
        f"**{len(blockers)}** with no 🟢 &nbsp;·&nbsp; "
        f"**{len(thin)}** thin &nbsp;·&nbsp; "
        f"**{len(variant_gaps)}** unqueued variant gaps"
    )
    add("")

    if blockers or thin or variant_gaps:
        add("## ⚠️ Action list")
        add("")
        if blockers:
            add("**No 🟢 — blocks per-algorithm phase exit.** Execution is unproven.")
            add("")
            for t in sorted(blockers, key=lambda t: t.name):
                probs = ", ".join(str(r.number) for r in t.rows)
                add(f"- **{t.name}** ({t.family}) — best {t.best_comfort} across {probs}")
            add("")
        if thin:
            add(
                "**Thin — fewer than the 3–4 surface forms a technique needs.** One instance "
                "trains recall of that problem, not the skill."
            )
            add("")
            for t in sorted(thin, key=lambda t: (len(t.rows), t.name)):
                probs = ", ".join(str(r.number) for r in t.rows) or "none"
                add(f"- **{t.name}** ({t.family}) — {len(t.rows)}/{t.min_problems}: {probs}")
            add("")
        if variant_gaps:
            add("**Unqueued variant gaps — a method never once exercised, and not in any queue.**")
            add("")
            for t, v in sorted(variant_gaps, key=lambda p: p[0].name):
                done = [k for k, rs in t.variant_rows.items() if rs]
                have = ", ".join(f"{k} ×{len(t.variant_rows[k])}" for k in done) or "none"
                add(f"- **{t.name}** — missing **{v}**. Exercised: {have}")
            add("")

    add("## Coverage")
    add("")
    add("| Technique | Family | Problems | Best | 🟢 | Variants | Gaps |")
    add("|---|---|---:|:---:|:---:|---|---|")
    for t in sorted(resolved, key=lambda t: (t.family, t.name)):
        probs = ", ".join(str(r.number) for r in sorted(t.rows, key=lambda r: r.number)) or "—"
        if t.variant_rows:
            parts = []
            for v, rs in t.variant_rows.items():
                if rs:
                    parts.append(f"{v} ×{len(rs)}")
                elif v in t.queued_variants:
                    parts.append(f"~~{v}~~ *(queued: `{t.queued_variants[v]}`)*")
                else:
                    parts.append(f"**{v} ×0**")
            variants = " · ".join(parts)
        else:
            variants = "—"
        add(
            f"| {t.name} | {t.family} | {len(t.rows)} ({probs}) | {t.best_comfort} | "
            f"{'✅' if t.has_green else '❌'} | {variants} | {' · '.join(t.gaps) or '—'} |"
        )
    add("")

    unmapped = sorted({r.label for r in rows} - claimed)
    review = sorted({label for t in resolved for label in t.needs_review})
    missing = sorted({label for t in resolved for label in t.missing})

    if unmapped or review or missing:
        add("## Vocabulary maintenance")
        add("")
        if unmapped:
            add(
                f"**Unmapped tracker rows ({len(unmapped)})** — solved but assigned to no "
                "technique. Add them to `techniques.yml`, or coverage silently drifts behind "
                "the tracker."
            )
            add("")
            for label in unmapped:
                add(f"- {label}")
            add("")
        if review:
            add(
                f"**Method unconfirmed ({len(review)})** — mapped, but the tracker row carries no "
                "method parenthetical, so the variant credited here is an assumption. Confirm and "
                "drop the `review: true` flag."
            )
            add("")
            for label in review:
                add(f"- {label}")
            add("")
        if missing:
            add(
                f"**Declared but not in the tracker ({len(missing)})** — the YAML names a problem "
                "with no matching row. Either it is unsolved, or the method string drifted."
            )
            add("")
            for label in missing:
                add(f"- {label}")
            add("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the report on disk differs from freshly generated output",
    )
    args = parser.parse_args()

    config = yaml.safe_load(TECHNIQUES_YML.read_text(encoding="utf-8"))
    rows = parse_tracker(TRACKER_MD)
    resolved, claimed = resolve(config, rows)
    report = render(resolved, rows, claimed)

    if args.check:
        current = REPORT_MD.read_text(encoding="utf-8") if REPORT_MD.exists() else ""
        if current != report:
            print(f"{REPORT_MD.name} is stale — run: python scripts/technique_coverage.py")
            return 1
        print(f"{REPORT_MD.name} is up to date.")
        return 0

    REPORT_MD.write_text(report, encoding="utf-8")
    unmapped = len({r.label for r in rows} - claimed)
    print(
        f"Wrote {REPORT_MD.relative_to(REPO_ROOT)} — "
        f"{len(resolved)} techniques, {len(rows)} rows, {unmapped} unmapped."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
