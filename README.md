# cse-review

A personal, spaced-repetition study system for technical-interview prep — spanning **DSA/algorithms** and **system design**, from NeetCode-150 interview readiness toward competitive-programming and architect-level depth.

Solutions are written by hand; progress is tracked with a comfort-based spaced-repetition schedule that decides *what to review when*.

## Repository layout

```
cse-review/
├── dsa/leetcode/<type>/*.py        # solution files (arrays_and_hash, graphs, linked_list, …)
├── docs/
│   └── foundations/                # the two study tracks
│       ├── dsa/
│       │   ├── study_guide.md      # master plan, phases, pace, ROI line
│       │   ├── fundamentals/       # concept references (e.g. big_o.md)
│       │   ├── patterns/           # the pattern library (see below)
│       │   ├── mastery/            # spaced-rep record: dsa_progress.md + stuck_log.md
│       │   └── schedules/          # weekly day-by-day plans (+ archive/)
│       └── system_design/
│           ├── study_guide.md      # mission, Interview-ROI line, tiers
│           ├── fundamentals/       # concept notes
│           └── templates/          # blank scaffolds to fill during practice
├── scripts/update_review_dates.py  # recomputes review dates + sorts the tracker
├── .githooks/pre-commit            # auto-runs the script on commit (version-controlled)
└── CLAUDE.md                       # working conventions for the AI pair-partner
```

## How the spaced repetition works

Every problem is logged in `docs/foundations/dsa/mastery/dsa_progress.md` with a **comfort** rating that sets its next review:

| Comfort | Meaning | Next review |
|---------|---------|-------------|
| 🟢 Clean | solved from a blank page, no hints | +30 days (+60 on a 2-streak, then retired) |
| 🟡 Shaky | needed a nudge or peeked | +10 days |
| 🔴 Blank | couldn't recall the approach | +2 days |

Weekly `schedules/` are built from those due dates. Non-Clean attempts get an entry in `stuck_log.md` (full write-up for Blank, one-liner for Shaky) so retries are rebuilds, not cold starts.

## The pattern library

`docs/foundations/dsa/patterns/` — the reusable problem-solving reference:
- **`techniques/`** — one atomic technique per file (sliding window, monotonic stack, union-find, …): recognition → template → practice ladder → pitfalls.
- **`data-structures/`** — hub pages mapping a data shape to the techniques you reach for.
- **`intuition_cheatsheet.md`** — fast problem-signal → technique triage.
- **`../fundamentals/big_o.md`** — complexity of every technique + data structure.

Start at [`patterns/README.md`](docs/foundations/dsa/patterns/README.md).

## Setup (one-time per machine)

Activate the version-controlled git hook so the tracker auto-updates on commit:

```sh
git config core.hooksPath .githooks
```

## Roadmap

This is currently a personal system; the goal is to make it a **reusable template** other developers can fork. Progress toward that is tracked in [`ROADMAP.md`](ROADMAP.md).

## External resources

- [NeetCode](https://neetcode.io/) — start with Blind 75, then NeetCode 150.
- [LeetCode questions by company frequency](https://github.com/xizhengszhang/Leetcode_company_frequency)

*Happy coding!*
