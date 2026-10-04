---
name: project_kattis_rebuild_followups
description: Open items left by the Oct 4, 2026 Kattis rebuild (9002/9003 specs) and the site's Over workload band — none blocks anything; pick up when the trigger arrives
metadata:
  type: project
reconciled: 2026-10-04
---

**Open items from the Oct 4, 2026 session** that rebuilt the queued Kattis problems on progressiveoverflow (decision `external-judge-plain-values-oct4`) and added the purple `Over` workload band to the site. Each is optional until its trigger. Delete an item when it is done; delete this file when the list is empty.

| # | Item | Where | Trigger |
|---|---|---|---|
| 1 | **Over band never seen rendered.** The site's full unit suite and build failed locally on compile errors in the learner's uncommitted interview work (`interview-session.service.ts`, `session-store.ts`, `session-id.ts`), so the purple bar and the `Over` label were checked by unit test only. | site repo, `/progress` Activity chart and Today board | next time the site builds locally, or on the live site after a day goes over the ceiling |
| 2 | **`role_gate.py` false positives.** It denied a read-only `git stash list` (matches `stash`) and a `python -c` whose comparison used `>` (matches the redirect pattern). One retry each. Narrowing a guardrail is the learner's call; it was not touched. | `~/.claude/hooks/role_gate.py` | the learner says to narrow it |
| 3 | **9002's `Tuple` annotation.** The spec signature is `rates: List[Tuple[str, str, float]]`, but `solution_template.py` imports only `List` (and `Optional`). It runs today: local Python defers annotations and the site's driver does `from typing import *`. The cases pass lists, so `List[list]` would be the honest type. | `dsa/tests/9002_arbitrage.yml`, `docs/foundations/dsa/templates/solution_template.py` | before 9002 is scaffolded |
| 4 | **Two purples.** `--color-over: #c084fc` sits beside `--color-trophy: #a78bfa`. Not checked whether both ever appear in one view; if they do, one mark reads two ways (`~/.claude/rules/interface-design.md`). | site `src/styles.scss` | a view that shows a trophy mark next to a workload bar |
| 5 | **`new_problem.py` / `update_review_dates.py` session date.** A dirty tree reads as "a session started yesterday". When the session itself dirtied the tree (edits before a scaffold), the stamp is one day early; 9003's Attempt 1 was corrected by hand to 2026-10-04. Pass `--date` in that case, or make the heuristic look at what is dirty. | `scripts/new_problem.py`, `scripts/update_review_dates.py` | the next scaffold run after same-session edits |
| 6 | **`practice.json` size.** 9002 and 9003 added about 168 KB (the file is about 1.5 MB, downloaded whole by the site), most of it 9003's matrices, pretty-printed one number per line. `spec.md` now caps a case line at about 1,500 characters. Further cuts: drop 9003's n ≥ 10 cases, or have `export_practice.py` write inner lists compactly. | `dsa/tests/9003_lost_map.yml`, `scripts/export_practice.py` | the practice page feels slow to load, or the next matrix-input spec |

Relates to [[project_grounded_solutions]] and [[project_site_refresh_resume]].
