package review.leetcode.leetcodeExtra;

public class FindTheCelebrity_277_M_MISC
{
    /*
    * This problem is Premium:
     * https://leetcode.com/problems/find-the-celebrity/
    *
    * You can find the same problem on LintCode:
    * https://www.lintcode.com/problem/645/
    * */

    /*
    * Given that we are at a party with n people and 1 of them is a celebrity
    * n-1 people at the party know the celebrity
    * but the celebrity does not know any of them
    *
    * We are also given a blackbox helper function: boolean knows(a,b) where A will tell you if A knows B
    *
    * From here, we can deduce that:
    *   1. if(knows(a,b)) then b is the candidate to be the celebrity
    *   2. if(!know(a,b)) then a is the candidate to be the celebrity
    *
    * */


    // Algorithm:
    // 1. Find celebrity
    // 2. Validate to make sure celebrity knows no one else and everyone knows him
    public int findCelebrity(int n)
    {
        int candidate = 0;

        // If candidate knows i, that means i can be the candidate
        // Thus we update candidate to be i, finding our celebrity
        for(int person=1;person<n;person++)
        {
            if(knows(candidate,person)) candidate = person;
        }

        // Check if celebrity knows anyone else or if everyone knows candidate
        for(int person=0;person<n;person++)
        {
            // Don't ask candidate about themselves
            // If candidate knows person OR if person doesn't know candidate
            // That means candidate is not the celebrity
            if(person!=candidate && knows(candidate,person) || !knows(person,candidate)) return -1;
        }

        return candidate;
    }

    // This is a blackbox from LeetCode
    // Adding a dummy here just so our project can build
    private boolean knows(int personA, int personB)
    {
        return false;
    }
}
