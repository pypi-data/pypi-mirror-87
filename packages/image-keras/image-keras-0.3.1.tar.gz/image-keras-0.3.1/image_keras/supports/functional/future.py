from __future__ import annotations
from functools import reduce
import threading
from threading import Thread
from typing import Callable, Generic, List, TypeVar

from .either import Either, Left, Right
from .monad import Monad
from .option import Option, Some, nil

D = TypeVar("D")
D2 = TypeVar("D2")

# https://github.com/alleycat-at-git/monad/blob/master/python/src/future.py
class Future(Monad, Generic[D]):
    # __init__ :: ((Either err a -> void) -> void) -> Future (Either err a)
    def __init__(self, f: Callable[[Callable[[Either[D, Exception]], None]], None]):
        self.subscribers: List[Callable[[Either[D, Exception]], None]] = []
        self.cache: Option[D] = nil
        self.semaphore: threading.BoundedSemaphore = threading.BoundedSemaphore(1)
        f(self.callback)

    # pure :: a -> Future a
    @staticmethod
    def pure(value: D) -> Future:
        # return Future(lambda cb: cb(Either.pure(value)))
        def _cbf(cb: Callable[[Either[D, Exception]], None]) -> None:
            return cb(Either.pure(value))

        return Future(_cbf)

    @staticmethod
    def exec(f: Callable[[], D], cb: Callable[[Either[D, Exception]], None]) -> None:
        try:
            data = f()
            cb(Right(data))
        except Exception as err:
            cb(Left(err))

    @staticmethod
    def exec_on_thread(
        f: Callable[[], D], cb: Callable[[Either[D, Exception]], None]
    ) -> None:
        t: Thread = threading.Thread(target=Future.exec, args=[f, cb])
        t.start()

    def async_f(self, f: Callable[[], D]) -> Future:
        # return Future(lambda cb: Future.exec_on_thread(f, cb))
        def _cbf(cb: Callable[[Either[D, Exception]], None]) -> None:
            return Future.exec_on_thread(f, cb)

        return Future(_cbf)

    # flat_map :: (a -> Future b) -> Future b
    def flat_map(self, f: Callable[[D], Future[D2]]) -> Future[D2]:
        def _cbf(cb: Callable[[Either[D, Exception]], None]) -> None:
            def _cbf2(value: Either[D, Exception]) -> None:
                return value.fold(lambda r: f(r).subscribe(cb), lambda l: cb(value))

            return self.subscribe(_cbf2)

        return Future(_cbf)

    # traverse :: [a] -> (a -> Future b) -> Future [b]
    def traverse(
        self, arr: List[D]
    ) -> Callable[[Callable[[D], Future[D2]]], Future[List[D2]]]:
        # return lambda f: reduce(
        #     lambda acc, elem: acc.flat_map(
        #         lambda values: f(elem).map(lambda value: values + [value])
        #     ),
        #     arr,
        #     Future.pure([]),
        # )
        def _f1(f: Callable[[D], Future[D2]]) -> Future[List[D2]]:
            def _f2(acc: Future[List[D2]], elem: D) -> Future[List[D2]]:
                def _f3(values: List[D2]) -> Future[List[D2]]:
                    def _f4(value: D2) -> List[D2]:
                        return values + [value]

                    return f(elem).map(_f4)

                return acc.flat_map(_f3)

            d2_list_future: Future[List[D2]] = Future.pure([])
            return reduce(_f2, arr, d2_list_future)

        return _f1

    # callback :: Either err a -> void
    def callback(self, d_either: Either[D, Exception]) -> None:
        self.semaphore.acquire()
        self.cache = Some(d_either)
        while len(self.subscribers) > 0:
            sub: Callable[[Either[D, Exception]], None] = self.subscribers.pop(0)
            t: threading.Thread = threading.Thread(target=sub, args=[d_either])
            t.start()
        self.semaphore.release()

    # subscribe :: (Either err a -> void) -> void
    def subscribe(self, subscriber: Callable[[Either[D, Exception]], None]) -> None:
        def _some(v: Either[D, Exception]) -> None:
            self.semaphore.release()
            subscriber(v)

        def _none() -> None:
            self.subscribers.append(subscriber)
            self.semaphore.release()

        self.semaphore.acquire()
        self.cache.fold(lambda value: _some(value), _none())
