"""
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

    LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
    int get(int key) Return the value of the key if the key exists, otherwise return -1.
    void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Example 1:

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4

Constraints:

    1 <= capacity <= 3000
    0 <= key <= 104
    0 <= value <= 105
    At most 2 * 105 calls will be made to get and put.
"""
from typing import Optional


# ── Attempt · 2026-07-16 ──────────────
class ListNode:

    def __init__(self, key: int, value: int, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next

class LRUCache_20260716:
# LRU is a doubly linked list
# we want to always have two dummies
# one for LRU and one for MRU
# this way both can be accessed in constant time
# we will have MRU at the head, and LRU at the tail
# this is also a cache with key value so we need a map of key -> Node

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = ListNode(-1,-1)
        self.tail = ListNode(-1,-1)
        self.head.next = self.tail
        self.head.prev = None
        self.tail.next = None
        self.tail.prev = self.head

    def delete(self, node: ListNode) -> None:
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode

    def insert(self, node: ListNode) -> None:
        headNext = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = headNext
        headNext.prev = node

    def get(self, key: int) -> int:
        returnValue = -1
        if key in self.cache:
            node = self.cache[key]
            returnValue = node.value
            # now we move this item to MRU
            # so we need a delete and insert for nodes
            self.delete(node)
            self.insert(node)
        return returnValue

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            # we accessed it, thus it is now MRU
            self.delete(node)
            self.insert(node)
        else:
            node = ListNode(key,value)
            self.cache[key] = node
            self.insert(node)

        # now we check if we are over capacity
        while len(self.cache) > self.capacity:
            lru = self.tail.prev
            self.delete(lru) # type: ignore
            del self.cache[lru.key]

class Node_20260704:
    def __init__(self, key,val,prev=None,next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next

class LRUCache:
    def __init__(self, capacity: int):
        # get needing O(1) average time means we need a map or a set
        # this cache will store key -> Node(key,value)
        self.cache = {}
        # put needing O(1) is a bit sus, we need to move the key, value to MSU if it already exists
        self.capacity = capacity
        # dummy head and tail to ensure no real data is on the edge
        # this way every single node works exactly the same way
        # MRU
        self.head = Node_20260704(-1,-1)
        # LRU
        self.tail = Node_20260704(-1,-1)
        self.head.next = self.tail
        self.tail.prev = self.head

    # we need to be able to remove when a key/value already exists
    def remove(self, node) -> None:
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode

    # we need to be able to insert at MRU
    def insert(self, node) -> None:
        headNext = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = headNext
        headNext.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # move the value to MRU
            self.remove(node)
            self.insert(node)
            return node.val
        return -1
        
    def put(self, key: int, value: int) -> None:
        # if key already exist in map, we do remove
        if key in self.cache:
            nodeToRemove = self.cache[key]
            self.remove(nodeToRemove)
        # now we put it in the front
        newNode = Node_20260704(key,value)
        self.insert(newNode)
        self.cache[key] = newNode
        # now we check if we are over capacity

        while len(self.cache) > self.capacity:
            lru = self.tail.prev
            self.remove(lru)
            del self.cache[lru.key]


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

# whole point of LRU is that we need to be able to access LRU and MRU at O(1) time
# so this means we should have a doubly linked list with two dummy nodes
# one at the head to be able to access MRU
# one at the tail to be able to access LRU

class ListNode_20260707:
    def __init__(self, key: int, value: int, prev: Optional[ListNode_20260707] = None, next: Optional[ListNode_20260707] = None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next

class LRUCache_20260707:

    def __init__(self, capacity: int):
        self.capacity = capacity
        # key -> ListNode
        self.map = {}
        self.head = ListNode_20260707(-1,-1)
        self.tail = ListNode_20260707(-1,-1)
        self.head.next = self.tail
        self.head.prev = None
        self.tail.next = None
        self.tail.prev = self.head

    def delete(self, node) -> None:
        nextNode = node.next
        prevNode = node.prev
        prevNode.next = node.next
        nextNode.prev = prevNode

    def insert(self, node) -> None:
        nextNode = self.head.next
        self.head.next = node
        node.next = nextNode
        node.prev = self.head
        nextNode.prev = node

    def get(self, key: int) -> int:
        # go through the list to get the value and then also put it to MRU
        # so we need a way to insert/delete a node here
        if key in self.map:
            node = self.map[key]
            self.delete(node)
            self.insert(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self.delete(self.map[key])
        node = ListNode_20260707(key,value)
        self.insert(node)
        self.map[key] = node
        # we did have a capacity, so check capacity and remove nodes from LRU as needed

        while len(self.map) > self.capacity:
            lru = self.tail.prev
            self.delete(lru)
            del self.map[lru.key]

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
