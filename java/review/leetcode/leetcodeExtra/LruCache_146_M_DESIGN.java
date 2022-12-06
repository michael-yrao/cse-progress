package review.leetcode.leetcodeExtra;

import DataModel.Node;
import DataStructure.Pair;

import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class LruCache_146_M_DESIGN
{
    /*
    * https://leetcode.com/problems/lru-cache/
    * */

    int capacity;
    Map<Integer,lruNode> cache;
    lruNode leastRecentlyUsed; // left side
    lruNode mostRecentlyUsed;  // right side

    /*
    * Difficulty of this problem comes in what it means when Least Recently Used
    * We need to keep track of how many times the values get used, both put and get counts as usages
    *
    *   1. Have a HashMap for O(1) access to the values
    *   2. Use a Doubly-Linked List so we can keep track of the ordering of the usages
    *   3. As such, we would need two pointers here, the least recently used and most recently used nodes
    *
    * */

    public LruCache_146_M_DESIGN(int capacity)
    {
        this.capacity = capacity;
        cache = new HashMap<>();

        // Create some dummy nodes
        this.leastRecentlyUsed = new lruNode(0,0);
        this.mostRecentlyUsed = new lruNode(0,0);
        this.leastRecentlyUsed.next = this.mostRecentlyUsed;
        this.mostRecentlyUsed.prev = this.leastRecentlyUsed;
    }

    public int get(int key)
    {
        if(cache.containsKey(key))
        {
            // We need to move this node up to most recently used
            // Easiest way to do this is to get rid of this node and re-insert it at the right
            // So we will have a remove function to remove from the list
            // As well as an insert function to add to the end of the list
            remove(cache.get(key));
            insert(cache.get(key));
            return cache.get(key).value;
        }
        else return -1;
    }

    public void put(int key, int value)
    {
        // If node already exist, we need to modify it to have newest value
        // But since we need to update it to most recently used, it is actually more practical just to remove it entirely
        if(cache.containsKey(key)) remove(cache.get(key));
        // Same idea here as get, we need to set this node to most recently used using our insert function
        cache.put(key, new lruNode(key,value));
        insert(cache.get(key));

        // If we are passed capacity, get rid of the least recently used node
        // Remember that we put a dummy node for both LRU and MRU, so we need to get rid of LRU.next
        // Our remove function will take care of the rerouting of the pointers
        if(cache.size() > capacity)
        {
            lruNode lruNode = leastRecentlyUsed.next;
            remove(lruNode);
            cache.remove(lruNode.key);
        }
    }

    private void remove(lruNode node)
    {
        lruNode prev = node.prev;
        lruNode next = node.next;
        prev.next = next;
        next.prev = prev;
    }

    private void insert(lruNode node)
    {
        lruNode prev = mostRecentlyUsed.prev;
        prev.next = node;
        node.prev = prev;
        node.next = mostRecentlyUsed;
        mostRecentlyUsed.prev = node;
    }

    private class lruNode
    {
        int key,value;
        lruNode prev,next;
        public lruNode(int key, int value)
        {
            this.key=key;
            this.value=value;
            prev = null;
            next = null;
        }
    }
}
