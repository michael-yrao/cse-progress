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

    # ── Attempt · 2026-07-18 ──────────────
    def removeNthFromEndRecursion_20260718(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # we are repointing len - n - 1's node's next to len - n + 1
        # this is the thinking if we go from the front
        # now if we go from the back, we can just use n
        # we do need to keep the n so we can reference it, so we need a traversal index
        # starting from the back is classic post order recursion so we will do that

        def removeNode(node):
            if not node:
                return 0
            
            currentCount = 1 + removeNode(node.next)
            # we need to point the previous node to current node's next
            # so that is node n + 1 from the end
            if currentCount == n + 1:
                node.next = node.next.next
            return currentCount
        
        # we actually need dummy since we might remove head
        dummy = ListNode(-1)
        dummy.next = head
        removeNode(dummy)
        return dummy.next

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
    
    def removeNthFromEnd_20260618(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # removing nth node from the end means we need to remove len - n node from the front
        # this is important since we are given head and we have to iterate from the front at some point
        # so what we can do is just recursive set current node's next to next
        # but if we hit len - n -1, we need to set next to next.next

        currentNode = head
        lenLinkedList = 0

        while currentNode:
            currentNode = currentNode.next
            lenLinkedList+=1

        def remove(currentNode, currentIndex):
            if not currentNode:
                return None
            
            # if we are at the node we need to change for the next

            returnNode = remove(currentNode.next, currentIndex + 1)

            if currentIndex == lenLinkedList - n - 1:
                currentNode.next = returnNode.next    
            else:
                currentNode.next = returnNode

            return currentNode

        dummyNode = ListNode(-1)
        dummyNode.next = head
        currentNode = dummyNode
        remove(currentNode, -1)

        return dummyNode.next

    def removeNthFromEnd_20260628_Recursive(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # requirement for today is to do this recursively
        # so we need to know where we are at each step
        # so we will pass it to the caller in recursion
        indexFromEnd = 0
        def remove(node):
            nonlocal indexFromEnd
            if not node:
                return None
            
            node.next = remove(node.next)
            indexFromEnd+=1
            # if equal, skip node
            if indexFromEnd == n:
                return node.next
            return node
        
        dummy = ListNode(-1)
        dummy.next = head
        remove(dummy)
        return dummy.next
    def removeNthFromEnd_20260630_Iterative(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # iterative
        # if doing iterative, we need to find the element in front of the one we need to set the next to
        # so that element is len - n - 2

        node = head
        length = 0
        while node:
            length+=1
            node = node.next
        
        dummy = ListNode(-1)
        dummy.next = head

        node = dummy
        counter = -1
        while node:
            if counter == length - n - 1:
                # update next to skip next element
                if node.next:
                    node.next = node.next.next
                    break
            node = node.next
            counter+=1
        return dummy.next
    def removeNthFromEnd_20260708(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # we can do preorder or postorder here
        # we will try postorder today
        # basically if the node returned is the node we are looking to replace
        # set its caller's next to return node's next
        nodeCountFromEnd = 0

        def postorder(node):
            nonlocal nodeCountFromEnd
            if not node or not node.next:
                return node
            
            returnNode = postorder(node.next)
            nodeCountFromEnd+=1
            if nodeCountFromEnd == n:
                node.next = node.next.next
            else:
                node.next = node.next
            return node
        
        dummy = ListNode(-1)
        dummy.next = head
        postorder(dummy)
        return dummy.next
    
    def removeNthFromEnd_20260709_Iterative(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # iterative
        
        dummy = ListNode(-1)
        dummy.next = head

        traversal = head
        lenList = 0

        while traversal:
            lenList+=1
            traversal = traversal.next

        # we are removing nth from the end, so from the front, it is len - n - 1 that we need to re-point
        traversal = dummy
        currentIndex = -1

        while traversal:
            # print(lenList - n - 1)
            if currentIndex == lenList - n - 1:
                if traversal.next:
                    traversal.next = traversal.next.next
                else:
                    traversal.next = None
                break
            traversal = traversal.next
            currentIndex+=1
        
        return dummy.next
