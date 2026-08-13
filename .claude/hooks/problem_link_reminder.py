"""Stop hook: block a turn that names a problem number without its link pair.

The rule — every problem mention carries `[file] · [LC/NC]` — has lapsed nine times
(Jul 20/21/23/30/31, Aug 3, Aug 5, Aug 6, Aug 12, 2026). The `PostToolUse` sibling
(`scaffold_links_reminder.py`) covers the *scaffold* case, and `new_problem.py` prints
a `LINKS:` line at source, but neither can reach the dominant remaining failure mode:
the **mid-session restate** — "next is 778", "still on the board: 271, 155", a
hand-over, a "what's next". No tool runs, so nothing fires. See the Aug 6 entry in
`.claude/memory/feedback_kickoff_table_links.md`, which named this hook as the fix and
then left it unbuilt for six days while the rule lapsed once more.

Mechanism: at Stop, read the last assistant message from the transcript and look for a
problem number that is NOT already inside a markdown link. If found, block once with
the offending numbers named, so the agent re-emits the turn with links.

Deliberately conservative — a hook that cries wolf trains the agent to skim past it,
which costs exactly the reliability that makes a hook stronger than prose (the lesson
recorded in scaffold_links_reminder.py's own header). Hence:
  - only 1–4 digit integers that look like problem references, and only when the turn
    carries a problem-ish cue word, so ordinary numbers in prose don't trip it;
  - any number already appearing inside a markdown link anywhere in the turn is
    considered linked, since one link block covers repeated mentions of the same
    problem later in the same message;
  - `stop_hook_active` short-circuits, so it can never loop.
"""
import json
import re
import sys

# A markdown link's visible text or its target. `[211 Add and Search](path)` and
# `[LC](https://leetcode.com/problems/...)` both count as linking 211.
MD_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")

# A bare problem reference: 1-4 digits, not part of a longer token, not a date/year,
# not a version. Bounded by non-word chars on both sides.
NUMBER = re.compile(r"(?<![\w.#/-])(\d{1,4})(?![\w.%/-])")

# The turn must look like it is talking about problems at all. Without this, a turn
# about complexity ("26 children", "O(n) with n = 10^4") lights up constantly.
PROBLEM_CUE = re.compile(
    r"\b(problem|leetcode|lc\b|neetcode|warmup|active block|board|scaffold|retry|"
    r"rep\b|next up|on deck|schedule|tracker)", re.IGNORECASE
)

# Numbers that are never problem references in this repo's vocabulary.
IGNORE = {
    # comfort/streak/interval vocabulary
    "0", "1", "2", "3", "10", "30", "60", "180",
    # years and common counts
    "2026", "2025",
}

MESSAGE = (
    "LINK RULE — this turn names problem number(s) {nums} without a markdown link.\n"
    "Re-send the turn with the full pair for each: [<repo-relative .py path>] · "
    "[LC](leetcode url)  (use [NC](neetcode url) if the problem is LC-premium).\n"
    "Applies to every mention — kickoff, restate, hand-over, 'what's next'. A bare "
    "number costs the learner a manual file hunt; this rule has lapsed 9 times.\n"
    "EXCEPTION — in a SELECTION MENU where the learner has not picked yet, an "
    "unscaffolded retry's file link is a SPOILER: link LC/NC only. If that is this "
    "turn, say so plainly instead of adding file links.\n"
    "Rule: .claude/memory/feedback_kickoff_table_links.md"
)


def last_assistant_text(transcript_path: str) -> str:
    """Concatenated text of the final assistant message in the transcript."""
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            entries = [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return ""

    for entry in reversed(entries):
        if entry.get("type") != "assistant":
            continue
        content = (entry.get("message") or {}).get("content") or []
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def unlinked_problem_numbers(text: str) -> list[str]:
    """Problem-looking numbers in `text` that appear nowhere inside a markdown link."""
    if not PROBLEM_CUE.search(text):
        return []

    linked = " ".join(MD_LINK.findall(text))
    linked_numbers = set(NUMBER.findall(linked))

    # Strip link constructs before scanning, so a number only counts when it is loose.
    bare = MD_LINK.sub(" ", text)

    found: list[str] = []
    for num in NUMBER.findall(bare):
        if num in IGNORE or num in linked_numbers or num in found:
            continue
        found.append(num)
    return found


# ⚠️ DISABLED 2026-08-12, same day it was written — see the note in
# `.claude/memory/feedback_kickoff_table_links.md`. `last_assistant_text()` is wrong:
# a single turn is split across SEVERAL assistant entries, one block-type each
# (`thinking` / `tool_use` / `text` are separate records), so the most recent assistant
# entry is usually a tool call with no text. The selector therefore returns either ""
# (silent miss) or a fragment from an EARLIER turn (false block). Observed live: it
# blocked a turn citing 269/17/15 — real bare numbers, but from the previous turn —
# while missing the 150 that was actually bare in the turn it claimed to check.
#
# The unit tests passed because they fed a hand-built transcript with one text entry per
# message. They tested the regex, which was fine; the transcript SHAPE was never tested.
#
# Left registered but inert rather than deleted: the detector below (`unlinked_problem_
# numbers`) is tested and correct, and only the message selection needs rewriting —
# gather text from ALL trailing assistant entries back to the last `user` entry, rather
# than from the last assistant entry alone.
DISABLED = True


def main() -> None:
    if DISABLED:
        return

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    # Never block twice on one turn: the second pass is the corrected reply.
    if payload.get("stop_hook_active"):
        return

    text = last_assistant_text(payload.get("transcript_path", ""))
    if not text:
        return

    nums = unlinked_problem_numbers(text)
    if not nums:
        return

    json.dump(
        {"decision": "block", "reason": MESSAGE.format(nums=", ".join(nums))},
        sys.stdout,
    )


if __name__ == "__main__":
    main()
