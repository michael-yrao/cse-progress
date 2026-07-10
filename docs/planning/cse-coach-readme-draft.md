# cse-coach

> **Draft** — intended `README.md` for the new `cse-coach` repo (see
> `cse-coach-extraction-design.md`). Written in the coach voice; teaches the
> interaction model first.

**A spaced-repetition coach for technical mastery — DSA, System Design, and AI
Systems.** You don't fill out a tracker. You *talk to your coach*, and it handles
the scheduling, the spaced repetition, and keeping you honest — so you just show
up and do the reps.

---

## The one thing to understand first

**This repo is a coach, not a spreadsheet.** You work with it through
conversation, the same way you'd work with a real mentor sitting next to you:

- You tell it when you're **starting** a problem. It sets up your file.
- You ask it questions while you work. It won't hand you the answer — that's the point.
- You tell it how it **felt** when you're done. It grades honestly, logs it, and
  schedules your next review for you.

You never manually edit the tracker, compute review dates, or plan your week.
**Your only job is to do the reps and answer one question honestly: "Clean,
Shaky, or Blank?"** The coach does the rest.

Open the repo in Claude Code and just talk to it in plain language. There are no
commands to memorize.

---

## Getting started (about 2 minutes)

1. Click **Use this template** on GitHub → clone your copy.
2. Open it in [Claude Code](https://claude.com/claude-code).
3. Say **"set me up"** (or run `/cse-init`). Your coach asks a handful of
   questions all at once — your name, start date, what you're aiming for, how
   many problems a day is realistic, your language, and which pillar to start
   with. Answer them in one pass.
4. That's it. It builds your roadmap, your first week's schedule, and installs a
   git hook that keeps your review dates current automatically.

> **One-time, per machine:** run `git config core.hooksPath .githooks` so the
> auto-scheduler runs on commit. (The setup step does this for you.)

---

## How you actually use it, day to day

It's a conversation. Here's a real one:

```
You:   Starting Two Sum.
Coach: Nice — set up dsa/leetcode/arrays_and_hash/1_two_sum.py for you with
       today's attempt banner. It's yours to write. Go.

You:   Can the array have duplicate values?
Coach: Yep, it can. (Ask me anything about the problem — I'll clarify freely.
       I just won't hand you the approach unless you're truly stuck.)

You:   Done.
Coach: How did that feel — Clean, Shaky, or Blank?

You:   Clean.
Coach: Logged 🟢 Clean. I'll bring it back in ~30 days and I've already put it
       on your schedule for Aug 12. Next up whenever you're ready: Valid Anagram.
```

Three moves, every problem:

| You say… | The coach does… |
|----------|-----------------|
| "Starting `<problem>`" | Scaffolds an empty, dated solution file — you write every line |
| (ask clarifying questions) | Answers freely; **won't spoil** the approach unless you're stuck or ask outright |
| "Clean / Shaky / Blank" | Grades honestly, logs it, computes your next review, and schedules it — proactively |

**Be honest with the grade.** 🟢 Clean means you wrote it from a blank page,
correct complexity, no peeking. If you glanced at a hint or weren't sure of the
data structure, that's 🟡 Shaky — and the coach will hold that line even if you're
tempted to round up. That honesty is what makes the spaced repetition actually work.

---

## What the coach is doing for you in the background

- **Spaced repetition** — Clean pushes a problem ~30 days out, Shaky ~10, Blank
  ~2. Three cleans in a row and it *retires* (spot-checked every ~6 months).
- **Scheduling** — it fills your weekly schedule, protects your main practice
  block, caps your day so you don't burn out, and re-slots anything you defer.
- **Keeping you honest** — strict Clean bar; coding required for Clean; it writes
  the scaffold but never the solution.
- **Reaching past your target** — whatever you're aiming for, it trains you one
  level beyond it, because that's how you clear the target with room to spare.
- **Unlocking the next pillar at the right time** — it starts you on DSA and tells
  you when you're ready to make System Design (and later AI Systems) your focus.
  You can lead with whatever you want; it'll just tell you honestly if you're
  reaching ahead of your foundation.

---

## The three pillars

| Pillar | You practice by… | Reviewed by… |
|--------|------------------|--------------|
| **DSA** | coding the solution from scratch | re-solving from a blank page |
| **System Design** | filling a design template | a "blind sprint" — designing it cold from memory |
| **AI Systems** | filling a build template | rebuilding the capability cold |

All three run on the same coach, the same Clean/Shaky/Blank scale, and the same
schedule. DSA is the weekday focus; System Design lives on Sundays until you're
ready to make it the main event.

---

## The philosophy (why it's built this way)

The goal isn't to pass an interview — it's genuine mastery, with the interview as
a milestone you clear on the way past it. Everything is organized around one idea:
**reach beyond the target so you always hit it.** For the full rationale — the
Interview-ROI line, the comfort system, backlog recovery — see
[`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md).

---

## Requirements

- Python 3.9+ (for the scheduling script)
- Git (the pre-commit hook auto-updates your review dates)
- [Claude Code](https://claude.com/claude-code) — this is how you talk to your coach
