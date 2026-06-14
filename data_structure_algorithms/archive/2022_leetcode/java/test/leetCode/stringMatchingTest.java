package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.interview.simonMarket.stringMatching;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class stringMatchingTest
{
    private stringMatching stringMatching = new stringMatching();

    @Test
    public void permutationStringMatchingFailureTest()
    {
        String needle = "abcd";
        String hay = "abcabdeabce";
        assertEquals(stringMatching.stringMatchingPermutation(hay,needle),-1);
    }

    @Test
    public void permutationStringMatchingBasicTest()
    {
        String needle = "abcd";
        String hay = "abcabdeabcd";
        assertEquals(stringMatching.stringMatchingPermutation(hay,needle),7);
    }

    @Test
    public void permutationStringMatchingBasicAsteriskTest()
    {
        String needle = "ab*d";
        String hay = "abcabdeabcd";
        assertEquals(stringMatching.stringMatchingPermutation(hay,needle),7);
    }

    @Test
    public void boyerMooreStringMatchingFailureTest()
    {
        String needle = "abcd";
        String hay = "abcabdeabce";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),-1);
    }

    @Test
    public void boyerMooreStringMatchingFirstTest()
    {
        String needle = "abcd";
        String hay = "abcabdeabcd";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),7);
    }

    @Test
    public void boyerMooreStringMatchingFirstAsteriskTest()
    {
        String needle = "ab*d";
        String hay = "abcabdeabcd";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),7);
    }

    @Test
    public void boyerMooreStringMatchingSecondTest()
    {
        String needle = "qrstuv";
        String hay = "abcdefghijklmnopqrstuvwxyz";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),16);
    }

    @Test
    public void boyerMooreStringMatchingSecondAsteriskTest()
    {
        String needle = "qrs*uv";
        String hay = "abcdefghijklmnopqrstuvwxyz";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),16);
    }

    @Test
    public void boyerMooreStringMatchingThirdTest()
    {
        String needle = "qrstuv";
        String hay = "abcdefghijklmnopabcdadbcefsasdfjklwertuiopqrstuvwxyz";
        assertEquals(stringMatching.stringMatchingBoyerMoore(hay,needle),42);
    }

}
