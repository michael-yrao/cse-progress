class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Problem wants us to ignore all non-alphanumerics

        alnum = ''.join([i for i in s if i.isalnum()]).lower()

        l,r=0,len(alnum)-1

        while l<r:
            if alnum[l] != alnum[r]: 
                return False
            l+=1
            r-=1

        return True
    
    def isPalindromePythonMagic(self, s: str) -> bool:
        alnum = ''.join([i for i in s if i.isalnum()]).lower()
        return alnum == alnum[::-1]