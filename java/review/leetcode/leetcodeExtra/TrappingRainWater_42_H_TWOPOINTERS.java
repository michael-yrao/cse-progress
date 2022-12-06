package review.leetcode.leetcodeExtra;

public class TrappingRainWater_42_H_TWOPOINTERS
{
    /*
    * https://leetcode.com/problems/trapping-rain-water/
    * */

    // Need to get max left and max right for each value in the array
    // We then need the min(maxLeft,maxRight) to get how much water is trapped for each index
    // We then need to subtract however much the height is at that specific index
    // Logic: min(maxLeft[i],maxRight[i]) - h[i] for each index

    public int trap(int[] height)
    {
        {
        /*
            things we can notice by reading the problem:
                1. left-most and right-most cannot gather water
                2. water gathered is constricted by Math.min(leftMax,rightMax) and value of water that can be gathered is
                   Math.min(leftMax,rightMax) - height[i]
                        a. Key is here, need to determine left Max and right Max for each element

                Example 1:

                maxLeft =  [0,0,1,1,2,2,2,2,3,3,3,3]
                maxRight = [3,3,3,3,3,3,3,2,2,2,1,0]
                height =   [0,1,0,2,1,0,1,3,2,1,2,1]

                endresult = 0+0+1+0+1+2+1+0+0+1+0+0 = 6

                So how to determine maxLeft/maxRight..
        */
            int[] maxLeft = new int[height.length];
            int[] maxRight = new int[height.length];

            // Java defaults to 0 always but write this for clarity sake

            maxLeft[0] = 0;

            int currentMax = Integer.MIN_VALUE;

            for(int i=0;i<maxLeft.length;i++)
            {
                currentMax = Math.max(currentMax,height[i]);
                maxLeft[i] = currentMax;
            }

            maxRight[maxRight.length-1] = 0;

            currentMax = Integer.MIN_VALUE;

            for(int i=maxRight.length-1;i>=0;i--)
            {
                currentMax = Math.max(currentMax,height[i]);
                maxRight[i] = currentMax;
            }

            int water = 0;

            for(int i=0;i<height.length;i++)
            {
                // If Math.min - height < 0, we need to just add 0
                water += Math.max(Math.min(maxLeft[i], maxRight[i]) - height[i], 0);
            }
            return water;
        }
    }

    public int trapTwoPointers(int[] height)
    {
        if(height==null || height.length==0) return 0;

        int left = 0, leftMax = height[left];
        int right = height.length-1, rightMax = height[right];
        int waterCount=0;

        while(left<right)
        {
            if(leftMax<rightMax)
            {
                left++;
                leftMax = Math.max(leftMax, height[left]); // leftMax will never be less than 0 here
                waterCount+=(leftMax-height[left]);
            }
            else
            {
                right--;
                rightMax = Math.max(rightMax, height[right]); // rightMax will never be less than 0 here
                waterCount+=(rightMax-height[right]);
            }
        }
        return waterCount;
    }
}
