"""Stop hook: block a turn that PROPOSES a comfort rating before the learner has
stated BOTH time and space complexity themselves.

The complexity gate (CLAUDE.md LeetCode Review Workflow step 1; `feedback_ask_complexity`)
requires the learner to volunteer **time AND space, each with a why-clause, BEFORE any
rating is proposed**. It kept being run backwards — the rating proposed first, the gate
treated as a formality:
  - 2026-08-22 (15): rating proposed, then the freebie ledger checked.
  - 2026-08-23 (127): 🟡 proposed with SPACE given but TIME never stated — and the coach
    then recited the time bound itself. Learner: *"i didn't do the time yet, we shouldn't
    be rushing towards the rating."*

Both are the same defect: the rating is the destination and the gate a box to tick on the
way. A memory-file note is the weakest fix (prose the agent must remember to obey). This
hook binds the check to the exact moment it fails — the rating proposal — so it cannot be
skipped. Learner's call, 2026-08-23: *"put a clear gate at the rating where it requires
code completion + time and space complexities given."*

Mechanism (mirror of `problem_link_reminder.py`): at Stop, read the assistant's last turn;
if it PROPOSES a rating, scan the learner's recent messages for a time signal AND a space
signal. Missing either → block once (`stop_hook_active` guards against a loop), naming what
is missing, so the gate is completed before the rating stands.

Deliberately conservative, for the same reason the link hook is — a hook that cries wolf
gets skimmed past:
  - it fires only when BOTH a comfort marker AND a proposal cue are present, so ordinary
    talk *about* ratings (explaining the scale, citing a past rating) does not trip it;
  - it checks the LEARNER's transcript, not a self-asserted checklist the agent could write
    falsely — the ungameable form;
  - code-completion is implicit: a rating on a `pass` stub can't arise, there's nothing to
    read, so the gate that matters is the complexity one;
  - a single block only. If both axes really were given without the literal words (rare —
    "O(n) then O(1)"), the re-send passes. One nudge, never a wall.

NOT in scope: whether the stated complexity is CORRECT, or whether the freebie ledger was
read. Those are judgement (the coach's job, and the freebie-ledger rule lives in
`feedback_ask_complexity`). This hook enforces only that both axes were ASKED FOR and given
before the rating — the mechanizable half.
"""
import json
import re
import sys

# ── Rating-proposal detection ───────────────────────────────────────────────────
# A comfort verdict: the emoji, the streak-tagged emoji, or the word.
COMFORT = re.compile(
    r"🟢|🟡|🔴|🎓|\b(?:clean|shaky|blank)\b|\bs[0-2]\b", re.IGNORECASE
)
# A cue that the turn is PROPOSING a rating — i.e. asking the learner to DECIDE, which is the
# defining feature of a proposal (workflow step 4: "propose it for confirmation"). A recap only
# REPORTS already-logged ratings and asks for nothing.
#
# ⚠️ Do NOT match a bare next-review date ("→ Sep 2", "Oct 22"): a session recap lists exactly
# those alongside the comfort emoji ("567 🟢 s2 · Oct 22"), so date-matching false-fired on the
# Aug 23 close-out recap. The decision-request cue is the clean discriminator — a recap has none.
PROPOSE_CUE = re.compile(
    r"\bconfirm\b|\bproposed?\b|\boverride\b|\baccept\b|\brating[:?]|\brate\b",
    re.IGNORECASE,
)

# ── Complexity signals in the LEARNER's messages ────────────────────────────────
BIG_O = re.compile(r"O\s*\(", re.IGNORECASE)
TIME_SIGNAL = re.compile(
    r"\btime\b|\bamortiz\w*|\bruntime\b|\bper[- ]call\b|\bO\([^)]*\)\s*(?:time|per)",
    re.IGNORECASE,
)
SPACE_SIGNAL = re.compile(
    r"\bspace\b|\bmemory\b|\bin[- ]?place\b|\bauxiliary\b|\bfootprint\b|\bextra\s+(?:space|storage)\b",
    re.IGNORECASE,
)

LOOKBACK_TURNS = 8  # a rep's discussion spans several turns; scan the learner's recent ones.


def _is_real_user_message(entry: dict) -> bool:
    """True for a human turn, False for a tool_result carrier (typed 'user', mid-turn)."""
    if entry.get("type") != "user":
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    if not isinstance(content, list):
        return False
    return not any(
        isinstance(block, dict) and block.get("type") == "tool_result"
        for block in content
    )


def _entries(transcript_path: str) -> "list[dict]":
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return []


def last_turn_text(entries: "list[dict]") -> str:
    """All assistant `text` since the last real user message (one turn, many entries)."""
    chunks: list[str] = []
    for entry in reversed(entries):
        if _is_real_user_message(entry):
            break
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = (entry.get("message") or {}).get("content") or []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    return "\n".join(reversed(chunks))


def learner_text(entries: "list[dict]", turns: int = LOOKBACK_TURNS) -> str:
    """Concatenated text of the last `turns` real user messages."""
    chunks: list[str] = []
    seen = 0
    for entry in reversed(entries):
        if not _is_real_user_message(entry):
            continue
        seen += 1
        if seen > turns:
            break
        content = (entry.get("message") or {}).get("content")
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    return "\n".join(reversed(chunks))


def proposes_rating(turn: str) -> bool:
    return bool(COMFORT.search(turn) and PROPOSE_CUE.search(turn))


def missing_axes(learner: str) -> "list[str]":
    """Which complexity axes the learner has NOT evidenced. Empty = gate satisfied.

    An axis counts as given only if its keyword/proxy appears. NO Big-O-count credit:
    the tempting "two O() expressions => both axes given" heuristic misfires on exactly
    the case this hook exists for -- the 127 rep gave `O(V)` and `O(V+E)`, *both space*,
    with time never stated; a count rule reads two O()s and wrongly credits time.

    There is no textual way to tell which axis a bare `O(...)` names, so the only robust
    rule is the axis word. The gate already requires a why-clause per axis, and a real
    why-clause names the axis ("O(1) space, one fixed array") -- so in practice both words
    appear. The accepted cost is the rare abbreviated answer ("O(n) time, then O(1)") where
    space is unworded: it blocks ONCE, and the re-send passes (stop_hook_active).
    """
    missing = []
    if not TIME_SIGNAL.search(learner):
        missing.append("TIME")
    if not SPACE_SIGNAL.search(learner):
        missing.append("SPACE")
    return missing


MESSAGE = (
    "RATING GATE — this turn proposes a comfort rating, but the learner has not stated "
    "{missing} complexity in their recent messages.\n"
    "The complexity gate is BOTH axes, each with a why-clause, stated by the LEARNER, "
    "BEFORE any rating (CLAUDE.md LeetCode Review Workflow step 1; feedback_ask_complexity). "
    "It was run backwards on 15 (Aug 22) and 127 (Aug 23) — rating first, gate as a "
    "formality.\n"
    "DO NOT rate yet. Ask the learner for {missing} (each itemized), wait for their answer, "
    "and — if a bound is a miss — read that problem's row in complexity_gotchas.md BEFORE "
    "proposing, so the freebie state is known. Only then propose the rating.\n"
    "If the learner genuinely already stated both axes above (just without the words "
    '"time"/"space"), re-send — this blocks once.\n'
    "Rule: .claude/memory/feedback_ask_complexity.md"
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    if payload.get("stop_hook_active"):
        return  # never block twice — the re-send passes.

    entries = _entries(payload.get("transcript_path", ""))
    if not entries:
        return
    turn = last_turn_text(entries)
    if not turn or not proposes_rating(turn):
        return

    missing = missing_axes(learner_text(entries))
    if not missing:
        return

    json.dump(
        {"decision": "block", "reason": MESSAGE.format(missing=" and ".join(missing))},
        sys.stdout,
    )


# ── Self-test ─────────────────────────────────────────────────────────────────
# python .claude/hooks/rating_gate.py --selftest
PROPOSE_CASES = [
    # (name, turn_text, should_be_detected_as_proposal)
    ("emoji + confirm", "That reads as 🟡 Shaky — confirm?", True),
    ("word + arrow date", "Rating: 🟢 s2 → Oct 22. Confirm?", True),
    ("blank + proposed", "Proposed: 🔴 Blank, streak resets.", True),
    ("scale explanation, no propose cue", "The scale is 🟢 clean, 🟡 shaky, 🔴 blank.", False),
    ("past rating cite, no cue", "Your last rep on this was 🟡.", False),
    ("plain prose", "Nice, the BFS looks correct and clean.", False),
    # The Aug 23 close-out recap false positive: comfort markers + next-review dates, but it
    # REPORTS logged ratings and asks for no decision. Must NOT trip.
    ("session recap, no decision request",
     "Recap: 567 🟢 s2 (Oct 22) · 901 🟢 s1 (Sep 22) · 127 🟡 (Sep 2). Pushed.", False),
    ("override-style proposal", "Proposed: 🟡 Shaky → Sep 2. Accept or override?", True),
]

AXES_CASES = [
    # (name, learner_text, expected_missing)
    ("both worded", "time is O(n) for the pass, space is O(1) fixed array", []),
    ("space only (the 127 case)", "visited holds O(V), adjMap is O(V+E) for space", ["TIME"]),
    ("time only", "time is O(n log n) because we sort", ["SPACE"]),
    # Accepted conservative misses: an axis stated only as a bare O() (no word) blocks
    # once, then the re-send passes. Documented, not a bug.
    ("time worded, space bare (blocks once)", "O(n) time, then O(1)", ["SPACE"]),
    ("space worded, time bare (blocks once)", "space O(n), and O(n log n)", ["TIME"]),
    ("neither — no complexity", "yeah I think that solution is done and correct", ["TIME", "SPACE"]),
    ("amortized counts as time", "amortized O(1) per call, O(n) space overall", []),
    ("memory counts as space", "runtime is O(n), memory is O(1)", []),
]


def _selftest() -> int:
    fails = 0
    for name, text, expected in PROPOSE_CASES:
        got = proposes_rating(text)
        if got != expected:
            fails += 1
            print(f"FAIL propose  {name}: got {got}, expected {expected}")
    for name, text, expected in AXES_CASES:
        got = missing_axes(text)
        if got != expected:
            fails += 1
            print(f"FAIL axes  {name}: got {got}, expected {expected}")
    total = len(PROPOSE_CASES) + len(AXES_CASES)
    print(f"rating_gate: {total - fails}/{total} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    main()
