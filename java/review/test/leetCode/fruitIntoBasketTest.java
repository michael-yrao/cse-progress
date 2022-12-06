package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.FruitIntoBaskets_904_M_SLIDINGWINDOW;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class fruitIntoBasketTest
{
    FruitIntoBaskets_904_M_SLIDINGWINDOW fruitTest = new FruitIntoBaskets_904_M_SLIDINGWINDOW();

    @Test
    public void fruitTest1()
    {
        int[] inputArray = new int[]{3,3,3,1,2,1,1,2,3,3,4};
        assertEquals(5,fruitTest.totalFruit(inputArray));
    }
}
