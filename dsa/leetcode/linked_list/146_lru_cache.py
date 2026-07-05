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