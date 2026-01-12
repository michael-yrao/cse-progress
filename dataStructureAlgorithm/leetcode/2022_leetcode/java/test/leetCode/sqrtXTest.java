package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.SqrtX_69_E_BINARYSEARCH;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class sqrtXTest
{
    SqrtX_69_E_BINARYSEARCH sqrtX = new SqrtX_69_E_BINARYSEARCH();

    @Test
    public void sqrtXTest1()
    {
        int result = sqrtX.mySqrt(1);
        assertEquals(1,result);
    }
}
