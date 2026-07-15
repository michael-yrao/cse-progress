# cse-progress — GitHub Copilot instructions

cse-progress is a personal **spaced-repetition study system** for technical-interview prep,
spanning DSA/algorithms and System Design (with an AI-engineering pillar). Solutions are
written by hand; a comfort-based review engine decides *what to review when*.

> **Source of truth:** [`AGENTS.md`](../AGENTS.md) is the agent-agnostic entry point and
> [`CLAUDE.md`](../CLAUDE.md) is the full workflow (comfort scale, review loop, guardrails,
> schedule rules). Read both before acting — the rules below are a summary, and those files win
> on any conflict.

## The contract (essentials)

1. **The learner writes all code and does all thinking.** No spoilers unless they're stuck or
   ask. Never paste a solution into a blank problem file.
2. **Comfort = infer, then confirm.** After a problem, infer 🟢 Clean / 🟡 Shaky / 🔴 Blank from
   the session and propose it for confirmation — don't ask an open "how did that feel?", don't
   log silently. Their call is final; flag a dishonest 🟢.
3. **Close the loop unprompted:** mark the week's schedule, update
   `docs/foundations/dsa/mastery/dsa_progress.md`, let the commit hook recompute the next review
   date, and re-slot the problem — never defer without assigning a new date.
4. **Log non-Clean results** in `docs/foundations/dsa/mastery/stuck_log.md` (🔴 full entry,
   🟡 one-liner).
5. **Batch commits** — edit as you go, commit + push once at session end (the pre-commit hook
   rewrites the tracker, so per-problem commits are expensive).

## Repository layout

```
cse-progress/
├── dsa/
│   ├── leetcode/<pattern>/<number>_<snake>.py   # active hand-written Python solutions
│   │      # patterns: 1d_dynamic_programming, arrays_and_hash, backtracking, binary_search,
│   │      #           graphs, greedy, heap, linked_list, sliding_window, stack, trees, trie,
│   │      #           two_pointers
│   └── archive/                                  # reference only: 2022_leetcode, 2026_replay,
│                                                 #   codeforce, other, typescript
├── docs/
│   ├── foundations/
│   │   ├── schedules/                # weekly day-by-day plans, ALL tracks (+ archive/)
│   │   ├── dsa/                      # study_guide.md, fundamentals/, patterns/, mastery/, templates/
│   │   ├── system_design/            # study_guide.md, fundamentals/, components/, technologies/, mastery/, templates/
│   │   └── ai_engineering/           # study_guide.md, templates/
│   └── archive/2022/                 # legacy .tex notes (LaTeX)
├── scripts/
│   ├── new_problem.py                # scaffolds a problem file (statement + blank stub)
│   ├── restore_history.py            # restores stashed prior attempts at session end
│   ├── update_review_dates.py        # Comfort→interval engine (runs on commit)
│   └── pull_interview.py
├── career/                           # resume + trajectory notes
├── image/                            # algorithm diagrams (svg/png)
├── cse.config.yml                    # engine settings
├── README.md · ROADMAP.md
├── CLAUDE.md                         # full workflow (source of truth)
└── AGENTS.md                         # agent-agnostic entry point
```

## File-naming convention (active set)

Solutions live at `dsa/leetcode/<pattern>/<number>_<snake_title>.py` — e.g.
`dsa/leetcode/graphs/743_network_delay_time.py`. The **problem number is the identity**.
Files are created by `scripts/new_problem.py`, never by hand; retries append a dated stub
(`def <method>_<YYYYMMDD>`) to the same file rather than making a new one.

> The old Java-style `Name_Number_Difficulty_Type.java` convention only applies to `dsa/archive/`.

## Comfort → next-review interval

| Comfort  | Meaning                              | Next review |
|----------|--------------------------------------|-------------|
| 🟢 Clean | Coded from blank page, no hints      | +30 days    |
| 🟡 Shaky | Got there with a nudge / peek        | +10 days    |
| 🔴 Blank | Couldn't recall; had to look it up   | +2 days     |

The intervals are computed by `scripts/update_review_dates.py`, which the version-controlled
`.githooks/pre-commit` runs automatically. Activate the hook once per clone with
`git config core.hooksPath .githooks`.

## Low-token / caveman mode

Under a low-credit setup: terse output, caveman-compressed problem statements, no recaps. The
rules above never change — only verbosity drops.
