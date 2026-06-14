package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.PermutationInString_567_M_SLIDINGWINDOW;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class permutationInStringTest
{
    private PermutationInString_567_M_SLIDINGWINDOW permutationInString = new PermutationInString_567_M_SLIDINGWINDOW();

    @Test
    public void permutationInStringTest1()
    {
        String needle = "ab";
        String hayStack = "eidbaooo";
        assertEquals(true,permutationInString.checkInclusion(needle,hayStack));
    }

    @Test
    public void permutationInStringTest2()
    {
        String needle = "ab";
        String hayStack = "eidboaoo";
        assertEquals(false,permutationInString.checkInclusion(needle,hayStack));
    }

    @Test
    public void permutationInStringTest3()
    {
        String needle = "aa";
        String hayStack = "eidbaaoo";
        assertEquals(true,permutationInString.checkInclusion(needle,hayStack));
    }

    @Test
    public void permutationInStringTest4()
    {
        String needle = "adc";
        String hayStack = "dcda";
        assertEquals(true,permutationInString.checkInclusion(needle,hayStack));
    }

    @Test
    public void permutationInStringFrequencyArrayTest1()
    {
        String needle = "ab";
        String hayStack = "eidbaooo";
        assertEquals(true,permutationInString.checkInclusionFrequencyArray(needle,hayStack));
    }

    @Test
    public void permutationInStringFrequencyArrayTest2()
    {
        String needle = "ab";
        String hayStack = "eidboaoo";
        assertEquals(false,permutationInString.checkInclusionFrequencyArray(needle,hayStack));
    }

    @Test
    public void permutationInStringFrequencyArrayTest3()
    {
        String needle = "aa";
        String hayStack = "eidbaaoo";
        assertEquals(true,permutationInString.checkInclusionFrequencyArray(needle,hayStack));
    }

    @Test
    public void permutationInStringFrequencyArrayTest4()
    {
        String needle = "adc";
        String hayStack = "dcda";
        assertEquals(true,permutationInString.checkInclusionFrequencyArray(needle,hayStack));
    }

}
