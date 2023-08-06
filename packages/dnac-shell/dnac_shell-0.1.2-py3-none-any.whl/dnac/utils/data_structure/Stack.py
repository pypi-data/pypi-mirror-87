from typing import TypeVar, Generic, List, Optional

#
# Define a Generic Stack to be reusable across  different types
# across wireless maps test automation.

# copyright (c) 2020 cisco Systems Inc., All rights reserved
# @author rks@cisco.com

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self, name_of_this_stack: Optional[str, int] = None) -> None:
        self._name_: str = name_of_this_stack
        self._container: List[T] = list()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__pop(self) -> str:
        return self._container.repr()
