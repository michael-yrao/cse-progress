package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.RangeSumQueryImmutable_303_E_PREFIXSUM;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class rangeSumQueryImmutableTest
{
    @Test
    public void test1()
    {
        int[] test1 = new int[]{-2,0,3,-5,2,-1};
        RangeSumQueryImmutable_303_E_PREFIXSUM rsqI = new RangeSumQueryImmutable_303_E_PREFIXSUM(test1);
        assertEquals(1,rsqI.sumRange(0,2));
    }

}
