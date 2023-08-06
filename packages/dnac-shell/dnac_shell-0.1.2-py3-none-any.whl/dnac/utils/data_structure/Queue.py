from collections import deque
from typing import Generic, TypeVar, Deque, NamedTuple, Callable, Optional

#
# Define a Generic Queue to be reusable across  different types
# across wireless maps test automation.

# copyright (c) 2020 cisco Systems Inc., All rights reserved
# @author rks@cisco.com
#

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self, name_of_this_queue: Optional[str, None]) -> None:
        self._name_ : str = name_of_this_queue
        self._container : Deque[T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item : T) -> None:
        self._container.append(item) # push on one side...

    def pop(self) -> T:
        return self._container.popleft() # pop on the other side...

    def __repr__(self) -> str:
        return self._container.repr()

