"""
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:

    The number of nodes in each linked list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have leading zeros.
"""
# Definition for singly-linked list.
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # so we have to go to the end of both linked list. this screams postorder recursion
        # on re-read, it actually says the linked list is in reverse order
        # so we don't need to do that at all
        # in that case, we will do while both nodes exist

        l1t = l1
        l2t = l2
        carryover = 0
        resultList = ListNode(-1)
        resultTraversal = resultList

        # because this is in reverse order, this works regardless of size
        while l1t and l2t:
            digitSum = l1t.val + l2t.val
            digitSum+=carryover
            # only special case is if they add to above 10
            if digitSum >= 10:
                carryover = 1
            else:
                carryover = 0
            resultNode = ListNode(digitSum%10)
            resultTraversal.next = resultNode
            resultTraversal = resultTraversal.next
            l1t = l1t.next
            l2t = l2t.next
        
        # now that we are here, we should check if either of l1t or l2t are not None
        while l1t:
            digitSum = l1t.val + carryover
            if digitSum >= 10:
                carryover = 1
            else:
                carryover = 0
            resultNode = ListNode(digitSum%10)
            resultTraversal.next = resultNode
            resultTraversal = resultTraversal.next
            l1t = l1t.next

        # now that we are here, we should check if either of l1t or l2t are not None
        while l2t:
            digitSum = l2t.val + carryover
            if digitSum >= 10:
                carryover = 1
            else:
                carryover = 0
            resultNode = ListNode(digitSum%10)
            resultTraversal.next = resultNode
            resultTraversal = resultTraversal.next
            l2t = l2t.next

        # if carryover is still one, we need to put a one at the end

        if carryover == 1:
            resultNode = ListNode(1)
            resultTraversal.next = resultNode
            resultTraversal = resultTraversal.next
        
        return resultList.next
    
    def addTwoNumbers_20260705_elegant(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        #