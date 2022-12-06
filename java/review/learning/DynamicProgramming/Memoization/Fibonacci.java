package review.learning.DynamicProgramming.Memoization;

import java.util.HashMap;
import java.util.Map;

public class Fibonacci
{

    // Classic Recursive solution of Fibonacci
    // However, this solution doesn't work for very big numbers as we would run into Stack Overflow
    // The issue here is we are recalculating the numbers that we have already calculated before
    // Time Complexity: O(2^n)

    public int fibonacci(int n)
    {
        if(n<=2) return 1;
        return fibonacci(n-1) + fibonacci(n-2);
    }

    // In order to solve bigger numbers, we need to use Memoization

    public int fibonacciMemoization(int n)
    {
        Map<Integer, Integer> memo = new HashMap<>();
        return fibonacciMemoizationHelper(n,memo);
    }

    public int fibonacciMemoizationHelper(int n, Map<Integer, Integer> memo)
    {
        // Memoization using HashMap
        // Add Memoization Map to argument so we don't create map on call stack
        // Key = n
        // Value = fib(n)

        if(memo.containsKey(n)) return memo.get(n);
        if(n<=2) return 1;
        memo.putIfAbsent(n,fibonacciMemoizationHelper(n-1,memo) + fibonacciMemoizationHelper(n-2,memo));
        return memo.get(n);
    }
}
