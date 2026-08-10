---
name: feedback_explanation_register
description: Explanations read as "foreign" when the principle is named before the mechanics are shown and every step is wrapped in why-this-matters framing — show literal values first, name things after, and when they say "I don't understand," ASK which link broke instead of re-explaining
metadata:
  type: feedback
---

**Learner, Aug 10, 2026, mid-Redis-teach:** *"I think I have trouble with Opus model's explanation
sometimes, it feels very foreign the way it explains things."*

This is **register**, not ordering, which is what makes it distinct from [[feedback_procedure_first]]
and [[feedback_spine_first]]. Those say *which* facts come first. This is about the **packaging around
them** — and the packaging was the problem on a session where the content was landing fine.

## What reads as foreign

| Habit | What it does to the learner |
|---|---|
| **Naming the principle before showing the thing** — *"the score IS the mechanism"* before they've seen a ZSet table | the sentence is a summary of an understanding they don't have yet, so it lands as noise |
| **Wrapping every step in why-this-matters framing** — *"which brings us to the thing card 8 is actually testing"*, *"why the score choice is the whole trick"* | doubles the text and buries the one operative line |
| **Dense em-dash prose with layered clauses** | fine to skim, bad to *learn* from — there's no visual place for the eye to rest on the fact |
| **Jargon before its referent** — "member", "score" used before showing they're just two columns | halts the paragraph, exactly like an unexpanded acronym |

## What worked in the same session

- **A literal two-column table with real values**, then *"Redis calls these `member` and `score`."*
  Show it, then name it. Never the reverse.
- **Decoding opaque names** — `ZCARD` = **CARD**inality, `ZREMRANGEBYSCORE` = **REM**ove **RANGE BY
  SCORE**. Three seconds, and the command set stops being arbitrary.
- **One concrete run with small numbers** (limit 3 per 10s; `t=9` / `t=10`), showing the table before
  and after each command.
- **Short declaratives.** *"Member is the primary key. Scores repeat freely."*

## ⚠️ The rule with the sharpest edge: on "I don't understand," ASK WHICH LINK BROKE

**Do not re-explain.** Twice on Aug 10 the learner said they didn't follow, and the second time the
"dumbed-down" version re-explained the **sliding window they had already understood and said so** —
because the confusion was assumed rather than located. The learner had to correct it: *"this just
explained sliding window of size 10."*

**What fixed it in one turn:** offering a **numbered list of the candidate links** and asking them to
point at one.

> 1. What "member" and "score" mean · 2. The uniqueness trap · 3. The commands · 4. "The score is the
>    mechanism"

They picked 1, said *"let's do 1 at a time"*, and then cleared all four in a few short turns. **A
numbered menu is cheap, it is not a spoiler, and it converts a vague "I'm lost" into a located gap.**

**Corollary, observed the same session:** *"I don't understand the question"* followed by a correct
answer means **tired, not lost**. Confirm the answer, don't re-teach it, and offer to park.

## How to apply

1. **Show literal values before naming anything.** Table first, term second, principle last.
2. **Cut the framing sentences.** If a line only explains why the next line matters, delete it.
3. **Decode any opaque name on first use** — same reflex as expanding an acronym.
4. **On confusion, ask which link broke** and offer a numbered menu. Never re-explain by default.
5. **Ask again afterwards whether the register improved** — the learner can only calibrate this by
   comparison, so make it an explicit check, not an assumption that one adjustment fixed it.
