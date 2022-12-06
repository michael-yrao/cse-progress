package review.learning.DynamicProgramming.Tabulation;

public class Fibonacci
{
    public int fibonacci(int n)
    {
        if(n==0) return 0;
        if(n==1) return 1;
        return fibonacci(n-1)+fibonacci(n-2);
    }


    /*
    * Time: O(n)
    * Space: O(n)
    * */

    public int fibonacciTabulation(int n)
    {
        int[] tab = new int[n+1]; // Java initializes int array with 0s
        tab[0] = 0;
        tab[1] = 1;

        int firstPosition = 0;
        int secondPosition = 1;

        for(int i=2;i<tab.length;i++)
        {
            tab[i] = tab[firstPosition++] + tab[secondPosition++];
        }
        return tab[n];
    }



}
