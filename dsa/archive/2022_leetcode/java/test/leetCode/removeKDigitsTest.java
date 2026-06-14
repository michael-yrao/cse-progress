package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.RemoveKDigits_402_M_STACK;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class removeKDigitsTest
{
    RemoveKDigits_402_M_STACK removeKDigits = new RemoveKDigits_402_M_STACK();

    @Test
    public void test1()
    {
        String input = "1432219";
        int k = 3;
        assertEquals("1219",removeKDigits.removeKdigits(input,k));
    }
}
