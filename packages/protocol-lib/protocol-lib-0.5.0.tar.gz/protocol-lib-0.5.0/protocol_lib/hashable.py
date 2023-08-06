from typing_extensions import Protocol, runtime_checkable

__all__ = ["Hashable"]


@runtime_checkable
class Hashable(Protocol):
    def __hash__(self) -> int:
        ...
