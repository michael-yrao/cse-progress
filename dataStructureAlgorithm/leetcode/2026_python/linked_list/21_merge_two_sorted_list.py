"""
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:

Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:

Input: list1 = [], list2 = []
Output: []

Example 3:

Input: list1 = [], list2 = [0]
Output: [0]

Constraints:

    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.

"""
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # creating new linked list
        # thus we should use a dummy node to keep track of new head
        
        # value is irrelevant, using -101 since constraint says node.val >= -100
        dummy = ListNode(-101)

        # now we need a cursor to actually traverse the list
        # we initialize it to dummy so we keep references to it
        current = dummy

        # while both of the lists are not null
        # we want to compare and provide lowest to current

        while list1 and list2:
            if list1.val < list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # when we are here, we know one of the list is null

        if list1:
            current.next = list1
        else:
            current.next = list2
        
        return dummy.next