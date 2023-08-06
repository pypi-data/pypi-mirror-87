from collections import Counter
from typing import Callable, List, TypeVar

T = TypeVar("T")


def list_filters(filters: List[Callable[[T], bool]], apply_to: List[T]) -> List[T]:
    """
    Apply multiple filters to list.

    Parameters
    ----------
    filters : List[Callable[[T], bool]]
        Multiple filters
    apply_to : List[T]
        A list to apply filters to.

    Returns
    -------
    List[T]
        A list after multiple filters are applied.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    l: List[T] = apply_to.copy()
    for _filter in filters:
        l = list(filter(_filter, l))
    return l


S = TypeVar("S")
T = TypeVar("T")


def compare_hashable_list(s: List[S], t: List[T]) -> bool:
    """
    Compare hashable list. O(n).

    Parameters
    ----------
    s : List[S]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    bool
        True if lists are same.

    Notes
    -----
    .. versionadded:: 0.1.0

    References
    ----------
    https://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python
    """
    return Counter(s) == Counter(t)


def compare_orderable_list(s: List[S], t: List[T]) -> bool:
    """
    Compare orderable list. O(n log n)

    Parameters
    ----------
    s : List[S]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    bool
        True if lists are same.

    Notes
    -----
    .. versionadded:: 0.1.0

    References
    ----------
    https://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python
    """
    return sorted(s) == sorted(t)


def list_diff(f: List[T], t: List[T]) -> List[T]:
    """
    Returns a list of the differences between lists without duplicate elements.

    Parameters
    ----------
    f : List[T]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    List[T]
        Difference between lists

    Notes
    -----
    .. versionadded:: 0.1.1

    Examples
    --------
    >>> list_diff([1,2,3,4], [1,2,3])
    [4]
    >>> list_diff([1,2,3], [1,2,3,4])
    []
    >>> list_diff([1,2,3,4,4], [1,2,3])
    [4]
    >>> list_diff([1,2,3,4,4], [1,2,3,3,3])
    [4]
    """
    return list(set(f) - set(t))


def list_intersection(f: List[T], t: List[T]) -> List[T]:
    """
    Returns a common list between lists without duplicate elements.

    Parameters
    ----------
    f : List[T]
        List 1
    t : List[T]
        List 2

    Returns
    -------
    List[T]
        Common list between lists

    Notes
    -----
    .. versionadded:: 0.1.1

    Examples
    --------
    >>> list_intersection([1,2,3], [1,5,9,2])
    [1, 2]
    >>> list_intersection([1,2,3,3,3,2], [1,5,9,2])
    [1, 2]
    """
    return list(set(f).intersection(t))
