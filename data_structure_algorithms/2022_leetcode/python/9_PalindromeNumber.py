class Solution:
    def isPalindrome(self, x: int) -> bool:

        # Scenario 1: If negative, return false
        # Otherwise the number read from left and right should be the same

        if x < 0: 
            return False
        
        # First thought, we can use a stack
        # We can then iterate through the number by doing x%10 and x/10
        # This would give us a complexity of O(n) where n is number of digits
            
        reverse = 0
        iterator = x
        
        while iterator!=0:
            reverse = reverse * 10 + iterator % 10
            iterator //= 10
        
        return reverse==x
    
    def isPalindromeString(self, x: int) -> bool:
        return str(x)==str(x)[::-1]