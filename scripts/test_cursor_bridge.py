"""Tests for scripts/hooks/cursor_bridge.py — the Cursor hook bridge.

See docs/cse-coach/AGENT_PORTABILITY_PLAN.md §6 brief E4. `cursor_bridge.py` lives under
`scripts/hooks/`, and the two Stop hooks it fronts live under `.claude/hooks/` — neither is
an importable package, so both are loaded by file path via `importlib`, the same pattern
`scripts/test_rating_gate.py` uses for a hook script.

Every test points `CSE_COACH_CURSOR_TMPDIR` at pytest's `tmp_path`, so no test run ever
touches the real machine temp dir the bridge uses outside of tests. The Stop-hook tests run
the real, unmodified `problem_link_reminder.py` / `rating_gate.py` as subprocesses against a
bridge-written shadow transcript — the same thing `handle_stop` does in production — rather
than mocking them, since the shape of the shadow transcript is the fact under test.

    python -m pytest scripts/test_cursor_bridge.py
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
BRIDGE_PATH = REPO / "scripts" / "hooks" / "cursor_bridge.py"
PROBLEM_LINK_PATH = REPO / ".claude" / "hooks" / "problem_link_reminder.py"
RATING_GATE_PATH = REPO / ".claude" / "hooks" / "rating_gate.py"

CONVERSATION_ID = "conv-test-1"


def _load(name: str, path: Path):
    """Import a hook/bridge script by file path — none of them are packages."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cursor_bridge = _load("cursor_bridge", BRIDGE_PATH)
problem_link_reminder = _load("problem_link_reminder", PROBLEM_LINK_PATH)
rating_gate = _load("rating_gate", RATING_GATE_PATH)


@pytest.fixture(autouse=True)
def shadow_tmpdir(tmp_path, monkeypatch):
    """Point the bridge's shadow-transcript directory at pytest's tmp_path."""
    monkeypatch.setenv(cursor_bridge.SHADOW_TMPDIR_ENV, str(tmp_path))
    return tmp_path


def _shadow_file(conversation_id: str = CONVERSATION_ID) -> Path:
    return cursor_bridge.shadow_transcript_path(conversation_id)


def _transcript_entries(conversation_id: str = CONVERSATION_ID) -> list[dict]:
    lines = _shadow_file(conversation_id).read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_before_submit_prompt_appends_a_real_user_turn():
    result = cursor_bridge.handle_before_submit_prompt(
        {"conversation_id": CONVERSATION_ID, "prompt": "time is O(n), space is O(1)"}
    )
    assert result == {"continue": True}

    entries = _transcript_entries()
    assert len(entries) == 1
    assert problem_link_reminder._is_real_user_message(entries[0])


def test_after_agent_response_appends_an_assistant_turn():
    result = cursor_bridge.handle_after_agent_response(
        {"conversation_id": CONVERSATION_ID, "text": "Nice, the BFS looks correct."}
    )
    assert result == {}

    entries = _transcript_entries()
    assert len(entries) == 1
    assert entries[0]["type"] == "assistant"
    assert entries[0]["message"]["content"][0]["text"] == "Nice, the BFS looks correct."


def test_shadow_transcript_is_read_correctly_by_both_stop_hooks():
    """The shape the bridge writes is the shape both Stop-hook parsers expect, unchanged."""
    cursor_bridge.handle_before_submit_prompt(
        {"conversation_id": CONVERSATION_ID, "prompt": "yeah I think that's done"}
    )
    cursor_bridge.handle_after_agent_response(
        {"conversation_id": CONVERSATION_ID, "text": "Looks right. Nice work."}
    )

    transcript_path = str(_shadow_file())
    assert problem_link_reminder.last_turn_text(transcript_path) == "Looks right. Nice work."

    entries = rating_gate._entries(transcript_path)
    assert rating_gate.last_turn_text(entries) == "Looks right. Nice work."
    assert rating_gate.learner_text(entries) == "yeah I think that's done"


def test_stop_blocks_exactly_once_on_a_rating_with_no_complexity():
    cursor_bridge.handle_before_submit_prompt(
        {"conversation_id": CONVERSATION_ID, "prompt": "yeah I think that solution is done and correct"}
    )
    cursor_bridge.handle_after_agent_response(
        {"conversation_id": CONVERSATION_ID, "text": "That reads as \U0001F7E1 Shaky — confirm?"}
    )

    result = cursor_bridge.handle_stop(
        {"conversation_id": CONVERSATION_ID, "status": "completed", "loop_count": 0}
    )
    assert set(result.keys()) == {"followup_message"}
    assert "TIME" in result["followup_message"]
    assert "SPACE" in result["followup_message"]


def test_stop_yields_empty_object_on_a_clean_turn():
    cursor_bridge.handle_before_submit_prompt({"conversation_id": CONVERSATION_ID, "prompt": "sounds good"})
    cursor_bridge.handle_after_agent_response(
        {"conversation_id": CONVERSATION_ID, "text": "Nice, the BFS looks correct and clean."}
    )

    result = cursor_bridge.handle_stop(
        {"conversation_id": CONVERSATION_ID, "status": "completed", "loop_count": 0}
    )
    assert result == {}


def test_session_start_maps_additional_context(monkeypatch):
    monkeypatch.setattr(
        cursor_bridge,
        "run_hook_script",
        lambda script_name, payload: {"hookSpecificOutput": {"additionalContext": "gates go here"}},
    )
    assert cursor_bridge.handle_session_start({}) == {"additional_context": "gates go here"}


def test_session_start_with_no_context_yields_empty_object(monkeypatch):
    monkeypatch.setattr(cursor_bridge, "run_hook_script", lambda script_name, payload: {})
    assert cursor_bridge.handle_session_start({}) == {}


def test_post_tool_use_maps_tool_fields_and_additional_context(monkeypatch):
    seen_payload = {}

    def fake_run_hook_script(script_name, payload):
        seen_payload.update(payload)
        return {"hookSpecificOutput": {"additionalContext": "link reminder"}}

    monkeypatch.setattr(cursor_bridge, "run_hook_script", fake_run_hook_script)
    result = cursor_bridge.handle_post_tool_use(
        {"tool_name": "runTerminalCmd", "tool_input": {"command": "python scripts/new_problem.py --number 1"}}
    )
    assert result == {"additional_context": "link reminder"}
    assert seen_payload == {
        "tool_name": "runTerminalCmd",
        "tool_input": {"command": "python scripts/new_problem.py --number 1"},
    }


def test_malformed_stdin_is_a_no_op(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cursor_bridge.py", "beforeSubmitPrompt"])
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    cursor_bridge.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "{}"
    assert "cursor_bridge" in captured.err


def test_unknown_event_is_a_no_op(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cursor_bridge.py", "notARealEvent"])
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))
    cursor_bridge.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "{}"
    assert "unknown event" in captured.err


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
