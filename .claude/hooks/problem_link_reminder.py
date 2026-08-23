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
from datetime import datetime
from pathlib import Path

# A markdown link's visible text or its target. `[211 Add and Search](path)` and
# `[LC](https://leetcode.com/problems/...)` both count as linking 211.
MD_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")

# Inline code span. A backticked number is a code/data reference under discussion, not
# a problem being handed over.
CODE_SPAN = re.compile(r"`[^`]*`")

# A bare problem reference: 1-4 digits, not part of a longer token, not a date/year,
# not a version. The trailing guard rejects a following `.` ONLY when a digit follows
# it (a decimal like `7.8`) - a plain sentence-ending period must not hide the number,
# which is how "next on the board: 155." slipped through before 2026-08-14.
NUMBER = re.compile(r"(?<![\w.#/-])(\d{1,4})(?![\w%/-])(?!\.\d)")

# Any digit run inside a link, however embedded. `[x](dsa/.../739_daily_temps.py)`
# links 739 even though the strict NUMBER regex rejects it for the trailing `_`.
LINKED_NUMBER = re.compile(r"(\d{1,4})")

# Prose that reliably contains non-problem numbers. Stripped before scanning, so a
# rating turn full of dates, line refs and worked arithmetic doesn't cry wolf.
NOISE = re.compile(
    r"(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}"
    r"|\b(?:line|lines|row|rows|streak|step|steps|page|turn|turns)"
    r"\s+\d{1,4}(?:\s*[-–—]\s*\d{1,4})?"
    r"|\d{1,4}(?:\.\d+)?\s*(?:[a-z-]+\s+){0,2}(?:%|units?|days?|entries|occurrences?|attempts?|cases?|runs?|tests?|sequences?|iterations?|mismatches|examples?)\b"
    r"|\d{1,4}\s+(?:children|letters|nodes|chars?|characters|elements|items|keys|"
    r"buckets|calls|pointers|levels|states|cells|edges|vertices|words|colou?rs)\b"
    r"|\bup to \d{1,4}\b"
    r"|\bO\([^)]*\)"
    r"|\bstreak\s*\d"
    r"|(?<![\d)])\+\d{1,3}\b"
    r"|\d{1,4}(?:\s*[-+*/×]\s*\d{1,4})+\s*=\s*\d{1,4})",
    re.IGNORECASE,
)

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

# ── The day's board ───────────────────────────────────────────────────────────
# Scope limit set by the learner Aug 14/15, 2026: *"if they are not in today's todo
# list, don't populate the links."* A link is an INVITATION. Linking an off-board
# problem advertises a rep that is not due — which is exactly how 503 (🟢, due Sep 9)
# got pulled 26 days early on the night the rule was set — and for an unscaffolded
# retry the file link is the spoiler the CAVEAT in the memory file already forbids.
#
# So the hook blocks only on numbers ACTIONABLE TODAY. Everything else — coverage
# roll-ups ("Monotonic Stack now holds 496/503/901"), regression comparisons,
# waiting-room mentions — is context and stays bare.
REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKERS = (
    REPO_ROOT / "docs" / "foundations" / "dsa" / "mastery" / "dsa_progress.md",
    # The SD tracker left with the SD track on Aug 15, 2026 (private sd-progress repo).
    # Not re-pointed across repos on purpose: this hook guards THIS repo's links, and a
    # path into a sibling clone would silently no-op on any machine that lacks it.
)
SCHEDULE_DIR = REPO_ROOT / "docs" / "foundations" / "schedules"

# `| Medium | [739. Daily Temperatures](url) | 🟡 | 0 | 2026-08-24 | ... |`
TRACKER_ROW = re.compile(
    r"^\|[^|]*\|\s*\[(\d{1,4})\.[^\]]*\]\([^)]*\)\s*\|[^|]*\|[^|]*\|([^|]*)\|"
)
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

# A problem reference INSIDE a schedule cell. Taking every digit run and filtering by
# the tracker vocabulary is not enough: a cell says "Fri Aug 14", "26 days early",
# "streak 1", and 14/26/1 are all real problem numbers, so the board silently grew a
# tail of things that are not on it. A problem reference is either a filename stem
# (`739_daily_temperatures.py`) or a number followed by its Title-Cased name.
SCHEDULE_REF = re.compile(r"(?:(\d{1,4})_[a-z]|(\d{1,4})\s+[A-Z][a-z])")


def _session_date() -> str:
    """Session date as `YYYY-MM-DD` — NOT the wall clock, which rolls past midnight.

    Reuses `scripts/session_date.py`, so this hook agrees with `new_problem.py` and
    `update_review_dates.py` about which day it is. Falls back to the clock if the
    import fails: a hook must never crash the turn it is policing.
    """
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import session_date  # type: ignore

        # announce=False is LOAD-BEARING, not tidiness: this hook writes its JSON
        # verdict to stdout, and resolve() otherwise prints "Using session date ..."
        # there first, corrupting every block into unparseable output.
        return session_date.resolve(announce=False)
    except Exception:
        return datetime.now().strftime("%Y-%m-%d")


def _tracker_numbers(today: str) -> "tuple[set[str], set[str]]":
    """(every number the trackers know, those the engine dates to `today` exactly).

    The first set is the vocabulary filter — it is what stops a bare `24` inside a
    schedule cell (`Aug 24`) being mistaken for a problem number.
    """
    known: set[str] = set()
    due: set[str] = set()
    for tracker in TRACKERS:
        try:
            lines = tracker.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            match = TRACKER_ROW.match(line.strip())
            if not match:
                continue
            number, next_review = match.group(1), match.group(2).strip()
            known.add(number)
            iso = ISO_DATE.search(next_review)
            # Exactly today, NOT `<=`. An overdue row is not on today's list unless
            # the schedule says so, and sweeping the whole slip tail in here would
            # re-widen the scope back to what the learner just asked to narrow.
            if iso and iso.group(0) == today:
                due.add(number)
    return known, due


DAY_BANNER = re.compile(r"\*\*[A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{1,2}\*\*")


def _todays_schedule_numbers(known: "set[str]", today: str) -> "set[str]":
    """Problem numbers in today's row of the current week's schedule file.

    The row is one physical line beginning `| **Fri Aug 14**`. Candidates must look
    like problem references (`SCHEDULE_REF`) AND be known to a tracker -- two filters,
    because either alone lets the cell's dates, unit costs and streaks through.
    """
    try:
        current = max(SCHEDULE_DIR.glob("*_schedule.md"), key=lambda f: f.name)
    except (OSError, ValueError):
        return set()
    try:
        stamp = datetime.strptime(today, "%Y-%m-%d")
    except ValueError:
        return set()

    # "Aug 14" / "Aug 4" — the schedule files do not zero-pad.
    label = re.compile(
        r"\*\*[A-Za-z]{3}\s+" + stamp.strftime("%b") + r"\s+" + str(stamp.day) + r"\*\*"
    )
    try:
        lines = current.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()

    # The daily table was restructured on Aug 16, 2026: a day is now a BANNER ROW
    # (`| > **Sun Aug 16** - 8.0 units | | | | |`) followed by one row per problem,
    # none of which repeat the day label. Scanning single labelled lines therefore
    # found no problems in the live table at all -- and silently fell through to the
    # only remaining line that still matched: the pre-Aug-16 row kept verbatim in the
    # appendix. The hook was reading SUPERSEDED data and flagging problems that had
    # been taken off the board hours earlier.
    #
    # So: stop at the first `## ` heading (the appendix lives below one), find the
    # banner, then read forward until the next banner or the end of the table.
    found: set[str] = set()
    started = False
    for line in lines:
        if line.startswith("## ") and started:
            break                                  # never walk into the appendix
        stripped = line.lstrip()
        is_row = stripped.startswith("|")
        if not started:
            if is_row and label.search(line):
                started = True                     # banner row for today
            continue
        # inside today's block: another day's banner ends it, as does leaving the table
        if not is_row:
            if stripped:
                break
            continue
        if DAY_BANNER.search(line) and not label.search(line):
            break
        # A DONE problem is not actionable, so it is not on the board. The table marks
        # completion by striking the problem link (`~~[261 ...]~~`) -- the same signal a
        # human reads. Without this the hook goes on demanding links for reps finished
        # hours ago, and a link is an INVITATION, which is the very thing this rule
        # exists to prevent. (Learner, Aug 16: "you linked 261 but we are already done
        # with 261.")
        if "~~" in line:
            continue
        for stem, titled in SCHEDULE_REF.findall(line):
            number = stem or titled
            if number in known:
                found.add(number)
    return found


def todays_board() -> "set[str] | None":
    """Numbers actionable today, or None when the board cannot be determined.

    `None` is the fail-SAFE: an unreadable tracker falls back to policing every bare
    number rather than silently policing nothing. A hook that quietly stops working is
    this repo's most expensive failure shape — it is why this file shipped DISABLED on
    Aug 12 and let the 10th lapse through.

    Known gap, stated rather than assumed away: a BRAND-NEW problem has no tracker row
    until it is logged, so a bare hand-over of one will not block here. That case is
    already covered at source — `new_problem.py` prints its own `LINKS:` line and
    `scaffold_links_reminder.py` fires on the same command.
    """
    today = _session_date()
    known, due = _tracker_numbers(today)
    if not known:
        return None
    return due | _todays_schedule_numbers(known, today)


MESSAGE = (
    "LINK RULE — this turn names problem number(s) {nums} without a markdown link.\n"
    "DO NOT RE-SEND THE TURN. Reply with ONLY the missing link pairs, one line each — "
    "no restated explanation, no summary of what you just said, nothing else:\n"
    "    [<repo-relative .py path>] · [LC](leetcode url)   (use [NC](neetcode url) if LC-premium)\n"
    "A lone re-emitted link reads as a directive (\"do this one first\"). When these links "
    "are ONLY a debt being paid — not a pick you are recommending — append the fixed tag "
    "`(links owed, order unchanged)` to the last line so it cannot be misread. Omit the tag "
    "only when you genuinely mean to steer the learner to that problem.\n"
    "Re-emitting a whole turn to fix a missing link doubles that turn's cost, and the cost is "
    "worst on the longest turns. Aug 15, 2026: a full algorithm teach was paid for twice, and the "
    "reply explaining that then tripped this hook again. The links are what was missing; only the "
    "links are owed.\n"
    "Applies to every mention — kickoff, restate, hand-over, 'what's next'. A bare "
    "number costs the learner a manual file hunt; this rule has lapsed 10 times. ONLY problems on TODAY'S BOARD are flagged; an off-board problem -- a coverage roll-up, a regression comparison, a waiting-room mention -- must NOT be linked at all, because a link is an invitation and linking one advertises a rep that is not due.\n"
    "EXCEPTION — in a SELECTION MENU where the learner has not picked yet, an "
    "unscaffolded retry's file link is a SPOILER: link LC/NC only. If that is this "
    "turn, say so plainly instead of adding file links.\n"
    "Rule: .claude/memory/feedback_kickoff_table_links.md"
)



def _is_real_user_message(entry: dict) -> bool:
    """True for a human turn, False for a `tool_result` carrier.

    Tool results are recorded as `type: "user"` entries *inside* an assistant turn, so
    they are NOT turn boundaries. Only an entry whose content holds no `tool_result`
    block ends the turn.
    """
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


def last_turn_text(transcript_path: str) -> str:
    """All assistant `text` emitted since the last real user message.

    One turn spans MANY assistant entries — `thinking`, `text` and `tool_use` are each
    their own record — so reading only the final assistant entry sees a tool call and
    nothing else. Walk back to the last human message instead, skipping the interleaved
    `tool_result` carriers and any sidechain (subagent) output.
    """
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            entries = [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return ""

    chunks: list[str] = []
    for entry in reversed(entries):
        if _is_real_user_message(entry):
            break
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = (entry.get("message") or {}).get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                chunks.append(block.get("text", ""))

    return chr(10).join(reversed(chunks))


LINK_LOOKBACK_TURNS = 4


def recently_linked(transcript_path: str, turns: int = LINK_LOOKBACK_TURNS) -> "set[str]":
    """Problem numbers already delivered as a link in the last `turns` assistant turns.

    The rule exists to save the learner a manual file hunt. A link handed over three
    turns ago has already done that, so demanding it again is noise -- and it is noise
    at exactly the wrong moment, because the problem being re-mentioned is usually the
    one they currently have OPEN. (Learner, Aug 16, twice: "you did the thing again,
    added 208 link when it was not necessary.")

    Deliberately narrow: it suppresses the DEMAND, never the rule. A number never linked
    in the window is still policed, so a genuine hand-over is unaffected.
    """
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            entries = [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return set()

    seen_users = 0
    chunks: list[str] = []
    for entry in reversed(entries):
        if _is_real_user_message(entry):
            seen_users += 1
            if seen_users > turns:
                break
            continue
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = (entry.get("message") or {}).get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                chunks.append(block.get("text", ""))

    text = chr(10).join(chunks)
    return {m.group(1) for m in re.finditer(r"\[(\d{1,4})[ .][^\]]*\]\([^)]+\)", text)}


def unlinked_problem_numbers(text: str, board: "set[str] | None" = None) -> list[str]:
    """Problem-looking numbers in `text` that appear nowhere inside a markdown link.

    `board` is the set of numbers actionable today (see `todays_board`). When given,
    only those are policed: an off-board number is context, and linking it is itself
    against the rule. `None` means the board could not be read, so every bare number
    is policed as before -- that fallback is deliberate, and is never silence.
    """
    if not PROBLEM_CUE.search(text):
        return []

    linked = " ".join(MD_LINK.findall(text))
    linked_numbers = set(LINKED_NUMBER.findall(linked))

    # Strip link constructs and known-noisy prose before scanning, so a number only
    # counts when it is genuinely a loose problem reference.
    bare = NOISE.sub(" ", CODE_SPAN.sub(" ", MD_LINK.sub(" ", text)))

    found: list[str] = []
    for num in NUMBER.findall(bare):
        if num in IGNORE or num in linked_numbers or num in found:
            continue
        if board is not None and num not in board:
            continue  # context, not a hand-over -- see todays_board()
        found.append(num)
    return found


# Re-enabled 2026-08-14 after the 10th lapse got past it. It was disabled on the day it
# was written because `last_assistant_text()` read only the FINAL assistant entry, which
# is almost always a `tool_use` record with no text. The replacement above gathers the
# whole turn. Note the disable-note's own proposed fix ("back to the last `user` entry")
# would still have been wrong: `tool_result` records are typed `user` and sit INSIDE a
# turn, so that boundary truncates mid-turn. The boundary is the last *human* message.
#
# The original unit tests passed on a hand-built transcript with one text entry per
# message — they exercised the regex, never the transcript SHAPE. Tests now run against
# a real `.jsonl` from this project (see `_selftest` below).


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    # Never block twice on one turn: the second pass is the corrected reply.
    if payload.get("stop_hook_active"):
        return

    text = last_turn_text(payload.get("transcript_path", ""))
    if not text:
        return

    nums = unlinked_problem_numbers(text, todays_board())
    # Already handed over in the last few turns? The file hunt is already saved.
    nums = [n for n in nums if n not in recently_linked(payload.get("transcript_path", ""))]
    if not nums:
        return

    json.dump(
        {"decision": "block", "reason": MESSAGE.format(nums=", ".join(nums))},
        sys.stdout,
    )


# ── Self-test ─────────────────────────────────────────────────────────────────
# `python .claude/hooks/problem_link_reminder.py --selftest`
#
# Two halves, and the SECOND is the one that matters. The Aug 12 version of this hook
# passed its tests and was still broken, because those tests fed a hand-built transcript
# with one text entry per message. Real transcripts split a turn across many assistant
# entries and interleave `tool_result` records typed `user`. So: point `--selftest` at a
# real `.jsonl` to exercise `last_turn_text` against the true shape.
CASES = [
    # (name, text, should_block)
    ("hand-over, bare", "Next on the board is **778 Swim in Rising Water**. Want 271 first?", True),
    ("restate, bare", "Remaining on the board: 155, 739. Which problem next?", True),
    ("sentence-final", "Next problem on the board: 155.", True),
    ("code span is not a link", "The `155` fix is done. Next problem on the board: 155.", True),
    ("multiple bare", "Your next problem on the board is 26, then 88.", True),
    ("correct pair", "Next: [778](dsa/leetcode/graphs/778_swim.py) · "
                     "[LC](https://leetcode.com/problems/swim-in-rising-water/)", False),
    ("complexity, exponent", "The trie has 26 children per node, so this rep is O(26^d), d up to 500.", False),
    ("complexity, bounds", "Time is O(E log V) for this problem, space O(V + E); the heap holds 6000 entries.", False),
    ("worked arithmetic", "For this problem the sum of the distances is 1+0+1+2 = 4, not the answer.", False),
    ("units and intervals", "The board is 7.8 units for this problem, ceiling 9.0; streak 2, +30 days.", False),
    ("dates and line refs", "Tracker row Aug 24, prior attempts Jul 13 and Aug 4; line 188; the Aug 17 build.", False),
    ("backticked examples", "On the board, `24` and `13` are dates and `188` is a line number.", False),
    ("turn references", "Catches turn 9 on the board; turns 1-4 stayed silent for this problem.", False),
    ("no cue word", "778 next?", False),
    ("file link only", "Scaffolded [739_daily_temperatures.py](dsa/leetcode/stack/739_daily_temperatures.py).", False),
    # Aug 15, 2026: the false positive that forced a link onto a verification count.
    ("randomized test count", "Verified this problem on 3000 randomized cases, zero mismatches.", False),
    ("case count", "The rep passed 500 cases and 250 runs on the board.", False),
]

# Board filtering is exercised separately: every entry in CASES runs with board=None,
# so those keep asserting the fallback behaviour, and these assert the scope limit.
BOARD_CASES = [
    # (name, text, board, should_block)
    ("on board, bare -> block", "Still on the board: 155 Min Stack.", {"155"}, True),
    ("off board, bare -> quiet",
     "This problem's technique now covers 496, 503 and 901.", {"155"}, False),
    ("mixed -> only the on-board one",
     "Coverage for this problem is 496 and 901; still on the board is 155.", {"155"}, True),
    ("board unknown -> policed as before",
     "This problem's coverage now holds 496 and 901.", None, True),
]


def _selftest(transcript: str | None = None) -> int:
    failures = 0
    for name, text, expected in CASES:
        got = bool(unlinked_problem_numbers(text))
        if got != expected:
            failures += 1
            print(f"FAIL  {name}: block={got}, expected {expected} -> "
                  f"{unlinked_problem_numbers(text)}")
    print(f"detector: {len(CASES) - failures}/{len(CASES)} passed")

    board_failures = 0
    for name, text, board, expected in BOARD_CASES:
        got = bool(unlinked_problem_numbers(text, board))
        if got != expected:
            board_failures += 1
            print(f"FAIL  {name}: block={got}, expected {expected} -> "
                  f"{unlinked_problem_numbers(text, board)}")
    failures += board_failures
    print(f"board:    {len(BOARD_CASES) - board_failures}/{len(BOARD_CASES)} passed")

    live = todays_board()
    shown = sorted(live, key=int) if live else "UNREADABLE -- policing every number"
    print(f"live board ({_session_date()}): {shown}")

    if transcript:
        text = last_turn_text(transcript)
        if not text.strip():
            failures += 1
            print("FAIL  last_turn_text returned nothing from a real transcript "
                  "-- this is the Aug 12 defect, do NOT ship")
        else:
            print(f"transcript: recovered {len(text)} chars of assistant text; "
                  f"bare = {unlinked_problem_numbers(text) or 'none'}")
    else:
        print("transcript: SKIPPED -- pass a real .jsonl path to exercise the shape")
    return 1 if failures else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        args = [a for a in sys.argv[1:] if a != "--selftest"]
        sys.exit(_selftest(args[0] if args else None))
    main()
