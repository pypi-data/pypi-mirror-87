from __future__ import annotations
from typing import Callable, Generic, List, Optional, TypeVar

from .monad import Monad

R = TypeVar("R")
R2 = TypeVar("R2")
L = TypeVar("L")
X = TypeVar("X")

# https://github.com/alleycat-at-git/monad/blob/master/python/src/either.py
class Either(Monad, Generic[R, L]):
    def __init__(self, right: Optional[R], left: Optional[L]):
        self.right: R = right
        self.left: L = left

    # pure :: a -> Either a
    @staticmethod
    def pure(right: R) -> Either[R, L]:
        return Right(right)

    # flat_map :: # Either a -> (a -> Either b) -> Either b
    def flat_map(self, f: Callable[[R], Either[R2, L]]) -> Either[R2, L]:
        if self.left is not None:
            return self
        else:
            return f(self.right)

    def fold(self, fa: Callable[[R], X], fb: Callable[[L], X]) -> X:
        if self.left is not None:
            return fb(self.left)
        else:
            return fa(self.right)


class Right(Either):
    def __init__(self, right: R):
        super(Right, self).__init__(right, None)


class Left(Either):
    def __init__(self, left: L):
        super(Left, self).__init__(None, left)


E = TypeVar("E")
A = TypeVar("A")


def sequences(es: List[Either[A, E]]) -> Either[List[A], E]:
    return traverse(es, lambda x: x)


B = TypeVar("B")


def traverse(es: List[A], f: Callable[[A], Either[B, E]]) -> Either[List[B], E]:
    lb: List[B] = []
    e: E = None
    left_flag: bool = False
    for e in es:
        a: Either[B, E] = f(e)
        if a.right is not None:
            lb.append(a.right)
        else:
            e = a.left
            left_flag = True
            continue
    return Either(lb, e) if left_flag else Right(lb)
