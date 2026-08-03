"""SessionStart hook: load the agent memory index into context, unprompted.

Fires at session startup/resume/clear/compact and injects `.claude/memory/MEMORY.md`
plus the small set of gates that must fire without being asked for.

Why this exists
---------------
CLAUDE.md already says "read MEMORY.md at the start of each session", but that is a
rule about starting a session, and a session that opens with a direct technical
question ("whats the issue with my code here") does not feel like a start. On
2026-08-02 the memory index was never loaded at all until the learner asked about it
nine turns in — so `feedback_ask_complexity` and `feedback_self_evaluation` were not
merely ignored, they were absent, and both failed in the same session.

The structural fact this encodes: **CLAUDE.md is always injected; `.claude/memory/*.md`
are opt-in reads.** A rule that must fire unprompted cannot live only in memory.
This hook removes the choice — the index arrives whether or not the session looks
like a start.

Note the header below is not decoration. Dumping the index alone would reproduce the
failure it is meant to fix: on 2026-08-02 the index line for the complexity gate
existed and was correct, and the gate still did not fire, because what was missing was
never the *content* — it was the binding to a *moment*. So the gates are restated as
if/then triggers, not as topics.

See the 2026-08-02 entry in `.claude/memory/self_eval_log.md`.
"""
import json
import os
import sys
from pathlib import Path

MEMORY_INDEX = Path("memory") / "MEMORY.md"

# Gates that must fire without being asked for. Kept deliberately short: this is
# injected every session, and a long list is one nobody reads. Entry criteria —
# (a) it must fire unprompted, (b) it has actually lapsed before, (c) no other hook
# already covers it (scaffold links are handled by scaffold_links_reminder.py).
ALWAYS_ON = """\
ALWAYS-ON GATES — each is bound to a MOMENT, not a topic. Check the trigger, not the mood of the session.

1. About to propose a comfort rating (🟢/🟡/🔴)? → The COMPLEXITY GATE is already overdue. Time AND
   space, each with an itemized why-clause, from the learner, BEFORE the rating. It fires on the rep,
   not the ritual: "what's wrong with my code" with no scaffold and no kickoff is still a rep.
   Step 1 of CLAUDE.md's LeetCode Review Workflow. (Skipped entirely 2026-08-02.)
2. Something you did just got corrected — by the learner OR by you, unprompted? → Append a dated entry
   to .claude/memory/self_eval_log.md IN THE SAME TURN. A sentence in chat is not a fix; it dies with
   the context window. (Caught-then-not-logged 2026-08-02.)
3. Past midnight? → Establish the session date from `git log --date=iso` BEFORE scaffolding, dating, or
   presenting a lineup. Commits from minutes ago mean a live session, not a new day. Every date-touching
   script defaults to wall clock and `new_problem.py` has no --date flag. (4+ occurrences.)
4. Asked to close out / commit / push / archive? → Verify it against the visible state of the work
   first, and ASK if they disagree. If any part of a turn contains fabricated tool output, none of that
   turn is evidence. (2 occurrences in one day.)
5. Handing over a retry? → Problem number and links only. No prior rating, no prior failure category,
   no "where the rep lives" — that is stuck_log content and it pre-localizes the rep. (2 occurrences.)

Load the individual memory file before acting on any rule you are unsure about. Index follows.
"""


def project_root() -> Path:
    """Resolve the .claude directory, preferring the harness-provided project dir."""
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        candidate = Path(env_dir) / ".claude"
        if candidate.is_dir():
            return candidate
    # Fall back to this script's own location (.claude/hooks/ -> .claude/), which is
    # correct regardless of the working directory the hook is invoked from.
    return Path(__file__).resolve().parent.parent


def emit(context: str) -> None:
    """Write the hook envelope to stdout.

    ⚠️ Do NOT add `ensure_ascii=False` here. The payload carries emoji (🟢/🟡/🔴, ⚠️)
    and this hook runs on Windows, where stdout defaults to cp1252 — encoding them
    raw raises UnicodeEncodeError and the session starts with no rules loaded, the
    exact failure this hook exists to prevent. `json.dump` escapes them to \\uXXXX by
    default, so the wire bytes stay pure ASCII and the emoji survive the round trip.
    Same class of bug as the 2026-07-04 / 2026-07-08 entries in self_eval_log.md.
    """
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )


def main() -> None:
    index_path = project_root() / MEMORY_INDEX
    try:
        index = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        # Surface the failure rather than starting a session that silently has no
        # rules loaded — a quiet no-op here recreates the exact bug this hook fixes.
        emit(
            f"⚠️ SessionStart hook could not read the memory index at {index_path} "
            f"({exc.__class__.__name__}: {exc}). Agent memory is NOT loaded — read "
            f".claude/memory/MEMORY.md manually before relying on any standing rule."
        )
        return

    emit(f"{ALWAYS_ON}\n{index}")


if __name__ == "__main__":
    main()
