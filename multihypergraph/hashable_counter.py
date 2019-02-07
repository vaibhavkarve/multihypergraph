#!/usr/bin/env python

"""A collections.Counter subclass that will be hashable.

This will allow for counter's keys to themselves be counters.
This will also require counter to be thereafter be frozen.
Immutability is not enforced but is required for this to make sense.

Reference link to various similar solutions:
https://stackoverflow.com/questions/1151658/python-hashable-dicts
"""

from typing import Tuple, Counter, TypeVar

T = TypeVar('T')

class FrozenCounter(Counter[T]):
    def __key(self) -> Tuple[Tuple[T, int], ...]:
        return tuple((key, self[key]) for key in sorted(self))
  
    def __hash__(self) -> int: # type: ignore
        if self.__key():
            return hash(self.__key())

frozencounter = FrozenCounter
