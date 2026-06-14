package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.PalindromeSubstrings_647_M_1DP;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class palindromeSubstringTest
{
    private PalindromeSubstrings_647_M_1DP palindromeSubstrings = new PalindromeSubstrings_647_M_1DP();

    @Test
    public void setPalindromeSubstringsTest1()
    {
        String inputString = "abc";
        assertEquals(3,palindromeSubstrings.countSubstrings(inputString));
    }

    @Test
    public void setPalindromeSubstringsTest2()
    {
        String inputString = "aaa";
        assertEquals(6,palindromeSubstrings.countSubstrings(inputString));
    }
}
