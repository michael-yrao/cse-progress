package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.blind75.DecodeWays_91_M_1DP;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class numDecodingsTest
{
    public DecodeWays_91_M_1DP decode = new DecodeWays_91_M_1DP();

    @Test
    public void decodeWaysZeroTest()
    {
        String input = "06";
        assertEquals(0,decode.numDecodings(input));
    }
}
