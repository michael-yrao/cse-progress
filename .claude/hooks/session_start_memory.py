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
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

MEMORY_INDEX = Path("memory") / "MEMORY.md"
SELF_EVAL_LOG = Path("memory") / "self_eval_log.md"

# Cadence thresholds for the meta-review overdue check. These live in cse.config.yml under
# `self_eval:`; the literals here are an ANNOUNCED-in-comment fallback for when the config or a
# YAML parser is unavailable (this hook must never depend on PyYAML — it runs at session start
# and a hard dependency here recreates the no-rules-loaded failure). A regex read keeps it
# dependency-free. These are an operational cadence, not an engine-tuned value, so they are not
# in check_single_source's tracked set.
_META_REVIEW_DAYS_FALLBACK = 14
_OPEN_THRESHOLD_FALLBACK = 8

# Gates that must fire without being asked for.
#
# **Keep this list short and keep it earned.** It is injected every single session, so
# every line costs tokens forever. Entry criteria: (a) it must fire unprompted, (b) it has
# actually lapsed before, (c) no source fix or other hook already covers it — a rule the
# tooling now enforces belongs in the script, not here. Scaffold links left on criterion
# (c) when new_problem.py started printing them; the past-midnight dating gate left on
# 2026-08-16 for the same reason, once session_date.py had source-fixed it and the gate's
# own text ("new_problem.py has no --date flag") had gone stale and wrong.
#
# Keep this text free of emoji and arrow glyphs — see the note in emit().
ALWAYS_ON = """\
ALWAYS-ON GATES — each is bound to a MOMENT, not a topic. Check the trigger, not the mood of the session.

1. About to propose a comfort rating (green/yellow/red)? -> The COMPLEXITY GATE is already overdue.
   Time AND space, each with an itemized why-clause, from the learner, BEFORE the rating. It fires on
   the rep, not the ritual: "what's wrong with my code" with no scaffold and no kickoff is still a rep.
   Step 1 of CLAUDE.md's LeetCode Review Workflow. (Skipped entirely 2026-08-02.)
2. Something you did just got corrected — by the learner OR by you, unprompted? -> Append a dated entry
   to .claude/memory/self_eval_log.md IN THE SAME TURN. A sentence in chat is not a fix; it dies with
   the context window. (Caught-then-not-logged 2026-08-02.)
3. Fixing a recurring miss? -> Climb the intervention ladder: source fix > hook > skill reference /
   CLAUDE.md step > memory file. A coaching-moment rule belongs in a skill reference (it loads at that
   moment); an unprompted one in CLAUDE.md. A rule that lapsed twice as prose won't be fixed by better prose.
4. Asked to close out / commit / push / archive? -> Verify it against the visible state of the work
   first, and ASK if they disagree. If any part of a turn contains fabricated tool output, none of that
   turn is evidence. (2 occurrences in one day.)
5. Handing over a retry? -> Problem number and links only. No prior rating, no prior failure category,
   no "where the rep lives" — that is stuck_log content and it pre-localizes the rep. (2 occurrences.)
6. Last session of the week? -> Archive this week's schedule AND generate next week's, before the
   commit. Both, or neither counts. Step 7 of CLAUDE.md's LeetCode Review Workflow. (Missed 2026-08-02.)

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


def _config_int(claude_dir: Path, key: str, fallback: int) -> int:
    """Read one `self_eval.<key>` int from cse.config.yml via regex (no PyYAML dep)."""
    try:
        text = (claude_dir.parent / "cse.config.yml").read_text(encoding="utf-8")
        block = re.search(r"(?ms)^self_eval:\s*$(.*?)^\S", text + "\n\\Z")
        scope = block.group(1) if block else text
        m = re.search(rf"^\s+{re.escape(key)}:\s*(\d+)", scope, re.M)
        return int(m.group(1)) if m else fallback
    except Exception:
        return fallback


def meta_review_banner(claude_dir: Path) -> str:
    """Return a loud one-line banner if the self-eval meta-review is overdue, else ''.

    Fail-soft: any parsing problem returns '' — a broken check must never block session start.
    The meta-review used to be an unfired paragraph ('weekly, or ~8 open'); this computes the
    trigger so it actually fires. Robust signal is the DAYS-since-last-meta-review (a date can't
    be miscounted); the open count is a secondary, approximate nudge.
    """
    try:
        log = (claude_dir / SELF_EVAL_LOG).read_text(encoding="utf-8")
    except OSError:
        return ""
    try:
        review_dates = re.findall(r"(?im)^#+.*META-REVIEW\D*(\d{4}-\d{2}-\d{2})", log)
        last = max(review_dates) if review_dates else None
        # A real entry starts a line and carries a [P1]/[P2] priority tag after its date
        # (## 2026-09-04 [P2] — … or - **2026-08-06 [P1]** …). Requiring the tag excludes the
        # many dated *references* inside prose/cross-refs — the over-count the earlier audit warned
        # about. Count only OPEN entries dated AFTER the last meta-review: legitimately-open one-offs
        # are meant to stay open, so counting the total would keep firing forever after a clean review.
        # The count resets at each review and climbs only as NEW opens accrue.
        open_count = 0
        for m in re.finditer(r"(?im)^(?:#+|-)\s+\**(\d{4}-\d{2}-\d{2})\s*\**\s*\[P\d\].*$", log):
            if "consolidated" in m.group(0).lower():
                continue
            if last is not None and m.group(1) <= last:
                continue
            open_count += 1
        days_thr = _config_int(claude_dir, "meta_review_days", _META_REVIEW_DAYS_FALLBACK)
        open_thr = _config_int(claude_dir, "open_threshold", _OPEN_THRESHOLD_FALLBACK)

        overdue_days = None
        if last:
            try:
                delta = (_dt.date.today() - _dt.date.fromisoformat(last)).days
                overdue_days = delta if delta >= days_thr else None
            except ValueError:
                overdue_days = None
        if overdue_days is None and open_count < open_thr:
            return ""
        why = []
        if overdue_days is not None:
            why.append(f"{overdue_days}d since last ({last})")
        if open_count >= open_thr:
            why.append(f"~{open_count} open entries")
        return (
            "!! SELF-EVAL META-REVIEW OVERDUE (" + "; ".join(why) + "). Before other work, cluster the "
            "open entries in .claude/memory/self_eval_log.md by root cause and promote any 2+ recurrence "
            "up the ladder (source fix > hook > skill reference / CLAUDE.md step > memory file); then "
            "archive consolidated entries. See feedback_self_evaluation.md.\n\n"
        )
    except Exception:
        return ""


def emit(context: str) -> None:
    """Write the hook envelope to stdout.

    ⚠️ Do NOT add `ensure_ascii=False` here, and keep emoji out of ALWAYS_ON. The memory
    index carries emoji (the Comfort scale is literally emoji) and this runs on Windows,
    where stdout defaults to cp1252 — encoding them raw raises UnicodeEncodeError and the
    session starts with no rules loaded, the exact failure this hook exists to prevent.
    `json.dump` escapes them to \\uXXXX by default, so the wire bytes stay pure ASCII and
    the emoji survive the round trip. Same class of bug as the 2026-07-04 / 2026-07-08
    entries in self_eval_log.md.
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
    claude_dir = project_root()
    index_path = claude_dir / MEMORY_INDEX
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

    emit(f"{meta_review_banner(claude_dir)}{ALWAYS_ON}\n{index}")


if __name__ == "__main__":
    main()
