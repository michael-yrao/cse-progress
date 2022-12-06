package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class NQueens_51_H_BACKTRACKING {
    /*
     * https://leetcode.com/problems/n-queens/
     * */


    private Set<Integer> columnSet = new HashSet<>();
    private Set<Integer> negDiagSet = new HashSet<>();
    private Set<Integer> posDiagSet = new HashSet<>();

    public List<List<String>> solveNQueens(int n)
    {
        /*
        *
        * Go through each vertex and try to place a queen
        * skip any vertices that is on same row/column/diagonal
        * diagonal logic: positive diagonals have same values using r + c
        *                 negative diagonals have same values using r - c
        *
        * We should have a set for vertices that cannot be placed so we can speed up the process
        *
        * Requirement is to have placed n queens, so that will be our first base case
        * Each item in the list is a row, so we can just work with that and just loop through in our
        * backtracking method row by row or column by column
        * */

        List<List<String>> result = new ArrayList<>();
        List<String> currentSolution = new ArrayList<>();

        nQueensBacktrack(n,0,currentSolution,result);

        return result;
    }

    public void nQueensBacktrack(int n, int currentRow, List<String> currentSolution, List<List<String>> result)
    {
        // Base case. Placed n queens
        if(currentRow==n)
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        for(int currentColumn=0;currentColumn<n;currentColumn++)
        {
            // Skip current row/column combination if they are part of the set
            if(columnSet.contains(currentColumn) || negDiagSet.contains(currentRow - currentColumn) || posDiagSet.contains(currentRow + currentColumn))
                continue;

            // If we are here, that means we can place the queen here

            char[] boardRow = new char[n];
            Arrays.fill(boardRow,'.');
            boardRow[currentColumn] = 'Q';
            String boardRowString = new String(boardRow);

            // Choose to fill this column/row combination with Q

            currentSolution.add(boardRowString);
            columnSet.add(currentColumn);
            negDiagSet.add(currentRow - currentColumn);
            posDiagSet.add(currentRow + currentColumn);

            nQueensBacktrack(n,currentRow+1,currentSolution,result);

            currentSolution.remove(currentSolution.size()-1);
            columnSet.remove(currentColumn);
            negDiagSet.remove(currentRow - currentColumn);
            posDiagSet.remove(currentRow + currentColumn);
        }
    }
}
