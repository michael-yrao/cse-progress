package review.leetcode.leetcodeExtra;

public class PalindromeSubstrings_647_M_1DP
{
    /*
    * https://leetcode.com/problems/palindromic-substrings/
    * */

    /*
        Input: s = "abc"
        Output: 3
        Explanation: Three palindromic strings: "a", "b", "c".
     */

    public int countSubstrings(String s)
    {
        /*
        * We should use Manacher's Algorithm by checking palindrome from the middle
        * We will need a counter for number of palindromes
        * Need to loop through each character and find all palindromes as them in the center
        * As such we will create a helper to perform the expansion from the center
        *
        * Algorithm:
        *   1. Initialize the counter to current length of the string since we can always assume
        *       that 1 single character by itself is always a palindrome
        *   2. Use Manacher's Algorithm to expand both evenly and oddly
        *   3. Add both even and odd results to counter
        *   4. Return counter
        *
        * */
        int count=s.length();

        for(int i=0;i<s.length();i++)
        {

            /*
            * When String is odd length, we have 1 single middle point
            * But when we have an even String, expander needs to expand from 2 characters
            * */

            count+=palindromeExpander(s,i,i);
            count+=palindromeExpander(s,i,i+1);
        }
        return count;
    }

    public int palindromeExpander(String s, int left, int right)
    {
        int manacherExpander=0;

        // For any subsequent outside the initial palindrome, we increment the counter
        while(left>=0 && right<s.length() && s.charAt(left)==s.charAt(right))
        {
            if(left!=right) manacherExpander++;
            left--;
            right++;
        }

        return manacherExpander;
    }
}
