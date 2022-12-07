package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.NQueens_51_H_BACKTRACKING;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class nQueensTest
{
    public NQueens_51_H_BACKTRACKING nQueens = new NQueens_51_H_BACKTRACKING();

    @Test
    public void nQueensTest1()
    {
        List<List<String>> expectedResult = new ArrayList<>();
        List<String> list1 = new ArrayList<>();
        list1.add(".Q..");
        list1.add("...Q");
        list1.add("Q...");
        list1.add("..Q.");
        expectedResult.add(list1);
        List<String> list2 = new ArrayList<>();
        list2.add("..Q.");
        list2.add("Q...");
        list2.add("...Q");
        list2.add(".Q..");
        expectedResult.add(list2);
        assertEquals(expectedResult, nQueens.solveNQueens(4));
    }
}
