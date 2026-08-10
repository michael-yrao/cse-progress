# 🎯 Recognition probes

**One unseen LeetCode problem per week, label stripped, solved cold.** Adopted Aug 9, 2026 — full
rationale in `.claude/memory/project_recognition_probes.md`.

## Why this directory exists at all

Two reasons, and both are structural rather than cosmetic.

**1. The normal scaffold path is a spoiler.** `new_problem.py` writes to
`dsa/leetcode/<pattern>/<number>_<name>.py` — so the *folder name tells you the technique* before you
have read the problem statement. For every other rep that is harmless. For a probe it destroys the only
thing being measured.

**2. It keeps probes out of the tracker automatically.** `cse.config.yml` sets
`solutions.roots: ["dsa/leetcode"]`, and `update_review_dates.py` auto-creates a tracker row for any
file it discovers under those roots. `dsa/probes/` sits **outside** that root, so a probe file is never
discovered and no `discovery_skip` entry is ever needed. That is the preferred handling for
**disposable reps** — the stopgap is `discovery_skip`, and stopgaps rot.

> ⚠️ **Never move this directory under `dsa/leetcode/`, and never add `dsa/probes` to
> `solutions.roots`.** Either change silently resurrects a tracker row for every probe ever run, which
> is the whole cost this design avoids.

## The rules

| | |
|---|---|
| **Cadence** | 1/week, in the Sunday slot unless the week says otherwise |
| **Pull from** | techniques already at **🟢 or 🎓** in `technique_coverage.md`, **Medium or below** |
| **Never pull from** | anything 🟡 or with no 🟢 — those need *conversion reps*, and a probe there just manufactures a 🟡 row at ~73 units/year |
| **Label** | stripped. No pattern name, no topic tag, no "this is like problem X" |
| **The measured thing** | the **pre-code call** — shape → technique → the one feature that picks it. The code is secondary |

## What gets logged

- **Always** → the recognition call (hit or miss) to
  [`recognition_gotchas.md`](../../docs/foundations/dsa/mastery/recognition_gotchas.md).
- **🟢 → no tracker row.** The probe was a test of whether the *technique* transfers, not an asset to
  maintain.
- **🟡 / 🔴 → it earns a row**, because only a gap needs repetition.

## The free diagnostic

Because a 🟢 creates no row and a 🟡/🔴 does, **the row-creation rate over a rolling ~15 probes *is* the
measure of whether the pool still teaches anything**:

- **≥85% 🟢** → the pool has stopped teaching; open the next expansion tier.
- **≤70% 🟢** → real gaps remain; keep consolidating.
