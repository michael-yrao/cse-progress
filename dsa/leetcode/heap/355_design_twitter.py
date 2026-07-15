"""
Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:

    Twitter() Initializes your twitter object.
    void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.
    List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be ordered from most recent to least recent.
    void follow(int followerId, int followeeId) The user with ID followerId started following the user with ID followeeId.
    void unfollow(int followerId, int followeeId) The user with ID followerId started unfollowing the user with ID followeeId.

Example 1:

Input
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
Output
[null, null, [5], null, null, [6, 5], null, [5]]

Explanation
Twitter twitter = new Twitter();
twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
twitter.follow(1, 2);    // User 1 follows user 2.
twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
twitter.unfollow(1, 2);  // User 1 unfollows user 2.
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.

Constraints:

    1 <= userId, followerId, followeeId <= 500
    0 <= tweetId <= 104
    All the tweets have unique IDs.
    At most 3 * 104 calls will be made to postTweet, getNewsFeed, follow, and unfollow.
    A user cannot follow himself.
"""
import collections
import heapq
from typing import List


# ── Attempt · 2026-07-15 ──────────────
class Twitter_20260715:

    def __init__(self):
        self.globalTime = 0
        self.tweetMap = collections.defaultdict(list)
        self.followeeMap = collections.defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append((self.globalTime, tweetId))
        self.globalTime+=1

    def getNewsFeed(self, userId: int) -> List[int]:
        minHeap = []
        if userId not in self.followeeMap[userId]:
            self.follow(userId, userId)
        # for each user this userId follows
        # add their tweet to the heap
        for followee in self.followeeMap[userId]:
            for time, tweetId in self.tweetMap[followee]:
                heapq.heappush(minHeap,(time,tweetId))
                while len(minHeap) > 10:
                    heapq.heappop(minHeap)
        # now we have a heap in reverse order
        returnList = []
        while minHeap:
            tweetId = heapq.heappop(minHeap)[1]
            returnList.append(tweetId)
        returnList.reverse()
        return returnList
        

    def follow(self, followerId: int, followeeId: int) -> None:
        # check if we follow ourselves, if not add self
        if followerId not in self.followeeMap[followerId]:
            self.followeeMap[followerId].append(followerId)
        
        if followeeId not in self.followeeMap[followerId]:
            self.followeeMap[followerId].append(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followeeMap[followerId]:
            self.followeeMap[followerId].remove(followeeId)

class Twitter:

    def __init__(self):
        # globalTweetCount to keep track of heap
        self.globalTweetCount = 0
        # person -> followee
        self.followMap = collections.defaultdict(list)
        # person -> (globalTweetCount, tweet)
        self.tweetMap = collections.defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        # add to tweet map
        self.tweetMap[userId].append((self.globalTweetCount, tweetId))
        self.globalTweetCount+=1

    def getNewsFeed(self, userId: int) -> List[int]:
        result = []
        heap = []
        
        # build a heap with all the values in tweetMap that this user follows
        # or the user himself
        
        relevantUsers = set(self.followMap[userId]) | {userId}
        
        for user in relevantUsers:
            for timestamp, tweetId in self.tweetMap[user]:
                # timestamp goes up, so we need to negate it to get latest
                heapq.heappush(heap, (-timestamp, tweetId))
        
        # now we get 10 or until heap
        while heap and len(result) < 10:
            currentFeed = heapq.heappop(heap)
            result.append(currentFeed[1])
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].append(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)

class Twitter_20260626:
    # when we initialize twitter, we are not initializing a twitter user
    # we are the backend, so when we initialize twitter, we are saying we are starting the services for twitter
    
    # need a way to track time so we will use a global counter like basic ID
    idCounter = 0

    def __init__(self):
        # post tweet needs to store a user's tweets
        # if we need to retrieve by latest, we need to store those with a timestamp
        # so we will do user -> list of (timestamp, tweetId)
        self.tweetMap = collections.defaultdict(list)
        # also need a map of who follows x, so x -> list of followers
        self.followingMap = collections.defaultdict(list)


    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append((self.idCounter, tweetId))
        self.idCounter+=1
        
    def getNewsFeed(self, userId: int) -> List[int]:
        # get the list of users userId follows
        followingSet = set(self.followingMap[userId])
        # add self to followingSet
        followingSet.add(userId)
        # now we need to get the latest tweets by these users
        maxHeap = []
        for followee in followingSet:
            for time, tweet in self.tweetMap[followee]:
                heapq.heappush(maxHeap, (-time, tweet))

        result = []
        # now we get top 10 and return
        while maxHeap and len(result) < 10:        
            tweet = heapq.heappop(maxHeap)[1]
            result.append(tweet)
        return result[::-1]

    def follow(self, followerId: int, followeeId: int) -> None:
        # follow means follower gained a followee
        self.followingMap[followerId].append(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followingMap[followerId]:
            self.followingMap[followerId].remove(followeeId)
        


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)

class Twitter_20260706:
    def __init__(self):
        # so we are starting up twitter
        # so we need to keep track of who each user follows (user -> followees)
        # we also need to keep track of the posts for each user so user -> posts
        # we need a way to keep track of 10 most recent, so we can use time
        # for simplicity, we will use a global integer time and we will use a heap for 10 highest time
        self.followeeMap = collections.defaultdict(list)
        self.tweetMap = collections.defaultdict(list)     
        self.time = 0   

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append((self.time, tweetId))
        self.time+=1

    def getNewsFeed(self, userId: int) -> List[int]:
        # add self as followee if not already in there
        if userId not in self.followeeMap[userId]:
            self.followeeMap[userId].append(userId)
        # now we go through top 10 posts by followees
        # how should we do this though, just go through tweetMap I guess
        # we also wanna use a min heap instead of max heap so we get rid of smallest
        heap = []
        for followee in self.tweetMap:
            if followee in self.followeeMap[userId]:
                for time, tweetId in self.tweetMap[followee]:
                    heapq.heappush(heap,(time, tweetId))
                    if len(heap) > 10:
                        heapq.heappop(heap)
        result = []
        while heap:
            time,tweetId = heapq.heappop(heap)
            result.append(tweetId)
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followeeMap[followerId].append(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followeeMap[followerId]:
            self.followeeMap[followerId].remove(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
