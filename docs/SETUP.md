# Repo Setup (one-time per machine/clone)

> Moved out of `CLAUDE.md` on Aug 3, 2026. It is read **once per machine, ever**, but it was loading
> into every session's context (~850 est. tokens/turn). The rules that must fire *unprompted* stayed
> in `CLAUDE.md`; this is the setup mechanics only.

Three one-time steps. Do all three on a fresh clone.

## 1. Git hooks path

The pre-commit hook that auto-updates the spaced-repetition tracker is **version-controlled** in
`.githooks/`. To activate it on a machine, run once:

```sh
git config core.hooksPath .githooks
```

This replaces the old per-machine `.git/hooks/pre-commit` (which was never synced). After this, the
hook stays in sync via git across all machines.

## 2. The scaffold-links agent hook

`.claude/hooks/scaffold_links_reminder.py` is version-controlled, but `.claude/settings.json` is
**gitignored** (it holds machine-absolute paths), so the wiring that invokes the script does *not*
sync. On each machine, add this block to `.claude/settings.json` once, merging with whatever
`permissions` are already there:

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

## 3. The session-start memory hook

Same deal: the script (`.claude/hooks/session_start_memory.py`) is version-controlled, the wiring is
not. Merge this into the same `hooks` block:

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
