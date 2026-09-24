---
name: feedback_resume_claims
description: Resume work — every number and claim touched in-session gets an explicit "is this accurate?" from the learner BEFORE the docx/PDF build; inherited prose is not evidence. Two misses in three days (Sep 21, Sep 23)
metadata:
  type: feedback
reconciled: 2026-09-23
---

**Rule:** when editing, defending, or explaining anything in `career/resume_draft_2026*.md` or the
`career/resume/` docx/PDF, treat every bullet as an unverified claim the learner must defend in an
interview. Before rendering a new docx/PDF:

1. List every number, tool, and outcome claim the session touched or added.
2. Ask the learner, item by item, "is this accurate as written?" — a multi-select confirmation is fine.
3. Write only what got a yes. A claim the learner rephrases is re-confirmed in its new wording.
4. When asked "what does X on my resume mean?", ask whether X is what actually happened BEFORE
   explaining what a reader infers from it.

**Why:** Sep 21 — "approval workflow" was explained as fact for EquityZen; it was true for RETINA only,
and had sat in both drafts for months. Sep 23 — a "99% accuracy bar" went into the Sep 21 build; the real
gate is a 0.70 F1 bar skewed to precision plus 100% groundedness. Both were inherited or drafted prose
carried into a published PDF without the check. Same family as [[feedback_verify_terminal_actions]]:
prose is not evidence of the fact it states.

**How to apply:** the check is a step in the build, not a paragraph — it runs before the PDF render, every
time, and the plan for any resume change names it explicitly. Log misses under fam `resume claim
verification` in `self_eval_log.md`.

**Build mechanics (so nobody rebuilds from scratch):** the one-pager docx is edited in place with
python-docx (name 21pt; section/company 11.5pt bold; job-title line 10pt; project headings 9.5pt bold
since Sep 23; bullets 10pt), the PDF is rendered through Word COM from PowerShell, and the previous dated
pair moves to `career/resume/archive/`. Acrobat holding the old PDF open blocks that move.
