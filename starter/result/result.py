from dataclasses import dataclass
from typing import TypeVar, Generic, TypeGuard

T = TypeVar('T')

type Result[T] = Success[T] | Failure


@dataclass
class Success(Generic[T]):
    value: T


@dataclass
class Failure:
    message: str


def is_success(result: Result[T]) -> TypeGuard[Success[T]]:
    return isinstance(result, Success)


def is_failure(result: Result[T]) -> TypeGuard[Failure]:
    return isinstance(result, Failure)
