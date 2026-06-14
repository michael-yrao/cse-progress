package review.leetcode.blind75;

import java.util.Arrays;

public class DecodeWays_91_M_1DP
{
    /*
    * https://leetcode.com/problems/decode-ways/
    * */

    /*
        "1" -> 1
        "12" -> 2 (1 2, 12)
        "122" -> 3 (1 2 2, 1 22, 12 2)
        "1221" -> 5 (1 2 2 1, 1 2 21, 1 22 1, 12 2 1, 12 21)

        table[i] = table[i-1] + table[i-2]

        "1" -> 1
        "10" -> 1
        "101" -> 1 (since 01 can't be mapped, we only got 1)
        "1010" -> 2

        not sure about zero yet, re-visit

        "1" -> 1
        "12" -> 2
        "123" -> 3
        "1234" -> 3 (1 2 3 4, 1 23 4, 12 3 4)

        table[i] = table[i-1]

        Try going from last character to first character instead to try to tackle 0s

        "0" -> 0
        "10" -> 1
        "01" -> 0

        From this example, we can see that if we are on the index of value 0, we will always end up with a zero
    */

    public int numDecodings(String s)
    {
        int[] table = new int[s.length()+1];
        table[table.length-1]=1;
        table[table.length-2]=(s.charAt(s.length()-1)=='0')?0:1;

        for(int i=table.length-3;i>=0;i--)
        {
            int calc = (s.charAt(i) - '0') * 10 + (s.charAt(i+1) - '0');
            if(s.charAt(i)=='0')
                table[i]=0;
            else
            {
                if(calc>26) table[i] = table[i+1];          // Logic described from lines 31 - 36
                else table[i] = table[i+1] + table[i+2];    // Base logic described from lines 14 - 22
            }
        }
        return table[0];
    }

    /*
    * This way feels really silly and convoluted
    * */

    public int numDecodingsConvoluted(String s)
    {
        // We will use the index of the table as the number of character in String input + 1
        // e.g. index 0 will mean we have empty string, defaulted to 1 way to decode
        //      index 1 will mean we are at first char in String s. If first index is 0, that means it's not a valid alphabet
        //      Thus if char==0, then 0 else 1

        int[] table = new int[s.length()+1];
        table[0]=1;
        table[1]=(s.charAt(0)-'0'==0)?0:1;

        for(int i=2;i<table.length;i++)
        {
            if(s.charAt(i-1) != '0') table[i] += table[i-1];
            if(s.charAt(i-2) == '1' || (s.charAt(i-2) == '2' && s.charAt(i-2) < '7')) table[i] += table[i-2];
        }
        return table[s.length()];
    }
}
