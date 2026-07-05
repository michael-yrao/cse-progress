# CSE Review Repository Instructions

## Project Overview

**back2basics** is a comprehensive interview preparation repository focused on:
- **LeetCode Problems**: Curated by year, language, and difficulty
- **Algorithm Learning**: Mental models and foundational concepts
- **Conceptual Review**: OOP, Big O notation, design patterns
- **Interview Experience**: Real problems faced in company interviews

**Primary Resources**:
- [NeetCode](https://neetcode.io/) for video explanations
- Blind 75 as the starting point for interview prep
- Algorithm mental model docs in `documentation/algorithm_mental_model.tex`

---

## Repository Structure

### 📁 `/dataStructureAlgorithm/leetcode/`

Contains organized LeetCode problems serving as the core interview prep material.

**File Naming Convention**: `$PROBLEM_NAME_$LEETCODE_NUMBER_$DIFFICULTY_$TYPE_OF_PROBLEM`

Example: `ClimbStairs_70_E_1DP.java` (Easy, 1D Dynamic Programming)

**Active problem set**: `leetcode/` — organized by algorithm type:
  - `1d_dynamic_programming/`, `arrays_and_hash/`, `backtracking/`, `binary_search/`
  - `graphs/`, `greedy/`, `linked_list/`, `sliding_window/`, `stack/`, `trees/`
  - `two_pointers/`

**Archive** (legacy, not actively used): `archive/` — contains `2022_leetcode/` (Java + Python), `2026_replay/` (playground), `other/` (company interview problems in Java), `codeforce/`, `typescript/`

**Important Notes**:
- Blind 75 focus: Covers most interview categories except strings (no Boyer-Moore, etc.)
- Watch video explanations on NeetCode for deeper understanding

### 📁 `/docs/archive/2022/`

**`algorithm_mental_model.tex`**: The "why" behind problem-solving approaches
- Explains mental frameworks for recognizing problem types

**`software_development_concepts.tex`**: Conceptual knowledge
- OOP principles, Big O notations, behavioral interview topics

### 📁 `/image/`

Visual aids, including Big O complexity chart (`data_structure_big_o.png`)

---

## Common Development Tasks

### Adding a New Problem Solution

1. **Identify the Category**: Map to the most relevant algorithm type
   - For `2026_python/`: Use subdirectory (e.g., `sliding_window/`, `trees/`)
   - For legacy: Use appropriate year/language folder

2. **Follow Naming Convention**:
   - Find LeetCode number, difficulty (E/M/H), and primary problem type
   - Example: `ReverseLinkedList_206_E_LINKEDLIST.java`

3. **Include Core Solution**:
   - Clean, readable code
   - Time/space complexity analysis in comments
   - Link to problem URL (for reference)

### Updating Documentation

- **Algorithm Mental Models**: Reference `documentation/algorithm_mental_model.tex`
  - Add insights when discovering new patterns
  - Update mental models as understanding deepens

- **Interview Experience**: Add to `dataStructureAlgorithm/other/interview/{company}/`
  - Document assessment/interview problems faced
  - Include solutions and key learnings

### 📓 "Why I Got Stuck" Log Template
Create a running notebook using this format. Review this document every Saturday morning to find your retention leaks.

```markdown
## ❌ Problem Name: [Insert LeetCode Name & Number]
* **Date**: [Insert Date]
* **Topic(s)**: [e.g., Stack / Monotonic Stack]

### 1. Where did I get stuck?
* [Write a 1-sentence description of the exact roadblock]

### 2. The Core Realization
* [What was the structural trick or pattern from the solution?]

### 3. Code Snippet to Remember
```python
# Paste the specific line of Python or pattern that unlocked the issue
```
```
```

### Learning Flow

**Recommended Approach**:
*Use this structure for the first 16 weeks of your study journey.*
*   **00:00–00:15 | Recall Warm-up**: Open a problem solved 2–3 days ago. Do not rewrite code; trace its variable state changes on paper or in comments.
*   **00:15–00:30 | Whiteboard & Ideate**: Read a new problem. Sketch the approach, constraints, and edge cases in plain English. No code!
*   **00:30–00:45 | Look up / Validate**: If completely stuck or your logic loops, stop. Watch the NeetCode video explanation immediately.
*   **00:45–01:00 | Python Implementation**: Type out the clean code, trace logic line-by-line, and add comments explaining the "why".

*Use this structure when focusing on System Design and AI Engineering to protect your DSA knowledge.*
*   **00:00–00:15 | DSA Maintenance Flashcard**: Look at a random past LeetCode prompt. Explain the data structure pattern and optimal Time/Space complexity out loud.
*   **00:15–01:00 | Architecture Deep Dive**: Spend 45 minutes learning your current block's design or AI concepts via engineering blogs or videos.

---

## File Type Handling

- **Python**: `.py` files in `dsa/leetcode/` (organized by algorithm type) — the active set
- **Java/TypeScript/legacy Python**: in `dsa/archive/` — reference only
- **LaTeX**: `.tex` files in `docs/archive/2022/` — requires LaTeX compiler to view rendered PDFs

---

## Build & Compilation

- **No centralized build system**: Solutions are standalone by language
- **Java**: Compile with `javac ClassName.java`
- **Python**: Execute with `python filename.py`
**Note**: The repo is a study/reference collection, not a production application.

---

## Quick Reference

| Task | Location |
|------|----------|
| Find problems by algorithm type | `dsa/leetcode/{type}/` |
| Spaced-repetition tracker | `docs/foundations/dsa/mastery/dsa_progress.md` |
| Algorithm pattern cheatsheets | `docs/foundations/dsa/patterns/` |
| Study schedule / stuck log | `docs/foundations/` |
| Legacy solutions (Java, 2022 Python) | `dsa/archive/` |
| Find Big O reference | `image/data_structure_big_o.png` |

---

## Useful External Links

- [NeetCode - Video Explanations](https://neetcode.io/)
- [Blind 75 LeetCode Problems](https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions)
- [LeetCode Company Frequency](https://github.com/xizhengszhang/Leetcode_company_frequency)
- [LeetCode](https://leetcode.com)

---

## Working with AI Assistance

When asking for help with this repository:

- **Specify the problem location**: e.g., "`2026_python/sliding_window/`" or "`2022_leetcode/java/`"
- **Include context**: Difficulty level (E/M/H), algorithm type, or company
- **Reference concepts**: "This is a Two Pointers problem" or "This uses Monotonic Stack"
- **Ask for patterns**: Help understanding when to apply specific techniques
- **Request mental models**: Explanation of problem-solving approach before jumping to code
- **If any LeetCode problem is mentioned, ensure it is logged in `docs/foundations/dsa/mastery/dsa_progress.md`.**
- Problem titles should include the solution method used, e.g. `(BFS)` or `(DFS)`.
- If a method is mentioned and the same problem number already exists with a different method, add a new row for the new method instead of editing the old row.
- When a review row is created or staged for commit with a missing latest date, the helper should auto-populate the current date.
- If the problem is not already present, add it with title, URL, difficulty, and current attempt info.

This helps provide focused, contextual assistance aligned with your interview prep strategy.
