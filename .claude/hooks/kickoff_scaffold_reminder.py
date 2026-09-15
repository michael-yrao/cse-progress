"""UserPromptSubmit hook: remind the agent that a kickoff greeting must scaffold the board.

Fires when the learner's prompt reads as a session KICKOFF ("let's do our sunday
session", "start saturday session", "/start-day", "what's up today") and injects a
reminder to scaffold the whole day's board BEFORE presenting it.

Why this exists
---------------
"A real kickoff scaffolds every problem on today's schedule before presenting the board"
used to live inline in the always-injected CLAUDE.md and fired every session. The
multi-skill migration demoted it into `references/scaffolding.md` — an opt-in read whose
open-trigger already presumes the decision to scaffold — so at a session-start greeting
the rule was never reached. It lapsed on "start saturday session" (Sep 12, 2026) and
again on "let's do our sunday session" (Sep 13). The Sep 12 fix was a note in that same
cold reference; it lasted one day.

This binds the rule to a MOMENT (the prompt) in a hot tier, the way
`scaffold_links_reminder.py` binds the links rule to a tool invocation. See the
2026-09-13 entry in `.claude/memory/self_eval_log.md` and `decisions.yml`
`kickoff-scaffold-gate`.

Warn-only: it injects context and never blocks. Costs no context tokens until it fires,
and stays silent on a named problem ("let's do 235"), a non-kickoff question ("what's
the bug in my code"), or a CLOSE-OUT ("close monday session", "wrap up and commit") —
a hook that cries wolf trains the agent to skim past it. The close-out guard was added
Sep 14, 2026 after "close monday session" tripped the `<weekday> session` pattern.
"""
import json
import re
import sys

_DAY = r"(?:mon|tues?|wednes?|thurs?|fri|satur?|sun)(?:day)?"

# Kickoff phrasings. Each requires the *day/session* framing — a bare "start" or a named
# problem must NOT match (that is a scoped scaffold, not a batch). Anchored loosely so
# leading filler ("ok, ", "alright ") still trips it.
KICKOFF_PATTERNS = [
    # "start /let's do/start our sunday session", "start the session", "start today's session"
    r"\b(?:start|do|begin)\b.{0,20}?\b(?:session)\b",
    # "start today", "start the day", "start our day"
    r"\bstart(?:ing)?\b.{0,12}?\b(?:the |our |today'?s )?day\b",
    # "what's up today", "what's on today", "what do we have today"
    r"\bwhat'?s\b.{0,20}?\btoday\b",
    # explicit weekday session, any verb
    rf"\b{_DAY}\b.{{0,8}}?\bsession\b",
    # the slash command
    r"/start-day\b",
]
KICKOFF = re.compile("|".join(KICKOFF_PATTERNS), re.IGNORECASE | re.DOTALL)

# A CLOSE-OUT is the opposite of a kickoff, but "close monday session" / "close out the
# session" match the `<weekday> session` / `do…session` kickoff patterns above and used to
# inject the "scaffold the whole board" reminder at the end of a day (verified Sep 14, 2026
# on "close monday session"). Close-outs use close/wrap/commit/push framing that a kickoff
# never does, so a leading close-out verb suppresses the kickoff reminder. This is also the
# phrase family that carries commit+push authorization (CLAUDE.md gate 8 / decisions.yml
# `close-out-commit-authorization`), so the two must not be confused.
CLOSEOUT = re.compile(
    r"\b(?:clos(?:e|ing)|wrap(?:ping)?(?:\s*up)?|commit|push|"
    r"call it (?:a )?(?:night|day)|done for (?:the )?(?:day|night))\b",
    re.IGNORECASE,
)

# If the prompt names a specific LeetCode problem number, it is a scoped request, not a
# batch kickoff — scaffold only that. A 1-4 digit run guards against matching dates/years.
NAMES_A_PROBLEM = re.compile(r"\b\d{1,4}\b")

REMINDER = (
    "This prompt reads as a session KICKOFF. Per the always-on kickoff gate (CLAUDE.md) "
    "and references/scaffolding.md, a kickoff scaffolds the WHOLE day's board BEFORE the "
    "board is presented: run new_problem.py for EVERY problem on today's schedule "
    "(active block AND both warmup slots, red/yellow/green alike), fill each statement, "
    "THEN present name+links only. Caveat: if the learner named a specific problem "
    "(\"let's do 235\") this is NOT a batch kickoff — scaffold only that one and ask "
    "before batching. Do not commit a scaffold that is never attempted (phantom tracker "
    "rows). Rule: references/scaffolding.md scope section."
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    prompt = payload.get("prompt", "") or ""
    if CLOSEOUT.search(prompt):
        return  # "close monday session", "wrap up and commit" — a close-out, never a kickoff
    if not KICKOFF.search(prompt):
        return
    # A kickoff phrase that also names a problem number is ambiguous; the reminder already
    # carries the "named problem is not a batch" caveat, so still fire — but this is where
    # a future quiet-guard would go if it proves noisy on "start 235".

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": REMINDER,
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
