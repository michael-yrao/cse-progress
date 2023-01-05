class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        map = {}
        for value in s:
            map[value] = 1 + map.get(value,0)
        
        for value in t:
            map[value] = -1 + map.get(value,0)
            if map[value] == 0:
                map.pop(value)
        
        return not bool(map)