"""
You are given the head of a singly linked-list. The list can be represented as:

L0 → L1 → … → Ln - 1 → Ln

Reorder the list to be on the following form:

L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …

You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Example 1:

Input: head = [1,2,3,4]
Output: [1,4,2,3]

Example 2:

Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]

Constraints:

    The number of nodes in the list is in the range [1, 5 * 104].
    1 <= Node.val <= 1000

"""
from typing import Optional

# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # naive solution is to make a hashmap
        # we can just loop through the list, construct hashmap of index -> node
        # build new linked list with result
        # L(0) -> L(n) -> L(1) -> L(n-1) -> L(2) -> L(n - 2)
        # effectively we are merging L(n/2) with the reverse top half of L(n/2) interchangeably
        # so first step is to find the middle of the linked list
        # for this, we do floyd's cycle detection which puts slow at the middle
        # then we reverse the second half of the linked list in place
        # then we loop through with two pointers, one at beginning, one at middle and assign interchangeably
        # also if we look at 1->2->3->4->5, we will notice that first half is 1,2,3 and second half is 4,5
        # thus we can't use slow node from floyd's algorithm, we need slow.next for second half
        # what an amazing problem!! floyd/reverse/merge all in one

        # starting slow 

        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # slow = middle of list
        # slow.next = start of second half of list
        current = slow.next
        # split the two lists
        slow.next = None
        prev = None

        while current:
            temp = current.next
            current.next = prev
            prev = current
            current = temp
        
        # now that we have reversed, we just need to interchangeably swap the nodes
        # current is null, prev is the actual new head of secondHalf

        firstHalf, secondHalf = head, prev

        # from 1,2,3,4,5, we know secondHalf is shorter
        # thus we loop based on secondHalf

        # 1,2,3
        # 5,4
        while secondHalf:
            # like in all reordering problems, we store next for all lists we traverse
            tmp1, tmp2 = firstHalf.next, secondHalf.next
            # 1.next = 5 
            firstHalf.next = secondHalf
            # 5.next = 2
            secondHalf.next = tmp1
            firstHalf = tmp1
            secondHalf = tmp2
    def reorderList_20260706(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # we can create two lists from this list
        # one going forward (L0 -> L1 -> l2), one going backwards (Ln -> Ln-1 -> Ln-2)
        # 1 -> 2
        # 4 -> 3
        # we also need length of the list
        # 1 -> 2 -> 3
        # 5 -> 4
        # what we notice is that we are effectively reversing right past midway
        # so we can use floyd algorithm to find middle node
        # then reverse rest of the linked list
        # then from there, we can have two pointers, one from beginning, one from middle
        # point alternatively
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # now slow is right before the nodes we need to reverse
        # now we reverse all nodes after slow
        # we do need slow pointer still so we will use another pointer to help reverse
        secondHalf = slow.next
        
        # sever the connection to the first half
        slow.next = None

        def reverse(node):
            prev = None
            # 1->2->3->None
            while node:
                nxt = node.next
                # 2-> None 1->None
                node.next = prev
                prev = node
                node = nxt
            return prev

        secondHalfHead = reverse(secondHalf)
        firstHalf = head
        secondHalf = secondHalfHead

        # second half is always shorter
        # so we use that as our end case
        while secondHalf:
            tmp1Next = firstHalf.next
            tmp2Next = secondHalf.next
            firstHalf.next = secondHalf
            secondHalf.next = tmp1Next
            firstHalf = tmp1Next
            secondHalf = tmp2Next