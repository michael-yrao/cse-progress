package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class DesignTwitter_335_M_HEAP
{
    /*
    * https://leetcode.com/problems/design-twitter/
    * */

    public static class Twitter
    {
        /*
        * For each twitter user, we should have the following:
        *   1. Most obvious is userId, but we are designing twitter and not a twitter person,
        *      Twitter would instead have userId as the Key to getting details about that userId.
        *
        *   2. List of tweets made by userId, prioritized by time (e.g. newest -> oldest)
        *       a. tweets have their own tweetId, is an int and seem to go up incrementally,
        *          so a maxHeap seems like a good prioritization strategy since we want the newest tweets first.
        *          But two users might have the same tweetIds, so we actually need another determiner here,
        *          The idea is to use time but we will use a count for number of tweets for simplicity.
        *          Thus we should use a MaxHeap of Pair of count and TweetId. This way we can use count as overall time
        *
        *   3. List of followers, we can probably use a Set here since the userIds are unique and using a HashSet
        *      will be a O(1) operation for Insert/Delete/Find
        * */


        int globalTimeCounter=0;
        static int newsFeed=10;

        Map<Integer, PriorityQueue<Pair<Integer,Integer>>> tweetMap;
        Map<Integer, Set<Integer>> followingMap;

        public Twitter()
        {
            tweetMap = new HashMap<>();
            followingMap = new HashMap<>();
        }

        public void postTweet(int userId, int tweetId)
        {
            // If user hasn't posted anything before, create new MaxHeap
            if(!tweetMap.containsKey(userId)) tweetMap.put(userId, new PriorityQueue<>((o1, o2) -> o2.y - o1.y));

            tweetMap.get(userId).offer(new Pair(globalTimeCounter++, tweetId));
        }


         /*
         * Supposed to get top 10 from follower feed + self feed
         *
         * Let's use a MinHeap here and will convert to List as a result
         * Reason we use minheap is so we can compare smallest time in current heap to our traversal
         * This way we can make sure the top 10 are the most recent feeds
         * After which, we can create list from the heap.y
         *
         * */

        public List<Integer> getNewsFeed(int userId)
        {
            PriorityQueue<Pair<Integer,Integer>> minHeap = new PriorityQueue<>(Comparator.comparingInt(o -> o.x));

            // Adding a default news feed of the userId's tweets

            if(tweetMap.get(userId) != null && !tweetMap.isEmpty())
            {
                for(Pair<Integer,Integer> tweet : tweetMap.get(userId))
                {
                    if(minHeap.size() < newsFeed) minHeap.offer(tweet);
                    else
                    {
                        if (!minHeap.isEmpty() && tweet.x >= minHeap.peek().x)
                        {
                            minHeap.poll();
                            minHeap.offer(tweet);
                        }
                    }
                }
            }

            // Go through follower's tweets and update minHeap accordingly

            if(followingMap.get(userId) != null && !followingMap.isEmpty())
            {
                for (Integer follower : followingMap.get(userId)) {
                    if(tweetMap.get(follower) != null && !tweetMap.isEmpty())
                    {
                        for (Pair<Integer, Integer> tweet : tweetMap.get(follower)) {
                            if (minHeap.size() < newsFeed) minHeap.offer(tweet);
                            else
                            {
                                if (!minHeap.isEmpty() && tweet.x >= minHeap.peek().x) {
                                    minHeap.poll();
                                    minHeap.offer(tweet);
                                }
                            }
                        }
                    }
                }
            }

            List<Integer> list = new ArrayList<>();

            while(!minHeap.isEmpty())
            {
                list.add(minHeap.poll().y);
            }
            Collections.reverse(list);
            return list;
        }

        public void follow(int followerId, int followeeId)
        {
            if(!followingMap.containsKey(followerId)) followingMap.put(followerId, new HashSet<>());
            followingMap.get(followerId).add(followeeId);
        }

        public void unfollow(int followerId, int followeeId)
        {
            if(!followingMap.containsKey(followerId)) return;
            followingMap.get(followerId).remove(followeeId);
        }
    }
}
