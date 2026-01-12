package review.test.learning;

import org.junit.jupiter.api.Test;
import review.learning.DynamicProgramming.Memoization.BestSum;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class bestSumTest
{
    private BestSum bestSum = new BestSum();

    @Test
    public void bestSumTest1()
    {
        int target = 7;
        int[] numbers = new int[] {5,3,4,7};
        assertArrayEquals(new int[]{7}, bestSum.bestSum(numbers,target));
    }

    /*
    @Test
    public void bestSumTest2()
    {
        int target = 8;
        int[] numbers = new int[] {2,3,5};
        assertArrayEquals(new int[]{3,5}, bestSum.bestSum(numbers,target));
    }
     */

    @Test
    public void bestSumTest3()
    {
        int target = 0;
        int[] numbers = new int[] {1,2,3};
        assertArrayEquals(new int[]{}, bestSum.bestSum(numbers,target));
    }

    @Test
    public void bestSumTest4()
    {
        int target = 7;
        int[] numbers = new int[] {1,2,5,7};
        assertArrayEquals(new int[]{7}, bestSum.bestSum(numbers,target));
    }

    @Test
    public void bestSumMemoTest1()
    {
        int target = 7;
        int[] numbers = new int[] {5,3,4,7};
        assertArrayEquals(new int[]{7}, bestSum.bestSumMemoization(numbers,target));
    }

    /*
    @Test
    public void bestSumMemoTest2()
    {
        int target = 8;
        int[] numbers = new int[] {2,3,5};
        assertArrayEquals(new int[]{3,5}, bestSum.bestSumMemoization(numbers,target));
    }
     */

    @Test
    public void bestSumMemoTest3()
    {
        int target = 0;
        int[] numbers = new int[] {1,2,3};
        assertArrayEquals(new int[]{}, bestSum.bestSumMemoization(numbers,target));
    }

    @Test
    public void bestSumMemoTest4()
    {
        int target = 7;
        int[] numbers = new int[] {1,2,5,7};
        assertArrayEquals(new int[]{7}, bestSum.bestSumMemoization(numbers,target));
    }

}
