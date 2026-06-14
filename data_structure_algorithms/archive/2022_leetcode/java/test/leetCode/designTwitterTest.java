package leetCode;

import org.junit.jupiter.api.Test;
import review.leetcode.leetcodeExtra.DesignTwitter_335_M_HEAP;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class designTwitterTest
{
    DesignTwitter_335_M_HEAP.Twitter twitter = new DesignTwitter_335_M_HEAP.Twitter();

    @Test
    public void twitterTest1()
    {
        twitter.postTweet(1,5);
        List<Integer> expectedList = new ArrayList<>();
        expectedList.add(5);
        assertEquals(expectedList,twitter.getNewsFeed(1));
    }

    @Test
    public void twitterTest2()
    {
        twitter.postTweet(1,5);
        twitter.follow(1,2);
        twitter.postTweet(2,6);

        List<Integer> expectedList = new ArrayList<>();
        expectedList.add(5);
        expectedList.add(6);
        assertEquals(expectedList,twitter.getNewsFeed(1));
    }

    @Test
    public void twitterTest3()
    {
        twitter.postTweet(1,5);
        twitter.postTweet(1,3);
        twitter.postTweet(1,101);
        twitter.postTweet(1,13);
        twitter.postTweet(1,10);
        twitter.postTweet(1,2);
        twitter.postTweet(1,94);
        twitter.postTweet(1,505);
        twitter.postTweet(1,333);
        twitter.postTweet(1,22);
        twitter.postTweet(1,11);

        List<Integer> expectedList = new ArrayList<>();
        expectedList.add(11);
        expectedList.add(22);
        expectedList.add(333);
        expectedList.add(505);
        expectedList.add(94);
        expectedList.add(2);
        expectedList.add(10);
        expectedList.add(13);
        expectedList.add(101);
        expectedList.add(3);
        assertEquals(expectedList,twitter.getNewsFeed(1));
    }

}
