package review.leetcode.leetcodeExtra;

public class ReverseInteger_7_M_MATH
{
    /*
    * https://leetcode.com/problems/reverse-integer/
    * */

    /*
    * we can retrieve lowest 10th by doing modular and division
    * and we can use a temporary variable to store current total.
    *
    * While this works just fine, the issue here becomes how do we ensure we don't have an integer overflow
    *
    */

    public int reverse(int x)
    {
        // if x - x = 0, then positive, else negative
        int signage = (x>0)?1:-1;
        int absoluteValue = Math.abs(x);
        int totalValue=0;

        while(absoluteValue!=0)
        {
            int modular = absoluteValue%10;

            int newTotal = totalValue * 10 + modular;

            /*
            * This code takes a bit of knowledge about how Integer overflows:
            * 1. Integer.MAX_VALUE + 1 = Integer.MIN_VALUE
            * 2. Integer.MIN_VALUE - 1 = Integer.MAX_VALUE
            *
            * What this means is if our values overflowed or underflowed,
            * any operations on it would no longer be the same number
            * */

            if(newTotal / 10 != totalValue) return 0;

            totalValue = newTotal;

            absoluteValue/=10;
        }

        return totalValue*signage;
    }
}
