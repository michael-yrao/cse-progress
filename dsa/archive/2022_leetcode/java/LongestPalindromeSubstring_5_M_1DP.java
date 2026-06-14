package review.leetcode.leetcodeExtra;

public class LongestPalindromeSubstring_5_M_1DP
{
    /*
    * https://leetcode.com/problems/longest-palindromic-substring/
    * */

    /*
    *
    * Input: s = "babad"
    * Output: "bab"
    * Explanation: "aba" is also a valid answer.
    *
    * Input: s = "cbbd"
    * Output: "bb"
    * */


    public String longestPalindromeSecondSubmission(String s)
    {
        /*

        This is a great opportunity to use Manacher's Algorithm

        1. Assuming each index is the center of the palindrome, we move our pointers in opposite directions to get largest palindrome possible

        */

        String maxString="";

        for(int i=0;i<s.length();i++)
        {
            // Odd length string
            String currentPalindrome = manacherPalindrome(s,i,i);
            if(currentPalindrome.length()>maxString.length()) maxString = currentPalindrome;

            // Even length string
            currentPalindrome = manacherPalindrome(s,i,i+1);
            if(currentPalindrome.length()>maxString.length()) maxString = currentPalindrome;
        }
        return maxString;
    }

    private String manacherPalindrome(String s, int left, int right)
    {
        while(left>=0 && right<s.length() && s.charAt(left) == s.charAt(right))
        {
            left--;
            right++;
        }
        // We don't do left -> right-1 since at this point left and right are both out of bounds of being a palindrome
        // Thus we reduce both sides by 1 which gives us left+1 -> right
        return s.substring(left+1,right);
    }

    public String longestPalindrome(String s)
    {
        /*
        * Instead of checking palindrome from the two ends,
        * We should instead check palindrome from middle character (Manacher's Algorithm)
        * We'll create a helper function to help us expand from left and right
        * */

        if(s==null || s.length()==0) return null;

        String maxLengthPalindrome="";
        String currentPalindrome="";

        int maxLength=Integer.MIN_VALUE;
        int currentLength=Integer.MIN_VALUE;

        for(int i=0;i<s.length();i++)
        {
            // We will try to treat each character as the middle point
            // If String is odd length, we have 1 true middle point
            // But if String is even length, we have 2 middle points

            // Odd Length String

            currentPalindrome = expandSubString(s,i,i);
            currentLength = currentPalindrome.length();

            maxLengthPalindrome = (maxLengthPalindrome.length() < currentPalindrome.length())?currentPalindrome:maxLengthPalindrome;
            maxLength = Math.max(maxLength, currentLength);

            // Even Length String

            currentPalindrome = expandSubString(s,i,i+1);
            currentLength = currentPalindrome.length();

            maxLengthPalindrome = (maxLengthPalindrome.length() < currentPalindrome.length())?currentPalindrome:maxLengthPalindrome;
            maxLength = Math.max(maxLength, currentLength);
        }
        return maxLengthPalindrome;
    }


    public String expandSubString(String s, int lowIndex, int highIndex)
    {
        // We do lowIndex >= 0 so that we check all characters
        // Similarly highIndex < s.length so we check all characters on that side
        // Since we go to 0th element, we need to do substring(lowIndex+1...) to make sure we account for
        // when the lowIndex was actually at 0 and decremented during the loop
        while(lowIndex >= 0 && highIndex < s.length()
                && s.charAt(lowIndex) == s.charAt(highIndex))
        {
            lowIndex--;
            highIndex++;
        }
        return s.substring(lowIndex+1,highIndex);
    }
}
