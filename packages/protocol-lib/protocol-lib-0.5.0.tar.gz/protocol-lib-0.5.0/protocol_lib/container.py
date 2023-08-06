from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

__all__ = ["Container"]


T = TypeVar("T", contravariant=True)


@runtime_checkable
class Container(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...
