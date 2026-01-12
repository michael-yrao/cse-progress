package review.leetcode.blind75;

public class ContainerWithMostWater_11_M_SLIDINGWINDOW
{
    /*
    * https://leetcode.com/problems/container-with-most-water/
    * */

    public int maxArea(int[] height)
    {
        int max = Integer.MIN_VALUE;
        int left=0, right=height.length-1;
        while(left<right)
        {
            max = Math.max(max,(right-left)*Math.min(height[left],height[right]));
            if(height[left] > height[right]) right--;
            else left++;
        }
        return max;
    }

    public int maxAreaLongerSolution(int[] height)
    {
        int maxArea=0;
        if(height.length<2) return maxArea;
        int leftIndex=0;
        int rightIndex=height.length-1;
        while(leftIndex<rightIndex)
        {
            int currentArea = (rightIndex-leftIndex) * Math.min(height[leftIndex],height[rightIndex]);
            maxArea = Math.max(maxArea,currentArea);
            if(height[leftIndex]<height[rightIndex])
            {
                leftIndex++;
            }
            else if (height[leftIndex]>height[rightIndex])
            {
                rightIndex--;
            }
            else // Shift with highest next one in mind
            {
                if(height[leftIndex+1]>height[rightIndex-1]) leftIndex++;
                else rightIndex--;
            }
        }
        return maxArea;
    }
}
