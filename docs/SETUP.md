# Repo Setup (one-time per machine/clone)

> Moved out of `CLAUDE.md` on Aug 3, 2026. It is read **once per machine, ever**, but it was loading
> into every session's context (~850 est. tokens/turn). The rules that must fire *unprompted* stayed
> in `CLAUDE.md`; this is the setup mechanics only.

⚠️ **As of Aug 19, 2026, `.claude/settings.json` is COMMITTED, not gitignored** — steps 2–4 below now
sync automatically on clone/pull and need no manual paste. It was gitignored on the stated grounds that
it "holds machine-absolute paths"; the actual content (`${CLAUDE_PROJECT_DIR:-.}`-relative hook commands)
never held one, so that was stale caution rather than a real constraint, caught after the wiring sat
missing on a machine for an unknown stretch and the link-hand-over rule lapsed unrecoverably every
session on it. **Only `.claude/settings.local.json` (personal permission overrides) stays gitignored** —
that one genuinely is per-machine. Steps 2–4 are kept below as the record of what the committed file
contains and why, not as manual work.

**Read this note if you're an agent working from an older or newly-created checkout:** the committed
`.claude/settings.json` reflects whatever was known to wire in as of the commit that last touched it —
it is not guaranteed to carry every hook this repo has ever described. If `docs/SETUP.md` or
`CLAUDE.md` names a hook you don't find in the file, that's drift to fix (add it, don't assume it was
deliberately dropped), not a sign the file is malformed.

⚠️ **Hook commands must probe `python3`/`python`, never name a bare interpreter (Aug 21, 2026).** On a
machine where `python` resolves to nothing (e.g. macOS with only a `python3` framework install), a
settings.json hook wired as `python "…hook.py"` **fails silently on every fire** — the Stop link-reminder
and the SessionStart memory injector both went dark this way, undetectable until a rule lapsed in front
of the learner. All three hook commands now use the pre-commit hook's idiom —
`if command -v python3 …; then python3 "…"; else python "…"; fi` — so they run on any machine. If you
add a hook, use that form, not a bare `python`/`python3`.

One remaining one-time step. Do it on a fresh clone.

## 1. Git hooks path

The pre-commit hook that auto-updates the spaced-repetition tracker is **version-controlled** in
`.githooks/`. To activate it on a machine, run once:

```sh
git config core.hooksPath .githooks
```

This replaces the old per-machine `.git/hooks/pre-commit` (which was never synced). After this, the
hook stays in sync via git across all machines.

## 2. The scaffold-links agent hook

`.claude/hooks/scaffold_links_reminder.py` is version-controlled, and — as of Aug 19, 2026 — so is
the wiring that invokes it: `.claude/settings.json` is committed (see the note at the top of this
file), so this block arrives automatically on clone/pull. Recorded here as documentation of what's in
it, not as a step to perform:

```json
"hooks": {
  "PostToolUse": [
    {
      "matcher": "Bash|PowerShell",
      "hooks": [
        { "type": "command",
          "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/scaffold_links_reminder.py\"",
          "timeout": 10 }
      ]
    }
  ]
}
```

It fires on a shell command that actually **invokes** `new_problem.py` (matched as
`new_problem.py … --number`, since `--number` is required by the script's argparse) and reminds the
agent to emit both the local file link and the problem-page link for every problem it just
scaffolded — a rule that lapsed five times while it lived only as prose. Costs nothing until it
fires. See `.claude/memory/feedback_kickoff_table_links.md`.

⚠️ **This hook is now the backup, not the enforcement.** As of Aug 3, 2026 `new_problem.py` prints
the links itself (`report_links()`), so they arrive as tool output on every machine regardless of
whether this block was ever pasted. That change was forced by the 6th lapse: the matcher read
`"Bash"` alone, and a scaffold run through the **PowerShell** tool skipped the hook silently. The
matcher above is widened, but the lesson is the general one — *a hook that depends on a tool matcher
plus a gitignored config has two ways to not exist, and the script has none*.

⚠️ The trigger was a bare substring until Aug 2, 2026, which also matched `grep`s and read-only
commands that merely *mentioned* the script. Tightened because **a hook that cries wolf trains the
agent to skim past it** — which costs precisely the reliability that makes a hook stronger than a
written rule.

## 3. The problem-link Stop hook

`.claude/hooks/problem_link_reminder.py`, wired the same way — both script and wiring are tracked now.
The block, for reference:

```json
"Stop": [
  {
    "hooks": [
      { "type": "command",
        "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/problem_link_reminder.py\"",
        "timeout": 10 }
    ]
  }
]
```

**What §2 cannot reach, and why this exists.** The scaffold hook and `new_problem.py`'s own `LINKS:`
line both key off a *tool invocation*, so they cover the moment a file is created and nothing else.
The dominant remaining failure is the **mid-session restate** — *"next is 778"*, *"still on the board:
271, 155"*, a hand-over, a *"what's next"*. No tool runs, so nothing fires, and the rule falls back to
recall. It has lapsed **nine times** that way (Jul 20/21/23/30/31, Aug 3, Aug 5, Aug 6, Aug 12, 2026);
the Aug 6 entry in `.claude/memory/feedback_kickoff_table_links.md` named this exact hook as the fix
and it sat unbuilt for six days, through one more lapse. That gap is the point: *a candidate fix
recorded in prose is still prose.*

At Stop it reads the last assistant message and blocks once if a problem-looking number appears
outside any markdown link, naming the offending numbers. Three guards keep it quiet, all for the
cry-wolf reason in §2: the turn must carry a problem cue word (so complexity talk about `26` children
or `10^4` calls never trips it); a number linked *anywhere* in the turn counts as linked for the whole
turn; and `stop_hook_active` short-circuits so it can never loop.

⚠️ **It restates the spoiler exception rather than assuming it away.** In a *selection menu* where the
learner has not picked yet, an unscaffolded retry's file link opens their prior solution — there, LC/NC
only is correct and the block should be answered by saying so, not by adding file links. A hook that
demanded links unconditionally would automate a spoiler.

## 4. The session-start memory hook

Same deal: the script (`.claude/hooks/session_start_memory.py`) is version-controlled, and the wiring
now travels with it. For reference:

```json
"SessionStart": [
  {
    "hooks": [
      { "type": "command",
        "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/session_start_memory.py\"",
        "timeout": 10 }
    ]
  }
]
```

It injects `.claude/memory/MEMORY.md` — plus the five gates that must fire unprompted — at session
start, resume, clear, and post-compact. **Unlike the other two hooks this one is not free: ~3.6k
tokens per fire.** That is the deliberate price of the thing it fixes. On 2026-08-02 the memory index
was never loaded at all until the learner asked about it nine turns in, so the complexity gate and
the self-eval loop weren't ignored — they were *absent*, and both failed in the same session. The
rule "read MEMORY.md at session start" is itself a rule about starting a session, and a session that
opens with a bare technical question doesn't feel like a start. Removing that judgement call is the
whole point.

If the token cost bites, drop `compact` from the fire list first — startup/resume/clear are the
load-bearing ones.
