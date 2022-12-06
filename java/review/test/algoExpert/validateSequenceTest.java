package review.test.algoExpert;

import org.junit.jupiter.api.Test;
import review.algoExpert.ValidateSequence;

import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class validateSequenceTest
{
    private ValidateSequence validateSequence = new ValidateSequence();

    @Test
    public void TestCase1() {
        var array = Arrays.asList(5, 1, 22, 25, 6, -1, 8, 10);
        var sequence = Arrays.asList(1, 6, -1, 10);
        assertEquals(true, validateSequence.isValidSubsequence(array, sequence));
    }
}
