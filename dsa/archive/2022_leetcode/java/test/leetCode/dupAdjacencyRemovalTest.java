package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.RemoveAllAdjacentDuplicatesInStringII_1209_M_STACK;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class dupAdjacencyRemovalTest
{
    RemoveAllAdjacentDuplicatesInStringII_1209_M_STACK removeII = new RemoveAllAdjacentDuplicatesInStringII_1209_M_STACK();

    @Test
    public void removeIITest1()
    {
        String input="deeedbbcccbdaa";
        int k = 3;
        assertEquals("aa",removeII.removeDuplicates(input,k));
    }
}
