from __future__ import annotations
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
T2 = TypeVar("T2")


# https://github.com/alleycat-at-git/monad/blob/master/python/src/monad.py
class Monad(Generic[T]):
    # pure :: a -> M a
    @staticmethod
    def pure(x):
        raise Exception("pure method needs to be implemented")

    # flat_map :: # M a -> (a -> M b) -> M b
    def flat_map(self, f: Callable[[T], T2]):
        raise Exception("flat_map method needs to be implemented")

    # M = TypeVar("M", bound=Monad)
    # map :: # M a -> (a -> b) -> M b
    def map(self, f: Callable[[T], T2]) -> M[T2]:  # type: ignore
        return self.flat_map(lambda x: self.pure(f(x)))


M = TypeVar("M", bound=Monad)
