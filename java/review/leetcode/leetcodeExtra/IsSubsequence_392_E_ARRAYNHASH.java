package review.leetcode.leetcodeExtra;

public class IsSubsequence_392_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/is-subsequence/
    * */

        /*

    One way is just to go through both strings together with two pointers
    once the s pointer goes out of bounds, that means we are good to return true
    otherwise, return false

    */

    public boolean isSubsequence(String s, String t)
    {
        int subPointer = 0;
        int strPointer = 0;

        while(subPointer<s.length())
        {
            if(strPointer >= t.length()) return false;
            if(s.charAt(subPointer) == t.charAt(strPointer))
            {
                subPointer++;
                strPointer++;
            }
            else
            {
                strPointer++;
            }
        }
        return true;
    }
}
