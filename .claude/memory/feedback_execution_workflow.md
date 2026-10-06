---
name: feedback-execution-workflow
description: Tech lead plans, owns optimization and hands the rest down; Opus team leads supervise Sonnet engineers who implement; tech lead reviews the consolidated diff before any commit/push — GLOBAL, three-tier pyramid at a 2:1 spawn ratio, for all non-trivial work (evidence/why for the always-on gate in ~/.claude/rules/execution-workflow.md)
metadata:
  type: feedback
reconciled: 2026-09-21
---
**NORMATIVE SSOT is the always-on global rule** `~/.claude/rules/execution-workflow.md` (auto-injected
in every repo), enforced by the global `UserPromptSubmit` hook
`~/.claude/hooks/execution_workflow_reminder.py`. This file is the *why/evidence/occurrence* layer only —
it must never be the only place the rule is stated.

**Widened 2026-09-21 (later the same day) by the learner — three-tier pyramid:** tech lead = the
orchestrating session (Fable on Max, Opus otherwise), Opus team leads at a 2:1 engineer:lead ratio
(ceil(n/2) leads, ≤ 2 engineers per lead, 1 engineer → the tech lead supervises direct), Sonnet engineers.
Roles are enforced as custom agent definitions — `~/.claude/agents/team-lead.md` and `engineer.md`
(model pinned, `disallowedTools` blocks Write/Edit on the lead) — not prose only. **Subagents are never
Fable** — Fable stays the orchestrating session; leads are Opus, engineers are Sonnet, pinned explicitly
(never `model: inherit`, never a Fable override on an Agent call). **Why:** the Max plan removes the cost
pressure that kept the tree flat; a lead per 2 engineers keeps review close to the diff while the session
stays on judgement; pinning the model and removing the editing tools in the definitions is stronger than
a prose "never writes" — but the lead keeps Bash for test runs, so the no-writing rule is part enforced
(the tools are gone) and part convention (Bash could still write; the lead just doesn't). See `decisions.yml`
`execution-workflow-pyramid-sep21`.

**Broadened 2026-09-21 by the learner:** from the gamification/site-integration scope to **all
non-trivial work, across every repo** (global), **strongly enforced** (gate + reminder hook), triggered
on **non-trivial work only** (trivial one-liners/typos/reads run inline). See `decisions.yml`
`execution-workflow-global-sep21`.

**Refined 2026-09-21:** the Opus role never writes implementation — it plans/supervises/advises/reviews/
integrates only; all edits go to Sonnet engineer subagents (spawn as many as needed).

**Set 2026-09-20 by the learner** for the gamification / site-integration work (cse-progress
`progress.json` + the progressiveoverflow.com dashboard).

| Tier | Model | What |
|---|---|---|
| Tech lead | the session (Fable on Max, Opus otherwise) | design, write the plan, get approval, review the consolidated diff, integrate, optimize (spend, wall-clock, shipped code, the workflow); hands down what does not need it |
| Team lead | Opus (`team-lead` agent) | own one plan slice, brief/supervise ≤ 2 engineers, review their diffs (correctness, scope, wasted work), optimize the slice's code through its engineers, report up |
| Engineer | Sonnet (`engineer` agent) | execute a brief — edits, tests, build; report the diff |

**Why:** the learner wants planning/judgement on the stronger model and mechanical execution on the
faster/cheaper one, with an Opus review gate so nothing lands unreviewed. Mirrors the repo's
deliberative-vs-mechanical register split.

**How to apply:** Opus spawns a Sonnet 5 subagent (`model: "sonnet"`) with the approved plan as its
brief; the subagent does NOT commit/push; Opus reviews, then commits/pushes per the
standing no-PR instruction.

**Extended 2026-09-20 to the weekly EOW schedule build** (learner's call). The Sunday close-out runs the
same split: **Opus** prices/designs the build (capacity, pulls, day placement — the judgement), a
**Sonnet 5 subagent** does the mechanical writeback only (`git mv` the archive, write the next-week
schedule file from the approved plan, run the checker scripts — no commit/push), **Opus** reviews the
diff, then commits/pushes. ⭐ Only the mechanical writeback goes to the subagent — never
the planning, and never a teach or a rep. Operational home for the build steps:
`.claude/skills/cse-coach/references/weekly-build.md`. See `decisions.yml` `eow-close-out-process-sep20`.

**Hardened 2026-09-21 from reminder-only to tool-level deny gates** (learner's call: "tackle the
enforcement layer first"). `~/.claude/hooks/role_gate.py` is a PreToolUse hook wired ONCE in
`~/.claude/settings.json` (matcher `Write|Edit|NotebookEdit|Bash`). Settings hooks fire inside
subagents with `agent_type` set, so one script branches per role: team-lead is denied file-write tools,
Bash writes matching a named pattern list, and all state-changing git; engineer is denied state-changing
git; the tech lead (no `agent_type`) gets a warn-only note on its first write of a session. What is
still convention: any Bash write path not in the pattern list; a lead spawning only `engineer`.
**Evidence that matters:** (1) agent-frontmatter `hooks:` blocks did NOT fire — an engineer spawned
after the edit ran `git add --dry-run` unblocked and a trace line showed the hook was never invoked;
the settings.json path denied the same command with the correct reason. Docs said frontmatter hooks
work; the harness disagreed. Enforcement wiring is proven by a live probe, never by docs. (2) The
agent-row UI label reads the SESSION model ("engineer · Fable 5.1"), not the pinned one; the subagent
transcript's `model` field is the ground truth and showed `claude-sonnet-5` on every engineer turn.
(3) The prompt reminder's trivial-suppressor was leaky both ways (silenced "implement X, here's how";
fired on "before i move forward, is this expected") and, in its first rewrite, silenced "can you
implement X" — now polite openers are stripped and an implementation verb in first position wins.
See `decisions.yml` `role-gate-deny-hooks-sep21`.

**Observed 2026-09-23 — a team lead cannot block on its engineers.** A `team-lead` that spawns its two
engineers in the background is force-handed-back as soon as its own turn ends, with the engineers still
running; the engineers' completion reports then route to the TECH LEAD (the spawner's spawner), not back
to the lead. So the lead's review step only happens if the tech lead resumes it via `SendMessage` after
both engineer reports have arrived ("both engineers done; review now"). Budget for it: each lead costs two
extra hand-backs (interim + final) and the tech lead does the collation. The engineers themselves, and
the lead's review once resumed, worked as designed — including a lead sending fixes back to an engineer.

**Observed 2026-09-23 (later, games slice) — a workaround that lets the lead stay resident.** The lead
had each engineer create an empty done-marker file in the session scratchpad on completion and waited
for both markers with a short `ping`-sleep loop in Bash, so its own turn never ended while engineers were
still running. Both engineer reports then came back to the lead as designed, the lead ran its review and
one rejection round per engineer, and the tech lead received a single consolidated hand-back — no interim
hand-backs, no `SendMessage` resume. Cost: engineers flag the marker request as unusual (harmless, the
files sit outside the repo). Prefer this over the resume dance when a lead supervises two engineers.

**Decided 2026-10-04 — only user-facing text waits on the user.** Asked to approve a skill-file paragraph
inside a link-order plan, the learner said: *"update the rule such that non-user facing wording does not need
my approval."* The review rule in `~/.claude/rules/execution-workflow.md` now names user-facing text (site
labels and copy, README, docs written for a reader) as the only text held for the user's yes; rule, skill and
memory files, `decisions.yml`, code comments, commit messages, fixtures, ledger and tracker entries land on the
tech lead's review. The paragraph-quote rule narrowed the same way: for non-user-facing text the tech lead
checks old against new itself for a dropped sentence or citation (the 2026-09-29 failure it guards).

**Widened 2026-10-04 (later the same day) — the tech lead owns optimization and keeps only what needs it.**
The learner, in four messages: *"update the workflow such that the tech lead is also responsible for
optimization, especially for fable"*; asked what optimization covers (token spend, wall-clock, shipped-code
efficiency, the workflow itself), *"all of the above, tech lead is responsible for them all"*; then *"this
gives the tech lead a lot more responsibilities so if more team leads and engineers are required to
alleviate tasks that are not required to be done by tech lead, this should be done as well"*; and *"how that
capacity is determined is up to your discretion for now"*. The rule in `~/.claude/rules/execution-workflow.md`
("The tech lead owns optimization, and keeps only what needs it") now names the four costs with the step
each is checked at, lists what stays with the tech lead (the design, the plan, the exchange with the user,
the consolidated review, commit/push, the cost decisions) and what goes down (sweeps, state collection for
briefs, supervision and the first diff review, checker runs), and lets one engineer have a lead when
supervising it would fill the tech lead's context. The team lead's review gained an efficiency pass.
**Why:** the rule had no owner for cost; on Fable the session's own context is the most expensive in the
tree, so moving legwork to an Opus lead or a Sonnet engineer is itself the saving; and a wider role only
holds if the legwork moves down. How many agents to spawn is the tech lead's call for now: no formula was
set. See `decisions.yml` `tech-lead-owns-optimization-oct4`.

**Removed 2026-10-04 — the last of `advisor`.** The advisor review step was retired on 2026-09-22 (learner's
call; dotfiles commit `52c73d7`). It had no tool behind it then: the site-refresh note of that week reads
"`advisor` in the workflow rule has no tool behind it here; the tech lead's own diff review plus the
`code-review` skill (Sep 21) served as the review gate." On 2026-10-04 the learner said *"let's get rid of
advisor if it does not work as expected"*. It still did not: the Fable session had `"advisorModel": "opus"`
in `~/.claude/settings.json` and was offered no advisor tool. Removed that day: the `advisorModel` setting,
the "no separate advisor" wording in the rule and the reminder hook, the "run `advisor`" step in
`weekly-build.md`'s Review row, and the two older mentions in this file. The lead's own review is the gate.
See `decisions.yml` `advisor-removed-oct4`.

**Widened 2026-10-04 (third change that day) — the team lead is responsible for code optimization inside its
slice.** The learner: *"let's also give team lead the ability to optimize code"*, then corrected the word:
*"responsibility*"*. Before this the lead flagged waste and the decision sat with the tech lead. Now the lead
decides the optimization and has its engineer make it without asking up, as long as the slice's behaviour
and scope stay the same; anything that would change either goes up. The lead still writes no code: its
Write/Edit tools stay removed and the role gate is unchanged. With no lead, the responsibility is the tech
lead's. **Why:** the lead is closest to the diff, and a round trip to the tech lead for each fix spends the
Fable context the same day's change set out to save.

**Observed 2026-10-05 — leads could not run git, node or tests, and PowerShell was ungated.** On this Windows
machine the Bash tool's PATH has no `git`, `node` or `python`, and a `team-lead` had only Bash, so three lead
rounds reviewed by reading files and relaying their engineers' pasted output. The role gate matched only
`Bash`, so a state-changing git command run through PowerShell by an engineer was not gated. One lead, after a
`SendMessage` fix round resumed its engineer in the background, held its turn open with a 120 s Bash busy-loop;
two leads that spawned a fresh foreground engineer with a self-contained brief had no such problem. **Fix:**
`PowerShell` added to the lead's tools, the gate extended to PowerShell in the same change (matcher, write
cmdlets and aliases, `-OutFile`, .NET file writes, `$null` redirect exception), and fix rounds re-spawned in the
foreground.

**Observed 2026-10-05 (later) — an engineer's shell write script emptied a 792-line file.** Extracting code
from the site's `interview-session.service.ts`, a Sonnet engineer ran a PowerShell edit script that read the
file through .NET `ReadAllText` with a relative path; the shell's working directory was cse-progress, not the
site repo, so the read failed silently and the `Set-Content` that followed wrote an empty file. The engineer's
restore (`git show HEAD:… | Set-Content`) was denied by the permission classifier; the lead escalated instead
of routing the restore to another engineer (correct: that would launder the denial), and the tech lead asked
the learner before running `git restore` on the one file. Cost: one slice-B run after its first step, a
slice-C engineer idle 15 minutes, one lead round. **Fix:** `~/.claude/agents/engineer.md` now says file
content is changed with Edit/Write only, never through a shell script, and every path is absolute; every
brief repeats it. Not done: a role-gate deny on relative-path shell writes (the learner chose the rule alone).
