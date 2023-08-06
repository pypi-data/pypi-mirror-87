from collections import deque


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class StackUtils:
    def __init__(self):
        pass

    #
    # Check if specified stack is empty
    #
    @staticmethod
    def isempty(stack: deque) -> bool:
        if not stack:
            return True
        if len(stack) > 1:
            return False
        if len(stack) == 0:
            return True
        return True if stack.count('') > 0 else False
