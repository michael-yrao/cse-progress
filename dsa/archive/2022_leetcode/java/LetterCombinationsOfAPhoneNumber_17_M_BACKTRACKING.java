package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class LetterCombinationsOfAPhoneNumber_17_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/letter-combinations-of-a-phone-number/
    * */

    /*
    * Input: digits = "23"
    * Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    * */

    /*
    * We will use a Hashmap to map the digits to their respective characters
    * */

    private Map<Character, String> digitToChar = Map.of
    (
            '2', "abc",
            '3', "def",
            '4', "ghi",
            '5', "jkl",
            '6', "mno",
            '7', "pqrs",
            '8', "tuv",
            '9', "wxyz"
    );

    public List<String> letterCombinations(String digits)
    {
        if(digits.length()==0) return new ArrayList<>();

        // Result List
        List<String> resultList = new ArrayList<>();

        // Current String we are trying to build
        String currentString = "";

        // We need to pass index for the current character we are traversing from digits
        backtrack(digits,0,currentString,resultList);

        return resultList;
    }

    private void backtrack(String digits, int index, String currentString, List<String> resultList)
    {
        // base cases
        if(currentString.length() == digits.length())
        {
            // We are not doing copy here since every traversal in this DFS is unique
            resultList.add(currentString);
            return;
        }
        else if(index >= digits.length()) return;

        // For each character in our character array, do DFS to get character at next index

        for(Character x : digitToChar.get(digits.charAt(index)).toCharArray())
        {
            backtrack(digits, index + 1,currentString + x, resultList);
        }
    }
}
