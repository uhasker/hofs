import heapq
from collections.abc import Iterator
from functools import reduce
from typing import TypeVar, Callable, List, Iterable, Any

T = TypeVar("T")


class FunctionalIterator(Iterator[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        super().__init__()
        self.it = iter(iterable)

    def __next__(self) -> T:
        return next(self.it)

    def filter(self, fun: Callable[[T], bool]) -> "FunctionalIterator[T]":
        return FunctionalIterator(filter(fun, self))

    def map(self, fun: Callable[[T], Any]) -> "FunctionalIterator[Any]":
        return FunctionalIterator(map(fun, self))

    def reduce(self, fun: Callable[[Any, T], T], start: Any) -> Any:
        return reduce(fun, self, start)

    def sum(self) -> int:
        return self.reduce(lambda acc, val: acc + val, 0)

    def len(self) -> int:
        return self.reduce(lambda acc, val: acc + 1, 0)

    def min(self) -> int:
        return min(self)  # type: ignore

    def max(self) -> int:
        return max(self)  # type: ignore

    def list(self) -> List[T]:
        return list(self)

    def sort_asc(self) -> List[T]:
        return sorted(self)  # type: ignore

    sort = sort_asc

    def sort_desc(self) -> List[T]:
        return sorted(self, reverse=True)  # type: ignore

    def top_n(self, n: int) -> List[T]:
        return heapq.nlargest(n, self)

    def for_each(self, fun: Callable[[T], None]) -> None:
        for val in self:
            fun(val)
