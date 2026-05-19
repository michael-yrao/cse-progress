package review.leetcode.blind75;

public class LongestCommonSubsequence_1143_M_2DP
{
    /*
    * https://leetcode.com/problems/longest-common-subsequence/
    * */

    public int longestCommonSubsequence(String text1, String text2)
    {
        int[][] cache = new int[text1.length()][text2.length()];
        return recursiveLCS(cache, text1, text2, 0, 0);
    }

    // If text1.char = text2.char, we know this row/column will have count+1,
    // So we can skip those and just do 1 + recursive(vertex currentRow + 1 , currentColumn + 1)
    // If text1.char != text2.char, we need to check the next character in the row as well as the next char in the column

    private int recursiveLCS(int[][] cache, String text1, String text2, int currentRow, int currentColumn)
    {
        // Base case, if out of bounds, we'll assume 0
        if(currentRow >= text1.length() || currentColumn >= text2.length()) return 0;
        // If we have already calculated this grid before, just return it
        if(cache[currentRow][currentColumn] != 0) return cache[currentRow][currentColumn];
        if(text1.charAt(currentRow)==text2.charAt(currentColumn))
            return 1 + recursiveLCS(cache,text1,text2,currentRow+1,currentColumn+1);
        else cache[currentRow][currentColumn] = Math.max(recursiveLCS(cache,text1,text2,currentRow+1, currentColumn),
                recursiveLCS(cache,text1,text2,currentRow, currentColumn+1));

        return cache[currentRow][currentColumn];
    }
}
