package review.test.learning;

import org.junit.jupiter.api.Test;
import review.learning.DynamicProgramming.Memoization.GridTraveler;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class gridTravelerTest
{
    private GridTraveler gridTraveler = new GridTraveler();
    private review.learning.DynamicProgramming.Tabulation.GridTraveler gridTravelerTab = new review.learning.DynamicProgramming.Tabulation.GridTraveler();

    @Test
    public void gridTravelerTest1()
    {
        int m = 3, n = 3;
        assertEquals(6,gridTraveler.gridTraveler(m,n));
    }

    @Test
    public void gridTravelerMemoTest1()
    {
        int m = 3, n = 3;
        assertEquals(6,gridTraveler.gridTravelerMemoization(m,n));
    }

    @Test
    public void gridTravelerTabTest1()
    {
        int m = 3, n = 3;
        assertEquals(6,gridTravelerTab.gridTraveler(m,n));
    }

    @Test
    public void gridTravelerTabTest2()
    {
        int m = 18, n = 18;
        assertEquals(2333606220L,gridTravelerTab.gridTraveler(m,n));
    }

    @Test
    public void gridTravelerMemoTest2()
    {
        int m = 18, n = 18;
        assertEquals(2333606220L,gridTraveler.gridTravelerMemoization(m,n));
    }

}
