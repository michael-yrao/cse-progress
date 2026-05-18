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

        # edge case
        # if indexToRemove == 0, i will be never be indexToRemove - 1
        # thus we cover the edge case here
        if indexToRemove == 0:
            return head.next

        current = head
        
        # from the start, we want to link index indexToRemove - 1 to next.next
        for i in range(listLength - 1):
            if (i == indexToRemove - 1):
                current.next = current.next.next
                break
            current = current.next
        
        return head
    
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # so we know from our previous implementation that we want to remove len - n node from the start
        # 1->2->3->4->5->None ; n = 2
        # 1->2->3->5->None ; 2nd value from end is removed; 4th element from the start, index of 3 (5 - 2)
        # we can use a two pointer approach where l and r are n apart
        # l will be the element to remove when r becomes None
        # so we want to re-link when r.next is None since we are removing l
        # since we are removing a node, we should use a dummy node

        dummy = ListNode(0)
        dummy.next = head

        l = dummy
        r = head

        # move r to l + n
        while n > 0 and r:
            r = r.next
            n-=1
        
        # now we just move l and r together
        while r:
            l = l.next
            r = r.next

        l.next = l.next.next

        return dummy.next
    
    def removeNthFromEndRecursion(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # we still need a dummy node in case of head removal
        
        dummy = ListNode(0)
        dummy.next = head

        # since it is recursion, we start at end of the list
        # this return is the caller's next value
        # however, when we are at nth node from the end
        # we want the return to be current.next so we remove reference
        # to the nth node from the end
        # keep track of current node # from the end

        counter = 0
        def removeNthNode(head):
            nonlocal counter
            if not head:
                return None
            
            # set caller's next to return
            head.next = removeNthNode(head.next)
            
            # [1,2,3] ; n = 2
            # head is at 3 when we are here for the first time
            # increment counter
            counter+=1

            # if counter is at n, return next instead of current
            # thus removing any reference to nth from the end 
            if counter == n:
                return head.next
            
            # otherwise return current node
            return head
        
        removeNthNode(dummy)
        return dummy.next