"""Unit tests for .claude/hooks/global_layer_canary.py.

Run with: python -m pytest .claude/hooks/tests -q
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import global_layer_canary as canary  # noqa: E402  (import after sys.path setup)
import session_start_memory  # noqa: E402  (import after sys.path setup)

WIRED_SETTINGS = {
    "hooks": {
        "PreToolUse": [{"hooks": [{"type": "command", "command": "python role_gate.py"}]}],
        "UserPromptSubmit": [
            {"hooks": [{"type": "command", "command": "python execution_workflow_reminder.py"}]}
        ],
        "SessionStart": [{"hooks": [{"type": "command", "command": "python dotfiles_sync.py"}]}],
    }
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_full_home(home: Path) -> None:
    """A ~/.claude tree with every required file present and settings.json fully wired."""
    claude_dir = home / ".claude"
    _write(claude_dir / "rules" / "execution-workflow.md", "# rules\n")
    _write(claude_dir / "agents" / "team-lead.md", "# team-lead\n")
    _write(claude_dir / "agents" / "engineer.md", "# engineer\n")
    for hook_file in canary.REQUIRED_HOOK_FILES:
        _write(claude_dir / "hooks" / hook_file, "# hook\n")
    _write(claude_dir / "settings.json", json.dumps(WIRED_SETTINGS))
    (claude_dir / ".git").mkdir(parents=True, exist_ok=True)


def _build_repo_with_hooks_path(repo_root: Path, hooks_path: str = ".githooks") -> None:
    _write(repo_root / ".git" / "config", f"[core]\n\thooksPath = {hooks_path}\n")


class FullyPresentTests(unittest.TestCase):
    def test_canary_lines_empty_when_everything_present(self):
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as repo_dir:
            home, repo = Path(home_dir), Path(repo_dir)
            _build_full_home(home)
            _build_repo_with_hooks_path(repo)
            self.assertEqual(canary.canary_lines(home, repo), ())

    def test_canary_banner_empty_when_everything_present(self):
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as repo_dir:
            home, repo = Path(home_dir), Path(repo_dir)
            _build_full_home(home)
            _build_repo_with_hooks_path(repo)
            self.assertEqual(canary.canary_banner(home, repo), "")


class MissingItemTests(unittest.TestCase):
    def _fresh(self):
        home_dir = tempfile.TemporaryDirectory()
        repo_dir = tempfile.TemporaryDirectory()
        self.addCleanup(home_dir.cleanup)
        self.addCleanup(repo_dir.cleanup)
        home, repo = Path(home_dir.name), Path(repo_dir.name)
        _build_full_home(home)
        _build_repo_with_hooks_path(repo)
        return home, repo

    def test_missing_rule_file(self):
        home, repo = self._fresh()
        (home / ".claude" / "rules" / "execution-workflow.md").unlink()
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("execution-workflow.md", lines[0])

    def test_missing_agent_file(self):
        home, repo = self._fresh()
        (home / ".claude" / "agents" / "team-lead.md").unlink()
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("team-lead.md", lines[0])

    def test_missing_hook_script(self):
        home, repo = self._fresh()
        (home / ".claude" / "hooks" / "dotfiles_sync.py").unlink()
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("dotfiles_sync.py", lines[0])

    def test_missing_dotfiles_checkout(self):
        home, repo = self._fresh()
        (home / ".claude" / ".git").rmdir()
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn(".git", lines[0])

    def test_hooks_path_absent(self):
        home, repo = self._fresh()
        _write(repo / ".git" / "config", "[core]\n\tbare = false\n")
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("core.hooksPath", lines[0])

    def test_hooks_path_wrong_value(self):
        home, repo = self._fresh()
        _build_repo_with_hooks_path(repo, hooks_path=".git/hooks")
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("core.hooksPath", lines[0])

    def test_hooks_path_absolute_windows_style_is_accepted(self):
        home, repo = self._fresh()
        _build_repo_with_hooks_path(repo, hooks_path=r"C:\Users\cnyra\project\.githooks")
        self.assertEqual(canary.canary_lines(home, repo), ())


class SettingsJsonTests(unittest.TestCase):
    def _fresh(self):
        home_dir = tempfile.TemporaryDirectory()
        repo_dir = tempfile.TemporaryDirectory()
        self.addCleanup(home_dir.cleanup)
        self.addCleanup(repo_dir.cleanup)
        home, repo = Path(home_dir.name), Path(repo_dir.name)
        _build_full_home(home)
        _build_repo_with_hooks_path(repo)
        return home, repo

    def test_dotfiles_sync_not_wired(self):
        home, repo = self._fresh()
        settings = json.loads((home / ".claude" / "settings.json").read_text(encoding="utf-8"))
        del settings["hooks"]["SessionStart"]
        _write(home / ".claude" / "settings.json", json.dumps(settings))
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("dotfiles_sync.py", lines[0])
        self.assertIn("SessionStart", lines[0])

    def test_unparsable_settings_json(self):
        home, repo = self._fresh()
        _write(home / ".claude" / "settings.json", "{not json")
        lines = canary.canary_lines(home, repo)
        self.assertEqual(len(lines), 1)
        self.assertIn("unreadable", lines[0])


class BannerTests(unittest.TestCase):
    def test_banner_starts_with_header_when_missing(self):
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as repo_dir:
            home, repo = Path(home_dir), Path(repo_dir)
            # An empty home: nothing present at all.
            banner = canary.canary_banner(home, repo)
            self.assertTrue(banner.startswith("!! GLOBAL LAYER CHECK FAILED"))
            self.assertTrue(banner.endswith("\n\n"))

    def test_banner_is_ascii(self):
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as repo_dir:
            home, repo = Path(home_dir), Path(repo_dir)
            banner = canary.canary_banner(home, repo)
            banner.encode("ascii")  # raises UnicodeEncodeError if any non-ASCII char sneaks in

    def test_emit_passes_an_ascii_banner_through_unchanged(self):
        """session_start_memory.emit must round-trip an ASCII-only canary_banner byte for byte."""
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as repo_dir:
            home, repo = Path(home_dir), Path(repo_dir)
            # An empty home: every check fails, so canary_banner is non-empty and ASCII-only.
            banner = canary.canary_banner(home, repo)
            self.assertNotEqual(banner, "")

            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                session_start_memory.emit(banner)
            raw_stdout = captured.getvalue()

            raw_stdout.encode("ascii")  # raises UnicodeEncodeError if any non-ASCII char sneaks in
            payload = json.loads(raw_stdout)
            self.assertEqual(payload["hookSpecificOutput"]["additionalContext"], banner)


if __name__ == "__main__":
    unittest.main()
