"""Cursor hook bridge — runs cse-coach's Claude Code hooks unchanged under Cursor.

Cursor's hook events do not match Claude Code's shape (plan `docs/cse-coach/AGENT_PORTABILITY_PLAN.md`
§1, §6 brief E4): `stop` carries no transcript in Claude's shape, and `beforeSubmitPrompt` cannot inject
context. So this bridge keeps its own *shadow transcript* — one JSONL file per Cursor
conversation, written in Claude's transcript shape — by appending a user entry on every
`beforeSubmitPrompt` and an assistant entry on every `afterAgentResponse`. At `stop` it hands
that shadow file to the unmodified Stop hooks (`problem_link_reminder.py`, `rating_gate.py`)
exactly as Claude Code would, and turns a `decision: block` into Cursor's `followup_message`.

Entry point: `python scripts/hooks/cursor_bridge.py <cursorEvent>`, reading Cursor's stdin
JSON and writing the mapped output JSON to stdout. A bridge failure must never block the
person's turn — every event handler runs inside a `try` in `main()` that falls back to a
no-op `{}` output and a stderr note, and stdin that is not valid JSON does the same.

Hook scripts are invoked with `sys.executable` and an absolute path resolved from this
file's own location, and are never edited — see `run_hook_script`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BRIDGE_FILE = Path(__file__).resolve()
REPO_ROOT = BRIDGE_FILE.parents[2]
HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"

# The four Claude Code hooks this bridge fronts. `kickoff_scaffold_reminder.py` is
# deliberately absent — a `UserPromptSubmit` reminder needs to inject context into the
# NEXT turn, and Cursor's `beforeSubmitPrompt` cannot inject context at all (plan §6 E4).
PROBLEM_LINK_HOOK = "problem_link_reminder.py"
RATING_GATE_HOOK = "rating_gate.py"
SESSION_START_HOOK = "session_start_memory.py"
SCAFFOLD_LINKS_HOOK = "scaffold_links_reminder.py"

HOOK_SUBPROCESS_TIMEOUT_SECONDS = 10

# Overridable so tests never touch the real machine temp dir (per brief: point this at
# `tmp_path` via an env var the bridge honors).
SHADOW_TMPDIR_ENV = "CSE_COACH_CURSOR_TMPDIR"
SHADOW_DIR_NAME = "cse-coach-cursor"
UNKNOWN_CONVERSATION_ID = "unknown-session"


def _shadow_base_dir() -> Path:
    """Directory holding one shadow transcript per Cursor conversation."""
    override = os.environ.get(SHADOW_TMPDIR_ENV)
    base = Path(override) if override else Path(tempfile.gettempdir())
    return base / SHADOW_DIR_NAME


def shadow_transcript_path(conversation_id: str) -> Path:
    """The shadow JSONL file for one Cursor conversation, keyed by its id."""
    safe_id = "".join(c for c in conversation_id if c.isalnum() or c in "-_") or UNKNOWN_CONVERSATION_ID
    return _shadow_base_dir() / f"{safe_id}.jsonl"


def _turn_entry(role: str, text: str) -> dict:
    """One transcript line in Claude's shape: a `type`/`message.content[].text` record.

    `problem_link_reminder.py` and `rating_gate.py` tell a real user turn from a
    `tool_result` carrier by checking `type == "user"` and that `content` holds no
    `tool_result` block (see their `_is_real_user_message`), and they read assistant
    text from `content` blocks whose `type == "text"`. A plain user/assistant text
    entry, with no `tool_result` block and no `isSidechain` key, satisfies both readers
    unchanged.
    """
    return {"type": role, "message": {"role": role, "content": [{"type": "text", "text": text}]}}


def append_shadow_entry(conversation_id: str, entry: dict) -> None:
    """Append one transcript line, creating the shadow directory on first use."""
    path = shadow_transcript_path(conversation_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as transcript_file:
        transcript_file.write(json.dumps(entry) + "\n")


def run_hook_script(script_name: str, stdin_payload: dict) -> dict:
    """Run one unmodified Claude Code hook as a subprocess and parse its JSON stdout.

    Empty stdout (the common case — most hooks stay silent) and unparseable stdout both
    map to `{}`, the same "nothing to report" shape the caller treats as a no-op.
    """
    script_path = HOOKS_DIR / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(stdin_payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        timeout=HOOK_SUBPROCESS_TIMEOUT_SECONDS,
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return {}
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        print(f"cursor_bridge: {script_name} emitted non-JSON stdout: {exc}", file=sys.stderr)
        return {}


def _additional_context_output(hook_result: dict) -> dict:
    """Map a Claude `hookSpecificOutput.additionalContext` result to Cursor's field name."""
    context = (hook_result.get("hookSpecificOutput") or {}).get("additionalContext", "")
    return {"additional_context": context} if context else {}


def handle_before_submit_prompt(payload: dict) -> dict:
    """Record the learner's prompt as a shadow user turn. Cannot inject context (§1)."""
    conversation_id = payload.get("conversation_id", "")
    prompt = payload.get("prompt", "") or ""
    append_shadow_entry(conversation_id, _turn_entry("user", prompt))
    return {"continue": True}


def handle_after_agent_response(payload: dict) -> dict:
    """Record the agent's reply as a shadow assistant turn. Observe-only (§1)."""
    conversation_id = payload.get("conversation_id", "")
    text = payload.get("text", "") or ""
    append_shadow_entry(conversation_id, _turn_entry("assistant", text))
    return {}


def handle_stop(payload: dict) -> dict:
    """Run the two Stop gates against the shadow transcript; the first block wins.

    `stop_hook_active` is always `False` — Cursor has no equivalent re-send flag, and
    `loop_limit: 1` in `.cursor/hooks.json` is what stops a `followup_message` from
    looping more than once.
    """
    conversation_id = payload.get("conversation_id", "")
    claude_stop_payload = {
        "transcript_path": str(shadow_transcript_path(conversation_id)),
        "stop_hook_active": False,
    }
    for hook_name in (PROBLEM_LINK_HOOK, RATING_GATE_HOOK):
        result = run_hook_script(hook_name, claude_stop_payload)
        if result.get("decision") == "block":
            return {"followup_message": result.get("reason", "")}
    return {}


def handle_session_start(payload: dict) -> dict:
    """`session_start_memory.py` reads no stdin fields, so it runs with an empty payload."""
    return _additional_context_output(run_hook_script(SESSION_START_HOOK, {}))


def handle_post_tool_use(payload: dict) -> dict:
    """Map Cursor's tool fields to Claude's and run the scaffold-links reminder."""
    claude_payload = {
        "tool_name": payload.get("tool_name", ""),
        "tool_input": payload.get("tool_input") or {},
    }
    return _additional_context_output(run_hook_script(SCAFFOLD_LINKS_HOOK, claude_payload))


EVENT_HANDLERS = {
    "beforeSubmitPrompt": handle_before_submit_prompt,
    "afterAgentResponse": handle_after_agent_response,
    "stop": handle_stop,
    "sessionStart": handle_session_start,
    "postToolUse": handle_post_tool_use,
}


def _read_stdin_json() -> dict:
    raw = sys.stdin.read()
    return json.loads(raw) if raw.strip() else {}


def main() -> None:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    handler = EVENT_HANDLERS.get(event)
    output: dict = {}
    if handler is None:
        print(f"cursor_bridge: unknown event {event!r}", file=sys.stderr)
    else:
        try:
            output = handler(_read_stdin_json())
        except Exception as exc:  # noqa: BLE001 — a bridge failure must never block the turn
            print(f"cursor_bridge: {event} failed: {exc.__class__.__name__}: {exc}", file=sys.stderr)
            output = {}
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
