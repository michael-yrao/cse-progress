package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class ValidSudoku_36_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/valid-sudoku/
    * */


    /*
    * 1. Each row must contain the digits 1-9 without repetition.
    * 2. Each column must contain the digits 1-9 without repetition.
    * 3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
    *
    * The problem kinda solves itself, just satisfy all 3 criteria, and we are done.
    * 1. Use a Map of Integer,Set to help us determine whether each row is unique
    * 2. Do exactly what we do on 1 but for column
    * 3. Think of each sub-box as a vertex of its own, e.g. top left is 0,0, top middle is 0,1, top right is 0,2, etc.
    *    We can come up with a formula to help uniquely link each original vertex to those sub-box vertices
    *    Therefore, for this criteria, we will use a Map of Pair,Set where the Pair is the sub-box vertices
    *
    * */

    public boolean isValidSudoku(char[][] board)
    {
        Map<Integer, Set<Character>> rowMap = new HashMap<>();
        Map<Integer, Set<Character>> columnMap = new HashMap<>();
        Map<Pair<Integer,Integer>, Set<Character>> subBoxMap = new HashMap<>();

        int row=board.length;
        int column=board[0].length;

        for(int i=0;i<row;i++)
        {
            for(int j=0;j<column;j++)
            {
                // Row check

                if(!rowMap.containsKey(i)) rowMap.put(i,new HashSet<>());
                if(board[i][j]-'.' != 0 && rowMap.get(i).contains(board[i][j])) return false;
                rowMap.get(i).add(board[i][j]);

                // Column check

                if(!columnMap.containsKey(j)) columnMap.put(j,new HashSet<>());
                if(board[i][j]-'.' != 0 && columnMap.get(j).contains(board[i][j])) return false;
                columnMap.get(j).add(board[i][j]);

                // Sub-Box check

                Pair<Integer,Integer> subBoxPair = new Pair<>(i/3,j/3);

                if(!subBoxMap.containsKey(subBoxPair)) subBoxMap.put(subBoxPair,new HashSet<>());
                if(board[i][j]-'.' != 0 && subBoxMap.get(subBoxPair).contains(board[i][j])) return false;
                subBoxMap.get(subBoxPair).add(board[i][j]);
            }
        }
        return true;
    }
}
