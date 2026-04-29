"""
Given the head of a linked list, remove the nth node from the end of the list and return its head.

Example 1:

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]

Example 2:

Input: head = [1], n = 1
Output: []

Example 3:

Input: head = [1,2], n = 1
Output: [1]

Constraints:

    The number of nodes in the list is sz.
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz

Follow up: Could you do this in one pass?
"""
from typing import Optional

# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEndTwoIteration(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # We need to get prev of the node and the next of the node
        # So one way to do this is just to loop through and set both
        # then just set prev.next = next
        # the tricky part here is n from the end
        # therefore we need length of the linked list

        nMinusOneNode = nPlusOneNode = None
        
        listLength = 0
        current = head
        # get the length of the list
        while current:
            current = current.next
            listLength += 1
        
        indexToRemove = listLength - n

        # i will be never be indexToRemove - 1 if indexToRemove == 0
        # thus we cover the edge case here
        if indexToRemove == 0:
            return head.next # type: ignore

        current = head
        
        # from the start, we want to link index indexToRemove - 1 to next.next
        for i in range(listLength - 1):
            if (i == indexToRemove - 1):
                current.next = current.next.next # type: ignore
                break
            current = current.next # type: ignore
        
        return head