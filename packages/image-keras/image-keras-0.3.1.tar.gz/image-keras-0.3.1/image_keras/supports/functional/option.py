from __future__ import annotations
from typing import Callable, Generic, Optional, TypeVar

from .monad import Monad

S = TypeVar("S")
S2 = TypeVar("S2")
X = TypeVar("X")

# https://github.com/alleycat-at-git/monad/blob/master/python/src/future.py
class Option(Monad, Generic[S]):
    def __init__(self, value: Optional[S]):
        self.value: Optional[S] = value

    # pure :: a -> Option a
    @staticmethod
    def pure(x: S) -> Option[S]:
        return Some(x)

    # flat_map :: # Option a -> (a -> Option b) -> Option b
    def flat_map(self, f: Callable[[S], Option[S2]]) -> Option[S2]:
        if self.value is None:
            return f(self.value)
        else:
            return nil

    def fold(self, fa: Callable[[S], X], default: X) -> X:
        if self.value is not None:
            return fa(self.value)
        else:
            return default


class Some(Option):
    def __init__(self, value: S):
        super(Some, self).__init__(value)


class Nil(Option):
    def __init__(self):
        self.value = None


nil = Nil()
