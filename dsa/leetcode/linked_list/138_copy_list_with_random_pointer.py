"""
A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.

Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.

For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y.

Return the head of the copied linked list.

The linked list is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where:

    val: an integer representing Node.val
    random_index: the index of the node (range from 0 to n-1) that the random pointer points to, or null if it does not point to any node.

Your code will only be given the head of the original linked list.

Example 1:

Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]

Example 2:

Input: head = [[1,1],[2,1]]
Output: [[1,1],[2,1]]

Example 3:

Input: head = [[3,null],[3,0],[3,null]]
Output: [[3,null],[3,0],[3,null]]

Constraints:

    0 <= n <= 1000
    -104 <= Node.val <= 104
    Node.random is null or is pointing to some node in the linked list.
"""
# Definition for a Node.
from typing import Optional


class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None): # type: ignore
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:

    # ── Attempt · 2026-08-13 ──────────────
    def copyRandomList_20260813(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None
        # deep copy, so we do a old to new map
        oldToNewMap = {}
        traversal = head
        while traversal:
            newNode = Node(traversal.val)
            oldToNewMap[traversal] = newNode
            traversal = traversal.next

        # now that we got the mapping going, let's connect the new nodes
        traversal = head
        while traversal:
            newNode = oldToNewMap[traversal]
            if traversal.random:
                random = oldToNewMap[traversal.random]
                newNode.random = random
            if traversal.next:
                nextNode = oldToNewMap[traversal.next]
                newNode.next = nextNode
            traversal = traversal.next
        return oldToNewMap[head]

    # ── Attempt · 2026-08-04 ──────────────
    def copyRandomList_20260804(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # to perform a deep copy, we need to create a map of old to new
        # so we go through the list, create a copy and link each old node to the new node via the map

        oldToNewMap = {}

        traversal = head

        # construct the map
        while traversal:
            newNode = Node(traversal.val)
            oldToNewMap[traversal] = newNode
            traversal = traversal.next

        traversal = head
        # map next
        while traversal:
            newNext = None
            if traversal.next:
                newNext = oldToNewMap[traversal.next]
            oldToNewMap[traversal].next = newNext
            traversal = traversal.next

        # go through the map and set the random
        for old, new in oldToNewMap.items():
            if old.random:
                newRandom = oldToNewMap[old.random]
                new.random = newRandom

        if not head:
            return None
        return oldToNewMap[head]

    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # we can do an old to new mapping like how we do tree copies

        if not head:
            return None

        oldToNew = {}

        node = head
        while node:
            newNode = Node(node.val)
            oldToNew[node] = newNode
            node = node.next
        
        node = head
        while node:
            copy = oldToNew[node]
            if node.next:
                copy.next = oldToNew[node.next]
            if node.random:
                copy.random = oldToNew[node.random]
            node = node.next
        return oldToNew[head]

    def copyRandomList_20260705(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # deep copy problems typically require a map of old to new
        oldToNew = {}

        node = head

        while node:
            newNode = Node(node.val)
            oldToNew[node] = newNode
            node = node.next
        
        node = head

        while node:
            newNode = oldToNew[node]
            if node.next:
                newNode.next = oldToNew[node.next]
            if node.random:
                newNode.random = oldToNew[node.random]
            node = node.next
        
        if not head:
            return None
        return oldToNew[head]
