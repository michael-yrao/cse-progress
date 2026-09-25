"""Pure check: is this machine's global Claude Code layer (~/.claude) actually present?

Why this exists
----------------
The execution-workflow pyramid (tech lead / team lead / engineer) is enforced by files that
live OUTSIDE this repo, in the dotfiles checkout at ~/.claude: rules/, agents/, hooks/, and the
settings.json that wires the hooks in. `~/.claude/hooks/dotfiles_sync.py` converges that
checkout once it exists, but nothing detects a machine where it never existed in the first
place, or existed and lost a piece. The Mac ran for days with no enforcement layer at all and
nothing said so, because the SessionStart hook that would have said so lives in the very
checkout that was missing. This repo's own SessionStart hook (`session_start_memory.py`)
always runs, so the canary is wired here instead — a project-repo check standing in for a
global-repo hook that can't check itself into existence.

What this checks, in order
---------------------------
1. `~/.claude/rules/execution-workflow.md` exists.
2. `~/.claude/agents/team-lead.md` and `agents/engineer.md` exist.
3. `~/.claude/hooks/role_gate.py`, `execution_workflow_reminder.py`, `dotfiles_sync.py` exist.
4. `~/.claude/settings.json` parses as JSON and wires each of those three hooks under its
   expected event (role_gate.py -> PreToolUse, execution_workflow_reminder.py ->
   UserPromptSubmit, dotfiles_sync.py -> SessionStart). "Wires" means some entry's
   `hooks[].command` string contains the script's filename.
5. `~/.claude/.git` exists (the dotfiles checkout, as opposed to a hand-copied tree that will
   never sync).
6. This repo's `core.hooksPath` is `.githooks` (read from `.git/config` directly — no
   subprocess, since this module must stay import-only and side-effect-free).

Enforced vs. convention: this module only ever REPORTS what it finds; it never edits, fetches,
or repairs anything (no subprocess, no network, no writes). The repair step named in every line
is convention — a person or agent still has to run it. `canary_banner` is what turns the check
into something a session actually sees; wiring it into `session_start_memory.py` (so it fires
unprompted) is convention too, in the sense that nothing stops a future edit from dropping that
one line — there is no hook-on-a-hook.

Every line is plain ASCII (no emoji, no em dash) — the caller's stdout may be cp1252 on
Windows, and a non-ASCII character here would recreate the exact "session starts with no rules
loaded" failure this canary exists to catch.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RESTORE_RECIPE = (
    "Restore the dotfiles repo: git clone https://github.com/michael-yrao/claude-dotfiles.git "
    "<tmp> && python <tmp>/bootstrap.py --repos-dir <dir holding this repo> "
    "(details in .claude/memory/project_global_claude_unversioned.md)."
)

REQUIRED_AGENT_FILES = ("team-lead.md", "engineer.md")
REQUIRED_HOOK_FILES = ("role_gate.py", "execution_workflow_reminder.py", "dotfiles_sync.py")

# Each hook script's expected event under settings.json's `hooks` object.
REQUIRED_HOOK_WIRING = (
    ("role_gate.py", "PreToolUse"),
    ("execution_workflow_reminder.py", "UserPromptSubmit"),
    ("dotfiles_sync.py", "SessionStart"),
)

HOOKS_PATH_MISSING_LINE = (
    "GLOBAL LAYER MISSING: core.hooksPath is not .githooks in this repo. "
    "Run: git config core.hooksPath .githooks"
)

BANNER_HEADER = (
    "!! GLOBAL LAYER CHECK FAILED - the execution-workflow enforcement (rules/agents/hooks) is "
    "not fully present on this machine. Nothing below this line from ~/.claude/rules is in "
    "force until fixed."
)

_SECTION_PATTERN = re.compile(r"^\[([^\]]+)\]\s*$", re.MULTILINE)
_HOOKS_PATH_PATTERN = re.compile(r"^\s*hooksPath\s*=\s*(.+?)\s*$", re.MULTILINE)


def _missing_file_line(path_label: str) -> str:
    """A `GLOBAL LAYER MISSING` line for one absent file, with the standard fix sentence."""
    return f"GLOBAL LAYER MISSING: {path_label} not found. {RESTORE_RECIPE}"


def _missing_file_lines(claude_dir: Path) -> tuple[str, ...]:
    """Checks 1-3: the rule file, the two agent files, the three hook scripts."""
    lines: list[str] = []
    if not (claude_dir / "rules" / "execution-workflow.md").exists():
        lines.append(_missing_file_line("~/.claude/rules/execution-workflow.md"))
    for agent_file in REQUIRED_AGENT_FILES:
        if not (claude_dir / "agents" / agent_file).exists():
            lines.append(_missing_file_line(f"~/.claude/agents/{agent_file}"))
    for hook_file in REQUIRED_HOOK_FILES:
        if not (claude_dir / "hooks" / hook_file).exists():
            lines.append(_missing_file_line(f"~/.claude/hooks/{hook_file}"))
    return tuple(lines)


def _is_wired(hooks: object, event: str, script_name: str) -> bool:
    """True when some `hooks[event][*].hooks[*].command` contains `script_name`."""
    entries = hooks.get(event, []) if isinstance(hooks, dict) else []
    if not isinstance(entries, list):
        return False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        inner_hooks = entry.get("hooks")
        if not isinstance(inner_hooks, list):
            continue
        for hook in inner_hooks:
            command = hook.get("command") if isinstance(hook, dict) else None
            if script_name in str(command or ""):
                return True
    return False


def _settings_lines(settings_path: Path) -> tuple[str, ...]:
    """Check 4: settings.json parses, and wires each required hook under its event."""
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - any read/parse failure is the same report
        return (f"GLOBAL LAYER MISSING: ~/.claude/settings.json unreadable ({exc.__class__.__name__})",)
    hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
    lines = [
        f"GLOBAL LAYER MISSING: ~/.claude/settings.json does not wire hooks/{script_name} "
        f"under {event}. {RESTORE_RECIPE}"
        for script_name, event in REQUIRED_HOOK_WIRING
        if not _is_wired(hooks, event, script_name)
    ]
    return tuple(lines)


def _read_hooks_path(git_config_text: str) -> "str | None":
    """The value of `hooksPath` inside the `[core]` section of a `.git/config` text, if any."""
    sections = list(_SECTION_PATTERN.finditer(git_config_text))
    for index, section in enumerate(sections):
        if section.group(1).strip() != "core":
            continue
        start = section.end()
        end = sections[index + 1].start() if index + 1 < len(sections) else len(git_config_text)
        match = _HOOKS_PATH_PATTERN.search(git_config_text[start:end])
        if match:
            return match.group(1).strip()
    return None


def _hooks_path_line(repo_root: Path) -> "str | None":
    """Check 6: this repo's `core.hooksPath` is `.githooks`, read straight from `.git/config`."""
    config_path = repo_root / ".git" / "config"
    try:
        text = config_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - any read failure is the same report
        return f"GLOBAL LAYER MISSING: cannot read .git/config ({exc.__class__.__name__})"
    hooks_path = _read_hooks_path(text)
    if hooks_path is None:
        return HOOKS_PATH_MISSING_LINE
    normalized = hooks_path.replace("\\", "/").strip().strip('"')
    return None if normalized.endswith(".githooks") else HOOKS_PATH_MISSING_LINE


def canary_lines(home: Path, repo_root: Path) -> tuple[str, ...]:
    """Zero lines when the global layer is fully present, else one line per missing item."""
    claude_dir = home / ".claude"
    lines: list[str] = list(_missing_file_lines(claude_dir))
    lines.extend(_settings_lines(claude_dir / "settings.json"))
    if not (claude_dir / ".git").exists():
        lines.append(_missing_file_line("~/.claude/.git"))
    hooks_path_line = _hooks_path_line(repo_root)
    if hooks_path_line is not None:
        lines.append(hooks_path_line)
    return tuple(lines)


def canary_banner(home: Path, repo_root: Path) -> str:
    """'' when the global layer is fully present, else a loud multi-line block naming why."""
    lines = canary_lines(home, repo_root)
    if not lines:
        return ""
    return BANNER_HEADER + "\n" + "\n".join(lines) + "\n\n"
