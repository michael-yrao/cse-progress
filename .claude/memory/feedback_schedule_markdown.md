---
name: feedback_schedule_markdown
description: In schedule markdown, escape the period on bullets that start with a bare problem number so they don't render as roman-numeral ordered lists
metadata:
  type: feedback
---

In schedule/preview markdown, a bullet that **starts with a bare number followed by a period** (`- 143. Reorder List`) gets parsed by many renderers as a nested ordered list beginning at that number, and the marker is styled as lowercase roman numerals (e.g. `143.` → `cxliii.`). The text after it still shows, but the number is replaced by a garbled roman-numeral marker.

**Fix:** escape the period — `- 143\. Reorder List`. Renders as a literal "143." bullet.

**Why:** User saw "cxliiii. reorder list" in the "Carryover from this week" preview section and asked what it was. Root cause was the unescaped `- 143.` bullet.

**How to apply:** When writing schedule bullets (carryover, preview, spaced-rep lists) that lead with a problem number, escape the dot as `<num>\.`. This does NOT apply to table cells (`| 42. Trapping ... |` is fine) or bullets that start with other text before the number (`- Jul 6: 355. Design Twitter` is fine). Only bare-number-first bullets need the escape. Related: [[feedback_new_vs_retry]].
