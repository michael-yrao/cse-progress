package review.test.learning;

import org.junit.jupiter.api.Test;
import review.learning.DynamicProgramming.Memoization.Fibonacci;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class fibonacciTest
{
    private Fibonacci fib = new Fibonacci();
    private review.learning.DynamicProgramming.Tabulation.Fibonacci fibTab = new review.learning.DynamicProgramming.Tabulation.Fibonacci();

    @Test
    public void fibSmallTest()
    {
        int n=40;
        assertEquals(102334155,fib.fibonacci(40));
    }

    @Test
    public void fibMemoizationTest()
    {
        int n=40;
        assertEquals(102334155,fib.fibonacciMemoization(40));
    }
    @Test
    public void fibTabulationTest()
    {
        int n=40;
        assertEquals(102334155,fibTab.fibonacciTabulation(40));
    }

}
