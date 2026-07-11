"""Behavior + config tests for update_review_dates.py.

Runnable two ways:
    python tests/test_engine.py          # plain asserts, no pytest needed
    pytest tests/test_engine.py

Covers: (1) intervals reproduce cse-review's defaults, (2) config overrides are
read, (3) the source-file regex is language-agnostic, (4) an end-to-end run
reorders the tracker by latest date and recomputes next-review dates.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_review_dates.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("ur", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_intervals_match_defaults():
    m = _load_module()
    base = datetime(2026, 1, 1)
    days = lambda d: (d - base).days
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 1)) == 30
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 2)) == 60
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 3)) == 180
    assert days(m.compute_next_review_date(m.COMFORT_RETIRED, base, 3)) == 180
    assert days(m.compute_next_review_date(m.COMFORT_SHAKY, base, 0)) == 10
    assert days(m.compute_next_review_date(m.COMFORT_BLANK, base, 0)) == 2
    assert m.compute_next_review_date(m.COMFORT_CLEAN, None, 1) is None


def test_load_config_overrides(tmp_path: Path):
    m = _load_module()
    cfg_file = tmp_path / "cse.config.yml"
    cfg_file.write_text(
        "intervals:\n"
        "  clean:  { streak1: 45, streak2: 90, retired: 200 }\n"
        "  shaky:  7\n"
        "  blank:  1\n"
        "retire_at_streak: 4\n"
        "solutions:\n"
        '  roots: ["problems/lc"]\n'
        '  globs: ["*.java", "*.py"]\n',
        encoding="utf-8",
    )
    cfg = m.load_config(cfg_file)
    assert cfg["clean_streak1"] == 45
    assert cfg["clean_streak2"] == 90
    assert cfg["retired"] == 200
    assert cfg["shaky"] == 7
    assert cfg["blank"] == 1
    assert cfg["retire_at_streak"] == 4
    assert cfg["source_root"] == "problems/lc"
    assert cfg["source_globs"] == ["*.java", "*.py"]


def test_source_regex_language_agnostic():
    m = _load_module()
    assert m.SOURCE_FILE_RE.match("1_two_sum.py")
    # default config is python-only, so .java should not match
    assert not m.SOURCE_FILE_RE.match("1_two_sum.java")


TRACKER = "docs/foundations/dsa/mastery/dsa_progress.md"

FIXTURE = """# DSA Progress

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | \U0001f7e2 | 1 | | 2026-01-10 | 2026-01-10 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | \U0001f534 | 0 | | 2026-02-01 | 2026-02-01 |
"""


def test_end_to_end_reorder_and_recompute(tmp_path: Path):
    repo = tmp_path / "repo"
    (repo / "docs/foundations/dsa/mastery").mkdir(parents=True)
    (repo / "dsa/leetcode").mkdir(parents=True)
    (repo / TRACKER).write_text(FIXTURE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

    out = (repo / TRACKER).read_text(encoding="utf-8")
    rows = [ln for ln in out.splitlines() if ln.startswith("| ") and "leetcode.com" in ln]
    # Sorted by latest attempt date descending → 3Sum (Feb) before Two Sum (Jan)
    assert "3Sum" in rows[0] and "Two Sum" in rows[1]
    # Clean streak-1 Two Sum: +30 from 2026-01-10 = 2026-02-09
    assert "2026-02-09" in rows[1]
    # Blank 3Sum: +2 from 2026-02-01 = 2026-02-03
    assert "2026-02-03" in rows[0]


SD_FIXTURE = """# System Design Progress

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Tier 1 | [URL Shortener](../case_studies/url_shortener.md) | \U0001f7e2 | 1 | | 2026-01-10 | 2026-01-10 |
| Tier 1 | [Rate Limiter](../components/rate_limiter.md) | \U0001f534 | 0 | | 2026-02-01 | 2026-02-01 |
"""


def test_recompute_simple_no_discovery(tmp_path: Path):
    m = _load_module()
    tracker = tmp_path / "design_progress.md"
    tracker.write_text(SD_FIXTURE, encoding="utf-8")
    m.recompute_simple(tracker)
    out = tracker.read_text(encoding="utf-8")
    rows = [ln for ln in out.splitlines() if ln.startswith("| ") and "](" in ln and "Comfort" not in ln]
    # Sorted by latest date desc → Rate Limiter (Feb) before URL Shortener (Jan)
    assert "Rate Limiter" in rows[0] and "URL Shortener" in rows[1]
    assert "2026-02-09" in rows[1]  # Clean streak-1 URL Shortener: +30
    assert "2026-02-03" in rows[0]  # Blank Rate Limiter: +2
    # No source discovery: exactly the two systems, nothing injected
    assert len(rows) == 2


def _run_all():
    import tempfile

    test_intervals_match_defaults()
    test_source_regex_language_agnostic()
    with tempfile.TemporaryDirectory() as d:
        test_load_config_overrides(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_end_to_end_reorder_and_recompute(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_recompute_simple_no_discovery(Path(d))
    print("All engine tests passed.")


if __name__ == "__main__":
    _run_all()
