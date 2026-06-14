package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class FruitIntoBaskets_904_M_SLIDINGWINDOW
{
    /*
    * https://leetcode.com/problems/fruit-into-baskets/
    * */

    /*
    * If we analyze the examples, we will see that we are trying to get the biggest window possible
    * So thus a sliding window problem.
    *
    * We are given that we have 2 baskets that can hold 1 type of fruit each, so we will start our pointers at 0 and 1
    * Idea is that we don't want fruits of different types than 2
    * So we just need to keep track of fruits we are currently holding, we can use a Set for that
    *
    * After implementing this, I realized I can't actually keep track of how many elements are between right and left
    * Just by using a Set, thus we will use a HashMap instead
    *
    * */
    public int totalFruit(int[] fruits)
    {
        int left=0, right=0;
        Map<Integer,Integer> fruitMap = new HashMap<>();

        int maxSize = 0;

        while(right < fruits.length)
        {
            // Put fruit into our basket
            fruitMap.put(fruits[right], fruitMap.getOrDefault(fruits[right],0) + 1);
            while (fruitMap.size() > 2)
            {
                // If more than 2 fruits, we want to decrement left side until
                fruitMap.put(fruits[left], fruitMap.get(fruits[left]) - 1);
                // Get rid of left fruit if it is at zero frequency
                fruitMap.remove(fruits[left],0);
                left++;
            }
            maxSize = Math.max(maxSize,right-left+1);
            right++;
        }
        return maxSize;
    }
}
