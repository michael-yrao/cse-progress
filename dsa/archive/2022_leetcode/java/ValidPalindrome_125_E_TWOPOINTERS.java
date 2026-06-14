package review.leetcode.blind75;

public class ValidPalindrome_125_E_TWOPOINTERS
{
    /*
    * https://leetcode.com/problems/valid-palindrome/
    * */

    public boolean isPalindrome(String s)
    {
        String alphanumeric = alphanumericOnly(s);
        if(alphanumeric==null || alphanumeric.isEmpty()) return true;

        int left=0, right=alphanumeric.length()-1;
        while(left<=right)
        {
            if(alphanumeric.charAt(left)!=alphanumeric.charAt(right)) return false;
            else
            {
                left++;
                right--;
            }
        }
        return true;
    }

    public String alphanumericOnly(String s)
    {
        StringBuffer sb = new StringBuffer();
        for(int i=0;i<s.length();i++)
        {
            if(Character.isLetterOrDigit(s.charAt(i)))
            {
                sb.append(Character.toLowerCase(s.charAt(i)));
            }
        }
        return sb.toString();
    }

    public boolean isPalindromeAlternative(String s)
    {
        StringBuilder content = new StringBuilder();
        for(int i = 0; i < s.length(); i++)
            if(Character.isLetterOrDigit(s.charAt(i)))
                content.append(s.charAt(i));
        content = new StringBuilder(content.toString().toLowerCase());
        String value = content.toString();
        return value.equals(content.reverse().toString());
    }

}
