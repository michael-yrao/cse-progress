"""cse-coach first-run setup.

Writes cse.config.yml, projects the milestone curriculum onto real dates
(study_guide roadmap + week-1 schedule), ensures the trackers/logs exist, and
installs the git hook. The conversational intake is the coach's job (the cse-init
skill); this script does the mechanical parts and can also run standalone.

Usage (all flags optional; prompts for anything omitted):
    python scripts/bootstrap.py --name "Alex" --start 2026-07-13 \
        --target competitive --daily-cap 5 --language python --lead dsa

Requires PyYAML (one-time setup only; the daily engine has no dependencies):
    pip install pyyaml
"""
from __future__ import annotations

import argparse
import math
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("bootstrap needs PyYAML for one-time setup: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "curriculum" / "dsa" / "milestone.yml"
DSA_TRACKER = ROOT / "docs/foundations/dsa/mastery/dsa_progress.md"
STUDY_GUIDE = ROOT / "docs/foundations/dsa/study_guide.md"
SCHED_DIR = ROOT / "docs/foundations/dsa/schedules"
CONFIG = ROOT / "cse.config.yml"

TARGETS = ("fintech_interview", "faang_interview", "competitive")


def ask(prompt: str, default: str) -> str:
    val = input(f"{prompt} [{default}]: ").strip()
    return val or default


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--name")
    p.add_argument("--start")
    p.add_argument("--target", choices=TARGETS)
    p.add_argument("--daily-cap", type=int)
    p.add_argument("--language")
    p.add_argument("--lead", choices=["dsa", "system_design", "ai_engineering"])
    p.add_argument("--reach-beyond", type=int, default=1)
    p.add_argument("--non-interactive", action="store_true",
                   help="use defaults for anything not passed (no prompts)")
    return p.parse_args()


def gather(a: argparse.Namespace) -> dict:
    d = {
        "name": a.name or "Learner",
        "start": a.start or date.today().isoformat(),
        "target": a.target or "competitive",
        "daily_cap": a.daily_cap or 5,
        "language": a.language or "python",
        "lead": a.lead or "dsa",
        "reach_beyond": max(1, a.reach_beyond),  # floor enforced — 0 is rejected
    }
    if a.non_interactive:
        return d
    print("\ncse-coach setup — answer all at once (Enter accepts the default):\n")
    d["name"] = a.name or ask("What should I call you?", d["name"])
    d["start"] = a.start or ask("Start date (YYYY-MM-DD)", d["start"])
    d["target"] = a.target or ask(f"Target {TARGETS}", d["target"])
    d["daily_cap"] = a.daily_cap or int(ask("Problems per day (cap)", str(d["daily_cap"])))
    d["language"] = a.language or ask("Solution language", d["language"])
    d["lead"] = a.lead or ask("Which pillar leads (dsa/system_design/ai_engineering)", d["lead"])
    return d


def write_config(d: dict) -> None:
    globs = {"python": '["*.py"]', "java": '["*.java"]', "typescript": '["*.ts"]',
             "cpp": '["*.cpp"]', "go": '["*.go"]'}.get(d["language"], '["*.py"]')
    CONFIG.write_text(
        f'learner: "{d["name"]}"\n'
        f'start_date: {d["start"]}\n'
        f'target: {d["target"]}\n'
        f'reach_beyond: {d["reach_beyond"]}   # MIN 1 — reaching past the target is non-negotiable\n'
        f'daily_cap: {d["daily_cap"]}\n\n'
        f'pillars:\n  priority: [{d["lead"]}, ' +
        ", ".join(p for p in ["dsa", "system_design", "ai_engineering"] if p != d["lead"]) + "]\n\n"
        "intervals:\n  clean:  { streak1: 30, streak2: 60, retired: 180 }\n"
        "  shaky:  10\n  blank:  2\nretire_at_streak: 3\n\n"
        f'solutions:\n  roots: ["dsa/leetcode"]\n  globs: {globs}\n'
        '  filename_pattern: "{number}_{name}"\n',
        encoding="utf-8",
    )


def project_roadmap(start: date) -> list[dict]:
    data = yaml.safe_load(MILESTONE.read_text(encoding="utf-8"))
    rows, cursor = [], start
    for phase in data["phases"]:
        n = len(phase["problems"])
        pace = phase.get("pace_per_week", data.get("default_pace_per_week", 5))
        weeks = max(1, math.ceil(n / pace))
        end = cursor + timedelta(weeks=weeks) - timedelta(days=1)
        rows.append({"name": phase["name"], "start": cursor, "end": end,
                     "count": n, "pace": pace, "problems": phase["problems"]})
        cursor = end + timedelta(days=1)
    return rows


def write_study_guide(d: dict, roadmap: list[dict]) -> None:
    lines = [
        "# DSA Study Guide — projected roadmap",
        "",
        f'For **{d["name"]}**, starting **{d["start"]}**. Target: **{d["target"]}** '
        f'(reach_beyond {d["reach_beyond"]}). See [PHILOSOPHY](../../PHILOSOPHY.md) for the '
        "why (Interview-ROI line, comfort system, reach-beyond).",
        "",
        "> Dates are a plan, not a deadline. The spaced-repetition tracker is the source",
        "> of truth; the weekly schedules reflect it. Phases complete when every problem",
        "> is 🏆 Retired — not when attempted once.",
        "",
        "| Phase | Dates | New problems | Pace/wk |",
        "|-------|-------|--------------|---------|",
    ]
    for r in roadmap:
        lines.append(f'| {r["name"]} | {r["start"]:%Y-%m-%d} → {r["end"]:%Y-%m-%d} '
                     f'| {r["count"]} | {r["pace"]} |')
    lines += ["", "After the milestone: expansion Tier 1 (above the ROI line), then Tier 2 "
              "for competitive depth — see `../../../curriculum/`.", ""]
    STUDY_GUIDE.write_text("\n".join(lines), encoding="utf-8")


def write_week1(d: dict, roadmap: list[dict]) -> Path:
    start = datetime.strptime(d["start"], "%Y-%m-%d").date()
    monday = start - timedelta(days=start.weekday())
    problems = roadmap[0]["problems"][:6]  # first phase feeds week 1 active blocks
    sched = SCHED_DIR / f"{monday:%Y%m%d}_schedule.md"
    rows = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        dt = monday + timedelta(days=i)
        if day == "Sun":
            active = "System Design sprint (Bootstrap: watch → sketch)"
        elif i < len(problems):
            pr = problems[i]
            active = f'{pr["number"]}. {pr["title"]} (new)'
        else:
            active = "—"
        rows.append(f'| {day} {dt:%Y-%m-%d} | — | {active} | ☐ |')
    sched.write_text(
        f"# Week of {monday:%Y-%m-%d} — Schedule\n\n"
        f'Learner: {d["name"]} · Daily cap: {d["daily_cap"]} · Lead pillar: {d["lead"]}.\n'
        "Active block is protected — trim warmups first if over cap.\n\n"
        "| Day | Warmup (15m) | Active block (45m) | Status |\n"
        "|-----|--------------|--------------------|--------|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    return sched


def install_hook() -> None:
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"],
                       cwd=ROOT, check=True, capture_output=True)
    except Exception as e:  # pragma: no cover
        print(f"  (could not set core.hooksPath automatically: {e})")


def main() -> None:
    d = gather(parse_args())
    write_config(d)
    roadmap = project_roadmap(datetime.strptime(d["start"], "%Y-%m-%d").date())
    write_study_guide(d, roadmap)
    sched = write_week1(d, roadmap)
    install_hook()

    first = roadmap[0]["problems"][0]
    print(f"\n  You're set, {d['name']}. Wrote cse.config.yml, your roadmap, and week 1.")
    print(f"  Hook installed. First up: {first['number']}. {first['title']}.")
    print(f"  Schedule: {sched.relative_to(ROOT)}")
    print("  When you finish a problem, just tell the coach: Clean, Shaky, or Blank.\n")


if __name__ == "__main__":
    main()
