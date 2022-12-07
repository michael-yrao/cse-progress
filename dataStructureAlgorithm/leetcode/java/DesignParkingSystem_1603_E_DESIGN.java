package review.leetcode.leetcodeExtra;

public class DesignParkingSystem_1603_E_DESIGN
{
    /*
    * https://leetcode.com/problems/design-parking-system/
    * */

    public static class ParkingSystem
    {
        private int bigMax;
        private int bigCounter=0;
        private int midMax;
        private int midCounter=0;
        private int smallMax;
        private int smallCounter=0;


        public ParkingSystem(int small, int medium, int big)
        {
            bigMax=big;
            midMax=medium;
            smallMax=small;
        }

        public boolean addCar(int carType)
        {
            if(carType==1)
            {
                if (smallCounter<smallMax) smallCounter++;
                else return false;
                return true;
            }
            else if(carType==2)
            {
                if (midCounter<midMax) midCounter++;
                else return false;
                return true;
            }
            else if(carType==3)
            {
                if (bigCounter<bigMax) bigCounter++;
                else return false;
                return true;
            }
            else return false;
        }
    }
}
