package review.test.learning;

import org.junit.jupiter.api.Test;
import review.learning.DynamicProgramming.Memoization.CanSum;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class canSumTest
{
    private CanSum canSum = new CanSum();

    @Test
    public void canSumTest1()
    {
        int target = 7;
        int[] numbers = new int[] {5,3,4,7};
        assertEquals(true,canSum.canSum(numbers,target));
    }

    @Test
    public void canSumMemoizationTest1()
    {
        int target = 7;
        int[] numbers = new int[] {5,3,4,7};
        assertEquals(true,canSum.canSumMemoization(numbers,target));

    }

    @Test
    public void canSumTest2()
    {
        int target = 7;
        int[] numbers = new int[] {2,4};
        assertEquals(false,canSum.canSum(numbers,target));
    }

    @Test
    public void canSumMemoizationTest2()
    {
        int target = 7;
        int[] numbers = new int[] {2,4};
        assertEquals(false,canSum.canSumMemoization(numbers,target));

    }
}
