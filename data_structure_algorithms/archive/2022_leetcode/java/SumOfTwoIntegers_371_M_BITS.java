package review.leetcode.blind75;

public class SumOfTwoIntegers_371_M_BITS
{
    /*
    * https://leetcode.com/problems/sum-of-two-integers/
    * */

    /*

    Adder Logic:
        1. Addition  = A ^ B
        2. Carry-Out = A & B
        3. Carry-In  = Carry-Out << 1

    Result = Addition + Carry-In

    0001
    0010
    0011 + (0000 << 1) = 0011 (No Carry-In)

    0010
    0011

    0001 + (0010 << 1) = 0001 + 0100 = 0101

    */

    public int getSumIterative(int a, int b)
    {
        while(b!=0)
        {
            int carry = a & b;  // Carry-Out
            a = a ^ b;          // Sum
            b = carry << 1;     // Carry-In, this allows it to be added to the Sum at each step
        }
        return a;
    }

    /*
    * param1 is to be used as Sum
    * param2 is to be used as Carry
    * */

    public int getSumRecursion(int a, int b)
    {
        if(b==0) return a; // If no carry, it's straightforward sum

        int initialSum = a ^ b;
        int carryOut = a & b;
        int carryIn = carryOut << 1;

        return getSumRecursion(initialSum,carryIn);
    }
}
