package review.leetcode.leetcodeExtra;

public class IntegerToEnglishWords_273_H_MATH
{
    /*
    * https://leetcode.com/problems/integer-to-english-words/
    * */

    /*
    * This problem seems quite annoying
    * First thing we need to do is think of all the unique words that can be formed
    * given that 0 <= num <= 2^31 - 1
    *   1. Increments of 1 up until 20: "One", "Two", etc.
    *   2. Increments of 10 up until 90: "Ten", "Twenty", "Thirty", etc.
    *   3. Hundred and Multiples of 1000: "Hundred", "Thousand", "Million", "Billion"
    *   5. There is also Zero, but that is only used for one single case so we can maybe use that as base case
    * */

    // Start all the Arrays with empty String so that the index matches the values
    private final String[] BELOW_10 = {"","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"};
    private final String[] BELOW_20 = {"Ten", "Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen"};
    private final String[] INCREMENTS_OF_10 = {"", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
    private final String[] SPECIAL_CASES = {"", "HUNDRED", "Thousand", "Million", "Billion"};


    // To generate the word, we need to do some modular arithmetic

    public String numberToWords(int num)
    {
        // Zero base case
        if(num==0) return "Zero";

        return generateWord(num);
    }

    private String generateWord(int num)
    {
        String result = "";

        // Between 1-19 are pretty straightforward and we can generate result immediately
        // Also these are used to describe every number thus we will use them as our base case
        // Starting at 21, we need to start concatting our Strings together and performing modular arithmetic

        // Below 20
        if (num<10) result = BELOW_10[num];
        else if (num<20) result = BELOW_20[num-10];
        // Below hundreds
        else if (num<100) result = INCREMENTS_OF_10[num/10] + " " + generateWord(num%10);
        // Below thousands
        else if(num<1000) result = generateWord(num/100) + " Hundred " + generateWord(num%100);
        // Below million
        else if(num<1000000) result = generateWord(num/1000) + " Thousand " + generateWord(num%1000);
        // Below billion
        else if(num<1000000000) result = generateWord(num/1000000) + " Million " + generateWord(num%1000000);
        // Above Billion
        else result = generateWord(num/1000000000) + " Billion " + generateWord(num%1000000000);
        return result.trim();
    }

}
