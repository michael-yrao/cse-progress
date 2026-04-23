# Binary Search Patterns

## 1. Exact Value Search
Loop: while l <= r

Midpoint: mid = (l + r) // 2

Updates: 
  - If match: return / add to result
  - Traverse right: l = mid + 1
  - Traverse left: r = mid - 1

Purpose: Find an exact target value in the array

Return: When matrix[mid] == target or if not found

Example: LeetCode 704 Binary Search

## 2. Minimum Boundary Search (first true position)
Loop: while l < r

Midpoint: mid = (l + r) // 2 (left-biased)

Updates:
  - If valid: r = mid (keep mid as candidate)
  - If invalid: l = mid + 1 (exclude mid and move past)

Purpose: Find the leftmost position where a monotonic predicate is true

Return: l at loop exit

Example: LeetCode 34 Find First Position

## 3. Maximum Boundary Search (last true position)
Loop: while l < r

Midpoint: mid = (l + r + 1) // 2 (right-biased)

Updates:
  - If valid: l = mid (keep mid as candidate)
  - If invalid: r = mid - 1 (exclude mid and move before)
Purpose: Find the rightmost position where a monotonic predicate is true

Return: l at loop exit

Example: LeetCode 74 Search a 2D Matrix

## Key Insight
Min boundary: left-biased mid + r = mid (keeps searching right for first valid)

Max boundary: right-biased mid + l = mid (keeps searching left for last valid)

The bias ensures the loop converges to the correct boundary without getting stuck.