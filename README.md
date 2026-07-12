# cse-review

A personal, spaced-repetition study system for technical-interview prep — spanning **DSA/algorithms** and **system design**, from NeetCode-150 interview readiness toward competitive-programming and architect-level depth.

Solutions are written by hand; progress is tracked with a comfort-based spaced-repetition schedule that decides *what to review when*. Drive it conversationally from [Claude Code](https://claude.com/claude-code) (recommended) — or another agent (Copilot, caveman) via [`AGENTS.md`](AGENTS.md) for a lower-credit option.

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
├── CLAUDE.md                       # working conventions for the AI pair-partner (Claude Code)
└── AGENTS.md                       # agent-agnostic entry point (Copilot, caveman, …)
```

## How the spaced repetition works

Every problem is logged in `docs/foundations/dsa/mastery/dsa_progress.md` with a **comfort** rating — inferred from the session and proposed for you to confirm — that sets its next review:

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
- **LeetCode company-wise questions** — a **reference pool** to *pull* application problems from once NC150 is solid, gated by patterns you've already learned. Not a checklist to follow. See "Post-NC150 — The Steady State" in the DSA study guide. Repos go stale, so a few options (freshest first, as of July 2026):
  - [snehasishroy/leetcode-companywise-interview-questions](https://github.com/snehasishroy/leetcode-companywise-interview-questions) — **primary**; snapshots through May 2026, recency buckets (last 30 days → all-time) + frequency data.
  - [krishnadey30/LeetCode-Questions-CompanyWise](https://github.com/krishnadey30/LeetCode-Questions-CompanyWise) — fallback; sorted by frequency and all-time.
  - [jobream/Leetcode-Company-Wise-Problems](https://github.com/jobream/Leetcode-Company-Wise-Problems) — fallback; PDF-per-company from LeetCode premium tags.
  - [MysteryVaibhav/leetcode_company_wise_questions](https://github.com/MysteryVaibhav/leetcode_company_wise_questions) — fallback.

  If all are stale when you reach the application phase, search GitHub for "leetcode company wise questions" sorted by recently-updated and pick the freshest.

*Happy coding!*
