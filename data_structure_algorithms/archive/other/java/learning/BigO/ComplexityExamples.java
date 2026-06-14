package review.learning.BigO;

import java.util.HashMap;
import java.util.Map;

public class ComplexityExamples
{
    /*
    * Below is a basic recursion method
    *
    * Since we have n function calls, we have a time complexity of O(n)
    * Similarly, since we have n function calls, due to the call stack, the space complexity is also O(n)
    * */

    public int recursion(int n)
    {
        if(n<=1) return 0;
        return 1+recursion(n-1);
    }

    /*
    * Here is another basic recursion method
    *
    * Even though we do half the recursive calls of the prior method,
    * we would still have O(n/2) which simplifies to O(n) for both space and time complexities
    * */

    public int differentRecursion(int n)
    {
        if(n<=1) return 0;
        return 1+differentRecursion(n-2);
    }

    /*
    * 2 recursive calls both at the speed of n - 1
    * Time Complexity: O(2^n)
    * Space Complexity: O(n)
    *
    * */

    public void dib(int n)
    {
        if(n<=1) return;
        dib(n-1);
        dib(n-1);
    }

    /*
    * Memoized Fibonacci copy pasted from DP/Memoization/Fibonacci
    *
    * Time Complexity: O(n)
    * Space Complexity: O(n)
    * */

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
