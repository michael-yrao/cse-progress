package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.GasStation_134_M_GREEDY;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class gasStationTest
{
    private GasStation_134_M_GREEDY gasStation = new GasStation_134_M_GREEDY();

    @Test
    public void gasStationTest1()
    {
        int[] gas = new int[] {5,1,2,3,4};
        int[] cost = new int[] {4,4,1,5,1};

        assertEquals(4,gasStation.canCompleteCircuit(gas,cost));

    }

}
