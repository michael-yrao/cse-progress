"""Tests for reconcile.py's `metadata.reconciled` frontmatter support.

Pytest with `tmp_path` (not stdlib unittest, unlike this repo's other `scripts/test_*.py`
files): `reconciled_date`/`stamp` are pure file-in, file/value-out functions over a tiny
fixture, and `tmp_path` is the cheapest way to give each case its own throwaway file
without touching a real rule file. Collected the same way as every other `scripts/test_*.py`:

    python -m pytest scripts/test_reconcile.py

Frontmatter went spec-shaped on SKILL.md (agentskills.io puts `reconciled` under
`metadata:`, not at the top level) — see docs/cse-coach/AGENT_PORTABILITY_PLAN.md D1. D1 is
scoped to the skill: the ~60 memory files keep their own top-level `reconciled:` frontmatter
untouched. These tests pin the shapes reconcile.py must round-trip: SKILL.md's flow-style
`metadata: {reconciled: "..."}`, an equivalent block-style mapping, and the ordinary
top-level `reconciled:` every other rule file uses — each stamped IN PLACE, in whatever
shape it already has, never converted to another file's shape.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reconcile

TODAY = dt.date(2026, 9, 23)


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_reads_flow_style_metadata(tmp_path):
    p = _write(tmp_path / "flow.md", '---\nname: x\nmetadata: {reconciled: "2026-09-20"}\n---\nbody\n')
    assert reconcile.reconciled_date(p) == dt.date(2026, 9, 20)


def test_reads_block_style_metadata(tmp_path):
    p = _write(
        tmp_path / "block.md",
        '---\nname: x\nmetadata:\n  reconciled: "2026-09-20"\n---\nbody\n',
    )
    assert reconcile.reconciled_date(p) == dt.date(2026, 9, 20)


def test_reads_legacy_top_level_field_as_fallback(tmp_path):
    p = _write(tmp_path / "legacy.md", "---\nname: x\nreconciled: 2026-09-20\n---\nbody\n")
    assert reconcile.reconciled_date(p) == dt.date(2026, 9, 20)


def test_metadata_wins_over_a_stray_top_level_field(tmp_path):
    # Shouldn't occur in practice (a file has one or the other), but if both are ever
    # present, the spec-shaped key governs the read.
    p = _write(
        tmp_path / "both.md",
        '---\nname: x\nreconciled: 2026-01-01\nmetadata: {reconciled: "2026-09-20"}\n---\nbody\n',
    )
    assert reconcile.reconciled_date(p) == dt.date(2026, 9, 20)


def test_stamp_updates_flow_style_in_place(tmp_path):
    p = _write(tmp_path / "flow.md", '---\nname: x\nmetadata: {reconciled: "2026-09-01"}\n---\nbody\n')
    assert reconcile.stamp(p, TODAY) is True
    assert 'metadata: {reconciled: "2026-09-23"}' in p.read_text(encoding="utf-8")
    assert reconcile.reconciled_date(p) == TODAY


def test_stamp_updates_block_style_in_place(tmp_path):
    p = _write(
        tmp_path / "block.md",
        '---\nname: x\nmetadata:\n  reconciled: "2026-09-01"\n---\nbody\n',
    )
    assert reconcile.stamp(p, TODAY) is True
    text = p.read_text(encoding="utf-8")
    assert "metadata:\n  reconciled: \"2026-09-23\"" in text
    assert reconcile.reconciled_date(p) == TODAY


def test_stamp_updates_legacy_top_level_field_in_place(tmp_path):
    # D1 is skill-scoped: a memory file's existing top-level `reconciled:` is refreshed
    # where it sits, never migrated into `metadata:` — see the review note in reconcile.py.
    p = _write(tmp_path / "legacy.md", "---\nname: x\nreconciled: 2026-09-01\n---\nbody\n")
    assert reconcile.stamp(p, TODAY) is True
    text = p.read_text(encoding="utf-8")
    assert "reconciled: 2026-09-23" in text
    assert "metadata:" not in text
    assert reconcile.reconciled_date(p) == TODAY


def test_stamp_creates_metadata_when_absent_on_skill_md(tmp_path):
    # SKILL.md is the one file D1 puts under `metadata:` — matched by filename, not path.
    p = _write(tmp_path / "SKILL.md", "---\nname: x\n---\nbody\n")
    assert reconcile.stamp(p, TODAY) is True
    assert 'metadata: {reconciled: "2026-09-23"}' in p.read_text(encoding="utf-8")
    assert reconcile.reconciled_date(p) == TODAY


def test_stamp_creates_top_level_when_absent_on_a_non_skill_file(tmp_path):
    p = _write(tmp_path / "some_reference.md", "---\nname: x\n---\nbody\n")
    assert reconcile.stamp(p, TODAY) is True
    text = p.read_text(encoding="utf-8")
    assert "reconciled: 2026-09-23" in text
    assert "metadata:" not in text
    assert reconcile.reconciled_date(p) == TODAY


def test_stamp_is_a_noop_when_already_current(tmp_path):
    p = _write(tmp_path / "flow.md", f'---\nname: x\nmetadata: {{reconciled: "{TODAY}"}}\n---\nbody\n')
    assert reconcile.stamp(p, TODAY) is False


def test_comment_marker_path_for_non_frontmatter_files_is_unchanged(tmp_path):
    p = _write(tmp_path / "AGENTS.md", "# AGENTS.md\n\n<!-- reconciled: 2026-09-01 -->\nbody\n")
    assert reconcile.reconciled_date(p) == dt.date(2026, 9, 1)
    assert reconcile.stamp(p, TODAY) is True
    assert "<!-- reconciled: 2026-09-23 -->" in p.read_text(encoding="utf-8")
