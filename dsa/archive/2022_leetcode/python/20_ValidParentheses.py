class Solution:
    def isValid(self, s: str) -> bool:
        # In Python, we can just use a List for all the Stack/Queue operations
        # As such, we can push the char in if it is an open bracket, pop if it is a closing.

        stack = []
        for char in s:
            if char == '(' or char == '{' or char == '[':
                stack.append(char)
            else:
                if not stack: return False
                elif char == ')':
                    if len(stack) > 0 and stack.pop() != '(': 
                        return False
                elif char == '}':
                    if len(stack) > 0 and stack.pop() != '{': 
                        return False
                elif char == ']':
                    if len(stack) > 0 and stack.pop() != '[': 
                        return False
                else:
                    return False
        return not stack # not stack means empty stack. if empty, return true, else false
    
    def isValidAlternative(self, s: str) -> bool:
        # Same approach but with different syntax
        stack = []

        for i in range(len(s)):
            if s[i] in '({[':
                stack.append(s[i])
            else:
                if not stack \
                    or (stack[-1] == '(' and s[i] != ')') \
                    or (stack[-1] == '[' and s[i] != ']') \
                    or (stack[-1] == '{' and s[i] != '}'): return False
                stack.pop()
        return not stack