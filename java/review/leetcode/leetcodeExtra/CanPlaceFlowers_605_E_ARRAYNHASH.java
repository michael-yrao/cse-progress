package review.leetcode.leetcodeExtra;

public class CanPlaceFlowers_605_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/can-place-flowers/
    * */

    /*
    * Best way to go about this problem is to create a new array of flowerbed but with an extra 0 at the beginning and end
    * This way, we can start at index 1, check up until size - 2 to see if it's plantable
    * plantable = f[i-1] == 0 && f[i] == 0 && f[i+1]==0
    * */

    public boolean canPlaceFlowers(int[] flowerbed, int n)
    {
        int[] newFlowerBed = new int[flowerbed.length+2];

        int numberOfFlowersPlanted=0;

        for(int i=0;i<flowerbed.length;i++) newFlowerBed[i + 1] = flowerbed[i];

        for(int i=1;i<newFlowerBed.length-1;i++)
        {
            if(newFlowerBed[i-1]==0 && newFlowerBed[i]==0 && newFlowerBed[i+1]==0)
            {
                newFlowerBed[i] = 1;
                numberOfFlowersPlanted++;
            }
        }
        return (n-numberOfFlowersPlanted<=0);
    }
}
