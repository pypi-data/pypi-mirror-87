from typing import List, TypeVar

T = TypeVar("T")


def list_diff(f: List[T], t: List[T]) -> List[T]:
    return list(set(f) - set(t))


def list_intersection(f: List[T], t: List[T]) -> List[T]:
    return list(set(f).intersection(t))
