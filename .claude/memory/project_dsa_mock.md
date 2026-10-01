---
name: project-dsa-mock
description: Recurring DSA mock interview — one cold unseen Medium/Hard plus a level raiser scored pass/partial/fail; 🎤 Sunday row, priced blank, never named in the schedule
metadata:
  type: project
reconciled: 2026-09-30
---

**The why behind [`references/dsa-mock.md`](../skills/cse-coach/references/dsa-mock.md)** (decision
`dsa-mock-interview-sep30`). The cadence is `dsa_mock.every_days` / `dsa_mock.first_due` in
`cse.config.yml`; the log is [`docs/foundations/dsa/mocks/README.md`](../../docs/foundations/dsa/mocks/README.md).

**The shape — Google/Amazon: one problem, then escalate.** The learner asked for "a Medium/Hard, then a
level raiser". Research (retrieved Sep 30, 2026):

- Google: 45 min, one problem, "followed by harder constraints or optimization questions"; adaptability
  (reusing work, revising under changed requirements) is its own scored axis. Sources:
  [PracHub Google guide 2026](https://prachub.com/resources/google-coding-interview-guide-2026-question-types-gca-and-how-to-think-out-loud) ·
  [copilotinterview Google](https://copilotinterview.com/blog/google-coding-interview-questions) ·
  [carrus.io](https://www.carrus.io/blog/crack-the-google-coding-interview)
- Amazon: SDE-II is "solve medium independently; handle one hard follow-up"; the follow-up is how level is
  read. Source: [copilotinterview Amazon](https://copilotinterview.com/blog/amazon-coding-interview-questions)
- The follow-up types (constraint change, complexity probe, correctness challenge, trade-off interrogation,
  rewrite) and the answer discipline (restate the delta, name what survives, trade-off first, code second).
  Sources: [interviewco.ai](https://interviewco.ai/blog/coding-interview-follow-up-questions) ·
  [interviewing.io BCtCI ch. 0-2](https://interviewing.io/blog/beyond-cracking-the-coding-interview-chapters-0-2-full-text)
- Escalation pairs (grid beyond memory, interval stream, API shape): copilotinterview Amazon and Google, and
  [dev.to Amazon SDE prep](https://dev.to/ifa_tade_d2a8607e4537b0fa/how-to-prepare-for-an-amazon-sde-coding-interview-4j2j)
- Not built now, reachable later from the same slot: Meta's two problems in 45 min
  ([hellointerview Meta E5](https://www.hellointerview.com/guides/meta/e5)), Apple/Netflix depth on a medium
  ([PracHub Apple](https://prachub.com/resources/apple-software-engineer-interview-the-complete-guide-2026),
  [Prepfully Netflix](https://prepfully.com/interview-guides/netflix-software-engineer)). The move bank's
  productionize, tighten-the-bound and relax-an-assumption moves carry those flavours.
- Interviewer craft: the best interviewers know the problem's rabbit holes and lay out structure at the
  outset ([interviewing.io](https://interviewing.io/blog/best-technical-interviews-common)).

**Design choices and why**

- **Adaptability, not comfort, scores the level raiser.** "Seen before" cannot matter for a pass/fail on
  adaptability, and one rating proposal per turn keeps `rating_gate.py` single-fire.
- **The base problem earns a tracker row always.** A Medium/Hard coded cold is an asset, unlike a 🟢 probe.
  The level raiser earns no row, so the mock adds no permanent demand beyond the base.
- **Sunday replaces the probe.** The mock is that week's unseen problem; priced as a 🔴 blank at the named
  difficulty so `every-coded-row-priced-sep29` holds.
- **Reuses the `dsa/probes/` path.** `new_problem.py --mock` writes outside `solutions.roots`, so no auto
  row and no technique-spoiling folder. After the debrief the file is moved into `dsa/leetcode/<category>/`
  with `git mv` in the same edit as the tracker row; `check_phantom_scaffolds.py` catches either half
  missing.
- **Debriefs are public.** The SD privacy boundary was only premium HelloInterview excerpts; none here.
- **Hook over prose.** The integrity script runs at pre-commit on the current week, too late for the build,
  so the SessionStart banner reads the config and the log and fires when a mock is due.
