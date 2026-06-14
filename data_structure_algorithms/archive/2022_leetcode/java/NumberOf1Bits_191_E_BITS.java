package review.leetcode.blind75;

public class NumberOf1Bits_191_E_BITS
{
    /*
    * https://leetcode.com/problems/number-of-1-bits/
    * */

    /*
    * Computers store integers as Two's Complements
    *
    * e.g. 28 in binary is 0 0 0 1 1 1 0 0
    *
    * In order to represent -28 in Two's Complements, we need to do the following:
    *   1. Flip all bits of 28
    *   2. Add 1
    *
    * Therefore, -28 would become something like this:
    *   1. Flip the bits : 0 0 0 1 1 1 0 0 -> 1 1 1 0 0 0 1 1
    *   2. Add 1         : 1 1 1 0 0 0 1 1 -> 1 1 1 0 0 1 0 0
    *
    * -28 is represented as 1 1 1 0 0 1 0 0 in Two's Complements
    *
    * */

    public int hammingWeight(int n)
    {
        // n&(n-1) is extremely useful in binary calculation:
        //  1. The result of n&(n-1) flips the right most 1 to 0, e..g. 0b00010110 & 0b00010101 = 0b00010100
        //  2. n&(n-1) == 0 is always true if the number is a power of 2
        //
        // We can use this as a way to count number of 1s, e.g. if n&(n-1)!=0, then add 1
        int count=0;
        while(n != 0)
        {
            n=n&(n-1);
            count++;
        }
        return count;
    }
}
