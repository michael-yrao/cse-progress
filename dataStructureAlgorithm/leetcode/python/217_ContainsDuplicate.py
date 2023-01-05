class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # use a set
        # if value already exist in set, return true

        dupSet = set()
        for index, value in enumerate(nums):
            if value in dupSet: return True
            dupSet.add(value)
        return False