package review.leetcode.leetcodeExtra;

public class LengthOfLastWord_58_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/length-of-last-word/
    * */

    /*
    1. Trim s
    2. Get last string in split
    3. return length
    */
    public int lengthOfLastWord(String s)
    {
        String trimmedString = s.trim();
        String[] splitString = trimmedString.split(" ");
        String lastString = splitString[splitString.length-1];
        return lastString.length();
    }

    /*
    * Since we know we just want the last String, we can just trim and find index of the last space
    * */
    public int cleanerLengthOfLastWord(String s)
    {
        String trimmedString = s.trim();
        return trimmedString.length() - trimmedString.lastIndexOf(" ") - 1;
    }
}
