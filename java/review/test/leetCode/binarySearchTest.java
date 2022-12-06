package review.test.leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.blind75.MinimumInRotatedSortedArray_153_M_BINARYSEARCH;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class binarySearchTest
{
    private MinimumInRotatedSortedArray_153_M_BINARYSEARCH minimum = new MinimumInRotatedSortedArray_153_M_BINARYSEARCH();

    @Test
    public void minimumFirstTest()
    {
        int[] nums = new int[]{3,4,5,1,2};
        assertEquals(minimum.findMin(nums),1);
    }

    @Test
    public void minimumSecondTest()
    {
        int[] nums = new int[]{4,5,6,7,0,1,2};
        assertEquals(minimum.findMin(nums),0);
    }

    @Test
    public void minimumThirdTest()
    {
        int[] nums = new int[]{11,13,15,17};
        assertEquals(minimum.findMin(nums),11);
    }

    @Test
    public void minimumFourthTest()
    {
        int[] nums = new int[]{2,3,4,5,1};
        assertEquals(minimum.findMin(nums),1);
    }

    @Test
    public void minimumLengthTwoTest()
    {
        int[] nums = new int[]{2,1};
        assertEquals(minimum.findMin(nums),1);
    }


}
