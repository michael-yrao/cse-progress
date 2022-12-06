package review.leetcode.leetcodeExtra;

public class PowerOfFour_342_E_MATH
{
    /*
    * https://leetcode.com/problems/power-of-four/
    * */

    /*
    * 0 1 2 4 8 16 32 64 128
    * - 0 1 2 3 4   5  6   7
    *
    * N Y N Y N Y   N  Y   N
    *
    * Even powers of 2 are also powers of 4, so we will be using that fact to do this problem
    *
    * We can use n&(n-1) to check if this is a power of 2 but am currently not sure how to check if even/odd without loop
    *
    * A really silly solution is literally just math:
    *
    *   num = log(n)/log(4)
    *   if(Math.pow(4,num) != n) return false;
    *
    * */

    public boolean isPowerOfFour(int n)
    {
        if(n==0) return false;
        int num = (int)(Math.log(n) / Math.log(4));
        return ((int)Math.pow(4,num))==n;
    }
}
