"""PostToolUse hook: remind the agent to emit problem links after scaffolding.

Fires on every Bash call whose command mentions `new_problem.py`, and injects a
reminder back into the model's context.

Why this exists: the "link every scaffolded problem" rule lapsed five times
(Jul 20/21/23/30/31, 2026) while it lived only as prose in
`.claude/memory/feedback_kickoff_table_links.md`. Rules anchored to an *artifact*
(the kickoff table) stop applying the moment the output format changes; a rule
anchored to a *tool invocation* cannot. See the Jul 31 entry in
`.claude/memory/self_eval_log.md`.

Costs no context tokens until it fires.
"""
import json
import re
import sys

# An *invocation*, not a mention. A bare "new_problem.py" substring also matches
# `grep -n ... scripts/new_problem.py` and `python -c "...new_problem.py..."`, which
# fired the reminder twice on 2026-08-02 during read-only work on the script itself.
# That is not harmless: a hook that cries wolf trains the agent to skim past it, which
# costs exactly the reliability that makes a hook stronger than a written rule.
# `--number` is required by the script's own argparse, so every real scaffold has it
# and no read-only command does.
TRIGGER = re.compile(r"new_problem\.py.*--number", re.DOTALL)

REMINDER = (
    "Scaffold complete. Before continuing, reply with BOTH links for EVERY problem "
    "just scaffolded: the repo-relative .py path AND its LeetCode URL (NeetCode "
    "mirror if premium). Unprompted, in this turn — do not defer to a later table. "
    "Rule: .claude/memory/feedback_kickoff_table_links.md"
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    command = (payload.get("tool_input") or {}).get("command", "")
    if not TRIGGER.search(command):
        return

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": REMINDER,
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
