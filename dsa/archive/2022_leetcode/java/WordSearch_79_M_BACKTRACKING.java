package review.leetcode.blind75;

import DataStructure.Pair;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class WordSearch_79_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/word-search/
    * */

    /*
    * My first thought here is that this is pretty much DFS
    * But we need to somehow be able to keep track of which character we are currently on, or rather which index of the word
    * So idea seems to be a DFS function that goes in all 4 directions of current vertex while passing in the index to search for
    * Dependent on whether the current character is a match or not
    *
    * Problem also states we cannot go past the same vertex twice, so we will need to keep track of whether the vertex
    * We will use a Set of Pair to keep track of the vertices we have traversed through already
    * */


    public boolean wordSearchSecondSubmission(char[][] board, String word)
    {
        /*

        1. We need to keep track of current character we are trying to match
        2. We need to mark whether or not we have visited current vertex or not
        3. From our main method, we should do a nested loop to find the starting position
        */

        int maxRow = board.length;
        int maxColumn = board[0].length;

        for(int cr=0;cr<maxRow;cr++)
        {
            for(int cc=0;cc<maxColumn;cc++)
            {
                if(backtrack(cr,cc,0,maxRow,maxColumn,board,word)) return true;
            }
        }
        return false;
    }

    private boolean backtrack(int cr, int cc, int currentIndex, int maxRow, int maxColumn, char[][] board, String word)
    {
        // If we incremented all the way to end of the word, we already found the answer, return true
        if(currentIndex>=word.length()) return true;

        // If we are out of bounds or if current character is not what we are looking for, return false
        if(cr<0 || cc<0 || cr>=maxRow || cc>=maxColumn || board[cr][cc]!=word.charAt(currentIndex)) return false;

        // If here, then we found a matching character <- THIS IS WRONG, CAN'T ASSUME THIS
        boolean visiting=false;

        if(board[cr][cc]==word.charAt(currentIndex))
        {
            // Mark current vertex as visited and then visit all its neighbors

            // Make the current char go out of bounds of alphabets to mark as visited
            board[cr][cc]+=100;

            visiting = backtrack(cr+1,cc,currentIndex+1,maxRow,maxColumn,board,word)
                    || backtrack(cr-1,cc,currentIndex+1,maxRow,maxColumn,board,word)
                    || backtrack(cr,cc+1,currentIndex+1,maxRow,maxColumn,board,word)
                    || backtrack(cr,cc-1,currentIndex+1,maxRow,maxColumn,board,word);

            board[cr][cc]-=100;
        }

        return visiting;
    }

    public boolean exist(char[][] board, String word)
    {
        int row=board.length;
        int column=board[0].length;
        for(int currentRow=0;currentRow<row;currentRow++)
        {
            for(int currentColumn=0;currentColumn<column;currentColumn++)
            {
                if(wordBacktrack(board,word,row,column,currentRow,currentColumn,0)) return true;
            }
        }
        return false;
    }

    public boolean wordBacktrack(char[][] board, String word, int maxRow, int maxColumn,
                                 int currentRow, int currentColumn, int currentWordIndex)
    {
        // Base cases
        if(currentWordIndex >= word.length()) return true;
        if(currentRow >= maxRow || currentColumn >= maxColumn || currentRow < 0 || currentColumn < 0
            || board[currentRow][currentColumn] != word.charAt(currentWordIndex)) return false;

        // Search all 4 directions of current vertex
        // Also note we cannot traverse same node again, so we need to mark our current node somehow

        boolean returnBool=false;

        if(board[currentRow][currentColumn] == word.charAt(currentWordIndex))
        {
            board[currentRow][currentColumn]+=100; // Add some arbitrary number larger than 26 to mark it as visited
            returnBool =
                    wordBacktrack(board,word,maxRow,maxColumn,currentRow+1,currentColumn,currentWordIndex+1)
                    || wordBacktrack(board,word,maxRow,maxColumn,currentRow-1,currentColumn,currentWordIndex+1)
                    || wordBacktrack(board,word,maxRow,maxColumn,currentRow,currentColumn-1,currentWordIndex+1)
                    || wordBacktrack(board,word,maxRow,maxColumn,currentRow,currentColumn+1,currentWordIndex+1);
            board[currentRow][currentColumn]-=100;
        }
        return returnBool;
    }
}
