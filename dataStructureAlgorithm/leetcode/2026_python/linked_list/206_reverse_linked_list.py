"""
Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:

Input: head = [1,2]
Output: [2,1]

Example 3:

Input: head = []
Output: []

Constraints:

    The number of nodes in the list is the range [0, 5000].
    -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?
"""

from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseListIterative(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # we need to initialize a prev so we can have the current head point to null
        # then we have a pointer to help us traverse through the list
        prev, current = None, head

        while current is not None:
            # put current.next in temp variable
            temp = current.next
            # change what current points to
            current.next = prev
            # prev should now be current
            prev = current
            # current is now next
            current = temp
        return prev

    def reverseListRecursion(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # base case to stop at the last node
        if head is None or head.next is None:
            return head
        
        # if we have 3 -> 4 -> 5 -> None only
        # returnNode would be 5 and head would be 4
        returnNode = self.reverseListRecursion(head.next)
        # since we passed head.next to the recursive call
        # we need to change its next
        # 4 is head in this case, 4.next is 5
        head.next.next = head
        # 4.next would be None
        head.next = None
        # return the base case node
        return returnNode