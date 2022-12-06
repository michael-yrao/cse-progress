package review.leetcode.leetcodeExtra;

public class SqrtX_69_E_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/sqrtx/
    * */

    /*
    * My initial attempt was actually just traversing through 0-x but wasn't accepted by LC as it took too long
    * So as a result, we needed a O(logn) solution which leads us to Binary Search
    *
    * If we draw out enumerate(x), we will see that we will never need to pass x/2 to get to the result
    * for example, if we were looking for sqrt(8), solution is 2, which is exactly halfway:     1 2 3 4
    * We can also notice that 2^2 is actually less than 8,                                      1 4 9 16
    * Therefore, the solution^2 <= x. So we will update solution if middle^2 < x
    * */
    public int mySqrt(int x)
    {
        if(x==0 || x==1) return x;
        int left=1, right=x/2, result=0;
        long middleSquared;
        while(right>=left)
        {
            int middle=(left+right)/2;
            middleSquared=(long)middle * (long)middle;
            if(middleSquared==x) return middle;
            else if(middleSquared < x)
            {
                result=middle;
                left = middle + 1;
            }
            else
            {
                right = middle - 1;
            }
        }
        return result;
    }

    /*
    * Newton's Algorithm
    * */
    public int mySqrtNewton(int x)
    {
        long result = x;
        while(result * result > x)
        {
            result = (result + x/result)/2;
        }
        return (int)result;
    }
}
