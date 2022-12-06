package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.blind75.HouseRobberII_213_M_1DP;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class houseRobberTest
{
    private HouseRobberII_213_M_1DP circularRobber = new HouseRobberII_213_M_1DP();

    @Test
    public void circularRobberTest1()
    {
        int[] input = new int[]{1,2,3,1};
        assertEquals(4,circularRobber.rob(input));
    }


    @Test
    public void circularRobberTest2()
    {
        int[] input = new int[]{2,3,2};
        assertEquals(3,circularRobber.rob(input));
    }

    @Test
    public void circularRobberTest3()
    {
        int[] input = new int[]{4,1,2,7,5,3,1};
        assertEquals(14,circularRobber.rob(input));
    }

}
