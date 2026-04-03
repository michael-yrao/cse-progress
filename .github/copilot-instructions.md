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

**Organization by Year/Language**:
- `2022_leetcode/java/`: Problems solved in Java (legacy)
- `2022_leetcode/python/`: Python solutions from 2022
- `2026_python/`: Current problem set organized by algorithm type
  - `1d_dynamic_programming/`, `2d_dynamic_programming/`
  - `arrays_and_hash/`, `backtracking/`, `binary_search/`
  - `graphs/`, `greedy/`, `heap_n_priorityqueue/`
  - `linked_list/`, `sliding_window/`, `stack/`, `trees/`, `tries/`
  - `two_pointers/`, `bit_manipulation/`, `intervals/`, `math_n_geometry/`
  - `advanced_graphs/`, `system_design/`

**Important Notes**:
- Blind 75 focus: Covers most interview categories except strings (no Boyer-Moore, etc.)
- Watch video explanations on NeetCode for deeper understanding
- Don't expect to solve everything immediately — preparation is iterative

### 📁 `/dataStructureAlgorithm/other/`

**`learning/`**: Foundational material by topic
- Covers basics of core algorithms and data structures

**`interview/`**: Real interview problems
- Organized by company
- Reflects actual assessment and interview experiences

### 📁 `/documentation/`

**`algorithm_mental_model.tex`**: The "why" behind problem-solving approaches
- Explains mental frameworks for recognizing problem types
- Key for understanding when to apply specific algorithms

**`software_development_concepts.tex`**: Conceptual knowledge
- OOP principles
- Big O notations and complexity analysis
- Behavioral interview topics

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

### Learning Flow

**Recommended Approach**:
1. Start with Blind 75 problems
2. Watch NeetCode explanations for weak areas
3. Practice the problem variations in `2026_python/` organized by type
4. Review `software_development_concepts.tex` for behavioral questions
5. Study company-specific patterns in `other/interview/{company}/`

---

## File Type Handling

- **Java**: `.java` files in `2022_leetcode/java/`
- **Python**: `.py` files in `2026_python/` (organized by algorithm type)
- **TypeScript**: `.ts` files (minimal, mostly learning examples)
- **LaTeX**: `.tex` files in `documentation/`
  - Requires LaTeX compiler to view rendered PDFs
  - Raw files document conceptual thinking

---

## Build & Compilation

- **No centralized build system**: Solutions are standalone by language
- **Java**: Compile with `javac ClassName.java`
- **Python**: Execute with `python filename.py`
- **TypeScript**: Requires `tsc` compilation (configured in `tsconfig.json`)

**Note**: The repo is a study/reference collection, not a production application.

---

## Code Organization Principles

1. **Year/Language Separation**: Keep legacy and current methods separate
2. **Algorithm Categorization**: `2026_python/` organizes by problem type for discovery
3. **Naming Clarity**: File names encode key information for quick scanning
4. **Mental Models First**: Reference `algorithm_mental_model.tex` before solving
5. **Reference External Resources**: Link to NeetCode, LeetCode, and other materials

---

## Quick Reference

| Task | Location |
|------|----------|
| Find problems by algorithm type | `2026_python/{type}/` |
| Find problems by year/language | `2022_leetcode/{year}/{language}/` |
| Learn algorithm concepts | `documentation/algorithm_mental_model.tex` |
| Learn interview fundamentals | `documentation/software_development_concepts.tex` |
| Review coding interviews | `dataStructureAlgorithm/other/interview/{company}/` |
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

This helps provide focused, contextual assistance aligned with your interview prep strategy.
