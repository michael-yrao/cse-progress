package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.blind75.ValidPalindrome_125_E_TWOPOINTERS;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class twoPointersTest
{
    private ValidPalindrome_125_E_TWOPOINTERS validPalindrome = new ValidPalindrome_125_E_TWOPOINTERS();

    @Test
    public void validPalindromeTest()
    {
        String input = "A man, a plan, a canal: Panama";
        assertEquals(validPalindrome.isPalindrome(input),true);
    }
}
