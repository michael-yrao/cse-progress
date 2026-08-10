---
name: feedback-unseen-on-non-sd-days
description: Standing rule — every day with no SD slot must carry at least one unseen problem (new intake or a recognition probe)
metadata:
  type: feedback
---

**Set by the learner Aug 9, 2026:** *"I want to always have new or probe problems on days that have no
system design. problems that i have seen more than twice will always be a bit more lenient on me."*

## The rule

**Every day without an SD lane slot carries at least one *unseen* problem** — either **new intake** from
the current study-guide phase, or a **recognition probe** ([[project_recognition_probes]]). Either
satisfies it; they are interchangeable for this purpose.

At `three_weekly` SD cadence that is **4 unseen problems per week** (the four non-SD days). SD days carry
none — they are already at ~8 units with the lane priced at 3.0 ([[feedback_dsa_before_sd]]).

## Why — the learner's reason, which is the right one

**A problem seen three or more times is a lenient test.** By then the rep measures retention of *that
problem's solution*, not the technique — the shape is familiar, the trap is remembered, and the tracker
row even names the method. It still has value as decay insurance, but its **diagnostic** value has
collapsed. An unseen problem is the only thing that tests recognition and transfer, which is exactly what
an interview grades in its first two minutes.

This is the same argument that produced the probe ([[feedback_recognition_gate]]): the board is ~100%
retries, and a retry half-spoils itself. The rule generalises it from *"one probe a week"* to *"no day
of pure review unless SD is doing the hard work instead."*

## How to apply at the weekly build

1. Mark the SD days first (lanes ①/②/③).
2. **Every remaining day gets an unseen problem before any 🟢 backlog is placed.**
3. Prefer **new intake from the active phase** — it is time-boxed and does not get done later for free.
   Fall back to a **probe** when phase intake is capped or exhausted.
4. Only then fill remaining units with due reviews and the 🟢 backlog.

⚠️ **The intake caps still bind.** Difficulty-tiered intake ([[feedback_difficulty_tiered_intake]]) is
moderate 5 / hard 4 / DP 3 per week. **The probe is the release valve**: in a DP phase capped at 3, the
fourth non-SD day takes a probe, not a fourth new problem. A probe costs no permanent demand (no tracker
row on 🟢), so it never fights the cap.

## ⚠️ What this costs, and why it is still right

**Unseen problems and the 🟢 backlog burn-down compete for the same units.** On the Aug 10 build, buying
6.5 units of intake pushed the slip list from 4 rows to 9.

Take the trade. **A 🟢 untouched for three months came back clean** — all 8 of the Apr–May block, swept
Aug 5–7, none slipped — so the backlog is **not decaying on the timeline the tracker implies**. Phase
progress *is* time-boxed. **The axis is deferrable vs. not-deferrable, not old vs. new.**

## The failure this was catching

The learner asked *"how come we don't have any new problems this week?"* and the answer exposed that the
**`Sliding Window (finish) + Stack` phase had been open since Aug 3 with zero problems in the tracker** —
a week into a three-week phase, invisible because the board looked full of legitimate review work.
**Nothing in the repo flags an active phase with no reps.** This rule is the structural fix: a day that
cannot be filled with an unseen problem forces the question *"why is there nothing new to pull?"* at
build time, instead of a month later.
