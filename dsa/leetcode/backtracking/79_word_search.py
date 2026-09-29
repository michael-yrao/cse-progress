"""
79. Word Search   ·   https://leetcode.com/problems/word-search/
Pattern: backtracking

Given an m x n grid of characters board and a string word, return true if word
exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where
adjacent cells are horizontally or vertically neighboring. The same letter cell may
not be used more than once.

Examples:
  board = [["A","B","C","E"],
           ["S","F","C","S"],
           ["A","D","E","E"]]
  word = "ABCCED"  ->  true
  word = "SEE"     ->  true
  word = "ABCB"    ->  false

Constraints:
  m == board.length
  n == board[i].length
  1 <= m, n <= 6
  1 <= word.length <= 15
  board and word consist of only lowercase and uppercase English letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-29 ────────────────────────────────────────────
    def exist(self, board: List[List[str]], word: str) -> bool:
        # first thought is DFS but we need to be able to backtrack if our current path is bad
        # so that basically lends itself into backtracking
        # find the node that matches, then check neighbors and backtrack accordingly
        # after finding the first node, we would need to define our backtracking criterias
        # path: current path
        # state: current set of nodes, current index of the word, current row, current col
        # validity: if not out of bounds and if char at index matches
        # choice: choose regardless
        # base case: bad cases : out of bound, char don't match | good cases : current index >= len(word)

        rows, cols = len(board), len(board[0])

        def backtrack(path, word_index_state, row_state, col_state, node_set_state):
            # all base cases
            if len(path) >= len(word) and word_index_state >= len(word):
                return True
            if row_state < 0 or row_state >= rows or col_state < 0 or col_state >= cols: 
                return False
            if word_index_state < len(word) and board[row_state][col_state] != word[word_index_state]:
                return False
            
            # at this point, we know we are not out of bound and current char does match
            # so the check for equals is actually redundant, thus we just check to make sure it is not already used then go look at neighbors
            # add to the set
            if (row_state, col_state) not in node_set_state: 
                # we picked the current node, so now check if any of our neighbors can satisfy our path
                node_set_state.add((row_state, col_state))
                current_path_status = (backtrack(path + [board[row_state][col_state]], word_index_state + 1, row_state + 1, col_state, node_set_state) 
                        or backtrack(path + [board[row_state][col_state]], word_index_state + 1, row_state -1, col_state, node_set_state) 
                        or backtrack(path + [board[row_state][col_state]], word_index_state + 1, row_state, col_state + 1, node_set_state) 
                        or backtrack(path + [board[row_state][col_state]], word_index_state + 1, row_state, col_state - 1, node_set_state))
                # remove from set in case it did not work out and we need to backtrack
                node_set_state.remove((row_state, col_state))
                return current_path_status

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == word[0]:
                    # path, current word index, row, col, node set
                    if backtrack([], 0, row, col, set()):
                        return True
        
        return False